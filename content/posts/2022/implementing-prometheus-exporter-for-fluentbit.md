---
title: "Implementing Prometheus Exporter for Fluentbit"
date: 2022-11-24T12:26:23+08:00
tags: [golang, fluentbit, prometheus]
aliases: [/posts/implementing-prometheus-exporter-for-fluentbit/]
description: "We want to export specific input data into Prometheus, therefore we have to implement our Prometheus exporter in a customized Fluent-bit output plugin."
draft: true
---

Fluent-bit is a great tool for logging and monitoring, many tech teams are using it to collect metrics and log data. Prometheus is also a popular tool for metrics analysis, but Fluent-bit can only output data to Proetheus by its own exporter input-plugin, which has fixed metrics and data format.

In our case, we want to export specific input data into Prometheus, therefore we have to implement our Prometheus exporter in a customized Fluent-bit output plugin.

## Fluent-bit Output Plugin

Fluent-bit provides a way to implement your own golang plugin. (See [Fluent-bit Go Output Plugin](https://docs.fluentbit.io/manual/v/1.9-pre/development/golang-output-plugins))

We can run an asynchronous HTTP server as the Prometheus exporter when Fluent-bit plugin initializing, and transform the Fluent-bit records to Prometheus metrics format when Fluent-bit flushing a record to output plugin.

To implement a Fluent-bit output plugin, there are four call-back functions we need to over write,

```go

func FLBPluginRegister(def unsafe.Pointer) int {
    // Here we define the plugin name and description.
	return output.FLBPluginRegister(def, "promexporter", "Prometheus Exporter")
}

func FLBPluginInit(plugin unsafe.Pointer) int {
    // We can extract output plugin parameters from `FLBPlguinConfigKey`.
	user := output.FLBPluginConfigKey(plugin, "username")
	passwd := output.FLBPluginConfigKey(plugin, "password")
    // Here we can run a new Prometheus exporter server.
	NewExporter()
	return output.FLB_OK
}

func FLBPluginFlushCtx(ctx, data unsafe.Pointer, length C.int, tag *C.char) int {
    // Here we process every record, extract it and ship to exporter
	dec := output.NewDecoder(data, int(length))
	for {
		// Extract Record
		ret, _, record := output.GetRecord(dec)
		if ret != 0 {
			break
		}

		for k, v := range record {
            // I'm using a go channel object for transporting records.
			collector.buff <- fmt.Sprintf("%s=%f", k, v)
		}
	}

	return output.FLB_OK
}

func FLBPluginExit() int {
	if err := server.srv.Shutdown(context.TODO()); err != nil {
		panic(err)
	}

    // Here we have to close go channel and daemon exporter server.
	close(collector.buff)
	server.wg.Wait()

	return output.FLB_OK
}

func main() {
}


```

The next step is to implement the HTTP server, make it running on daemon.

```go

// Here we start a background server on port 8989, the server will handle `/metrics` path, prometheus exporter will implement the handler.
func startHttpServer(wg *sync.WaitGroup, reg *prometheus.Registry) *http.Server {
	srv := &http.Server{Addr: ":8989"}

	http.Handle("/metrics", promhttp.HandlerFor(
		reg,
		promhttp.HandlerOpts{
			EnableOpenMetrics: true,
			Registry:          reg,
		},
	))

	go func() {
		defer wg.Done()
		if err := srv.ListenAndServe(); err != http.ErrServerClosed {
			fmt.Println("ListenAndServe():", err)
		}
	}()

	return srv
}

func NewExporter() {
	reg := prometheus.NewRegistry()
	reg.MustRegister(collector)

    // Here, we start a new HTTP server and save the instance object into a golang sync.WaitGroup, so that we can watch its status in `FLBPluginExit`
	server.wg = &sync.WaitGroup{}
	server.wg.Add(1)
	server.srv = startHttpServer(server.wg, reg)
}

```
