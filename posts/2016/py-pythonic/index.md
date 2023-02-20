# Python 巧妙地将rpc接口封装成pythonic的链式调用


这是一个外国人实现的 Zabbix(一个开源监控工具)的 Python Client——pyzabbix 里的代码片段。

## RPC 调用

Rpc 调用的流程是向 rpc 服务端指定的 uri(如http://www.abc.com/jsonrpc.php) 发送 json(或其他双方约定格式)数据包，数据包里有 rpc 版本信息、方法名、参数等。下面`Zabbix`类里的`do_request`方法就完成了将方法名和方法参数打包 json 后发送请求的过程。

```python
class Zabbix(object):
    # ... skip other class methods

    def do_request(self, method, params=None):
        request_json = {
            'jsonrpc': '2.0',
            'method': method,
            'params': params or {},
            'id': self.id,
        }

        response = self.session.post(
            self.url,
            data=json.dumps(request_json),
            timeout=self.timeout
        )
```

## 技巧

但是为了方便，我们在 python 里一般使用`zabbixclient.host.get(args)`这样的链式调用，而不用`zabbixclient('host.get', args)`这样的调用方式。pyzabbix 的作者巧妙的实现了这样的转换。

```python
class Zabbix(object):
    # ... skip other class methods

    def do_request(self, method, params=None):
        request_json = {
            'jsonrpc': '2.0',
            'method': method,
            'params': params or {},
            'id': self.id,
        }

        response = self.session.post(
            self.url,
            data=json.dumps(request_json),
            timeout=self.timeout
        )

    # python内建方法，当获取某个对象的属性时，调用该对象的该方法
    def __getattr__(self, attr):
        """Dynamically create an object class (ie: host)"""
        # 此处把self传给ZabbixAPIObjectClass的self.parent
        return ZabbixAPIObjectClass(attr, self)


class ZabbixAPIObjectClass(object):
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent

    def __getattr__(self, attr):
        """Dynamically create a method (ie: get)"""

        def fn(*args, **kwargs):
            if args and kwargs:
                raise TypeError("Found both args and kwargs")

            # 此处把父类传进来的方法名name和子方法attr拼成rpc的方法名
            return self.parent.do_request(
                '{0}.{1}'.format(self.name, attr),
                args or kwargs
            )['result']

        return fn
```

类似地，很多接口的实现都可以照搬这种方式把参数调用改成链式调用，如 pymongo，redis-py 等。

## 参考资料：

<https://github.com/lukecyca/pyzabbix>

