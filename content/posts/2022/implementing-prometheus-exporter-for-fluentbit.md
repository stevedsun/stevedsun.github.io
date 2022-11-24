---
title: "Implementing Prometheus Exporter for Fluentbit"
date: 2022-11-24T12:26:23+08:00
tags: [golang, fluentbit, prometheus]
aliases: [/posts/implementing-prometheus-exporter-for-fluentbit/]
description: "We want to export specific input data into Prometheus, therefore we have to implement our Prometheus exporter in a customized Fluent-bit output plugin."
---

## Background

Fluent-bit is a great tool for logging and monitoring, many teams are using it to collect metrics and logs. Prometheus is also a popular tool for metrics analysis, but if you want to output Fluent-bit data to Prometheus, the only way is to use the node-exporter input plugin, which has fixed metrics and data format.

In our case, we want to export specific input data into Prometheus, therefore we have to implement our Prometheus exporter in a customized Fluent-bit output plugin.

Today I want to share the final solution for this case. The complete demo code can be found on this Github repo: <https://github.com/stevedsun/fluent-bit-output-prometheus-demo>

## Fluent-bit Output Plugin

Fluent-bit provides a way to implement your own golang plugin. (See [Fluent-bit Go Output Plugin](https://docs.fluentbit.io/manual/v/1.9-pre/development/golang-output-plugins))

We can run an asynchronous HTTP server as the Prometheus exporter when Fluent-bit plugin initializing, and transform the Fluent-bit records to Prometheus metrics format when Fluent-bit flushing a record to output plugin.

To implement a Fluent-bit output plugin, there are four call-back functions we need to over write.

```go
//export FLBPluginRegister
func FLBPluginRegister(def unsafe.Pointer) int {
    // Here we define the plugin name and description.
	return output.FLBPluginRegister(def, "promexporter", "Prometheus Exporter")
}

//export FLBPluginInit
func FLBPluginInit(plugin unsafe.Pointer) int {
    // We can extract output plugin parameters from `FLBPlguinConfigKey`.
	user := output.FLBPluginConfigKey(plugin, "username")
	passwd := output.FLBPluginConfigKey(plugin, "password")
    // Here we can run a new Prometheus exporter server.
	NewExporter()
	return output.FLB_OK
}

//export FLBPluginFlushCtx
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
			// You have to extract record here, ship them to exporter.
		}
	}

	return output.FLB_OK
}

//export FLBPluginExit
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

{{< admonition tip "Note" >}}
You should not remove the comment lines above function, they are important for building \*.so file.

```
//export FLBPluginExit
```

{{< /admonition >}}

## The Exporter HTTP Server

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

## The Exporter Collector

Now we have an HTTP server, but if we want to make it as an exporter, we have to define the **collector**. The collector is a Prometheus concept which implements two call-back function:

```go

// Here for instance, we define metrics to collect cpu info, which reuses the default Fluent-bit CPU metrics input data
func NewMyCollector() *myCollector {
	return &myCollector{
		metrics: map[string]*prometheus.Desc{
			"cpu": prometheus.NewDesc(
				"cpu",
				"Collect CPU usage",
				[]string{"cpu", "mode"}, nil,
			),
		},
		// this buff is a golang channel object, which receive data sending from `FLBPluginFlushCtx` function
		buff: make(chan cpuMetrics),
	}
}

// `Describe` send our metrics name and defination to Prometheus exporter
func (collector *myCollector) Describe(ch chan<- *prometheus.Desc) {
	for _, desc := range collector.metrics {
		ch <- desc
	}
}

// `Collect` will read data from golang channel `buff` and send data to HTTP server handler
func (collector *myCollector) Collect(ch chan<- prometheus.Metric) {

	for _, desc := range collector.metrics {
		select {
		case metric := <-collector.buff:
			fmt.Println(metric.cpu, metric.mode, metric.value)
			ch <- prometheus.MustNewConstMetric(desc, prometheus.GaugeValue, metric.value, metric.cpu, metric.mode)
		default:
			return
		}
	}

}

var collector = NewMyCollector()
```

## Building so file and running in Fluent-bit

The last but not least, building golang plugin into so file.

```bash
go build -buildmode=c-shared -o out_prom_exporter.so prom_exporter.go
```

Run Fluent-bit with CLI flags:

```bash
fluent-bit -v -e ./out_prom_exporter.so -i cpu -o promexporter
```

That's all steps to implement a customized Fluent-bit Prometheus exporter plugin. See more details, please go to Github repo <https://github.com/stevedsun/fluent-bit-output-prometheus-demo>.
