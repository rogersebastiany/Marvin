# OpenTelemetry


---

## 1. Metrics

A measurement captured at runtime.

A **metric** is a **measurement** of a service captured at runtime. The moment
of capturing a measurement is known as a **metric event**, which consists not
only of the measurement itself, but also the time at which it was captured and
associated metadata.

Application and request metrics are important indicators of availability and
performance. Custom metrics can provide insights into how availability
indicators impact user experience or the business. Collected data can be used to
alert of an outage or trigger scheduling decisions to scale up a deployment
automatically upon high demand.

To understand how metrics in OpenTelemetry works, let’s look at a list of
components that will play a part in instrumenting our code.

## Meter Provider

A Meter Provider (sometimes called `MeterProvider`) is a factory for `Meter`s.
In most applications, a Meter Provider is initialized once and its lifecycle
matches the application’s lifecycle. Meter Provider initialization also includes
Resource and Exporter initialization. It is typically the first step in metering
with OpenTelemetry. In some language SDKs, a global Meter Provider is already
initialized for you.

## Meter

A Meter creates [metric instruments](#metric-instruments), capturing
measurements about a service at runtime. Meters are created from Meter
Providers.

## Metric Exporter

Metric Exporters send metric data to a consumer. This consumer can be standard
output for debugging during development, the OpenTelemetry Collector, or any
open source or vendor backend of your choice.

## Metric Instruments

In OpenTelemetry measurements are captured by **metric instruments**. A metric
instrument is defined by:

* Name
* Kind
* Unit (optional)
* Description (optional)

The name, unit, and description are chosen by the developer or defined via
[semantic conventions](/docs/specs/semconv/general/metrics/) for common ones
like request and process metrics.

The instrument kind is one of the following:

* **Counter**: A value that accumulates over time – you can think of this like
  an odometer on a car; it only ever goes up.
* **Asynchronous Counter**: Same as the **Counter**, but is collected once for
  each export. Could be used if you don’t have access to the continuous
  increments, but only to the aggregated value.
* **UpDownCounter**: A value that accumulates over time, but can also go down
  again. An example could be a queue length, it will increase and decrease with
  the number of work items in the queue.
* **Asynchronous UpDownCounter**: Same as the **UpDownCounter**, but is
  collected once for each export. Could be used if you don’t have access to the
  continuous changes, but only to the aggregated value (e.g., current queue
  size).
* **Gauge**: Measures a current value at the time it is read. An example would
  be the fuel gauge in a vehicle. Gauges are synchronous.
* **Asynchronous Gauge**: Same as the **Gauge**, but is collected once for each
  export. Could be used if you don’t have access to the continuous changes, but
  only to the aggregated value.
* **Histogram**: A client-side aggregation of values, such as request latencies.
  A histogram is a good choice if you are interested in value statistics. For
  example: How many requests take fewer than 1s?

For more on synchronous and asynchronous instruments, and which kind is best
suited for your use case, see
[Supplementary Guidelines](/docs/specs/otel/metrics/supplementary-guidelines/).

## Aggregation

In addition to the metric instruments, the concept of **aggregations** is an
important one to understand. An aggregation is a technique whereby a large
number of measurements are combined into either exact or estimated statistics
about metric events that took place during a time window. The OTLP protocol
transports such aggregated metrics. The OpenTelemetry API provides a default
aggregation for each instrument which can be overridden using the Views. The
OpenTelemetry project aims to provide default aggregations that are supported by
visualizers and telemetry backends.

Unlike [request tracing](../traces/), which is intended to capture request
lifecycles and provide context to the individual pieces of a request, metrics
are intended to provide statistical information in aggregate. Some examples of
use cases for metrics include:

* Reporting the total number of bytes read by a service, per protocol type.
* Reporting the total number of bytes read and the bytes per request.
* Reporting the duration of a system call.
* Reporting request sizes in order to determine a trend.
* Reporting CPU or memory usage of a process.
* Reporting average balance values from an account.
* Reporting current active requests being handled.

## Views

A view provides SDK users with the flexibility to customize the metrics output
by the SDK. You can customize which metric instruments are to be processed or
ignored. You can also customize aggregation and what attributes you want to
report on metrics.

## Language Support

Metrics are a [stable](/docs/specs/otel/versioning-and-stability/#stable) signal
in the OpenTelemetry specification. For the individual language specific
implementations of the Metrics API & SDK, the status is as follows:

| Language | Metrics |
| --- | --- |
| [C++](/docs/languages/cpp/) | Stable |
| [C#/.NET](/docs/languages/dotnet/) | Stable |
| [Erlang/Elixir](/docs/languages/erlang/) | Development |
| [Go](/docs/languages/go/) | Stable |
| [Java](/docs/languages/java/) | Stable |
| [JavaScript](/docs/languages/js/) | Stable |
| [PHP](/docs/languages/php/) | Stable |
| [Python](/docs/languages/python/) | Stable |
| [Ruby](/docs/languages/ruby/) | Development |
| [Rust](/docs/languages/rust/) | Beta |
| [Swift](/docs/languages/swift/) | Development |

## Specification

To learn more about metrics in OpenTelemetry, see the
[metrics specification](/docs/specs/otel/overview/#metric-signal).

## Feedback

Was this page helpful?

Thank you. Your feedback is appreciated!

Please let us know [how we can improve this page](https://github.com/open-telemetry/opentelemetry.io/issues/new?template=PAGE_FEEDBACK.yml&title=[Page+feedback]%3A+ADD+A+SUMMARY+OF+YOUR+FEEDBACK+HERE). Your feedback is appreciated!

  

Last modified July 15, 2025: [fix typo (#7318) (34f672f4)](https://github.com/open-telemetry/opentelemetry.io/commit/34f672f4afbc083423d5c03a03f97c308591d255)

---

## 2. What is OpenTelemetry?

A brief explanation of what OpenTelemetry is and isn’t.

OpenTelemetry is:

* An **[observability](../concepts/observability-primer/#what-is-observability) framework and toolkit** designed to facilitate the

  + [Generation](../concepts/instrumentation)
  + Export
  + [Collection](../concepts/components/#collector)

  of [telemetry data](../concepts/signals/) such as [traces](../concepts/signals/traces/), [metrics](../concepts/signals/metrics/), and [logs](../concepts/signals/logs/).
* **Open source**, as well as **vendor- and tool-agnostic**, meaning that it can
  be used with a broad variety of observability backends, including open source
  tools like [Jaeger](https://www.jaegertracing.io/) and [Prometheus](https://prometheus.io/), as well as commercial offerings.
  OpenTelemetry is **not** an observability backend itself.

A major goal of OpenTelemetry is to enable easy instrumentation of your
applications and systems, regardless of the programming language,
infrastructure, and runtime environments used.

The backend (storage) and the frontend (visualization) of telemetry data are
intentionally left to other tools.

For more videos in this series and additional resources, see
[What next?](#what-next)

## What is observability?

[Observability](../concepts/observability-primer/#what-is-observability) is the ability to understand the internal state of a system by
examining its outputs.

In software, this is typically achieved by analyzing telemetry data such as
traces, metrics, and logs.

To make a system observable, it must be [instrumented](../concepts/instrumentation). That is, the code
must emit [traces](../concepts/signals/traces/), [metrics](../concepts/signals/metrics/), or [logs](../concepts/signals/logs/). The instrumented data must then
be sent to an observability backend.

## Why OpenTelemetry?

With the rise of cloud computing, microservices architectures, and increasingly
complex business requirements, the need for software and infrastructure
[observability](../concepts/observability-primer/#what-is-observability) is greater than ever.

OpenTelemetry satisfies the need for observability while following two key
principles:

1. You own the data that you generate. There’s no vendor lock-in.
2. You only have to learn a single set of APIs and conventions.

Both principles combined grant teams and organizations the flexibility they need
in today’s modern computing world.

If you want to learn more, take a look at OpenTelemetry’s
[mission, vision, and values](/community/mission/).

## Main OpenTelemetry components

OpenTelemetry consists of the following major components:

* A [specification](/docs/specs/otel/) for all components
* A standard [protocol](/docs/specs/otlp/) that defines the shape of telemetry
  data
* [Semantic conventions](/docs/specs/semconv/) that define a standard naming
  scheme for common telemetry data types
* APIs that define how to generate telemetry data
* [Language SDKs](../languages) that implement the specification, APIs, and
  export of telemetry data
* A [library ecosystem](/ecosystem/registry/) that implements instrumentation for
  common libraries and frameworks
* Automatic instrumentation components that generate telemetry data without
  requiring code changes
* The [OpenTelemetry Collector](../collector), a proxy that receives, processes,
  and exports telemetry data
* Various other tools, such as the
  [OpenTelemetry Operator for Kubernetes](../platforms/kubernetes/operator/),
  [OpenTelemetry Helm Charts](../platforms/kubernetes/helm/), and
  [community assets for FaaS](../platforms/faas/)

OpenTelemetry is used by a wide variety of
[libraries, services and apps](/ecosystem/integrations/) that have OpenTelemetry
integrated to provide observability by default.

OpenTelemetry is supported by numerous [vendors](/ecosystem/vendors/), many of
whom provide commercial support for OpenTelemetry and contribute to the project
directly.

## Extensibility

OpenTelemetry is designed to be extensible. Some examples of how it can be
extended include:

* Adding a receiver to the OpenTelemetry Collector to support telemetry data
  from a custom source
* Loading custom instrumentation libraries into an SDK
* Creating a [distribution](../concepts/distributions/) of an SDK or the
  Collector tailored to a specific use case
* Creating a new exporter for a custom backend that doesn’t yet support the
  OpenTelemetry protocol (OTLP)
* Creating a custom propagator for a nonstandard context propagation format

Although most users might not need to extend OpenTelemetry, the project is
designed to make it possible at nearly every level.

## History

OpenTelemetry is a [Cloud Native Computing Foundation](https://www.cncf.io) (CNCF) project that is
the result of a [merger](https://www.cncf.io/blog/2019/05/21/a-brief-history-of-opentelemetry-so-far/) between two prior projects,
[OpenTracing](https://opentracing.io) and [OpenCensus](https://opencensus.io).
Both of these projects were created to solve the same problem: the lack of a
standard for how to instrument code and send telemetry data to an Observability
backend. As neither project was fully able to solve the problem independently,
they merged to form OpenTelemetry and combine their strengths while offering a
single solution.

If you are currently using OpenTracing or OpenCensus, you can learn how to
migrate to OpenTelemetry in the [Migration guide](../compatibility/migration/).

## What next?

* [Getting started](../getting-started/) — jump right in!
* Learn about [OpenTelemetry concepts](../concepts/).
* [Watch videos](https://www.youtube.com/@otel-official) from the [OTel for beginners](https://www.youtube.com/playlist?list=PLVYDBkQ1TdyyWjeWJSjXYUaJFVhplRtvN) or other [playlists](https://www.youtube.com/@otel-official/playlists).
* Sign up for [training](/training/), including the **free course**
  [Getting started with OpenTelemetry](/training/#courses).

## Feedback

Was this page helpful?

Thank you. Your feedback is appreciated!

Please let us know [how we can improve this page](https://github.com/open-telemetry/opentelemetry.io/issues/new?template=PAGE_FEEDBACK.yml&title=[Page+feedback]%3A+ADD+A+SUMMARY+OF+YOUR+FEEDBACK+HERE). Your feedback is appreciated!

  

Last modified April 6, 2026: [docs: improve clarity in observability definition (#9530) (ee9a3aeb)](https://github.com/open-telemetry/opentelemetry.io/commit/ee9a3aeb6501bb788a03571f08be856dfdedc4d5)

---

## 3. Traces

The path of a request through your application.

**Traces** give us the big picture of what happens when a request is made to an
application. Whether your application is a monolith with a single database or a
sophisticated mesh of services, traces are essential to understanding the full
“path” a request takes in your application.

Let’s explore this with three units of work, represented as [Spans](#spans):

Note

The following JSON examples do not represent a specific format, and especially
not [OTLP/JSON](/docs/specs/otlp/#json-protobuf-encoding), which is more
verbose.

`hello` span:

```
{
  "name": "hello",
  "context": {
    "trace_id": "5b8aa5a2d2c872e8321cf37308d69df2",
    "span_id": "051581bf3cb55c13"
  },
  "parent_id": null,
  "start_time": "2022-04-29T18:52:58.114201Z",
  "end_time": "2022-04-29T18:52:58.114687Z",
  "attributes": {
    "http.route": "some_route1"
  },
  "events": [
    {
      "name": "Guten Tag!",
      "timestamp": "2022-04-29T18:52:58.114561Z",
      "attributes": {
        "event_attributes": 1
      }
    }
  ]
}
```

This is the root span, denoting the beginning and end of the entire operation.
Note that it has a `trace_id` field indicating the trace, but has no
`parent_id`. That’s how you know it’s the root span.

`hello-greetings` span:

```
{
  "name": "hello-greetings",
  "context": {
    "trace_id": "5b8aa5a2d2c872e8321cf37308d69df2",
    "span_id": "5fb397be34d26b51"
  },
  "parent_id": "051581bf3cb55c13",
  "start_time": "2022-04-29T18:52:58.114304Z",
  "end_time": "2022-04-29T22:52:58.114561Z",
  "attributes": {
    "http.route": "some_route2"
  },
  "events": [
    {
      "name": "hey there!",
      "timestamp": "2022-04-29T18:52:58.114561Z",
      "attributes": {
        "event_attributes": 1
      }
    },
    {
      "name": "bye now!",
      "timestamp": "2022-04-29T18:52:58.114585Z",
      "attributes": {
        "event_attributes": 1
      }
    }
  ]
}
```

This span encapsulates specific tasks, like saying greetings, and its parent is
the `hello` span. Note that it shares the same `trace_id` as the root span,
indicating it’s a part of the same trace. Additionally, it has a `parent_id`
that matches the `span_id` of the `hello` span.

`hello-salutations` span:

```
{
  "name": "hello-salutations",
  "context": {
    "trace_id": "5b8aa5a2d2c872e8321cf37308d69df2",
    "span_id": "93564f51e1abe1c2"
  },
  "parent_id": "051581bf3cb55c13",
  "start_time": "2022-04-29T18:52:58.114492Z",
  "end_time": "2022-04-29T18:52:58.114631Z",
  "attributes": {
    "http.route": "some_route3"
  },
  "events": [
    {
      "name": "hey there!",
      "timestamp": "2022-04-29T18:52:58.114561Z",
      "attributes": {
        "event_attributes": 1
      }
    }
  ]
}
```

This span represents the third operation in this trace and, like the previous
one, it’s a child of the `hello` span. That also makes it a sibling of the
`hello-greetings` span.

These three blocks of JSON all share the same `trace_id`, and the `parent_id`
field represents a hierarchy. That makes it a Trace!

Another thing you’ll note is that each Span looks like a structured log. That’s
because it kind of is! One way to think of Traces is that they’re a collection
of structured logs with context, correlation, hierarchy, and more baked in.
However, these “structured logs” can come from different processes, services,
VMs, data centers, and so on. This is what allows tracing to represent an
end-to-end view of any system.

To understand how tracing in OpenTelemetry works, let’s look at a list of
components that will play a part in instrumenting our code.

## Tracer Provider

A Tracer Provider (sometimes called `TracerProvider`) is a factory for
`Tracer`s. In most applications, a Tracer Provider is initialized once and its
lifecycle matches the application’s lifecycle. Tracer Provider initialization
also includes Resource and Exporter initialization. It is typically the first
step in tracing with OpenTelemetry. In some language SDKs, a global Tracer
Provider is already initialized for you.

## Tracer

A Tracer creates spans containing more information about what is happening for a
given operation, such as a request in a service. Tracers are created from Tracer
Providers.

## Trace Exporters

Trace Exporters send traces to a consumer. This consumer can be standard output
for debugging and development-time, the OpenTelemetry Collector, or any open
source or vendor backend of your choice.

## Context Propagation

Context Propagation is the core concept that enables Distributed Tracing. With
Context Propagation, Spans can be correlated with each other and assembled into
a trace, regardless of where Spans are generated. To learn more about this
topic, see the concept page on [Context Propagation](../../context-propagation).

## Spans

A **span** represents a unit of work or operation. Spans are the building blocks
of Traces. In OpenTelemetry, they include the following information:

* Name
* Parent span ID (empty for root spans)
* Start and End Timestamps
* [Span Context](#span-context)
* [Attributes](#attributes)
* [Span Events](#span-events)
* [Span Links](#span-links)
* [Span Status](#span-status)

Sample span:

```
{
  "name": "/v1/sys/health",
  "context": {
    "trace_id": "7bba9f33312b3dbb8b2c2c62bb7abe2d",
    "span_id": "086e83747d0e381e"
  },
  "parent_id": "",
  "start_time": "2021-10-22 16:04:01.209458162 +0000 UTC",
  "end_time": "2021-10-22 16:04:01.209514132 +0000 UTC",
  "status_code": "STATUS_CODE_OK",
  "status_message": "",
  "attributes": {
    "net.transport": "IP.TCP",
    "net.peer.ip": "172.17.0.1",
    "net.peer.port": "51820",
    "net.host.ip": "10.177.2.152",
    "net.host.port": "26040",
    "http.method": "GET",
    "http.target": "/v1/sys/health",
    "http.server_name": "mortar-gateway",
    "http.route": "/v1/sys/health",
    "http.user_agent": "Consul Health Check",
    "http.scheme": "http",
    "http.host": "10.177.2.152:26040",
    "http.flavor": "1.1"
  },
  "events": [
    {
      "name": "",
      "message": "OK",
      "timestamp": "2021-10-22 16:04:01.209512872 +0000 UTC"
    }
  ]
}
```

Spans can be nested, as is implied by the presence of a parent span ID: child
spans represent sub-operations. This allows spans to more accurately capture the
work done in an application.

### Span Context

Span context is an immutable object on every span that contains the following:

* The Trace ID representing the trace that the span is a part of
* The span’s Span ID
* Trace Flags, a binary encoding containing information about the trace
* Trace State, a list of key-value pairs that can carry vendor-specific trace
  information

Span context is the part of a span that is serialized and propagated alongside
[Distributed Context](#context-propagation) and [Baggage](../baggage).

Because Span Context contains the Trace ID, it is used when creating
[Span Links](#span-links).

### Attributes

Attributes are key-value pairs that contain metadata that you can use to
annotate a Span to carry information about the operation it is tracking.

For example, if a span tracks an operation that adds an item to a user’s
shopping cart in an eCommerce system, you can capture the user’s ID, the ID of
the item to add to the cart, and the cart ID.

You can add attributes to spans during or after span creation. Prefer adding
attributes at span creation to make the attributes available to SDK sampling. If
you have to add a value after span creation, update the span with the value.

Attributes have the following rules that each language SDK implements:

* Keys must be non-null string values
* Values must be a non-null string, boolean, floating point value, integer, or
  an array of these values

Additionally, there are
[Semantic Attributes](/docs/specs/semconv/general/trace/), which are known
naming conventions for metadata that is typically present in common operations.
It’s helpful to use semantic attribute naming wherever possible so that common
kinds of metadata are standardized across systems.

### Span Events

A Span Event can be thought of as a structured log message (or annotation) on a
Span, typically used to denote a meaningful, singular point in time during the
Span’s duration.

For example, consider two scenarios in a web browser:

1. Tracking a page load
2. Denoting when a page becomes interactive

A Span is best used to track the first scenario because it’s an operation with a
start and an end.

A Span Event is best used to track the second scenario because it represents a
meaningful, singular point in time.

#### When to use span events versus span attributes

Since span events also contain attributes, the question of when to use events
instead of attributes might not always have an obvious answer. To inform your
decision, consider whether a specific timestamp is meaningful.

For example, when you’re tracking an operation with a span and the operation
completes, you might want to add data from the operation to your telemetry.

* If the timestamp in which the operation completes is meaningful or relevant,
  attach the data to a span event.
* If the timestamp isn’t meaningful, attach the data as span attributes.

### Span Links

Links exist so that you can associate one span with one or more spans, implying
a causal relationship. For example, let’s say we have a distributed system where
some operations are tracked by a trace.

In response to some of these operations, an additional operation is queued to be
executed, but its execution is asynchronous. We can track this subsequent
operation with a trace as well.

We would like to associate the trace for the subsequent operations with the
first trace, but we cannot predict when the subsequent operations will start. We
need to associate these two traces, so we will use a span link.

You can link the last span from the first trace to the first span in the second
trace. Now, they are causally associated with one another.

Links are optional but serve as a good way to associate trace spans with one
another.

For more information see [Span Links](/docs/specs/otel/trace/api/#link).

### Span Status

Each span has a status. The three possible values are:

* `Unset`
* `Error`
* `Ok`

The default value is `Unset`. A span status that is `Unset` means that the
operation it tracked successfully completed without an error.

When a span status is `Error`, then that means some error occurred in the
operation it tracks. For example, this could be due to an HTTP 500 error on a
server handling a request.

When a span status is `Ok`, then that means the span was explicitly marked as
error-free by the developer of an application. Although this is unintuitive,
it’s not required to set a span status as `Ok` when a span is known to have
completed without error, as this is covered by `Unset`. What `Ok` does is
represent an unambiguous “final call” on the status of a span that has been
explicitly set by a user. This is helpful in any situation where a developer
wishes for there to be no other interpretation of a span other than
“successful”.

To reiterate: `Unset` represents a span that completed without an error. `Ok`
represents when a developer explicitly marks a span as successful. In most
cases, it is not necessary to explicitly mark a span as `Ok`.

### Span Kind

When a span is created, it is one of `Client`, `Server`, `Internal`, `Producer`,
or `Consumer`. This span kind provides a hint to the tracing backend as to how
the trace should be assembled. According to the OpenTelemetry specification, the
parent of a server span is often a remote client span, and the child of a client
span is usually a server span. Similarly, the parent of a consumer span is
always a producer and the child of a producer span is always a consumer. If not
provided, the span kind is assumed to be internal.

For more information regarding SpanKind, see
[SpanKind](/docs/specs/otel/trace/api/#spankind).

#### Client

A client span represents a synchronous outgoing remote call such as an outgoing
HTTP request or database call. Note that in this context, “synchronous” does not
refer to `async/await`, but to the fact that it is not queued for later
processing.

#### Server

A server span represents a synchronous incoming remote call such as an incoming
HTTP request or remote procedure call.

#### Internal

Internal spans represent operations which do not cross a process boundary.
Things like instrumenting a function call or an Express middleware may use
internal spans.

#### Producer

Producer spans represent the creation of a job which may be asynchronously
processed later. It may be a remote job such as one inserted into a job queue or
a local job handled by an event listener.

#### Consumer

Consumer spans represent the processing of a job created by a producer and may
start long after the producer span has already ended.

## Specification

For more information, see the
[traces specification](/docs/specs/otel/overview/#tracing-signal).

## Feedback

Was this page helpful?

Thank you. Your feedback is appreciated!

Please let us know [how we can improve this page](https://github.com/open-telemetry/opentelemetry.io/issues/new?template=PAGE_FEEDBACK.yml&title=[Page+feedback]%3A+ADD+A+SUMMARY+OF+YOUR+FEEDBACK+HERE). Your feedback is appreciated!

  

Last modified January 14, 2026: [Convert all `en` page Note alerts to markdown syntax (#8894) (6bf06ddb)](https://github.com/open-telemetry/opentelemetry.io/commit/6bf06ddb9fc057dd6e8092f26d988ffe7b1af5ed)

---

## Bibliography

1. [Metrics](https://opentelemetry.io/docs/concepts/signals/metrics/)
2. [What is OpenTelemetry?](https://opentelemetry.io/docs/what-is-opentelemetry/)
3. [Traces](https://opentelemetry.io/docs/concepts/signals/traces/)