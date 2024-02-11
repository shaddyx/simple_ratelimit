# A bunch of tools for parsing/scrapping

## Proxy factory

The proxy factory is the tool to rotate proxies using the round robin algo

Example usage:
```python
    import parserian.proxy_factory as pf
    import parserian.proxy as proxy
    f = pf.ProxyFactory()
    f.add(proxy.Proxy("http://1.1.1.1"))
    f.add(proxy.Proxy("http://2.2.2.2"))
    with f.next() as p:
        assert p.url == "http://1.1.1.1"
    with f.next() as p:
        assert p.url == "http://2.2.2.2"
    with f.next() as p:
        assert p.url == "http://1.1.1.1"
```

The code will automatically delete incorrect proxy from the list if some error happened 
(for now the main policy is to delete proxies after any error, other policies will be added in the future)


```python
    import parserian.proxy_factory as pf
    import parserian.proxy as proxy
    f = pf.ProxyFactory()
    f.add(proxy.Proxy("http://1.1.1.1"))
    f.add(proxy.Proxy("http://2.2.2.2"))
    try:
        with f.next() as p:
            assert p.url == "http://1.1.1.1"
            raise Exception("test")
    except:
        pass
    with f.next():
        assert f.proxies[0].url == "http://2.2.2.2"
```