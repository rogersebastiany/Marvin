# httpx HTTP Client


---

## 1. Timeouts

HTTPX is careful to enforce timeouts everywhere by default.

The default behavior is to raise a `TimeoutException` after 5 seconds of
network inactivity.

## Setting and disabling timeouts

You can set timeouts for an individual request:

```
# Using the top-level API:
httpx.get('http://example.com/api/v1/example', timeout=10.0)

# Using a client instance:
with httpx.Client() as client:
    client.get("http://example.com/api/v1/example", timeout=10.0)
```

Or disable timeouts for an individual request:

```
# Using the top-level API:
httpx.get('http://example.com/api/v1/example', timeout=None)

# Using a client instance:
with httpx.Client() as client:
    client.get("http://example.com/api/v1/example", timeout=None)
```

## Setting a default timeout on a client

You can set a timeout on a client instance, which results in the given
`timeout` being used as the default for requests made with this client:

```
client = httpx.Client()              # Use a default 5s timeout everywhere.
client = httpx.Client(timeout=10.0)  # Use a default 10s timeout everywhere.
client = httpx.Client(timeout=None)  # Disable all timeouts by default.
```

## Fine tuning the configuration

HTTPX also allows you to specify the timeout behavior in more fine grained detail.

There are four different types of timeouts that may occur. These are **connect**,
**read**, **write**, and **pool** timeouts.

* The **connect** timeout specifies the maximum amount of time to wait until
  a socket connection to the requested host is established. If HTTPX is unable to connect
  within this time frame, a `ConnectTimeout` exception is raised.
* The **read** timeout specifies the maximum duration to wait for a chunk of
  data to be received (for example, a chunk of the response body). If HTTPX is
  unable to receive data within this time frame, a `ReadTimeout` exception is raised.
* The **write** timeout specifies the maximum duration to wait for a chunk of
  data to be sent (for example, a chunk of the request body). If HTTPX is unable
  to send data within this time frame, a `WriteTimeout` exception is raised.
* The **pool** timeout specifies the maximum duration to wait for acquiring
  a connection from the connection pool. If HTTPX is unable to acquire a connection
  within this time frame, a `PoolTimeout` exception is raised. A related
  configuration here is the maximum number of allowable connections in the
  connection pool, which is configured by the `limits` argument.

You can configure the timeout behavior for any of these values...

```
# A client with a 60s timeout for connecting, and a 10s timeout elsewhere.
timeout = httpx.Timeout(10.0, connect=60.0)
client = httpx.Client(timeout=timeout)

response = client.get('http://example.com/')
```

---

## 2. Clients

Hint

If you are coming from Requests, `httpx.Client()` is what you can use instead of `requests.Session()`.

## Why use a Client?

TL;DR

If you do anything more than experimentation, one-off scripts, or prototypes, then you should use a `Client` instance.

**More efficient usage of network resources**

When you make requests using the top-level API as documented in the [Quickstart](../../quickstart/) guide, HTTPX has to establish a new connection *for every single request* (connections are not reused). As the number of requests to a host increases, this quickly becomes inefficient.

On the other hand, a `Client` instance uses [HTTP connection pooling](https://en.wikipedia.org/wiki/HTTP_persistent_connection). This means that when you make several requests to the same host, the `Client` will reuse the underlying TCP connection, instead of recreating one for every single request.

This can bring **significant performance improvements** compared to using the top-level API, including:

* Reduced latency across requests (no handshaking).
* Reduced CPU usage and round-trips.
* Reduced network congestion.

**Extra features**

`Client` instances also support features that aren't available at the top-level API, such as:

* Cookie persistence across requests.
* Applying configuration across all outgoing requests.
* Sending requests through HTTP proxies.
* Using [HTTP/2](../../http2/).

The other sections on this page go into further detail about what you can do with a `Client` instance.

## Usage

The recommended way to use a `Client` is as a context manager. This will ensure that connections are properly cleaned up when leaving the `with` block:

```
with httpx.Client() as client:
    ...
```

Alternatively, you can explicitly close the connection pool without block-usage using `.close()`:

```
client = httpx.Client()
try:
    ...
finally:
    client.close()
```

## Making requests

Once you have a `Client`, you can send requests using `.get()`, `.post()`, etc. For example:

```
>>> with httpx.Client() as client:
...     r = client.get('https://example.com')
...
>>> r
<Response [200 OK]>
```

These methods accept the same arguments as `httpx.get()`, `httpx.post()`, etc. This means that all features documented in the [Quickstart](../../quickstart/) guide are also available at the client level.

For example, to send a request with custom headers:

```
>>> with httpx.Client() as client:
...     headers = {'X-Custom': 'value'}
...     r = client.get('https://example.com', headers=headers)
...
>>> r.request.headers['X-Custom']
'value'
```

## Sharing configuration across requests

Clients allow you to apply configuration to all outgoing requests by passing parameters to the `Client` constructor.

For example, to apply a set of custom headers *on every request*:

```
>>> url = 'http://httpbin.org/headers'
>>> headers = {'user-agent': 'my-app/0.0.1'}
>>> with httpx.Client(headers=headers) as client:
...     r = client.get(url)
...
>>> r.json()['headers']['User-Agent']
'my-app/0.0.1'
```

## Merging of configuration

When a configuration option is provided at both the client-level and request-level, one of two things can happen:

* For headers, query parameters and cookies, the values are combined together. For example:

```
>>> headers = {'X-Auth': 'from-client'}
>>> params = {'client_id': 'client1'}
>>> with httpx.Client(headers=headers, params=params) as client:
...     headers = {'X-Custom': 'from-request'}
...     params = {'request_id': 'request1'}
...     r = client.get('https://example.com', headers=headers, params=params)
...
>>> r.request.url
URL('https://example.com?client_id=client1&request_id=request1')
>>> r.request.headers['X-Auth']
'from-client'
>>> r.request.headers['X-Custom']
'from-request'
```

* For all other parameters, the request-level value takes priority. For example:

```
>>> with httpx.Client(auth=('tom', 'mot123')) as client:
...     r = client.get('https://example.com', auth=('alice', 'ecila123'))
...
>>> _, _, auth = r.request.headers['Authorization'].partition(' ')
>>> importbase64
>>> base64.b64decode(auth)
b'alice:ecila123'
```

If you need finer-grained control on the merging of client-level and request-level parameters, see [Request instances](#request-instances).

## Other Client-only configuration options

Additionally, `Client` accepts some configuration options that aren't available at the request level.

For example, `base_url` allows you to prepend an URL to all outgoing requests:

```
>>> with httpx.Client(base_url='http://httpbin.org') as client:
...     r = client.get('/headers')
...
>>> r.request.url
URL('http://httpbin.org/headers')
```

For a list of all available client parameters, see the [`Client`](../../api/#client) API reference.

---

## Request instances

For maximum control on what gets sent over the wire, HTTPX supports building explicit [`Request`](../../api/#request) instances:

```
request = httpx.Request("GET", "https://example.com")
```

To dispatch a `Request` instance across to the network, create a [`Client` instance](#client-instances) and use `.send()`:

```
with httpx.Client() as client:
    response = client.send(request)
    ...
```

If you need to mix client-level and request-level options in a way that is not supported by the default [Merging of parameters](#merging-of-parameters), you can use `.build_request()` and then make arbitrary modifications to the `Request` instance. For example:

```
headers = {"X-Api-Key": "...", "X-Client-ID": "ABC123"}

with httpx.Client(headers=headers) as client:
    request = client.build_request("GET", "https://api.example.com")

    print(request.headers["X-Client-ID"])  # "ABC123"

    # Don't send the API key for this particular request.
    del request.headers["X-Api-Key"]

    response = client.send(request)
    ...
```

## Monitoring download progress

If you need to monitor download progress of large responses, you can use response streaming and inspect the `response.num_bytes_downloaded` property.

This interface is required for properly determining download progress, because the total number of bytes returned by `response.content` or `response.iter_content()` will not always correspond with the raw content length of the response if HTTP response compression is being used.

For example, showing a progress bar using the [`tqdm`](https://github.com/tqdm/tqdm) library while a response is being downloaded could be done like this…

```
importtempfile

importhttpx
fromtqdmimport tqdm

with tempfile.NamedTemporaryFile() as download_file:
    url = "https://speed.hetzner.de/100MB.bin"
    with httpx.stream("GET", url) as response:
        total = int(response.headers["Content-Length"])

        with tqdm(total=total, unit_scale=True, unit_divisor=1024, unit="B") as progress:
            num_bytes_downloaded = response.num_bytes_downloaded
            for chunk in response.iter_bytes():
                download_file.write(chunk)
                progress.update(response.num_bytes_downloaded - num_bytes_downloaded)
                num_bytes_downloaded = response.num_bytes_downloaded
```

Or an alternate example, this time using the [`rich`](https://github.com/willmcgugan/rich) library…

```
importtempfile
importhttpx
importrich.progress

with tempfile.NamedTemporaryFile() as download_file:
    url = "https://speed.hetzner.de/100MB.bin"
    with httpx.stream("GET", url) as response:
        total = int(response.headers["Content-Length"])

        with rich.progress.Progress(
            "[progress.percentage]{task.percentage:>3.0f}%",
            rich.progress.BarColumn(bar_width=None),
            rich.progress.DownloadColumn(),
            rich.progress.TransferSpeedColumn(),
        ) as progress:
            download_task = progress.add_task("Download", total=total)
            for chunk in response.iter_bytes():
                download_file.write(chunk)
                progress.update(download_task, completed=response.num_bytes_downloaded)
```

## Monitoring upload progress

If you need to monitor upload progress of large responses, you can use request content generator streaming.

For example, showing a progress bar using the [`tqdm`](https://github.com/tqdm/tqdm) library.

```
importio
importrandom

importhttpx
fromtqdmimport tqdm

defgen():
"""
    this is a complete example with generated random bytes.
    you can replace `io.BytesIO` with real file object.
    """
    total = 32 * 1024 * 1024  # 32m
    with tqdm(ascii=True, unit_scale=True, unit='B', unit_divisor=1024, total=total) as bar:
        with io.BytesIO(random.randbytes(total)) as f:
            while data := f.read(1024):
                yield data
                bar.update(len(data))

httpx.post("https://httpbin.org/post", content=gen())
```

## Multipart file encoding

As mentioned in the [quickstart](../../quickstart/#sending-multipart-file-uploads)
multipart file encoding is available by passing a dictionary with the
name of the payloads as keys and either tuple of elements or a file-like object or a string as values.

```
>>> with open('report.xls', 'rb') as report_file:
...     files = {'upload-file': ('report.xls', report_file, 'application/vnd.ms-excel')}
...     r = httpx.post("https://httpbin.org/post", files=files)
>>> print(r.text)
{
  ...
  "files": {
    "upload-file": "<... binary content ...>"
  },
  ...
}
```

More specifically, if a tuple is used as a value, it must have between 2 and 3 elements:

* The first element is an optional file name which can be set to `None`.
* The second element may be a file-like object or a string which will be automatically
  encoded in UTF-8.
* An optional third element can be used to specify the
  [MIME type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_Types)
  of the file being uploaded. If not specified HTTPX will attempt to guess the MIME type based
  on the file name, with unknown file extensions defaulting to "application/octet-stream".
  If the file name is explicitly set to `None` then HTTPX will not include a content-type
  MIME header field.

```
>>> files = {'upload-file': (None, 'text content', 'text/plain')}
>>> r = httpx.post("https://httpbin.org/post", files=files)
>>> print(r.text)
{
  ...
  "files": {},
  "form": {
    "upload-file": "text-content"
  },
  ...
}
```

Tip

It is safe to upload large files this way. File uploads are streaming by default, meaning that only one chunk will be loaded into memory at a time.

Non-file data fields can be included in the multipart form using by passing them to `data=...`.

You can also send multiple files in one go with a multiple file field form.
To do that, pass a list of `(field, <file>)` items instead of a dictionary, allowing you to pass multiple items with the same `field`.
For instance this request sends 2 files, `foo.png` and `bar.png` in one request on the `images` form field:

```
>>> with open('foo.png', 'rb') as foo_file, open('bar.png', 'rb') as bar_file:
...     files = [
...         ('images', ('foo.png', foo_file, 'image/png')),
...         ('images', ('bar.png', bar_file, 'image/png')),
...     ]
...     r = httpx.post("https://httpbin.org/post", files=files)
```

---

## 3. Async Support

HTTPX offers a standard synchronous API by default, but also gives you
the option of an async client if you need it.

Async is a concurrency model that is far more efficient than multi-threading,
and can provide significant performance benefits and enable the use of
long-lived network connections such as WebSockets.

If you're working with an async web framework then you'll also want to use an
async client for sending outgoing HTTP requests.

## Making Async requests

To make asynchronous requests, you'll need an `AsyncClient`.

```
>>> async with httpx.AsyncClient() as client:
...     r = await client.get('https://www.example.com/')
...
>>> r
<Response [200 OK]>
```

Tip

Use [IPython](https://ipython.readthedocs.io/en/stable/) or Python 3.9+ with `python -m asyncio` to try this code interactively, as they support executing `async`/`await` expressions in the console.

## API Differences

If you're using an async client then there are a few bits of API that
use async methods.

### Making requests

The request methods are all async, so you should use `response = await client.get(...)` style for all of the following:

* `AsyncClient.get(url, ...)`
* `AsyncClient.options(url, ...)`
* `AsyncClient.head(url, ...)`
* `AsyncClient.post(url, ...)`
* `AsyncClient.put(url, ...)`
* `AsyncClient.patch(url, ...)`
* `AsyncClient.delete(url, ...)`
* `AsyncClient.request(method, url, ...)`
* `AsyncClient.send(request, ...)`

### Opening and closing clients

Use `async with httpx.AsyncClient()` if you want a context-managed client...

```
async with httpx.AsyncClient() as client:
    ...
```

Warning

In order to get the most benefit from connection pooling, make sure you're not instantiating multiple client instances - for example by using `async with` inside a "hot loop". This can be achieved either by having a single scoped client that's passed throughout wherever it's needed, or by having a single global client instance.

Alternatively, use `await client.aclose()` if you want to close a client explicitly:

```
client = httpx.AsyncClient()
...
await client.aclose()
```

### Streaming responses

The `AsyncClient.stream(method, url, ...)` method is an async context block.

```
>>> client = httpx.AsyncClient()
>>> async with client.stream('GET', 'https://www.example.com/') as response:
...     async for chunk in response.aiter_bytes():
...         ...
```

The async response streaming methods are:

* `Response.aread()` - For conditionally reading a response inside a stream block.
* `Response.aiter_bytes()` - For streaming the response content as bytes.
* `Response.aiter_text()` - For streaming the response content as text.
* `Response.aiter_lines()` - For streaming the response content as lines of text.
* `Response.aiter_raw()` - For streaming the raw response bytes, without applying content decoding.
* `Response.aclose()` - For closing the response. You don't usually need this, since `.stream` block closes the response automatically on exit.

For situations when context block usage is not practical, it is possible to enter "manual mode" by sending a [`Request` instance](../advanced/clients/#request-instances) using `client.send(..., stream=True)`.

Example in the context of forwarding the response to a streaming web endpoint with [Starlette](https://www.starlette.io):

```
importhttpx
fromstarlette.backgroundimport BackgroundTask
fromstarlette.responsesimport StreamingResponse

client = httpx.AsyncClient()

async defhome(request):
    req = client.build_request("GET", "https://www.example.com/")
    r = await client.send(req, stream=True)
    return StreamingResponse(r.aiter_text(), background=BackgroundTask(r.aclose))
```

Warning

When using this "manual streaming mode", it is your duty as a developer to make sure that `Response.aclose()` is called eventually. Failing to do so would leave connections open, most likely resulting in resource leaks down the line.

### Streaming requests

When sending a streaming request body with an `AsyncClient` instance, you should use an async bytes generator instead of a bytes generator:

```
async defupload_bytes():
    ...  # yield byte content

await client.post(url, content=upload_bytes())
```

### Explicit transport instances

When instantiating a transport instance directly, you need to use `httpx.AsyncHTTPTransport`.

For instance:

```
>>> importhttpx
>>> transport = httpx.AsyncHTTPTransport(retries=1)
>>> async with httpx.AsyncClient(transport=transport) as client:
>>>     ...
```

## Supported async environments

HTTPX supports either `asyncio` or `trio` as an async environment.

It will auto-detect which of those two to use as the backend
for socket operations and concurrency primitives.

### [AsyncIO](https://docs.python.org/3/library/asyncio.html)

AsyncIO is Python's [built-in library](https://docs.python.org/3/library/asyncio.html)
for writing concurrent code with the async/await syntax.

```
importasyncio
importhttpx

async defmain():
    async with httpx.AsyncClient() as client:
        response = await client.get('https://www.example.com/')
        print(response)

asyncio.run(main())
```

### [Trio](https://github.com/python-trio/trio)

Trio is [an alternative async library](https://trio.readthedocs.io/en/stable/),
designed around the [the principles of structured concurrency](https://en.wikipedia.org/wiki/Structured_concurrency).

```
importhttpx
importtrio

async defmain():
    async with httpx.AsyncClient() as client:
        response = await client.get('https://www.example.com/')
        print(response)

trio.run(main)
```

Important

The `trio` package must be installed to use the Trio backend.

### [AnyIO](https://github.com/agronholm/anyio)

AnyIO is an [asynchronous networking and concurrency library](https://anyio.readthedocs.io/) that works on top of either `asyncio` or `trio`. It blends in with native libraries of your chosen backend (defaults to `asyncio`).

```
importhttpx
importanyio

async defmain():
    async with httpx.AsyncClient() as client:
        response = await client.get('https://www.example.com/')
        print(response)

anyio.run(main, backend='trio')
```

## Calling into Python Web Apps

For details on calling directly into ASGI applications, see [the `ASGITransport` docs](../advanced/transports#asgitransport).

---

## 4. Transports

HTTPX's `Client` also accepts a `transport` argument. This argument allows you
to provide a custom Transport object that will be used to perform the actual
sending of the requests.

## HTTP Transport

For some advanced configuration you might need to instantiate a transport
class directly, and pass it to the client instance. One example is the
`local_address` configuration which is only available via this low-level API.

```
>>> importhttpx
>>> transport = httpx.HTTPTransport(local_address="0.0.0.0")
>>> client = httpx.Client(transport=transport)
```

Connection retries are also available via this interface. Requests will be retried the given number of times in case an `httpx.ConnectError` or an `httpx.ConnectTimeout` occurs, allowing smoother operation under flaky networks. If you need other forms of retry behaviors, such as handling read/write errors or reacting to `503 Service Unavailable`, consider general-purpose tools such as [tenacity](https://github.com/jd/tenacity).

```
>>> importhttpx
>>> transport = httpx.HTTPTransport(retries=1)
>>> client = httpx.Client(transport=transport)
```

Similarly, instantiating a transport directly provides a `uds` option for
connecting via a Unix Domain Socket that is only available via this low-level API:

```
>>> importhttpx
>>> # Connect to the Docker API via a Unix Socket.
>>> transport = httpx.HTTPTransport(uds="/var/run/docker.sock")
>>> client = httpx.Client(transport=transport)
>>> response = client.get("http://docker/info")
>>> response.json()
{"ID": "...", "Containers": 4, "Images": 74, ...}
```

## WSGI Transport

You can configure an `httpx` client to call directly into a Python web application using the WSGI protocol.

This is particularly useful for two main use-cases:

* Using `httpx` as a client inside test cases.
* Mocking out external services during tests or in dev or staging environments.

### Example

Here's an example of integrating against a Flask application:

```
fromflaskimport Flask
importhttpx

app = Flask(__name__)

@app.route("/")
defhello():
    return "Hello World!"

transport = httpx.WSGITransport(app=app)
with httpx.Client(transport=transport, base_url="http://testserver") as client:
    r = client.get("/")
    assert r.status_code == 200
    assert r.text == "Hello World!"
```

### Configuration

For some more complex cases you might need to customize the WSGI transport. This allows you to:

* Inspect 500 error responses rather than raise exceptions by setting `raise_app_exceptions=False`.
* Mount the WSGI application at a subpath by setting `script_name` (WSGI).
* Use a given client address for requests by setting `remote_addr` (WSGI).

For example:

```
# Instantiate a client that makes WSGI requests with a client IP of "1.2.3.4".
transport = httpx.WSGITransport(app=app, remote_addr="1.2.3.4")
with httpx.Client(transport=transport, base_url="http://testserver") as client:
    ...
```

## ASGI Transport

You can configure an `httpx` client to call directly into an async Python web application using the ASGI protocol.

This is particularly useful for two main use-cases:

* Using `httpx` as a client inside test cases.
* Mocking out external services during tests or in dev or staging environments.

### Example

Let's take this Starlette application as an example:

```
fromstarlette.applicationsimport Starlette
fromstarlette.responsesimport HTMLResponse
fromstarlette.routingimport Route

async defhello(request):
    return HTMLResponse("Hello World!")

app = Starlette(routes=[Route("/", hello)])
```

We can make requests directly against the application, like so:

```
transport = httpx.ASGITransport(app=app)

async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
    r = await client.get("/")
    assert r.status_code == 200
    assert r.text == "Hello World!"
```

### Configuration

For some more complex cases you might need to customise the ASGI transport. This allows you to:

* Inspect 500 error responses rather than raise exceptions by setting `raise_app_exceptions=False`.
* Mount the ASGI application at a subpath by setting `root_path`.
* Use a given client address for requests by setting `client`.

For example:

```
# Instantiate a client that makes ASGI requests with a client IP of "1.2.3.4",
# on port 123.
transport = httpx.ASGITransport(app=app, client=("1.2.3.4", 123))
async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
    ...
```

See [the ASGI documentation](https://asgi.readthedocs.io/en/latest/specs/www.html#connection-scope) for more details on the `client` and `root_path` keys.

### ASGI startup and shutdown

It is not in the scope of HTTPX to trigger ASGI lifespan events of your app.

However it is suggested to use `LifespanManager` from [asgi-lifespan](https://github.com/florimondmanca/asgi-lifespan#usage) in pair with `AsyncClient`.

## Custom transports

A transport instance must implement the low-level Transport API which deals
with sending a single request, and returning a response. You should either
subclass `httpx.BaseTransport` to implement a transport to use with `Client`,
or subclass `httpx.AsyncBaseTransport` to implement a transport to
use with `AsyncClient`.

At the layer of the transport API we're using the familiar `Request` and
`Response` models.

See the `handle_request` and `handle_async_request` docstrings for more details
on the specifics of the Transport API.

A complete example of a custom transport implementation would be:

```
importjson
importhttpx

classHelloWorldTransport(httpx.BaseTransport):
"""
    A mock transport that always returns a JSON "Hello, world!" response.
    """

    defhandle_request(self, request):
        return httpx.Response(200, json={"text": "Hello, world!"})
```

Or this example, which uses a custom transport and `httpx.Mounts` to always redirect `http://` requests.

```
classHTTPSRedirect(httpx.BaseTransport):
"""
    A transport that always redirects to HTTPS.
    """
    defhandle_request(self, request):
        url = request.url.copy_with(scheme="https")
        return httpx.Response(303, headers={"Location": str(url)})

# A client where any `http` requests are always redirected to `https`
transport = httpx.Mounts({
    'http://': HTTPSRedirect()
    'https://': httpx.HTTPTransport()
})
client = httpx.Client(transport=transport)
```

A useful pattern here is custom transport classes that wrap the default HTTP implementation. For example...

```
classDebuggingTransport(httpx.BaseTransport):
    def__init__(self, **kwargs):
        self._wrapper = httpx.HTTPTransport(**kwargs)

    defhandle_request(self, request):
        print(f">>> {request}")
        response = self._wrapper.handle_request(request)
        print(f"<<< {response}")
        return response

    defclose(self):
        self._wrapper.close()

transport = DebuggingTransport()
client = httpx.Client(transport=transport)
```

Here's another case, where we're using a round-robin across a number of different proxies...

```
classProxyRoundRobin(httpx.BaseTransport):
    def__init__(self, proxies, **kwargs):
        self._transports = [
            httpx.HTTPTransport(proxy=proxy, **kwargs)
            for proxy in proxies
        ]
        self._idx = 0

    defhandle_request(self, request):
        transport = self._transports[self._idx]
        self._idx = (self._idx + 1) % len(self._transports)
        return transport.handle_request(request)

    defclose(self):
        for transport in self._transports:
            transport.close()

proxies = [
    httpx.Proxy("http://127.0.0.1:8081"),
    httpx.Proxy("http://127.0.0.1:8082"),
    httpx.Proxy("http://127.0.0.1:8083"),
]
transport = ProxyRoundRobin(proxies=proxies)
client = httpx.Client(transport=transport)
```

## Mock transports

During testing it can often be useful to be able to mock out a transport,
and return pre-determined responses, rather than making actual network requests.

The `httpx.MockTransport` class accepts a handler function, which can be used
to map requests onto pre-determined responses:

```
defhandler(request):
    return httpx.Response(200, json={"text": "Hello, world!"})

# Switch to a mock transport, if the TESTING environment variable is set.
if os.environ.get('TESTING', '').upper() == "TRUE":
    transport = httpx.MockTransport(handler)
else:
    transport = httpx.HTTPTransport()

client = httpx.Client(transport=transport)
```

For more advanced use-cases you might want to take a look at either [the third-party
mocking library, RESPX](https://lundberg.github.io/respx/), or the [pytest-httpx library](https://github.com/Colin-b/pytest_httpx).

## Mounting transports

You can also mount transports against given schemes or domains, to control
which transport an outgoing request should be routed via, with [the same style
used for specifying proxy routing](#routing).

```
importhttpx

classHTTPSRedirectTransport(httpx.BaseTransport):
"""
    A transport that always redirects to HTTPS.
    """

    defhandle_request(self, method, url, headers, stream, extensions):
        scheme, host, port, path = url
        if port is None:
            location = b"https://%s%s" % (host, path)
        else:
            location = b"https://%s:%d%s" % (host, port, path)
        stream = httpx.ByteStream(b"")
        headers = [(b"location", location)]
        extensions = {}
        return 303, headers, stream, extensions

# A client where any `http` requests are always redirected to `https`
mounts = {'http://': HTTPSRedirectTransport()}
client = httpx.Client(mounts=mounts)
```

A couple of other sketches of how you might take advantage of mounted transports...

Disabling HTTP/2 on a single given domain...

```
mounts = {
    "all://": httpx.HTTPTransport(http2=True),
    "all://*example.org": httpx.HTTPTransport()
}
client = httpx.Client(mounts=mounts)
```

Mocking requests to a given domain:

```
# All requests to "example.org" should be mocked out.
# Other requests occur as usual.
defhandler(request):
    return httpx.Response(200, json={"text": "Hello, World!"})

mounts = {"all://example.org": httpx.MockTransport(handler)}
client = httpx.Client(mounts=mounts)
```

Adding support for custom schemes:

```
# Support URLs like "file:///Users/sylvia_green/websites/new_client/index.html"
mounts = {"file://": FileSystemTransport()}
client = httpx.Client(mounts=mounts)
```

### Routing

HTTPX provides a powerful mechanism for routing requests, allowing you to write complex rules that specify which transport should be used for each request.

The `mounts` dictionary maps URL patterns to HTTP transports. HTTPX matches requested URLs against URL patterns to decide which transport should be used, if any. Matching is done from most specific URL patterns (e.g. `https://<domain>:<port>`) to least specific ones (e.g. `https://`).

HTTPX supports routing requests based on **scheme**, **domain**, **port**, or a combination of these.

### Wildcard routing

Route everything through a transport...

```
mounts = {
    "all://": httpx.HTTPTransport(proxy="http://localhost:8030"),
}
```

### Scheme routing

Route HTTP requests through one transport, and HTTPS requests through another...

```
mounts = {
    "http://": httpx.HTTPTransport(proxy="http://localhost:8030"),
    "https://": httpx.HTTPTransport(proxy="http://localhost:8031"),
}
```

### Domain routing

Proxy all requests on domain "example.com", let other requests pass through...

```
mounts = {
    "all://example.com": httpx.HTTPTransport(proxy="http://localhost:8030"),
}
```

Proxy HTTP requests on domain "example.com", let HTTPS and other requests pass through...

```
mounts = {
    "http://example.com": httpx.HTTPTransport(proxy="http://localhost:8030"),
}
```

Proxy all requests to "example.com" and its subdomains, let other requests pass through...

```
mounts = {
    "all://*example.com": httpx.HTTPTransport(proxy="http://localhost:8030"),
}
```

Proxy all requests to strict subdomains of "example.com", let "example.com" and other requests pass through...

```
mounts = {
    "all://*.example.com": httpx.HTTPTransport(proxy="http://localhost:8030"),
}
```

### Port routing

Proxy HTTPS requests on port 1234 to "example.com"...

```
mounts = {
    "https://example.com:1234": httpx.HTTPTransport(proxy="http://localhost:8030"),
}
```

Proxy all requests on port 1234...

```
mounts = {
    "all://*:1234": httpx.HTTPTransport(proxy="http://localhost:8030"),
}
```

### No-proxy support

It is also possible to define requests that *shouldn't* be routed through the transport.

To do so, pass `None` as the proxy URL. For example...

```
mounts = {
    # Route requests through a proxy by default...
    "all://": httpx.HTTPTransport(proxy="http://localhost:8031"),
    # Except those for "example.com".
    "all://example.com": None,
}
```

### Complex configuration example

You can combine the routing features outlined above to build complex proxy routing configurations. For example...

```
mounts = {
    # Route all traffic through a proxy by default...
    "all://": httpx.HTTPTransport(proxy="http://localhost:8030"),
    # But don't use proxies for HTTPS requests to "domain.io"...
    "https://domain.io": None,
    # And use another proxy for requests to "example.com" and its subdomains...
    "all://*example.com": httpx.HTTPTransport(proxy="http://localhost:8031"),
    # And yet another proxy if HTTP is used,
    # and the "internal" subdomain on port 5550 is requested...
    "http://internal.example.com:5550": httpx.HTTPTransport(proxy="http://localhost:8032"),
}
```

### Environment variables

There are also environment variables that can be used to control the dictionary of the client mounts.
They can be used to configure HTTP proxying for clients.

See documentation on [`HTTP_PROXY`, `HTTPS_PROXY`, `ALL_PROXY`](../../environment_variables/#http_proxy-https_proxy-all_proxy)
and [`NO_PROXY`](../../environment_variables/#no_proxy) for more information.

---

## 5. QuickStart

First, start by importing HTTPX:

```
>>> importhttpx
```

Now, let’s try to get a webpage.

```
>>> r = httpx.get('https://httpbin.org/get')
>>> r
<Response [200 OK]>
```

Similarly, to make an HTTP POST request:

```
>>> r = httpx.post('https://httpbin.org/post', data={'key': 'value'})
```

The PUT, DELETE, HEAD, and OPTIONS requests all follow the same style:

```
>>> r = httpx.put('https://httpbin.org/put', data={'key': 'value'})
>>> r = httpx.delete('https://httpbin.org/delete')
>>> r = httpx.head('https://httpbin.org/get')
>>> r = httpx.options('https://httpbin.org/get')
```

## Passing Parameters in URLs

To include URL query parameters in the request, use the `params` keyword:

```
>>> params = {'key1': 'value1', 'key2': 'value2'}
>>> r = httpx.get('https://httpbin.org/get', params=params)
```

To see how the values get encoding into the URL string, we can inspect the
resulting URL that was used to make the request:

```
>>> r.url
URL('https://httpbin.org/get?key2=value2&key1=value1')
```

You can also pass a list of items as a value:

```
>>> params = {'key1': 'value1', 'key2': ['value2', 'value3']}
>>> r = httpx.get('https://httpbin.org/get', params=params)
>>> r.url
URL('https://httpbin.org/get?key1=value1&key2=value2&key2=value3')
```

## Response Content

HTTPX will automatically handle decoding the response content into Unicode text.

```
>>> r = httpx.get('https://www.example.org/')
>>> r.text
'<!doctype html>\n<html>\n<head>\n<title>Example Domain</title>...'
```

You can inspect what encoding will be used to decode the response.

```
>>> r.encoding
'UTF-8'
```

In some cases the response may not contain an explicit encoding, in which case HTTPX
will attempt to automatically determine an encoding to use.

```
>>> r.encoding
None
>>> r.text
'<!doctype html>\n<html>\n<head>\n<title>Example Domain</title>...'
```

If you need to override the standard behaviour and explicitly set the encoding to
use, then you can do that too.

```
>>> r.encoding = 'ISO-8859-1'
```

## Binary Response Content

The response content can also be accessed as bytes, for non-text responses:

```
>>> r.content
b'<!doctype html>\n<html>\n<head>\n<title>Example Domain</title>...'
```

Any `gzip` and `deflate` HTTP response encodings will automatically
be decoded for you. If `brotlipy` is installed, then the `brotli` response
encoding will be supported. If `zstandard` is installed, then `zstd`
response encodings will also be supported.

For example, to create an image from binary data returned by a request, you can use the following code:

```
>>> fromPILimport Image
>>> fromioimport BytesIO
>>> i = Image.open(BytesIO(r.content))
```

## JSON Response Content

Often Web API responses will be encoded as JSON.

```
>>> r = httpx.get('https://api.github.com/events')
>>> r.json()
[{u'repository': {u'open_issues': 0, u'url': 'https://github.com/...' ...  }}]
```

## Custom Headers

To include additional headers in the outgoing request, use the `headers` keyword argument:

```
>>> url = 'https://httpbin.org/headers'
>>> headers = {'user-agent': 'my-app/0.0.1'}
>>> r = httpx.get(url, headers=headers)
```

## Sending Form Encoded Data

Some types of HTTP requests, such as `POST` and `PUT` requests, can include data
in the request body. One common way of including that is as form-encoded data,
which is used for HTML forms.

```
>>> data = {'key1': 'value1', 'key2': 'value2'}
>>> r = httpx.post("https://httpbin.org/post", data=data)
>>> print(r.text)
{
  ...
  "form": {
    "key2": "value2",
    "key1": "value1"
  },
  ...
}
```

Form encoded data can also include multiple values from a given key.

```
>>> data = {'key1': ['value1', 'value2']}
>>> r = httpx.post("https://httpbin.org/post", data=data)
>>> print(r.text)
{
  ...
  "form": {
    "key1": [
      "value1",
      "value2"
    ]
  },
  ...
}
```

## Sending Multipart File Uploads

You can also upload files, using HTTP multipart encoding:

```
>>> with open('report.xls', 'rb') as report_file:
...     files = {'upload-file': report_file}
...     r = httpx.post("https://httpbin.org/post", files=files)
>>> print(r.text)
{
  ...
  "files": {
    "upload-file": "<... binary content ...>"
  },
  ...
}
```

You can also explicitly set the filename and content type, by using a tuple
of items for the file value:

```
>>> with open('report.xls', 'rb') report_file:
...     files = {'upload-file': ('report.xls', report_file, 'application/vnd.ms-excel')}
...     r = httpx.post("https://httpbin.org/post", files=files)
>>> print(r.text)
{
  ...
  "files": {
    "upload-file": "<... binary content ...>"
  },
  ...
}
```

If you need to include non-file data fields in the multipart form, use the `data=...` parameter:

```
>>> data = {'message': 'Hello, world!'}
>>> with open('report.xls', 'rb') as report_file:
...     files = {'file': report_file}
...     r = httpx.post("https://httpbin.org/post", data=data, files=files)
>>> print(r.text)
{
  ...
  "files": {
    "file": "<... binary content ...>"
  },
  "form": {
    "message": "Hello, world!",
  },
  ...
}
```

## Sending JSON Encoded Data

Form encoded data is okay if all you need is a simple key-value data structure.
For more complicated data structures you'll often want to use JSON encoding instead.

```
>>> data = {'integer': 123, 'boolean': True, 'list': ['a', 'b', 'c']}
>>> r = httpx.post("https://httpbin.org/post", json=data)
>>> print(r.text)
{
  ...
  "json": {
    "boolean": true,
    "integer": 123,
    "list": [
      "a",
      "b",
      "c"
    ]
  },
  ...
}
```

## Sending Binary Request Data

For other encodings, you should use the `content=...` parameter, passing
either a `bytes` type or a generator that yields `bytes`.

```
>>> content = b'Hello, world'
>>> r = httpx.post("https://httpbin.org/post", content=content)
```

You may also want to set a custom `Content-Type` header when uploading
binary data.

## Response Status Codes

We can inspect the HTTP status code of the response:

```
>>> r = httpx.get('https://httpbin.org/get')
>>> r.status_code
200
```

HTTPX also includes an easy shortcut for accessing status codes by their text phrase.

```
>>> r.status_code == httpx.codes.OK
True
```

We can raise an exception for any responses which are not a 2xx success code:

```
>>> not_found = httpx.get('https://httpbin.org/status/404')
>>> not_found.status_code
404
>>> not_found.raise_for_status()
Traceback (most recent call last):
  File "/Users/tomchristie/GitHub/encode/httpcore/httpx/models.py", line 837, in raise_for_status
raise HTTPStatusError(message, response=self)
httpx._exceptions.HTTPStatusError: 404 Client Error: Not Found for url: https://httpbin.org/status/404
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404
```

Any successful response codes will return the `Response` instance rather than raising an exception.

```
>>> r.raise_for_status()
```

The method returns the response instance, allowing you to use it inline. For example:

```
>>> r = httpx.get('...').raise_for_status()
>>> data = httpx.get('...').raise_for_status().json()
```

## Response Headers

The response headers are available as a dictionary-like interface.

```
>>> r.headers
Headers({
    'content-encoding': 'gzip',
    'transfer-encoding': 'chunked',
    'connection': 'close',
    'server': 'nginx/1.0.4',
    'x-runtime': '148ms',
    'etag': '"e1ca502697e5c9317743dc078f67693f"',
    'content-type': 'application/json'
})
```

The `Headers` data type is case-insensitive, so you can use any capitalization.

```
>>> r.headers['Content-Type']
'application/json'

>>> r.headers.get('content-type')
'application/json'
```

Multiple values for a single response header are represented as a single comma-separated value, as per [RFC 7230](https://tools.ietf.org/html/rfc7230#section-3.2):

> A recipient MAY combine multiple header fields with the same field name into one “field-name: field-value” pair, without changing the semantics of the message, by appending each subsequent field-value to the combined field value in order, separated by a comma.

## Streaming Responses

For large downloads you may want to use streaming responses that do not load the entire response body into memory at once.

You can stream the binary content of the response...

```
>>> with httpx.stream("GET", "https://www.example.com") as r:
...     for data in r.iter_bytes():
...         print(data)
```

Or the text of the response...

```
>>> with httpx.stream("GET", "https://www.example.com") as r:
...     for text in r.iter_text():
...         print(text)
```

Or stream the text, on a line-by-line basis...

```
>>> with httpx.stream("GET", "https://www.example.com") as r:
...     for line in r.iter_lines():
...         print(line)
```

HTTPX will use universal line endings, normalising all cases to `\n`.

In some cases you might want to access the raw bytes on the response without applying any HTTP content decoding. In this case any content encoding that the web server has applied such as `gzip`, `deflate`, `brotli`, or `zstd` will
not be automatically decoded.

```
>>> with httpx.stream("GET", "https://www.example.com") as r:
...     for chunk in r.iter_raw():
...         print(chunk)
```

If you're using streaming responses in any of these ways then the `response.content` and `response.text` attributes will not be available, and will raise errors if accessed. However you can also use the response streaming functionality to conditionally load the response body:

```
>>> with httpx.stream("GET", "https://www.example.com") as r:
...     if int(r.headers['Content-Length']) < TOO_LONG:
...         r.read()
...         print(r.text)
```

## Cookies

Any cookies that are set on the response can be easily accessed:

```
>>> r = httpx.get('https://httpbin.org/cookies/set?chocolate=chip')
>>> r.cookies['chocolate']
'chip'
```

To include cookies in an outgoing request, use the `cookies` parameter:

```
>>> cookies = {"peanut": "butter"}
>>> r = httpx.get('https://httpbin.org/cookies', cookies=cookies)
>>> r.json()
{'cookies': {'peanut': 'butter'}}
```

Cookies are returned in a `Cookies` instance, which is a dict-like data structure
with additional API for accessing cookies by their domain or path.

```
>>> cookies = httpx.Cookies()
>>> cookies.set('cookie_on_domain', 'hello, there!', domain='httpbin.org')
>>> cookies.set('cookie_off_domain', 'nope.', domain='example.org')
>>> r = httpx.get('http://httpbin.org/cookies', cookies=cookies)
>>> r.json()
{'cookies': {'cookie_on_domain': 'hello, there!'}}
```

## Redirection and History

By default, HTTPX will **not** follow redirects for all HTTP methods, although
this can be explicitly enabled.

For example, GitHub redirects all HTTP requests to HTTPS.

```
>>> r = httpx.get('http://github.com/')
>>> r.status_code
301
>>> r.history
[]
>>> r.next_request
<Request('GET', 'https://github.com/')>
```

You can modify the default redirection handling with the `follow_redirects` parameter:

```
>>> r = httpx.get('http://github.com/', follow_redirects=True)
>>> r.url
URL('https://github.com/')
>>> r.status_code
200
>>> r.history
[<Response [301 Moved Permanently]>]
```

The `history` property of the response can be used to inspect any followed redirects.
It contains a list of any redirect responses that were followed, in the order
in which they were made.

## Timeouts

HTTPX defaults to including reasonable timeouts for all network operations,
meaning that if a connection is not properly established then it should always
raise an error rather than hanging indefinitely.

The default timeout for network inactivity is five seconds. You can modify the
value to be more or less strict:

```
>>> httpx.get('https://github.com/', timeout=0.001)
```

You can also disable the timeout behavior completely...

```
>>> httpx.get('https://github.com/', timeout=None)
```

For advanced timeout management, see [Timeout fine-tuning](../advanced/timeouts/#fine-tuning-the-configuration).

## Authentication

HTTPX supports Basic and Digest HTTP authentication.

To provide Basic authentication credentials, pass a 2-tuple of
plaintext `str` or `bytes` objects as the `auth` argument to the request
functions:

```
>>> httpx.get("https://example.com", auth=("my_user", "password123"))
```

To provide credentials for Digest authentication you'll need to instantiate
a `DigestAuth` object with the plaintext username and password as arguments.
This object can be then passed as the `auth` argument to the request methods
as above:

```
>>> auth = httpx.DigestAuth("my_user", "password123")
>>> httpx.get("https://example.com", auth=auth)
<Response [200 OK]>
```

## Exceptions

HTTPX will raise exceptions if an error occurs.

The most important exception classes in HTTPX are `RequestError` and `HTTPStatusError`.

The `RequestError` class is a superclass that encompasses any exception that occurs
while issuing an HTTP request. These exceptions include a `.request` attribute.

```
try:
    response = httpx.get("https://www.example.com/")
except httpx.RequestError as exc:
    print(f"An error occurred while requesting {exc.request.url!r}.")
```

The `HTTPStatusError` class is raised by `response.raise_for_status()` on responses which are not a 2xx success code.
These exceptions include both a `.request` and a `.response` attribute.

```
response = httpx.get("https://www.example.com/")
try:
    response.raise_for_status()
except httpx.HTTPStatusError as exc:
    print(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.")
```

There is also a base class `HTTPError` that includes both of these categories, and can be used
to catch either failed requests, or 4xx and 5xx responses.

You can either use this base class to catch both categories...

```
try:
    response = httpx.get("https://www.example.com/")
    response.raise_for_status()
except httpx.HTTPError as exc:
    print(f"Error while requesting {exc.request.url!r}.")
```

Or handle each case explicitly...

```
try:
    response = httpx.get("https://www.example.com/")
    response.raise_for_status()
except httpx.RequestError as exc:
    print(f"An error occurred while requesting {exc.request.url!r}.")
except httpx.HTTPStatusError as exc:
    print(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.")
```

For a full list of available exceptions, see [Exceptions (API Reference)](../exceptions/).

---

## Bibliography

1. [Timeouts](https://www.python-httpx.org/advanced/timeouts/)
2. [Clients](https://www.python-httpx.org/advanced/clients/)
3. [Async Support](https://www.python-httpx.org/async/)
4. [Transports](https://www.python-httpx.org/advanced/transports/)
5. [QuickStart](https://www.python-httpx.org/quickstart/)