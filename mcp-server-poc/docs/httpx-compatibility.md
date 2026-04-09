Requests Compatibility - HTTPX

:root{--md-text-font:"Roboto";--md-code-font:"Roboto Mono"}

\_\_md\_scope=new URL("..",location),\_\_md\_hash=e=>[...e].reduce(((e,\_)=>(e<<5)-e+\_.charCodeAt(0)),0),\_\_md\_get=(e,\_=localStorage,t=\_\_md\_scope)=>JSON.parse(\_.getItem(t.pathname+"."+e)),\_\_md\_set=(e,\_,t=localStorage,a=\_\_md\_scope)=>{try{t.setItem(a.pathname+"."+e,JSON.stringify(\_))}catch(e){}}

[Skip to content](#requests-compatibility-guide)

HTTPX

Requests Compatibility

var palette=\_\_md\_get("\_\_palette");if(palette&&palette.color){if("(prefers-color-scheme)"===palette.color.media){var media=matchMedia("(prefers-color-scheme: light)"),input=document.querySelector(media.matches?"[data-md-color-media='(prefers-color-scheme: light)']":"[data-md-color-media='(prefers-color-scheme: dark)']");palette.color.media=input.getAttribute("data-md-color-media"),palette.color.scheme=input.getAttribute("data-md-color-scheme"),palette.color.primary=input.getAttribute("data-md-color-primary"),palette.color.accent=input.getAttribute("data-md-color-accent")}for(var[key,value]of Object.entries(palette.color))document.body.setAttribute("data-md-color-"+key,value)}

Initializing search

[encode/httpx](https://github.com/encode/httpx/ "Go to repository")

HTTPX

[encode/httpx](https://github.com/encode/httpx/ "Go to repository")

* [Introduction](..)
* [QuickStart](../quickstart/)
* Advanced

  Advanced
  + [Clients](../advanced/clients/)
  + [Authentication](../advanced/authentication/)
  + [SSL](../advanced/ssl/)
  + [Proxies](../advanced/proxies/)
  + [Timeouts](../advanced/timeouts/)
  + [Resource Limits](../advanced/resource-limits/)
  + [Event Hooks](../advanced/event-hooks/)
  + [Transports](../advanced/transports/)
  + [Text Encodings](../advanced/text-encodings/)
  + [Extensions](../advanced/extensions/)
* Guides

  Guides
  + [Async Support](../async/)
  + [HTTP/2 Support](../http2/)
  + [Logging](../logging/)
  + Requests Compatibility

    [Requests Compatibility](./)

    Table of contents
    - [Redirects](#redirects)
    - [Client instances](#client-instances)
    - [Request URLs](#request-urls)
    - [Determining the next redirect request](#determining-the-next-redirect-request)
    - [Request Content](#request-content)
    - [Upload files](#upload-files)
    - [Content encoding](#content-encoding)
    - [Cookies](#cookies)
    - [Status Codes](#status-codes)
    - [Streaming responses](#streaming-responses)
    - [Timeouts](#timeouts)
    - [Proxy keys](#proxy-keys)
    - [SSL configuration](#ssl-configuration)
    - [Request body on HTTP methods](#request-body-on-http-methods)
    - [Checking for success and failure responses](#checking-for-success-and-failure-responses)
    - [Request instantiation](#request-instantiation)
    - [Mocking](#mocking)
    - [Caching](#caching)
    - [Networking layer](#networking-layer)
    - [Query Parameters](#query-parameters)
    - [Event Hooks](#event-hooks)
    - [Exceptions and Errors](#exceptions-and-errors)
  + [Troubleshooting](../troubleshooting/)
* API Reference

  API Reference
  + [Developer Interface](../api/)
  + [Exceptions](../exceptions/)
  + [Environment Variables](../environment_variables/)
* Community

  Community
  + [Third Party Packages](../third_party_packages/)
  + [Contributing](../contributing/)
  + [Code of Conduct](../code_of_conduct/)

Table of contents

* [Redirects](#redirects)
* [Client instances](#client-instances)
* [Request URLs](#request-urls)
* [Determining the next redirect request](#determining-the-next-redirect-request)
* [Request Content](#request-content)
* [Upload files](#upload-files)
* [Content encoding](#content-encoding)
* [Cookies](#cookies)
* [Status Codes](#status-codes)
* [Streaming responses](#streaming-responses)
* [Timeouts](#timeouts)
* [Proxy keys](#proxy-keys)
* [SSL configuration](#ssl-configuration)
* [Request body on HTTP methods](#request-body-on-http-methods)
* [Checking for success and failure responses](#checking-for-success-and-failure-responses)
* [Request instantiation](#request-instantiation)
* [Mocking](#mocking)
* [Caching](#caching)
* [Networking layer](#networking-layer)
* [Query Parameters](#query-parameters)
* [Event Hooks](#event-hooks)
* [Exceptions and Errors](#exceptions-and-errors)

# Requests Compatibility Guide

HTTPX aims to be broadly compatible with the `requests` API, although there are a
few design differences in places.

This documentation outlines places where the API differs...

## Redirects

Unlike `requests`, HTTPX does **not follow redirects by default**.

We differ in behaviour here [because auto-redirects can easily mask unnecessary network
calls being made](https://github.com/encode/httpx/discussions/1785).

You can still enable behaviour to automatically follow redirects, but you need to
do so explicitly...

```
response = client.get(url, follow_redirects=True)
```

Or else instantiate a client, with redirect following enabled by default...

```
client = httpx.Client(follow_redirects=True)
```

## Client instances

The HTTPX equivalent of `requests.Session` is `httpx.Client`.

```
session = requests.Session(**kwargs)
```

is generally equivalent to

```
client = httpx.Client(**kwargs)
```

## Request URLs

Accessing `response.url` will return a `URL` instance, rather than a string.

Use `str(response.url)` if you need a string instance.

## Determining the next redirect request

The `requests` library exposes an attribute `response.next`, which can be used to obtain the next redirect request.

```
session = requests.Session()
request = requests.Request("GET", ...).prepare()
while request is not None:
    response = session.send(request, allow_redirects=False)
    request = response.next
```

In HTTPX, this attribute is instead named `response.next_request`. For example:

```
client = httpx.Client()
request = client.build_request("GET", ...)
while request is not None:
    response = client.send(request)
    request = response.next_request
```

## Request Content

For uploading raw text or binary content we prefer to use a `content` parameter,
in order to better separate this usage from the case of uploading form data.

For example, using `content=...` to upload raw content:

```
# Uploading text, bytes, or a bytes iterator.
httpx.post(..., content=b"Hello, world")
```

And using `data=...` to send form data:

```
# Uploading form data.
httpx.post(..., data={"message": "Hello, world"})
```

Using the `data=<text/byte content>` will raise a deprecation warning,
and is expected to be fully removed with the HTTPX 1.0 release.

## Upload files

HTTPX strictly enforces that upload files must be opened in binary mode, in order
to avoid character encoding issues that can result from attempting to upload files
opened in text mode.

## Content encoding

HTTPX uses `utf-8` for encoding `str` request bodies. For example, when using `content=<str>` the request body will be encoded to `utf-8` before being sent over the wire. This differs from Requests which uses `latin1`. If you need an explicit encoding, pass encoded bytes explicitly, e.g. `content=<str>.encode("latin1")`.
For response bodies, assuming the server didn't send an explicit encoding then HTTPX will do its best to figure out an appropriate encoding. HTTPX makes a guess at the encoding to use for decoding the response using `charset_normalizer`. Fallback to that or any content with less than 32 octets will be decoded using `utf-8` with the `error="replace"` decoder strategy.

## Cookies

If using a client instance, then cookies should always be set on the client rather than on a per-request basis.

This usage is supported:

```
client = httpx.Client(cookies=...)
client.post(...)
```

This usage is **not** supported:

```
client = httpx.Client()
client.post(..., cookies=...)
```

We prefer enforcing a stricter API here because it provides clearer expectations around cookie persistence, particularly when redirects occur.

## Status Codes

In our documentation we prefer the uppercased versions, such as `codes.NOT_FOUND`, but also provide lower-cased versions for API compatibility with `requests`.

Requests includes various synonyms for status codes that HTTPX does not support.

## Streaming responses

HTTPX provides a `.stream()` interface rather than using `stream=True`. This ensures that streaming responses are always properly closed outside of the stream block, and makes it visually clearer at which points streaming I/O APIs may be used with a response.

For example:

```
with httpx.stream("GET", "https://www.example.com") as response:
    ...
```

Within a `stream()` block request data is made available with:

* `.iter_bytes()` - Instead of `response.iter_content()`
* `.iter_text()` - Instead of `response.iter_content(decode_unicode=True)`
* `.iter_lines()` - Corresponding to `response.iter_lines()`
* `.iter_raw()` - Use this instead of `response.raw`
* `.read()` - Read the entire response body, making `response.text` and `response.content` available.

## Timeouts

HTTPX defaults to including reasonable [timeouts](../quickstart/#timeouts) for all network operations, while Requests has no timeouts by default.

To get the same behavior as Requests, set the `timeout` parameter to `None`:

```
httpx.get('https://www.example.com', timeout=None)
```

## Proxy keys

HTTPX uses the mounts argument for HTTP proxying and transport routing.
It can do much more than proxies and allows you to configure more than just the proxy route.
For more detailed documentation, see [Mounting Transports](../advanced/transports/#mounting-transports).

When using `httpx.Client(mounts={...})` to map to a selection of different transports, we use full URL schemes, such as `mounts={"http://": ..., "https://": ...}`.

This is different to the `requests` usage of `proxies={"http": ..., "https": ...}`.

This change is for better consistency with more complex mappings, that might also include domain names, such as `mounts={"all://": ..., httpx.HTTPTransport(proxy="all://www.example.com": None})` which maps all requests onto a proxy, except for requests to "www.example.com" which have an explicit exclusion.

Also note that `requests.Session.request(...)` allows a `proxies=...` parameter, whereas `httpx.Client.request(...)` does not allow `mounts=...`.

## SSL configuration

When using a `Client` instance, the ssl configurations should always be passed on client instantiation, rather than passed to the request method.

If you need more than one different SSL configuration, you should use different client instances for each SSL configuration.

## Request body on HTTP methods

The HTTP `GET`, `DELETE`, `HEAD`, and `OPTIONS` methods are specified as not supporting a request body. To stay in line with this, the `.get`, `.delete`, `.head` and `.options` functions do not support `content`, `files`, `data`, or `json` arguments.

If you really do need to send request data using these http methods you should use the generic `.request` function instead.

```
httpx.request(
  method="DELETE",
  url="https://www.example.com/",
  content=b'A request body on a DELETE request.'
)
```

## Checking for success and failure responses

We don't support `response.is_ok` since the naming is ambiguous there, and might incorrectly imply an equivalence to `response.status_code == codes.OK`. Instead we provide the `response.is_success` property, which can be used to check for a 2xx response.

## Request instantiation

There is no notion of [prepared requests](https://requests.readthedocs.io/en/stable/user/advanced/#prepared-requests) in HTTPX. If you need to customize request instantiation, see [Request instances](../advanced/clients/#request-instances).

Besides, `httpx.Request()` does not support the `auth`, `timeout`, `follow_redirects`, `mounts`, `verify` and `cert` parameters. However these are available in `httpx.request`, `httpx.get`, `httpx.post` etc., as well as on [`Client` instances](../advanced/clients/#client-instances).

## Mocking

If you need to mock HTTPX the same way that test utilities like `responses` and `requests-mock` does for `requests`, see [RESPX](https://github.com/lundberg/respx).

## Caching

If you use `cachecontrol` or `requests-cache` to add HTTP Caching support to the `requests` library, you can use [Hishel](https://hishel.com) for HTTPX.

## Networking layer

`requests` defers most of its HTTP networking code to the excellent [`urllib3` library](https://urllib3.readthedocs.io/en/latest/).

On the other hand, HTTPX uses [HTTPCore](https://github.com/encode/httpcore) as its core HTTP networking layer, which is a different project than `urllib3`.

## Query Parameters

`requests` omits `params` whose values are `None` (e.g. `requests.get(..., params={"foo": None})`). This is not supported by HTTPX.

For both query params (`params=`) and form data (`data=`), `requests` supports sending a list of tuples (e.g. `requests.get(..., params=[('key1', 'value1'), ('key1', 'value2')])`). This is not supported by HTTPX. Instead, use a dictionary with lists as values. E.g.: `httpx.get(..., params={'key1': ['value1', 'value2']})` or with form data: `httpx.post(..., data={'key1': ['value1', 'value2']})`.

## Event Hooks

`requests` allows event hooks to mutate `Request` and `Response` objects. See [examples](https://requests.readthedocs.io/en/master/user/advanced/#event-hooks) given in the documentation for `requests`.

In HTTPX, event hooks may access properties of requests and responses, but event hook callbacks cannot mutate the original request/response.

If you are looking for more control, consider checking out [Custom Transports](../advanced/transports/#custom-transports).

## Exceptions and Errors

`requests` exception hierarchy is slightly different to the `httpx` exception hierarchy. `requests` exposes a top level `RequestException`, where as `httpx` exposes a top level `HTTPError`. see the exceptions exposes in requests [here](https://requests.readthedocs.io/en/latest/_modules/requests/exceptions/). See the `httpx` error hierarchy [here](https://www.python-httpx.org/exceptions/).

var target=document.getElementById(location.hash.slice(1));target&&target.name&&(target.checked=target.name.startsWith("\_\_tabbed\_"))

Made with
[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)

{"base": "..", "features": [], "search": "../assets/javascripts/workers/search.6ce7567c.min.js", "translations": {"clipboard.copied": "Copied to clipboard", "clipboard.copy": "Copy to clipboard", "search.result.more.one": "1 more on this page", "search.result.more.other": "# more on this page", "search.result.none": "No matching documents", "search.result.one": "1 matching document", "search.result.other": "# matching documents", "search.result.placeholder": "Type to start searching", "search.result.term.missing": "Missing", "select.version": "Select version"}}