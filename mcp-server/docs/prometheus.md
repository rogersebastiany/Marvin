# Prometheus


---

## 1. Querying basics

Prometheus provides a functional query language called PromQL (Prometheus Query
Language) that lets the user select and aggregate time series data in real
time.

When you send a query request to Prometheus, it can be an *instant query*, evaluated at one point in time,
or a *range query* at equally-spaced steps between a start and an end time. PromQL works exactly the same
in each case; the range query is just like an instant query run multiple times at different timestamps.

In the Prometheus UI, the "Table" tab is for instant queries and the "Graph" tab is for range queries.

Other programs can fetch the result of a PromQL expression via the [HTTP API](/docs/prometheus/latest/querying/api/).

## Examples

This document is a Prometheus basic language reference. For learning, it may be easier to
start with a couple of [examples](/docs/prometheus/latest/querying/examples/).

## Samples

The value of a sample at a given timestamp returned by PromQL may be a float or
a [native histogram](/docs/specs/native_histograms/). A
float sample is a simple floating point number, whereas a native histograms
sample contains a full histogram including count, sum, and buckets.

Note that the term “histogram sample” in the PromQL documentation always refers
to a native histogram. The term "classic histogram" refers to a set of time
series containing float samples with the `_bucket`, `_count`, and `_sum`
suffixes that together describe a histogram. From the perspective of PromQL,
these contain just float samples, there are no “classic histogram samples”.

Both float samples and histogram samples can have a counter or a gauge “flavor”.
Float samples with a counter or gauge flavor are generally simply called
“counters” or “gauges”, respectively, while their histogram counterparts are
called “counter histograms” or “gauge histograms”. Float samples do not store
their flavor, leaving it to the user to take their flavor into account when
writing PromQL queries. (By convention, time series containing float counters
have a name ending on `_total` to help with the distinction.)

Since histogram samples “know” their counter or gauge flavor, this allows
reliable warnings about mismatched operations. For example, applying the `rate`
function to gauge floats will most likely produce a
nonsensical result, but the query will be processed without complains. However,
if applied to gauge histograms, the result of the query will be
annotated with a warning.

## Expression language data types

In Prometheus's expression language, an expression or sub-expression can
evaluate to one of four types:

* **Instant vector** - a set of time series containing a single sample for each time series, all sharing the same timestamp
* **Range vector** - a set of time series containing a range of data points over time for each time series
* **Scalar** - a simple numeric floating point value
* **String** - a simple string value; currently unused

Depending on the use case (e.g. when graphing vs. displaying the output of an
expression), only some of these types are legal as the result of a
user-specified expression.
For [instant queries](/docs/prometheus/latest/querying/api/#instant-queries), any of the above data types are allowed as the root of the expression.
[Range queries](/docs/prometheus/latest/querying/api/#range-queries) only support scalar-typed and instant-vector-typed expressions.

Both vectors and time series may contain a mix of float samples and histogram
samples.

## Reconciliation of histogram bucket layouts

Native histograms can have different bucket layouts, but they are generally
convertible to compatible versions to apply binary and aggregation operations
to them. Functions acting on range vectors that are applicable to native
histograms also perform such reconciliation. In binary operations this
reconciliation is performed pairwise, in aggregation operations and functions
all histogram samples are reconciled to one compatible bucket layout.

Not all bucket layouts can be reconciled, if incompatible histograms are
encountered in an operation, the corresponding output vector element is removed
from the result, flagged with a warn-level annotation.
More details can be found in the
[native histogram specification](/docs/specs/native_histograms/#compatibility-between-histograms).

## Literals

The following section describes literal values of various kinds.
Note that there is no “histogram literal”.

### String literals

String literals are designated by single quotes, double quotes or backticks.

PromQL follows the same [escaping rules as
Go](https://golang.org/ref/spec#String_literals). For string literals in single or double quotes, a
backslash begins an escape sequence, which may be followed by `a`, `b`, `f`,
`n`, `r`, `t`, `v` or `\`. Specific characters can be provided using octal
(`\nnn`) or hexadecimal (`\xnn`, `\unnnn` and `\Unnnnnnnn`) notations.

Conversely, escape characters are not parsed in string literals designated by backticks. It is important to note that, unlike Go, Prometheus does not discard newlines inside backticks.

Example:

```
"this is a string"
'these are unescaped: \n \\ \t'
`these are not unescaped: \n ' " \t`
```

### Float literals and time durations

Scalar float values can be written as literal integer or floating-point numbers
in the format (whitespace only included for better readability):

```
[-+]?(
      [0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?
    | 0[xX][0-9a-fA-F]+
    | [nN][aA][nN]
    | [iI][nN][fF]
)
```

Examples:

```
23
-2.43
3.4e-9
0x8f
-Inf
NaN
```

Additionally, underscores (`_`) can be used in between decimal or hexadecimal
digits to improve readability.

Examples:

```
1_000_000
.123_456_789
0x_53_AB_F3_82
```

Float literals are also used to specify durations in seconds. For convenience,
decimal integer numbers may be combined with the following
time units:

* `ms` – milliseconds
* `s` – seconds – 1s equals 1000ms
* `m` – minutes – 1m equals 60s (ignoring leap seconds)
* `h` – hours – 1h equals 60m
* `d` – days – 1d equals 24h (ignoring so-called daylight saving time)
* `w` – weeks – 1w equals 7d
* `y` – years – 1y equals 365d (ignoring leap days)

Suffixing a decimal integer number with one of the units above is a different
representation of the equivalent number of seconds as a bare float literal.

Examples:

```
1s # Equivalent to 1.
2m # Equivalent to 120.
1ms # Equivalent to 0.001.
-2h # Equivalent to -7200.
```

The following examples do *not* work:

```
0xABm # No suffixing of hexadecimal numbers.
1.5h # Time units cannot be combined with a floating point.
+Infd # No suffixing of ±Inf or NaN.
```

Multiple units can be combined by concatenation of suffixed integers. Units
must be ordered from the longest to the shortest. A given unit must only appear
once per float literal.

Examples:

```
1h30m # Equivalent to 5400s and thus 5400.
12h34m56s # Equivalent to 45296s and thus 45296.
54s321ms # Equivalent to 54.321.
```

## Time series selectors

These are the basic building-blocks that instruct PromQL what data to fetch.

### Instant vector selectors

Instant vector selectors allow the selection of a set of time series and a
single sample value for each at a given timestamp (point in time). In the simplest
form, only a metric name is specified, which results in an instant vector
containing elements for all time series that have this metric name.

The value returned will be that of the most recent sample at or before the
query's evaluation timestamp (in the case of an
[instant query](/docs/prometheus/latest/querying/api/#instant-queries))
or the current step within the query (in the case of a
[range query](/docs/prometheus/latest/querying/api/#range-queries)).
The [`@` modifier](#modifier) allows overriding the timestamp relative to which
the selection takes place. Time series are only returned if their most recent sample is less than the [lookback period](#staleness) ago.

This example selects all time series that have the `http_requests_total` metric
name, returning the most recent sample for each:

```
http_requests_total
```

It is possible to filter these time series further by appending a comma-separated list of label
matchers in curly braces (`{}`).

This example selects only those time series with the `http_requests_total`
metric name that also have the `job` label set to `prometheus` and their
`group` label set to `canary`:

```
http_requests_total{job="prometheus",group="canary"}
```

It is also possible to negatively match a label value, or to match label values
against regular expressions. The following label matching operators exist:

* `=`: Select labels that are exactly equal to the provided string.
* `!=`: Select labels that are not equal to the provided string.
* `=~`: Select labels that regex-match the provided string.
* `!~`: Select labels that do not regex-match the provided string.

[Regex](#regular-expressions) matches are fully anchored. A match of `env=~"foo"` is treated as `env=~"^foo$"`.

For example, this selects all `http_requests_total` time series for `staging`,
`testing`, and `development` environments and HTTP methods other than `GET`.

```
http_requests_total{environment=~"staging|testing|development",method!="GET"}
```

Label matchers that match empty label values also select all time series that
do not have the specific label set at all. It is possible to have multiple matchers for the same label name.

For example, given the dataset:

```
http_requests_total
http_requests_total{replica="rep-a"}
http_requests_total{replica="rep-b"}
http_requests_total{environment="development"}
```

The query `http_requests_total{environment=""}` would match and return:

```
http_requests_total
http_requests_total{replica="rep-a"}
http_requests_total{replica="rep-b"}
```

and would exclude:

```
http_requests_total{environment="development"}
```

Multiple matchers can be used for the same label name; they all must pass for a result to be returned.

The query:

```
http_requests_total{replica!="rep-a",replica=~"rep.*"}
```

Would then match:

```
http_requests_total{replica="rep-b"}
```

Vector selectors must either specify a name or at least one label matcher
that does not match the empty string. The following expression is illegal:

```
{job=~".*"} # Bad!
```

In contrast, these expressions are valid as they both have a selector that does not
match empty label values.

```
{job=~".+"}              # Good!
{job=~".*",method="get"} # Good!
```

Label matchers can also be applied to metric names by matching against the internal
`__name__` label. For example, the expression `http_requests_total` is equivalent to
`{The following expression selects all metrics that have a name starting with `job:`:

```
{```

The metric name must not be one of the keywords `bool`, `on`, `ignoring`, `group_left` and `group_right`. The following expression is illegal:

```
on{} # Bad!
```

A workaround for this restriction is to use the `__name__` label:

```
{```

### Range Vector Selectors

Range vector literals work like instant vector literals, except that they
select a range of samples back from the current instant. Syntactically, a
[float literal](#float-literals-and-time-durations) is appended in square
brackets (`[]`) at the end of a vector selector to specify for how many seconds
back in time values should be fetched for each resulting range vector element.
Commonly, the float literal uses the syntax with one or more time units, e.g.
`[5m]`. The range is a left-open and right-closed interval, i.e. samples with
timestamps coinciding with the left boundary of the range are excluded from the
selection, while samples coinciding with the right boundary of the range are
included in the selection.

In this example, we select all the values recorded less than 5m ago for all
time series that have the metric name `http_requests_total` and a `job` label
set to `prometheus`:

```
http_requests_total{job="prometheus"}[5m]
```

### Offset modifier

The `offset` modifier allows changing the time offset for individual
instant and range vectors in a query.

For example, the following expression returns the value of
`http_requests_total` 5 minutes in the past relative to the current
query evaluation time:

```
http_requests_total offset 5m
```

Note that the `offset` modifier always needs to follow the selector
immediately, i.e. the following would be correct:

```
sum(http_requests_total{method="GET"} offset 5m) // GOOD.
```

While the following would be *incorrect*:

```
sum(http_requests_total{method="GET"}) offset 5m // INVALID.
```

The same works for range vectors. This returns the 5-minute [rate](/docs/prometheus/latest/querying/functions/#rate)
that `http_requests_total` had a week ago:

```
rate(http_requests_total[5m] offset 1w)
```

When querying for samples in the past, a negative offset will enable temporal comparisons forward in time:

```
rate(http_requests_total[5m] offset -1w)
```

Note that this allows a query to look ahead of its evaluation time.

### @ modifier

The `@` modifier allows changing the evaluation time for individual instant
and range vectors in a query. The time supplied to the `@` modifier
is a Unix timestamp and described with a float literal.

For example, the following expression returns the value of
`http_requests_total` at `2021-01-04T07:40:00+00:00`:

```
http_requests_total @ 1609746000
```

Note that the `@` modifier always needs to follow the selector
immediately, i.e. the following would be correct:

```
sum(http_requests_total{method="GET"} @ 1609746000) // GOOD.
```

While the following would be *incorrect*:

```
sum(http_requests_total{method="GET"}) @ 1609746000 // INVALID.
```

The same works for range vectors. This returns the 5-minute rate that
`http_requests_total` had at `2021-01-04T07:40:00+00:00`:

```
rate(http_requests_total[5m] @ 1609746000)
```

The `@` modifier supports all representations of numeric literals described above.
It works with the `offset` modifier where the offset is applied relative to the `@`
modifier time. The results are the same irrespective of the order of the modifiers.

For example, these two queries will produce the same result:

```
# offset after @
http_requests_total @ 1609746000 offset 5m
# offset before @
http_requests_total offset 5m @ 1609746000
```

Additionally, `start()` and `end()` can also be used as values for the `@` modifier as special values.

For a range query, they resolve to the start and end of the range query respectively and remain the same for all steps.

For an instant query, `start()` and `end()` both resolve to the evaluation time.

```
http_requests_total @ start()
rate(http_requests_total[5m] @ end())
```

Note that the `@` modifier allows a query to look ahead of its evaluation time.

## Subquery

Subquery allows you to run an instant query for a given range and resolution. The result of a subquery is a range vector.

Syntax: `<instant_query> '[' <range> ':' [<resolution>] ']' [ @ <float_literal> ] [ offset <float_literal> ]`

* `<resolution>` is optional. Default is the global evaluation interval.

## Operators

Prometheus supports many binary and aggregation operators. These are described
in detail in the [expression language operators](/docs/prometheus/latest/querying/operators/) page.

## Functions

Prometheus supports several functions to operate on data. These are described
in detail in the [expression language functions](/docs/prometheus/latest/querying/functions/) page.

## Comments

PromQL supports line comments that start with `#`. Example:

```
    # This is a comment
```

## Regular expressions

All regular expressions in Prometheus use [RE2 syntax](https://github.com/google/re2/wiki/Syntax).

Regex matches are always fully anchored.

## Gotchas

### Staleness

The timestamps at which to sample data, during a query, are selected
independently of the actual present time series data. This is mainly to support
cases like aggregation (`sum`, `avg`, and so on), where multiple aggregated
time series do not precisely align in time. Because of their independence,
Prometheus needs to assign a value at those timestamps for each relevant time
series. It does so by taking the newest sample that is less than the lookback period ago.
The lookback period is 5 minutes by default, but can be
[set with the `--query.lookback-delta` flag](/docs/prometheus/latest/command-line/prometheus/)
or overridden on an individual query via the `lookback_delta` parameter.

If a target scrape or rule evaluation no longer returns a sample for a time
series that was previously present, this time series will be marked as stale.
If a target is removed, the previously retrieved time series will be marked as
stale soon after removal.

If a query is evaluated at a sampling timestamp after a time series is marked
as stale, then no value is returned for that time series. If new samples are
subsequently ingested for that time series, they will be returned as expected.

A time series will go stale when it is no longer exported, or the target no
longer exists. Such time series will disappear from graphs
at the times of their latest collected sample, and they will not be returned
in queries after they are marked stale.

Some exporters, which put their own timestamps on samples, get a different behaviour:
series that stop being exported take the last value for (by default) 5 minutes before
disappearing. The `track_timestamps_staleness` setting can change this.

### Avoiding slow queries and overloads

If a query needs to operate on a substantial amount of data, graphing it might
time out or overload the server or browser. Thus, when constructing queries
over unknown data, always start building the query in the tabular view of
Prometheus's expression browser until the result set seems reasonable
(hundreds, not thousands, of time series at most). Only when you have filtered
or aggregated your data sufficiently, switch to graph mode. If the expression
still takes too long to graph ad-hoc, pre-record it via a [recording
rule](/docs/prometheus/latest/configuration/recording_rules/#recording-rules).

This is especially relevant for Prometheus's query language, where a bare
metric name selector like `api_http_requests_total` could expand to thousands
of time series with different labels. Also, keep in mind that expressions that
aggregate over many time series will generate load on the server even if the
output is only a small number of time series. This is similar to how it would
be slow to sum all values of a column in a relational database, even if the
output value is only a single number.

On this page

---

## 2. Overview

## What is Prometheus?

[Prometheus](https://github.com/prometheus) is an open-source systems
monitoring and alerting toolkit originally built at
[SoundCloud](https://soundcloud.com). Since its inception in 2012, many
companies and organizations have adopted Prometheus, and the project has a very
active developer and user [community](/community/). It is now a standalone open source project
and maintained independently of any company. To emphasize this, and to clarify
the project's governance structure, Prometheus joined the
[Cloud Native Computing Foundation](https://cncf.io/) in 2016
as the second hosted project, after [Kubernetes](http://kubernetes.io/).

Prometheus collects and stores its metrics as time series data, i.e. metrics information is stored with the timestamp at which it was recorded, alongside optional key-value pairs called labels.

For more elaborate overviews of Prometheus, see the resources linked from the
[media](/docs/introduction/media/) section.

### Features

Prometheus's main features are:

* a multi-dimensional [data model](/docs/concepts/data_model/) with time series data identified by metric name and key/value pairs
* PromQL, a [flexible query language](/docs/prometheus/latest/querying/basics/)
  to leverage this dimensionality
* no reliance on distributed storage; single server nodes are autonomous
* time series collection happens via a pull model over HTTP
* [pushing time series](/docs/instrumenting/pushing/) is supported via an intermediary gateway
* targets are discovered via service discovery or static configuration
* multiple modes of graphing and dashboarding support

### What are metrics?

Metrics are numerical measurements in layperson terms. The term time series refers to the recording of changes over time. What users want to measure differs from application to application. For a web server, it could be request times; for a database, it could be the number of active connections or active queries, and so on.

Metrics play an important role in understanding why your application is working in a certain way. Let's assume you are running a web application and discover that it is slow. To learn what is happening with your application, you will need some information. For example, when the number of requests is high, the application may become slow. If you have the request count metric, you can determine the cause and increase the number of servers to handle the load.

### Components

The Prometheus ecosystem consists of multiple components, many of which are
optional:

* the main [Prometheus server](https://github.com/prometheus/prometheus) which scrapes and stores time series data
* [client libraries](/docs/instrumenting/clientlibs/) for instrumenting application code
* a [push gateway](https://github.com/prometheus/pushgateway) for supporting short-lived jobs
* special-purpose [exporters](/docs/instrumenting/exporters/) for services like HAProxy, StatsD, Graphite, etc.
* an [alertmanager](https://github.com/prometheus/alertmanager) to handle alerts
* various support tools

Most Prometheus components are written in [Go](https://golang.org/), making
them easy to build and deploy as static binaries.

### Architecture

This diagram illustrates the architecture of Prometheus and some of
its ecosystem components:

Prometheus scrapes metrics from instrumented jobs, either directly or via an
intermediary push gateway for short-lived jobs. It stores all scraped samples
locally and runs rules over this data to either aggregate and record new time
series from existing data or generate alerts. [Grafana](https://grafana.com/) or
other API consumers can be used to visualize the collected data.

## When does it fit?

Prometheus works well for recording any purely numeric time series. It fits
both machine-centric monitoring as well as monitoring of highly dynamic
service-oriented architectures. In a world of microservices, its support for
multi-dimensional data collection and querying is a particular strength.

Prometheus is designed for reliability, to be the system you go to
during an outage to allow you to quickly diagnose problems. Each Prometheus
server is standalone, not depending on network storage or other remote services.
You can rely on it when other parts of your infrastructure are broken, and
you do not need to setup extensive infrastructure to use it.

## When does it not fit?

Prometheus values reliability. You can always view what statistics are
available about your system, even under failure conditions. If you need 100%
accuracy, such as for per-request billing, Prometheus is not a good choice as
the collected data will likely not be detailed and complete enough. In such a
case you would be best off using some other system to collect and analyze the
data for billing, and Prometheus for the rest of your monitoring.

On this page

---

## 3. Metric types

The Prometheus instrumentation libraries offer four core metric types. With the
exception of native histograms, these are currently only differentiated in the
API of instrumentation libraries and in the exposition protocols.
The Prometheus server does not yet make
use of the type information and flattens all types except native histograms
into untyped time series of floating point values. Native histograms, however,
are ingested as time series of special composite histogram samples. In the
future, Prometheus might handle other metric types as [composite
types](/blog/2026/02/14/modernizing-prometheus-composite-samples/), too. There
is also ongoing work to persist the type information of the simple float
samples.

## Counter

A *counter* is a cumulative metric that represents a single [monotonically
increasing counter](https://en.wikipedia.org/wiki/Monotonic_function) whose
value can only increase or be reset to zero on restart. For example, you can
use a counter to represent the number of requests served, tasks completed, or
errors.

Do not use a counter to expose a value that can decrease. For example, do not
use a counter for the number of currently running processes; instead use a gauge.

Instrumentation library usage documentation for counters:

* [Go](http://godoc.org/github.com/prometheus/client_golang/prometheus#Counter)
* [Java](https://prometheus.github.io/client_java/getting-started/metric-types/#counter)
* [Python](https://prometheus.github.io/client_python/instrumenting/counter/)
* [Ruby](https://github.com/prometheus/client_ruby#counter)
* [.Net](https://github.com/prometheus-net/prometheus-net#counters)
* [Rust](https://docs.rs/prometheus-client/latest/prometheus_client/metrics/counter/index.html)

## Gauge

A *gauge* is a metric that represents a single numerical value that can
arbitrarily go up and down.

Gauges are typically used for measured values like temperatures or current
memory usage, but also "counts" that can go up and down, like the number of
concurrent requests.

Instrumentation library usage documentation for gauges:

* [Go](http://godoc.org/github.com/prometheus/client_golang/prometheus#Gauge)
* [Java](https://prometheus.github.io/client_java/getting-started/metric-types/#gauge)
* [Python](https://prometheus.github.io/client_python/instrumenting/gauge/)
* [Ruby](https://github.com/prometheus/client_ruby#gauge)
* [.Net](https://github.com/prometheus-net/prometheus-net#gauges)
* [Rust](https://docs.rs/prometheus-client/latest/prometheus_client/metrics/gauge/index.html)

## Histogram

A *histogram* records observations (usually things like request durations or
response sizes) by counting them in configurable buckets. It also provides a sum
of all observed values. As such, a histogram is essentially a bucketed counter.
However, a histogram can also represent the current state of a distribution, in
which case it is called a *gauge histogram*. In contrast to the usual
counter-like histograms, gauge histograms are rarely directly exposed by
instrumented programs and are thus not (yet) usable in instrumentation
libraries, but they are represented in newer versions of the protobuf
exposition format and in [OpenMetrics](https://openmetrics.io/). They are also
created regularly by PromQL expressions. For example, the outcome of applying
the `rate` function to a counter histogram is a gauge histogram, in the same
way as the outcome of applying the `rate` function to a counter is a gauge.

Histograms exists in two fundamentally different versions: The more recent
*native histograms* and the older *classic histograms*.

A native histogram is exposed and ingested as composite samples, where each
sample represents the count and sum of observations together with a dynamic set
of buckets.

A classic histogram, however, consists of multiple time series of simple float
samples. A classic histogram with a base metric name of `<basename>` results in
the following time series:

* cumulative counters for the observation buckets, exposed as
  `<basename>_bucket{le="<upper inclusive bound>"}`
* the **total sum** of all observed values, exposed as `<basename>_sum`
* the **count** of events that have been observed, exposed as
  `<basename>_count` (identical to `<basename>_bucket{le="+Inf"}` above)

Native histograms are generally much more efficient than classic histograms,
allow much higher resolution, do not require explicit configuration of bucket
boundaries during instrumentation, and provide atomicity when transferred over
the network (e.g. via the Prometheus remote write procol, where classic
histograms suffer from possible partial transfer because their constituent time
series are transferred independently). Their bucketing schema ensures that they
are always aggregatable with each other, even if the resolution might have
changed, while classic histograms with different bucket boundaries are not
generally aggregatable. If the instrumentation library you are using supports
native histograms (currently this is the case for Go and Java), you should
probably [prefer native histograms over classic
histograms](/docs/practices/histograms/).

If you are stuck with classic histograms for whatever reason, there is a way to
get at least some of the benefits of native histograms: You can configure
Prometheus to ingest classic histograms into a special form of native
histograms, called Native Histograms with Custom Bucket boundaries (NHCB).
NHCBs are stored as the same composite samples as usual native histograms,
providing increased efficiency and atomic network transfers, similar to regular
native histgorms. However, the buckets of NHCBs still have the same layout as
in their classic counterparts, statically configured during instrumentation,
with the same limited resolution and range and the same problems of
aggregatability upon changing the bucket boundaries.

Use the [`histogram_quantile()`
function](/docs/prometheus/latest/querying/functions/#histogram_quantile) to
calculate quantiles from histograms or even aggregations of histograms. It
works for both classic and native histograms, using a slightly different
syntax. Histograms are also suitable to calculate an [Apdex
score](https://en.wikipedia.org/wiki/Apdex).

You can operate directly on the buckets of a classic histogram, as they are
represented as individual series (called `<basename>_bucket{le="<upper inclusive bound>"}` as described above). Remember, however, that these buckets
are [cumulative](https://en.wikipedia.org/wiki/Histogram#Cumulative_histogram),
i.e. every bucket counts all observations less than or equal to the upper
boundary provided as a label. With native histograms, you can look at
observations within given boundaries with the [`histogram_fraction()`
function](/docs/prometheus/latest/querying/functions/#histogram_fraction) (to
calculate fractions of observations) and the trim operators (to filter for
the desired band of observations).

See [histograms and summaries](/docs/practices/histograms/) for details of
histogram usage and differences to [summaries](#summary).

> **NOTE**: Beginning with Prometheus v3.0, the values of the `le` label of classic
> histograms are normalized during ingestion to follow the format of
> [OpenMetrics Canonical Numbers](https://github.com/prometheus/OpenMetrics/blob/main/specification/OpenMetrics.md#considerations-canonical-numbers).

Instrumentation library usage documentation for histograms:

* [Go](http://godoc.org/github.com/prometheus/client_golang/prometheus#Histogram)
* [Java](https://prometheus.github.io/client_java/getting-started/metric-types/#histogram)
* [Python](https://prometheus.github.io/client_python/instrumenting/histogram/)
* [Ruby](https://github.com/prometheus/client_ruby#histogram)
* [.Net](https://github.com/prometheus-net/prometheus-net#histogram)
* [Rust](https://docs.rs/prometheus-client/latest/prometheus_client/metrics/histogram/index.html)

## Summary

Similar to a *histogram*, a *summary* samples observations (usually things like
request durations and response sizes). While it also provides a total count of
observations and a sum of all observed values, it calculates configurable
quantiles over a sliding time window.

A summary with a base metric name of `<basename>` exposes multiple time series
during a scrape:

* streaming **φ-quantiles** (0 ≤ φ ≤ 1) of observed events, exposed as `<basename>{quantile="<φ>"}`
* the **total sum** of all observed values, exposed as `<basename>_sum`
* the **count** of events that have been observed, exposed as `<basename>_count`

See [histograms and summaries](/docs/practices/histograms/) for
detailed explanations of φ-quantiles, summary usage, and differences
to [histograms](#histogram).

> **NOTE**: Beginning with Prometheus v3.0, the values of the `quantile` label are normalized during
> ingestion to follow the format of [OpenMetrics Canonical Numbers](https://github.com/prometheus/OpenMetrics/blob/main/specification/OpenMetrics.md#considerations-canonical-numbers).

Instrumentation library usage documentation for summaries:

* [Go](http://godoc.org/github.com/prometheus/client_golang/prometheus#Summary)
* [Java](https://prometheus.github.io/client_java/getting-started/metric-types/#summary)
* [Python](https://prometheus.github.io/client_python/instrumenting/summary/)
* [Ruby](https://github.com/prometheus/client_ruby#summary)
* [.Net](https://github.com/prometheus-net/prometheus-net#summary)

On this page

---

## 4. Operators

PromQL supports unary, binary, and aggregation operators.

## Unary operator

The only unary operator in PromQL is `-` (unary minus). It can be applied to a
scalar or an instant vector. In the former case, it returns a scalar with
inverted sign. In the latter case, it returns an instant vector with inverted
sign for each element. The sign of a histogram sample is inverted by inverting
the sign of all bucket populations and the count and the sum of observations.
The resulting histogram sample is always considered a gauge histogram.

> **NOTE**: A histogram with any negative bucket population or a negative count of
> observations should only be used as an intermediate result. If such a negative
> histogram is the final outcome of a recording rule, the rule evaluation will
> fail. Negative histograms cannot be represented by any of the exchange formats
> (exposition, remote-write, OTLP), so they cannot ingested into Prometheus in
> any way and are only created by PromQL expressions.

## Binary operators

Binary operators cover basic logical and arithmetic operations. For operations
between two instant vectors, the [matching behavior](#vector-matching) can be
modified.

### Arithmetic binary operators

The following binary arithmetic operators exist in PromQL:

* `+` (addition)
* `-` (subtraction)
* `*` (multiplication)
* `/` (division)
* `%` (modulo)
* `^` (power/exponentiation)

Binary arithmetic operators are defined between scalar/scalar, vector/scalar,
and vector/vector value pairs. They follow the usual [IEEE 754 floating point
arithmetic](https://en.wikipedia.org/wiki/IEEE_754), including the handling of
special values like `NaN`, `+Inf`, and `-Inf`.

**Between two scalars**, the behavior is straightforward: they evaluate to another
scalar that is the result of the operator applied to both scalar operands.

**Between an instant vector and a scalar**, the operator is applied to the
value of every data sample in the vector.

If the data sample is a float, the operation is performed between that float and the scalar.
For example, if an instant vector of float samples is multiplied by 2,
the result is another vector of float samples in which every sample value of
the original vector is multiplied by 2.

For vector elements that are histogram samples, the behavior is the
following:

* For `*`, all bucket populations and the count and the sum of observations are
  multiplied by the scalar. If the scalar is negative, the resulting histogram
  is considered a gauge histogram. Otherwise, the counter vs. gauge flavor of
  the input histogram sample is retained.
* For `/`, the histogram sample has to be on the left hand side (LHS), followed
  by the scalar on the right hand side (RHS). All bucket populations and the
  count and the sum of observations are then divided by the scalar. A division
  by zero results in a histogram with no regular buckets and the zero bucket
  population and the count and sum of observations all set to `+Inf`, `-Inf`,
  or `NaN`, depending on their values in the input histogram (positive,
  negative, or zero/`NaN`, respectively). If the scalar is negative, the
  resulting histogram is considered a gauge histogram. Otherwise, the counter
  vs. gauge flavor of the input histogram sample is retained.
* For `/` with a scalar on the LHS and a histogram sample on the RHS, and
  similarly for all other arithmetic binary operators in any combination of a
  scalar and a histogram sample, there is no result and the corresponding
  element is removed from the resulting vector. Such a removal is flagged by an
  info-level annotation.

**Between two instant vectors**, a binary arithmetic operator is applied to
each entry in the LHS vector and its [matching element](#vector-matching) in
the RHS vector. The result is propagated into the result vector with the
grouping labels becoming the output label set. By default, series for which
no matching entry in the opposite vector can be found are not part of the
result. This behavior can be adjusted using [fill modifiers](#filling-in-missing-matches).

If two float samples are matched, the arithmetic operator is applied to the two
input values.

If a float sample is matched with a histogram sample, the behavior follows the
same logic as between a scalar and a histogram sample (see above), i.e. `*` and
`/` (the latter with the histogram sample on the LHS) are valid operations,
while all others lead to the removal of the corresponding element from the
resulting vector.

If two histogram samples are matched, only `+` and `-` are valid operations,
each adding or subtracting all matching bucket populations and the count and
the sum of observations. All other operations result in the removal of the
corresponding element from the output vector, flagged by an info-level
annotation. The `+` and `-` operations should generally only be applied to gauge
histograms, but PromQL allows them for counter histograms, too, to cover
specific use cases, for which special attention is required to avoid problems
with unaligned counter resets. (Certain incompatibilities of counter resets can
be detected by PromQL and are flagged with a warn-level annotations.) Adding
two counter histograms results in a counter histogram. All other combination of
operands and all subtractions result in a gauge histogram.

**In any arithmetic binary operation involving vectors**, the metric name is
dropped. This occurs even if `__name__` is explicitly mentioned in `on`
(see <https://github.com/prometheus/prometheus/issues/16631> for further discussion).

**For any arithmetic binary operation that may result in a negative
histogram**, take into account the [respective note above](#unary-operator).

### Trigonometric binary operators

The following trigonometric binary operators, which work in radians, exist in Prometheus:

* `atan2` (based on <https://pkg.go.dev/math#Atan2>)

Trigonometric operators allow trigonometric functions to be executed on two
vectors using vector matching, which isn't available with normal functions.
They act in the same manner as arithmetic operators. They only operate on float
samples. Operations involving histogram samples result in the removal of the
corresponding vector elements from the output vector, flagged by an
info-level annotation.

### Histogram trim operators

The following binary histogram trim operators exist in Prometheus:

* `</` (trim upper): removes all observations above a threshold value
* `>/` (trim lower): removes all observations below a threshold value

Histogram trim operators are defined between vector/scalar and vector/vector value pairs,
where the left hand side is a native histogram (either exponential or NHCB),
and the right hand side is a float threshold value.

In case the threshold value is not aligned to one of the bucket boundaries of the histogram,
either linear (for NHCB and zero buckets of exponential histogram) or exponential (for non zero
bucket of exponential histogram) interpolation is applied to compute the estimated count
of observations that remain in the bucket containing the threshold.

In case when some observations get trimmed, the new sum of observation values is recomputed
(approximately) based on the remaining observations.

### Comparison binary operators

The following binary comparison operators exist in Prometheus:

* `==` (equal)
* `!=` (not-equal)
* `>` (greater-than)
* `<` (less-than)
* `>=` (greater-or-equal)
* `<=` (less-or-equal)

Comparison operators are defined between scalar/scalar, vector/scalar,
and vector/vector value pairs. By default they filter. Their behavior can be
modified by providing `bool` after the operator, which will return `0` or `1`
for the value rather than filtering.

**Between two scalars**, the `bool` modifier must be provided and these
operators result in another scalar that is either `0` (`false`) or `1`
(`true`), depending on the comparison result.

**Between an instant vector and a scalar**, these operators are applied to the
value of every data sample in the vector, and vector elements between which the
comparison result is false get dropped from the result vector. These
operations only work with float samples in the vector. For histogram samples,
the corresponding element is removed from the result vector, flagged by an
info-level annotation.

**Between two instant vectors**, these operators behave as a filter by default,
applied to matching entries. Vector elements for which the expression is not
true or which do not find a match on the other side of the expression get
dropped from the result, while the others are propagated into a result vector
with the grouping labels becoming the output label set.

Matches between two float samples work as usual.

Matches between a float sample and a histogram sample are invalid, and the
corresponding element is removed from the result vector, flagged by an info-level
annotation.

Between two histogram samples, `==` and `!=` work as expected, but all other
comparison binary operations are again invalid.

**In any comparison binary operation involving vectors**, providing the `bool`
modifier changes the behavior in the following ways:

* Vector elements which find a match on the other side of the expression but for
  which the expression is false instead have the value `0`, and vector elements
  that do find a match and for which the expression is true have the value `1`.
  (Note that elements with no match or invalid operations involving histogram
  samples still return no result rather than the value `0`.)
* The metric name is dropped.

If the `bool` modifier is not provided, then the metric name from the left side
is retained, with some exceptions:

* If `on` is used, then the metric name is dropped.
* If `group_right` is used, then the metric name from the right side is retained,
  to avoid collisions.

### Logical/set binary operators

These logical/set binary operators are only defined between instant vectors:

* `and` (intersection)
* `or` (union)
* `unless` (complement)

`vector1 and vector2` results in a vector consisting of the elements of
`vector1` for which there are elements in `vector2` with exactly matching
label sets. Other elements are dropped. The metric name and values are carried
over from the left-hand side vector.

`vector1 or vector2` results in a vector that contains all original elements
(label sets + values) of `vector1` and additionally all elements of `vector2`
which do not have matching label sets in `vector1`.

`vector1 unless vector2` results in a vector consisting of the elements of
`vector1` for which there are no elements in `vector2` with exactly matching
label sets. All matching elements in both vectors are dropped.

As these logical/set binary operators do not interact with the sample values,
they work in the same way for float samples and histogram samples.

## Vector matching

Operations between vectors attempt to find a matching element in the right-hand side
vector for each entry in the left-hand side. There are two basic types of
matching behavior: One-to-one and many-to-one/one-to-many.

### Vector matching keywords

These vector matching keywords allow for matching between series with different label sets:

* `on(<label list>)`: Only match on provided labels.
* `ignoring(<label list>)`: Ignore provided labels when matching.

Label lists provided to matching keywords will determine how vectors are combined. Examples
can be found in [One-to-one vector matches](#one-to-one-vector-matches) and in
[Many-to-one and one-to-many vector matches](#many-to-one-and-one-to-many-vector-matches)

### Group modifiers

These group modifiers enable many-to-one/one-to-many vector matching:

* `group_left`: Allow many-to-one matching, where the left vector has higher cardinality.
* `group_right`: Allow one-to-many matching, where the right vector has higher cardinality.

Label lists can be provided to the group modifier which contain labels from the "one"-side to
be included in the result metrics.

*Many-to-one and one-to-many matching are advanced use cases that should be carefully considered.
Often a proper use of `ignoring(<labels>)` provides the desired outcome.*

*Grouping modifiers can only be used for [comparison](#comparison-binary-operators),
[arithmetic](#arithmetic-binary-operators), and [trigonometric](#trigonometric-binary-operators)
operators. Set operators match with all possible entries on either side by default.*

### One-to-one vector matches

**One-to-one** finds a unique pair of entries from each side of the operation.
In the default case, that is an operation following the format `vector1 <operator> vector2`.
Two entries match if they have the exact same set of labels and corresponding values.
The `ignoring` keyword allows ignoring certain labels when matching, while the
`on` keyword allows reducing the set of considered labels to a provided list:

```
<vector expr> <bin-op> ignoring(<label list>) <vector expr>
<vector expr> <bin-op> on(<label list>) <vector expr>
```

Example input:

```
method_code:http_errors:rate5m{method="get", code="500"}  24
method_code:http_errors:rate5m{method="get", code="404"}  30
method_code:http_errors:rate5m{method="put", code="501"}  3
method_code:http_errors:rate5m{method="post", code="500"} 6
method_code:http_errors:rate5m{method="post", code="404"} 21

method:http_requests:rate5m{method="get"}  600
method:http_requests:rate5m{method="del"}  34
method:http_requests:rate5m{method="post"} 120
```

Example query:

```
method_code:http_errors:rate5m{code="500"} / ignoring(code) method:http_requests:rate5m
```

This returns a result vector containing the fraction of HTTP requests with status code
of 500 for each method, as measured over the last 5 minutes. Without `ignoring(code)` there
would have been no match as the metrics do not share the same set of labels.
The entries with methods `put` and `del` have no match and will not show up in the result:

```
{method="get"}  0.04            //  24 / 600
{method="post"} 0.05            //   6 / 120
```

### Many-to-one and one-to-many vector matches

**Many-to-one** and **one-to-many** matchings refer to the case where each vector element on
the "one"-side can match with multiple elements on the "many"-side. This has to
be explicitly requested using the `group_left` or `group_right` [modifiers](#group-modifiers), where
left/right determines which vector has the higher cardinality.

```
<vector expr> <bin-op> ignoring(<label list>) group_left(<label list>) <vector expr>
<vector expr> <bin-op> ignoring(<label list>) group_right(<label list>) <vector expr>
<vector expr> <bin-op> on(<label list>) group_left(<label list>) <vector expr>
<vector expr> <bin-op> on(<label list>) group_right(<label list>) <vector expr>
```

The label list provided with the [group modifier](#group-modifiers) contains additional labels from
the "one"-side to be included in the result metrics. For `on` a label can only
appear in one of the lists. Every time series of the result vector must be
uniquely identifiable.

Example query:

```
method_code:http_errors:rate5m / ignoring(code) group_left method:http_requests:rate5m
```

In this case the left vector contains more than one entry per `method` label
value. Thus, we indicate this using `group_left`. The elements from the right
side are now matched with multiple elements with the same `method` label on the
left:

```
{method="get", code="500"}  0.04            //  24 / 600
{method="get", code="404"}  0.05            //  30 / 600
{method="post", code="500"} 0.05            //   6 / 120
{method="post", code="404"} 0.175           //  21 / 120
```

### Filling in missing matches

Fill modifiers are **experimental** and must be enabled with `--enable-feature=promql-binop-fill-modifiers`.

By default, vector elements that do not find a match on the other side of a binary operation
are not included in the result vector. Fill modifiers allow overriding this behavior by filling
in missing series on either side of a binary operation with a provided default sample value:

* `fill(<value>)`: Fill in missing matches on either side with `value`.
* `fill_left(<value>)`: Fill in missing matches on the left side with `value`.
* `fill_right(<value>)`: Fill in missing matches on the right side with `value`.

`value` has to be a numeric literal representing a float sample. Histogram samples are not supported.

Note that these modifiers can only fill in series that are missing on one side of the operation.
If a series is missing on both sides, it cannot be created by these modifiers.

The fill modifiers can be used in the following combinations:

* `fill(<default>)`
* `fill_left(<default>)`
* `fill_right(<default>)`
* `fill_left(<default>) fill_right(<default>)`
* `fill_right(<default>) fill_left(<default>)`

If other binary operator modifiers like `bool`, `on`, `ignoring`, `group_left`, or `group_right`
are used, the fill modifiers must be provided last.

When using fill modifiers in combination with `group_left` or `group_right`, they behave as follows:

* If a fill modifier is used on the "many" side of a match, it will only fill in a single series
  for the "many" side of each match group, using the group's matching labels as the series identity.
* If a fill modifier is used on the "one" side of a match and the grouping modifier specifies
  label names to include from the "one" side (e.g. `left_vector * on(instance, job) group_left(info_label) fill_right(1) right_vector`), those labels will not be filled in for missing
  series, as there is no source for their values.

Fill modifiers are not supported for set operators (`and`, `or`, `unless`), as the purpose of those
operators is to filter series based on presence or absence in the other vector.

Example query, filling in missing series on the either side with `0`:

```
method_code:http_errors:rate5m{status="500"} / ignoring(code) fill(0) method:http_requests:rate5m
```

This returns a result vector containing the fraction of HTTP requests with status code
of 500 for each method, as measured over the last 5 minutes. The entries with methods `put` and `del`
are now included in the result with a filled-in default sample value of `0`, as they had no matching
series on the respective other side:

```
{method="get"}  0.04            #  24 / 600
{method="put"}  +Inf            #   3 /   0 (missing right side filled in)
{method="del"}  0               #   0 /  34 (missing left side filled in)
{method="post"} 0.05            #   6 / 120
```

## Aggregation operators

Prometheus supports the following built-in aggregation operators that can be
used to aggregate the elements of a single instant vector, resulting in a new
vector of fewer elements with aggregated values:

* `sum(v)` (calculate sum over dimensions)
* `avg(v)` (calculate the arithmetic average over dimensions)
* `min(v)` (select minimum over dimensions)
* `max(v)` (select maximum over dimensions)
* `bottomk(k, v)` (smallest `k` elements by sample value)
* `topk(k, v)` (largest `k` elements by sample value)
* `limitk(k, v)` (sample `k` elements, **experimental**, must be enabled with `--enable-feature=promql-experimental-functions`)
* `limit_ratio(r, v)` (sample a pseudo-random ratio `r` of elements, **experimental**, must be enabled with `--enable-feature=promql-experimental-functions`)
* `group(v)` (all values in the resulting vector are 1)
* `count(v)` (count number of elements in the vector)
* `count_values(l, v)` (count number of elements with the same value)
* `stddev(v)` (calculate population standard deviation over dimensions)
* `stdvar(v)` (calculate population variance over dimensions)
* `quantile(φ, v)` (calculate φ-quantile (0 ≤ φ ≤ 1) over dimensions)

These operators can either be used to aggregate over **all** label dimensions
or preserve distinct dimensions by including a `without` or `by` clause. These
clauses may be used before or after the expression.

```
<aggr-op> [without|by (<label list>)] ([parameter,] <vector expression>)
```

or

```
<aggr-op>([parameter,] <vector expression>) [without|by (<label list>)]
```

`label list` is a list of unquoted labels that may include a trailing comma, i.e.
both `(label1, label2)` and `(label1, label2,)` are valid syntax.

`without` removes the listed labels from the result vector, while
all other labels are preserved in the output. `by` does the opposite and drops
labels that are not listed in the `by` clause, even if their label values are
identical between all elements of the vector.

### Detailed explanations

#### `sum`

`sum(v)` sums up sample values in `v` in the same way as the `+` binary operator does
between two values.

All sample values being aggregated into a single resulting vector element must either be
float samples or histogram samples. An aggregation of a mix of both is invalid,
resulting in the removal of the corresponding vector element from the output
vector, flagged by a warn-level annotation.

##### Examples

If the metric `memory_consumption_bytes` had time series that fan out by
`application`, `instance`, and `group` labels, we could calculate the total
memory consumption per application and group over all instances via:

```
sum without (instance) (memory_consumption_bytes)
```

Which is equivalent to:

```
sum by (application, group) (memory_consumption_bytes)
```

If we are just interested in the total memory consumption in **all**
applications, we could simply write:

```
sum(memory_consumption_bytes)
```

#### `avg`

`avg(v)` divides the sum of `v` by the number of aggregated samples in the same way
as the `/` binary operator.

All sample values being aggregated into a single resulting vector element must either be
float samples or histogram samples. An aggregation of a mix of both is invalid,
resulting in the removal of the corresponding vector element from the output
vector, flagged by a warn-level annotation.

#### `min` and `max`

`min(v)` and `max(v)` return the minimum or maximum value, respectively, in `v`.

They only operate on float samples, following IEEE 754 floating
point arithmetic, which in particular implies that `NaN` is only ever
considered a minimum or maximum if all aggregated values are `NaN`. Histogram
samples in the input vector are ignored, flagged by an info-level annotation.

#### `topk` and `bottomk`

`topk(k, v)` and `bottomk(k, v)` are different from other aggregators in that a subset of
`k` values from the input samples, including the original labels, are returned in the result vector.

`by` and `without` are only used to bucket the input vector.

Similar to `min` and `max`, they only operate on float samples, considering `NaN` values
to be farthest from the top or bottom, respectively. Histogram samples in the
input vector are ignored, flagged by an info-level annotation.

If used in an instant query, `topk` and `bottomk` return series ordered by
value in descending or ascending order, respectively. If used with `by` or
`without`, then series within each bucket are sorted by value, and series in
the same bucket are returned consecutively, but there is no guarantee that
buckets of series will be returned in any particular order.

No sorting applies to range queries.

##### Example

To get the 5 instances with the highest memory consumption across all instances we could write:

```
topk(5, memory_consumption_bytes)
```

#### `limitk`

`limitk(k, v)` returns a subset of `k` input samples, including
the original labels in the result vector.

The subset is selected in a deterministic pseudo-random way.
This happens independent of the sample type.
Therefore, it works for both float samples and histogram samples.

##### Example

To sample 10 timeseries we could write:

```
limitk(10, memory_consumption_bytes)
```

#### `limit_ratio`

`limit_ratio(r, v)` returns a subset of the input samples, including
the original labels in the result vector.

The subset is selected in a deterministic pseudo-random way.
This happens independent of the sample type.
Therefore, it works for both float samples and histogram samples.

`r` can be between +1 and -1. The absolute value of `r` is used as the selection ratio,
but the selection order is inverted for a negative `r`, which can be used to select complements.
For example, `limit_ratio(0.1, ...)` returns a deterministic set of approximatiely 10% of
the input samples, while `limit_ratio(-0.9, ...)` returns precisely the
remaining approximately 90% of the input samples not returned by `limit_ratio(0.1, ...)`.

#### `group`

`group(v)` returns 1 for each group that contains any value at that timestamp.

The value may be a float or histogram sample.

#### `count`

`count(v)` returns the number of values at that timestamp, or no value at all
if no values are present at that timestamp.

The value may be a float or histogram sample.

#### `count_values`

`count_values(l, v)` outputs one time series per unique sample value in `v`.
Each series has an additional label, given by `l`, and the label value is the
unique sample value. The value of each time series is the number of times that sample value was present.

`count_values` works with both float samples and histogram samples. For the
latter, a compact string representation of the histogram sample value is used
as the label value.

##### Example

To count the number of binaries running each build version we could write:

```
count_values("version", build_version)
```

#### `stddev`

`stddev(v)` returns the standard deviation of `v`.

`stddev` only works with float samples, following IEEE 754 floating
point arithmetic. Histogram samples in the input vector are ignored, flagged by
an info-level annotation.

#### `stdvar`

`stdvar(v)` returns the variance of `v`.

`stdvar` only works with float samples, following IEEE 754 floating
point arithmetic. Histogram samples in the input vector are ignored, flagged by
an info-level annotation.

#### `quantile`

`quantile(φ, v)` calculates the φ-quantile, the value that ranks at number φ\*N among
the N metric values of the dimensions aggregated over.

`quantile` only works with float samples. Histogram samples in the input vector
are ignored, flagged by an info-level annotation.

`NaN` is considered the smallest possible value.

For example, `quantile(0.5, ...)` calculates the median, `quantile(0.95, ...)` the 95th percentile.

Special cases:

* For φ = `NaN`, `NaN` is returned.
* For φ < 0, `-Inf` is returned.
* For φ > 1, `+Inf` is returned.

## Binary operator precedence

The following list shows the precedence of binary operators in Prometheus, from
highest to lowest.

1. `^`
2. `*`, `/`, `%`, `atan2`
3. `+`, `-`
4. `==`, `!=`, `<=`, `<`, `>=`, `>`
5. `and`, `unless`
6. `or`

Operators on the same precedence level are left-associative. For example,
`2 * 3 % 2` is equivalent to `(2 * 3) % 2`. However `^` is right associative,
so `2 ^ 3 ^ 2` is equivalent to `2 ^ (3 ^ 2)`.

On this page

---

## 5. Query functions

Some functions have default arguments, e.g. `year(v=vector(time()) instant-vector)`. This means that there is one argument `v` which is an instant
vector, which if not provided it will default to the value of the expression
`vector(time())`.

## `abs()`

`abs(v instant-vector)` returns a vector containing all float samples in the
input vector converted to their absolute value. Histogram samples in the input
vector are ignored silently.

## `absent()`

`absent(v instant-vector)` returns an empty vector if the vector passed to it
has any elements (float samples or histogram samples) and a 1-element vector
with the value 1 if the vector passed to it has no elements.

This is useful for alerting on when no time series exist for a given metric name
and label combination.

```
absent(nonexistent{job="myjob"})
# => {job="myjob"}

absent(nonexistent{job="myjob",instance=~".*"})
# => {job="myjob"}

absent(sum(nonexistent{job="myjob"}))
# => {}
```

In the first two examples, `absent()` tries to be smart about deriving labels
of the 1-element output vector from the input vector.

## `absent_over_time()`

`absent_over_time(v range-vector)` returns an empty vector if the range vector
passed to it has any elements (float samples or histogram samples) and a
1-element vector with the value 1 if the range vector passed to it has no
elements.

This is useful for alerting on when no time series exist for a given metric name
and label combination for a certain amount of time.

```
absent_over_time(nonexistent{job="myjob"}[1h])
# => {job="myjob"}

absent_over_time(nonexistent{job="myjob",instance=~".*"}[1h])
# => {job="myjob"}

absent_over_time(sum(nonexistent{job="myjob"})[1h:])
# => {}
```

In the first two examples, `absent_over_time()` tries to be smart about deriving
labels of the 1-element output vector from the input vector.

## `ceil()`

`ceil(v instant-vector)` returns a vector containing all float samples in the
input vector rounded up to the nearest integer value greater than or equal to
their original value. Histogram samples in the input vector are ignored silently.

* `ceil(+Inf) = +Inf`
* `ceil(±0) = ±0`
* `ceil(1.49) = 2.0`
* `ceil(1.78) = 2.0`

## `changes()`

For each input time series, `changes(v range-vector)` returns the number of
times its value has changed within the provided time range as an instant
vector. A float sample followed by a histogram sample, or vice versa, counts as
a change. A counter histogram sample followed by a gauge histogram sample with
otherwise exactly the same values, or vice versa, does not count as a change.

## `clamp()`

`clamp(v instant-vector, min scalar, max scalar)` clamps the values of all
float samples in `v` to have a lower limit of `min` and an upper limit of
`max`. Histogram samples in the input vector are ignored silently.

Special cases:

* Return an empty vector if `min > max`
* Float samples are clamped to `NaN` if `min` or `max` is `NaN`

## `clamp_max()`

`clamp_max(v instant-vector, max scalar)` clamps the values of all float
samples in `v` to have an upper limit of `max`. Histogram samples in the input
vector are ignored silently.

## `clamp_min()`

`clamp_min(v instant-vector, min scalar)` clamps the values of all float
samples in `v` to have a lower limit of `min`. Histogram samples in the input
vector are ignored silently.

## `day_of_month()`

`day_of_month(v=vector(time()) instant-vector)` interprets float samples in
`v` as timestamps (number of seconds since January 1, 1970 UTC) and returns the
day of the month (in UTC) for each of those timestamps. Returned values are
from 1 to 31. Histogram samples in the input vector are ignored silently.

## `day_of_week()`

`day_of_week(v=vector(time()) instant-vector)` interprets float samples in `v`
as timestamps (number of seconds since January 1, 1970 UTC) and returns the day
of the week (in UTC) for each of those timestamps. Returned values are from 0
to 6, where 0 means Sunday etc. Histogram samples in the input vector are
ignored silently.

## `day_of_year()`

`day_of_year(v=vector(time()) instant-vector)` interprets float samples in `v`
as timestamps (number of seconds since January 1, 1970 UTC) and returns the day
of the year (in UTC) for each of those timestamps. Returned values are from 1
to 365 for non-leap years, and 1 to 366 in leap years. Histogram samples in the
input vector are ignored silently.

## `days_in_month()`

`days_in_month(v=vector(time()) instant-vector)` interprets float samples in
`v` as timestamps (number of seconds since January 1, 1970 UTC) and returns the
number of days in the month of each of those timestamps (in UTC). Returned
values are from 28 to 31. Histogram samples in the input vector are ignored silently.

## `delta()`

`delta(v range-vector)` calculates the difference between the
first and last value of each time series element in a range vector `v`,
returning an instant vector with the given deltas and equivalent labels.
The delta is extrapolated to cover the full time range as specified in
the range vector selector, so that it is possible to get a non-integer
result even if the sample values are all integers.

The following example expression returns the difference in CPU temperature
between now and 2 hours ago:

```
delta(cpu_temp_celsius{host="zeus"}[2h])
```

`delta` acts on histogram samples by calculating a new histogram where each
component (sum and count of observations, buckets) is the difference between
the respective component in the first and last native histogram in `v`.
However, each element in `v` that contains a mix of float samples and histogram
samples within the range will be omitted from the result vector, flagged by a
warn-level annotation.

`delta` should only be used with gauges (for both floats and histograms).

## `deriv()`

`deriv(v range-vector)` calculates the per-second derivative of each float time
series in the range vector `v`, using [simple linear
regression](https://en.wikipedia.org/wiki/Simple_linear_regression). The range
vector must have at least two float samples in order to perform the
calculation. When `+Inf` or `-Inf` are found in the range vector, the slope and
offset value calculated will be `NaN`.

`deriv` should only be used with gauges and only works for float samples.
Elements in the range vector that contain only histogram samples are ignored
entirely. For elements that contain a mix of float and histogram samples, only
the float samples are used as input, which is flagged by an info-level
annotation.

## `double_exponential_smoothing()`

**This function has to be enabled via the [feature
flag](/docs/prometheus/latest/feature_flags/#experimental-promql-functions)
`--enable-feature=promql-experimental-functions`.**

`double_exponential_smoothing(v range-vector, sf scalar, tf scalar)` produces a
smoothed value for each float time series in the range in `v`. The lower the
smoothing factor `sf`, the more importance is given to old data. The higher the
trend factor `tf`, the more trends in the data is considered. Both `sf` and
`tf` must be between 0 and 1. For additional details, refer to [NIST
Engineering Statistics
Handbook](https://www.itl.nist.gov/div898/handbook/pmc/section4/pmc433.htm). In
Prometheus V2 this function was called `holt_winters`. This caused confusion
since the Holt-Winters method usually refers to triple exponential smoothing.
Double exponential smoothing as implemented here is also referred to as "Holt
Linear".

`double_exponential_smoothing` should only be used with gauges and only works
for float samples. Elements in the range vector that contain only histogram
samples are ignored entirely. For elements that contain a mix of float and
histogram samples, only the float samples are used as input, which is flagged
by an info-level annotation.

## `exp()`

`exp(v instant-vector)` calculates the exponential function for all float
samples in `v`. Histogram samples are ignored silently. Special cases are:

* `Exp(+Inf) = +Inf`
* `Exp(NaN) = NaN`

## `floor()`

`floor(v instant-vector)` returns a vector containing all float samples in the
input vector rounded down to the nearest integer value smaller than or equal
to their original value. Histogram samples in the input vector are ignored silently.

* `floor(+Inf) = +Inf`
* `floor(±0) = ±0`
* `floor(1.49) = 1.0`
* `floor(1.78) = 1.0`

## `histogram_avg()`

`histogram_avg(v instant-vector)` returns the arithmetic average of observed
values stored in each native histogram sample in `v`. Float samples are ignored and do
not show up in the returned vector.

Use `histogram_avg` as demonstrated below to compute the average request duration
over a 5-minute window from a native histogram:

```
histogram_avg(rate(http_request_duration_seconds[5m]))
```

Which is equivalent to the following query:

```
  histogram_sum(rate(http_request_duration_seconds[5m]))
/
  histogram_count(rate(http_request_duration_seconds[5m]))
```

## `histogram_count()` and `histogram_sum()`

`histogram_count(v instant-vector)` returns the count of observations stored in
each native histogram sample in `v`. Float samples are ignored and do not show up in
the returned vector.

Similarly, `histogram_sum(v instant-vector)` returns the sum of observations
stored in each native histogram sample.

Use `histogram_count` in the following way to calculate a rate of observations
(in this case corresponding to “requests per second”) from a series of
histogram samples:

```
histogram_count(rate(http_request_duration_seconds[10m]))
```

## `histogram_fraction()`

`histogram_fraction(lower scalar, upper scalar, b instant-vector)` returns the
estimated fraction of observations between the provided lower and upper values
for each classic or native histogram contained in `b`. Float samples in `b` are
considered the counts of observations in each bucket of one or more classic
histograms, while native histogram samples in `b` are treated each individually
as a separate histogram. This works in the same way as for `histogram_quantile()`.
(See there for more details.)

If the provided lower and upper values do not coincide with bucket boundaries,
the calculated fraction is an estimate, using the same interpolation method as for
`histogram_quantile()`. (See there for more details.) Especially with classic
histograms, it is easy to accidentally pick lower or upper values that are very
far away from any bucket boundary, leading to large margins of error. Rather than
using `histogram_fraction()` with classic histograms, it is often a more robust approach
to directly act on the bucket series when calculating fractions. See the
[calculation of the Apdex score](/docs/practices/histograms/#apdex-score)
as a typical example.

For example, the following expression calculates the fraction of HTTP requests
over the last hour that took 200ms or less:

```
histogram_fraction(0, 0.2, rate(http_request_duration_seconds[1h]))
```

The error of the estimation depends on the resolution of the underlying native
histogram and how closely the provided boundaries are aligned with the bucket
boundaries in the histogram.

`+Inf` and `-Inf` are valid boundary values. For example, if the histogram in
the expression above included negative observations (which shouldn't be the
case for request durations), the appropriate lower boundary to include all
observations less than or equal 0.2 would be `-Inf` rather than `0`.

Whether the provided boundaries are inclusive or exclusive is only relevant if
the provided boundaries are precisely aligned with bucket boundaries in the
underlying native histogram. In this case, the behavior depends on the schema
definition of the histogram. (The usual standard exponential schemas all
feature inclusive upper boundaries and exclusive lower boundaries for positive
values, and vice versa for negative values.) Without a precise alignment of
boundaries, the function uses interpolation to estimate the fraction. With the
resulting uncertainty, it becomes irrelevant if the boundaries are inclusive or
exclusive.

Special case for native histograms with standard exponential buckets:
`NaN` observations are considered outside of any buckets in this case.
`histogram_fraction(-Inf, +Inf, b)` effectively returns the fraction of
non-`NaN` observations and may therefore be less than 1.

## `histogram_quantile()`

`histogram_quantile(φ scalar, b instant-vector)` calculates the φ-quantile (0 ≤
φ ≤ 1) from a [classic
histogram](/docs/concepts/metric_types/#histogram) or from
a native histogram. (See [histograms and
summaries](/docs/practices/histograms/) for a detailed
explanation of φ-quantiles and the usage of the (classic) histogram metric
type in general.)

The float samples in `b` are considered the counts of observations in each
bucket of one or more classic histograms. Each float sample must have a label
`le` where the label value denotes the inclusive upper bound of the bucket.
(Float samples without such a label are silently ignored.) The other labels and
the metric name are used to identify the buckets belonging to each classic
histogram. The [histogram metric
type](/docs/concepts/metric_types/#histogram)
automatically provides time series with the `_bucket` suffix and the
appropriate labels.

The (native) histogram samples in `b` are treated each individually as a
separate histogram to calculate the quantile from.

As long as no naming collisions arise, `b` may contain a mix of classic
and native histograms.

Use the `rate()` function to specify the time window for the quantile
calculation.

Example: A histogram metric is called `http_request_duration_seconds` (and
therefore the metric name for the buckets of a classic histogram is
`http_request_duration_seconds_bucket`). To calculate the 90th percentile of request
durations over the last 10m, use the following expression in case
`http_request_duration_seconds` is a classic histogram:

```
histogram_quantile(0.9, rate(http_request_duration_seconds_bucket[10m]))
```

For a native histogram, use the following expression instead:

```
histogram_quantile(0.9, rate(http_request_duration_seconds[10m]))
```

The quantile is calculated for each label combination in
`http_request_duration_seconds`. To aggregate, use the `sum()` aggregator
around the `rate()` function. Since the `le` label is required by
`histogram_quantile()` to deal with classic histograms, it has to be
included in the `by` clause. The following expression aggregates the 90th
percentile by `job` for classic histograms:

```
histogram_quantile(0.9, sum by (job, le) (rate(http_request_duration_seconds_bucket[10m])))
```

When aggregating native histograms, the expression simplifies to:

```
histogram_quantile(0.9, sum by (job) (rate(http_request_duration_seconds[10m])))
```

To aggregate all classic histograms, specify only the `le` label:

```
histogram_quantile(0.9, sum by (le) (rate(http_request_duration_seconds_bucket[10m])))
```

With native histograms, aggregating everything works as usual without any `by` clause:

```
histogram_quantile(0.9, sum(rate(http_request_duration_seconds[10m])))
```

In the (common) case that a quantile value does not coincide with a bucket
boundary, the `histogram_quantile()` function interpolates the quantile value
within the bucket the quantile value falls into. For classic histograms, for
native histograms with custom bucket boundaries, and for the zero bucket of
other native histograms, it assumes a uniform distribution of observations
within the bucket (also called *linear interpolation*). For the
non-zero-buckets of native histograms with a standard exponential bucketing
schema, the interpolation is done under the assumption that the samples within
the bucket are distributed in a way that they would uniformly populate the
buckets in a hypothetical histogram with higher resolution. (This is also
called *exponential interpolation*. See the [native histogram
specification](/docs/specs/native_histograms/#interpolation-within-a-bucket)
for more details.)

If `b` has 0 observations, `NaN` is returned. For φ < 0, `-Inf` is
returned. For φ > 1, `+Inf` is returned. For φ = `NaN`, `NaN` is returned.

Special cases for classic histograms:

* If `b` contains fewer than two buckets, `NaN` is returned.
* The highest bucket must have an upper bound of `+Inf`. (Otherwise, `NaN` is
  returned.)
* If a quantile is located in the highest bucket, the upper bound of the second
  highest bucket is returned.
* The lower limit of the lowest bucket is assumed to be 0 if the upper bound of
  that bucket is greater than 0. In that case, the usual linear interpolation
  is applied within that bucket. Otherwise, the upper bound of the lowest
  bucket is returned for quantiles located in the lowest bucket.

Special cases for native histograms:

* If a native histogram with standard exponential buckets has `NaN`
  observations and the quantile falls into one of the existing exponential
  buckets, the result is skewed towards higher values due to `NaN`
  observations treated as `+Inf`. This is flagged with an info level
  annotation.
* If a native histogram with standard exponential buckets has `NaN`
  observations and the quantile falls above all of the existing exponential
  buckets, `NaN` is returned. This is flagged with an info level annotation.
* A zero bucket with finite width is assumed to contain no negative
  observations if the histogram has observations in positive buckets, but none
  in negative buckets.
* A zero bucket with finite width is assumed to contain no positive
  observations if the histogram has observations in negative buckets, but none
  in positive buckets.

You can use `histogram_quantile(0, v instant-vector)` to get the estimated
minimum value stored in a histogram.

You can use `histogram_quantile(1, v instant-vector)` to get the estimated
maximum value stored in a histogram.

Buckets of classic histograms are cumulative. Therefore, the following should
always be the case:

* The counts in the buckets are monotonically increasing (strictly
  non-decreasing).
* A lack of observations between the upper limits of two consecutive buckets
  results in equal counts in those two buckets.

However, floating point precision issues (e.g. small discrepancies introduced
by computing of buckets with `sum(rate(...))`) or invalid data might violate
these assumptions. In that case, `histogram_quantile` would be unable to return
meaningful results. To mitigate the issue, `histogram_quantile` assumes that
tiny relative differences between consecutive buckets are happening because of
floating point precision errors and ignores them. (The threshold to ignore a
difference between two buckets is a trillionth (1e-12) of the sum of both
buckets.) Furthermore, if there are non-monotonic bucket counts even after this
adjustment, they are increased to the value of the previous buckets to enforce
monotonicity. The latter is evidence for an actual issue with the input data
and is therefore flagged by an info-level annotation reading `input to histogram_quantile needed to be fixed for monotonicity`. If you encounter this
annotation, you should find and remove the source of the invalid data.

## `histogram_quantiles()`

**This function has to be enabled via the [feature
flag](/docs/prometheus/latest/feature_flags/#experimental-promql-functions)
`--enable-feature=promql-experimental-functions`.**

`histogram_quantiles(v instant-vector, quantile_label string, φ_1 scalar, φ_2 scalar, ...)` calculates multiple (between 1 and 10) φ-quantiles (0 ≤
φ ≤ 1) from a [classic
histogram](/docs/concepts/metric_types/#histogram) or from
a native histogram. Quantile calculation works the same way as in `histogram_quantile()`.
The second argument (a string) specifies the label name that is used to identify different quantiles in the query result.

```
histogram_quantiles(sum(rate(foo[1m])), "quantile", 0.9, 0.99)
# => {quantile="0.9"} 123
     {quantile="0.99"} 128
```

## `histogram_stddev()` and `histogram_stdvar()`

`histogram_stddev(v instant-vector)` returns the estimated standard deviation
of observations for each native histogram sample in `v`. For this estimation, all observations
in a bucket are assumed to have the value of the mean of the bucket boundaries. For
the zero bucket and for buckets with custom boundaries, the arithmetic mean is used.
For the usual exponential buckets, the geometric mean is used. Float samples are ignored
and do not show up in the returned vector.

Similarly, `histogram_stdvar(v instant-vector)` returns the estimated
variance of observations for each native histogram sample in `v`.

## `hour()`

`hour(v=vector(time()) instant-vector)` interprets float samples in `v` as
timestamps (number of seconds since January 1, 1970 UTC) and returns the hour
of the day (in UTC) for each of those timestamps. Returned values are from 0
to 23. Histogram samples in the input vector are ignored silently.

## `idelta()`

`idelta(v range-vector)` calculates the difference between the last two samples
in the range vector `v`, returning an instant vector with the given deltas and
equivalent labels. Both samples must be either float samples or histogram
samples. Elements in `v` where one of the last two samples is a float sample
and the other is a histogram sample will be omitted from the result vector,
flagged by a warn-level annotation.

`idelta` should only be used with gauges (for both floats and histograms).

## `increase()`

`increase(v range-vector)` calculates the increase in the time series in the
range vector. Breaks in monotonicity (such as counter resets due to target
restarts) are automatically adjusted for. The increase is extrapolated to cover
the full time range as specified in the range vector selector, so that it is
possible to get a non-integer result even if a counter increases only by
integer increments.

The following example expression returns the number of HTTP requests as measured
over the last 5 minutes, per time series in the range vector:

```
increase(http_requests_total{job="api-server"}[5m])
```

`increase` acts on histogram samples by calculating a new histogram where each
component (sum and count of observations, buckets) is the increase between the
respective component in the first and last native histogram in `v`. However,
each element in `v` that contains a mix of float samples and histogram samples
within the range, will be omitted from the result vector, flagged by a
warn-level annotation.

`increase` should only be used with counters (for both floats and histograms).
It is syntactic sugar for `rate(v)` multiplied by the number of seconds under
the specified time range window, and should be used primarily for human
readability. Use `rate` in recording rules so that increases are tracked
consistently on a per-second basis.

## `info()`

*The `info` function is an experiment to improve UX
around including labels from [info metrics](https://grafana.com/blog/2021/08/04/how-to-use-promql-joins-for-more-effective-queries-of-prometheus-metrics-at-scale/#info-metrics).
The behavior of this function may change in future versions of Prometheus,
including its removal from PromQL. `info` has to be enabled via the
[feature flag](/docs/prometheus/latest/feature_flags/#experimental-promql-functions) `--enable-feature=promql-experimental-functions`.*

`info(v instant-vector, [data-label-selector instant-vector])` finds, for each time
series in `v`, all info series with matching *identifying* labels (more on
this later), and adds the union of their *data* (i.e., non-identifying) labels
to the time series. The second argument `data-label-selector` is optional.
It is not a real instant vector, but uses a subset of its syntax.
It must start and end with curly braces (`{ ... }`) and may only contain label matchers.
The label matchers are used to constrain which info series to consider
and which data labels to add to `v`.

Identifying labels of an info series are the subset of labels that uniquely
identify the info series. The remaining labels are considered
*data labels* (also called non-identifying). (Note that Prometheus's concept
of time series identity always includes *all* the labels. For the sake of the `info`
function, we “logically” define info series identity in a different way than
in the conventional Prometheus view.) The identifying labels of an info series
are used to join it to regular (non-info) series, i.e. those series that have
the same labels as the identifying labels of the info series. The data labels, which are
the ones added to the regular series by the `info` function, effectively encode
metadata key value pairs. (This implies that a change in the data labels
in the conventional Prometheus view constitutes the end of one info series and
the beginning of a new info series, while the “logical” view of the `info` function is
that the same info series continues to exist, just with different “data”.)

The conventional approach of adding data labels is sometimes called a “join query”,
as illustrated by the following example:

```
  rate(http_server_request_duration_seconds_count[2m])
* on (job, instance) group_left (k8s_cluster_name)
  target_info
```

The core of the query is the expression `rate(http_server_request_duration_seconds_count[2m])`.
But to add data labels from an info metric, the user has to use elaborate
(and not very obvious) syntax to specify which info metric to use (`target_info`), what the
identifying labels are (`on (job, instance)`), and which data labels to add
(`group_left (k8s_cluster_name)`).

This query is not only verbose and hard to write, it might also run into an “identity crisis”:
If any of the data labels of `target_info` changes, Prometheus sees that as a change of series
(as alluded to above, Prometheus just has no native concept of non-identifying labels).
If the old `target_info` series is not properly marked as stale (which can happen with certain ingestion paths),
the query above will fail for up to 5m (the lookback delta) because it will find a conflicting
match with both the old and the new version of `target_info`.

The `info` function not only resolves this conflict in favor of the newer series, it also simplifies the syntax
because it knows about the available info series and what their identifying labels are. The example query
looks like this with the `info` function:

```
info(
  rate(http_server_request_duration_seconds_count[2m]),
  {k8s_cluster_name=~".+"}
)
```

The common case of adding *all* data labels can be achieved by
omitting the 2nd argument of the `info` function entirely, simplifying
the example even more:

```
info(rate(http_server_request_duration_seconds_count[2m]))
```

While `info` normally automatically finds all matching info series, it's possible to
restrict them by providing a `__name__` label matcher, e.g.
`{
Note that if there are any time series in `v` that match the `data-label-selector` (or the default `target_info` if that argument is not specified), they will be treated as info series and will be returned unchanged.

### Limitations

In its current iteration, `info` defaults to considering only info series with
the name `target_info`. It also assumes that the identifying info series labels are
`instance` and `job`. `info` does support other info series names however, through
`__name__` label matchers. E.g., one can explicitly say to consider both
`target_info` and `build_info` as follows:
`{have to be `instance` and `job`.

These limitations are partially defeating the purpose of the `info` function.
At the current stage, this is an experiment to find out how useful the approach
turns out to be in practice. A final version of the `info` function will indeed
consider all matching info series and with their appropriate identifying labels.

## `irate()`

`irate(v range-vector)` calculates the per-second instant rate of increase of
the time series in the range vector. This is based on the last two data points.
Breaks in monotonicity (such as counter resets due to target restarts) are
automatically adjusted for. Both samples must be either float samples or
histogram samples. Elements in `v` where one of the last two samples is a float
sample and the other is a histogram sample will be omitted from the result
vector, flagged by a warn-level annotation.

`irate` should only be used with counters (for both floats and histograms).

The following example expression returns the per-second rate of HTTP requests
looking up to 5 minutes back for the two most recent data points, per time
series in the range vector:

```
irate(http_requests_total{job="api-server"}[5m])
```

`irate` should only be used when graphing volatile, fast-moving counters.
Use `rate` for alerts and slow-moving counters, as brief changes
in the rate can reset the `FOR` clause and graphs consisting entirely of rare
spikes are hard to read.

Note that when combining `irate()` with an
[aggregation operator](/docs/prometheus/latest/querying/operators/#aggregation-operators) (e.g. `sum()`)
or a function aggregating over time (any function ending in `_over_time`),
always take an `irate()` first, then aggregate. Otherwise `irate()` cannot detect
counter resets when your target restarts.

## `label_join()`

For each timeseries in `v`, `label_join(v instant-vector, dst_label string, separator string, src_label_1 string, src_label_2 string, ...)` joins all the values of all the `src_labels`
using `separator` and returns the timeseries with the label `dst_label` containing the joined value.
There can be any number of `src_labels` in this function.

`label_join` acts on float and histogram samples in the same way.

This example will return a vector with each time series having a `foo` label with the value `a,b,c` added to it:

```
label_join(up{job="api-server",src1="a",src2="b",src3="c"}, "foo", ",", "src1", "src2", "src3")
```

## `label_replace()`

For each timeseries in `v`, `label_replace(v instant-vector, dst_label string, replacement string, src_label string, regex string)`
matches the [regular expression](/docs/prometheus/latest/querying/basics/#regular-expressions) `regex` against the value of the label `src_label`. If it
matches, the value of the label `dst_label` in the returned timeseries will be the expansion
of `replacement`, together with the original labels in the input. Capturing groups in the
regular expression can be referenced with `$1`, `$2`, etc. Named capturing groups in the regular expression can be referenced with `$name` (where `name` is the capturing group name). If the regular expression doesn't match then the timeseries is returned unchanged.

`label_replace` acts on float and histogram samples in the same way.

This example will return timeseries with the values `a:c` at label `service` and `a` at label `foo`:

```
label_replace(up{job="api-server",service="a:c"}, "foo", "$1", "service", "(.*):.*")
```

This second example has the same effect than the first example, and illustrates use of named capturing groups:

```
label_replace(up{job="api-server",service="a:c"}, "foo", "$name", "service", "(?P<name>.*):(?P<version>.*)")
```

## `ln()`

`ln(v instant-vector)` calculates the natural logarithm for all float samples
in `v`. Histogram samples in the input vector are ignored silently. Special cases are:

* `ln(+Inf) = +Inf`
* `ln(0) = -Inf`
* `ln(x < 0) = NaN`
* `ln(NaN) = NaN`

## `log2()`

`log2(v instant-vector)` calculates the binary logarithm for all float samples
in `v`. Histogram samples in the input vector are ignored silently. The special cases
are equivalent to those in `ln`.

## `log10()`

`log10(v instant-vector)` calculates the decimal logarithm for all float
samples in `v`. Histogram samples in the input vector are ignored silently. The special
cases are equivalent to those in `ln`.

## `minute()`

`minute(v=vector(time()) instant-vector)` interprets float samples in `v` as
timestamps (number of seconds since January 1, 1970 UTC) and returns the minute
of the hour (in UTC) for each of those timestamps. Returned values are from 0
to 59. Histogram samples in the input vector are ignored silently.

## `month()`

`month(v=vector(time()) instant-vector)` interprets float samples in `v` as
timestamps (number of seconds since January 1, 1970 UTC) and returns the month
of the year (in UTC) for each of those timestamps. Returned values are from 1
to 12, where 1 means January etc. Histogram samples in the input vector are
ignored silently.

## `predict_linear()`

`predict_linear(v range-vector, t scalar)` predicts the value of time series
`t` seconds from now, based on the range vector `v`, using [simple linear
regression](https://en.wikipedia.org/wiki/Simple_linear_regression). The range
vector must have at least two float samples in order to perform the
calculation. When `+Inf` or `-Inf` are found in the range vector, the predicted
value will be `NaN`.

`predict_linear` should only be used with gauges and only works for float
samples. Elements in the range vector that contain only histogram samples are
ignored entirely. For elements that contain a mix of float and histogram
samples, only the float samples are used as input, which is flagged by an
info-level annotation.

## `rate()`

`rate(v range-vector)` calculates the per-second average rate of increase of the
time series in the range vector. Breaks in monotonicity (such as counter
resets due to target restarts) are automatically adjusted for. Also, the
calculation extrapolates to the ends of the time range, allowing for missed
scrapes or imperfect alignment of scrape cycles with the range's time period.

The following example expression returns the per-second average rate of HTTP requests
over the last 5 minutes, per time series in the range vector:

```
rate(http_requests_total{job="api-server"}[5m])
```

`rate` acts on native histograms by calculating a new histogram where each
component (sum and count of observations, buckets) is the rate of increase
between the respective component in the first and last native histogram in `v`.
However, each element in `v` that contains a mix of float and native histogram
samples within the range, will be omitted from the result vector, flagged by a
warn-level annotation.

`rate` should only be used with counters (for both floats and histograms). It
is best suited for alerting, and for graphing of slow-moving counters.

Note that when combining `rate()` with an aggregation operator (e.g. `sum()`)
or a function aggregating over time (any function ending in `_over_time`),
always take a `rate()` first, then aggregate. Otherwise `rate()` cannot detect
counter resets when your target restarts.

## `resets()`

For each input time series, `resets(v range-vector)` returns the number of
counter resets within the provided time range as an instant vector. Any
decrease in the value between two consecutive float samples is interpreted as a
counter reset. A reset in a native histogram is detected in a more complex way:
Any decrease in any bucket, including the zero bucket, or in the count of
observation constitutes a counter reset, but also the disappearance of any
previously populated bucket, a decrease of the zero-bucket width, or any schema
change that is not a compatible decrease of resolution.

`resets` should only be used with counters (for both floats and histograms).

A float sample followed by a histogram sample, or vice versa, counts as a
reset. A counter histogram sample followed by a gauge histogram sample, or vice
versa, also counts as a reset (but note that `resets` should not be used on
gauges in the first place, see above).

## `round()`

`round(v instant-vector, to_nearest=1 scalar)` rounds the sample values of all
elements in `v` to the nearest integer. Ties are resolved by rounding up. The
optional `to_nearest` argument allows specifying the nearest multiple to which
the sample values should be rounded. This multiple may also be a fraction.
Histogram samples in the input vector are ignored silently.

## `scalar()`

Given an input vector that contains only one element with a float sample,
`scalar(v instant-vector)` returns the sample value of that float sample as a
scalar. If the input vector does not have exactly one element with a float
sample, `scalar` will return `NaN`. Histogram samples in the input vector are
ignored silently.

## `sgn()`

`sgn(v instant-vector)` returns a vector with all float sample values converted
to their sign, defined as this: 1 if v is positive, -1 if v is negative and 0
if v is equal to zero. Histogram samples in the input vector are ignored silently.

## `sort()`

`sort(v instant-vector)` returns vector elements sorted by their float sample
values, in ascending order. Histogram samples in the input vector are ignored silently.

Please note that `sort` only affects the results of instant queries, as range
query results always have a fixed output ordering.

## `sort_desc()`

Same as `sort`, but sorts in descending order.

## `sort_by_label()`

**This function has to be enabled via the [feature
flag](/docs/prometheus/latest/feature_flags/#experimental-promql-functions)
`--enable-feature=promql-experimental-functions`.**

`sort_by_label(v instant-vector, label string, ...)` returns vector elements
sorted by the values of the given labels in ascending order. In case these
label values are equal, elements are sorted by their full label sets.
`sort_by_label` acts on float and histogram samples in the same way.

Please note that `sort_by_label` only affects the results of instant queries, as
range query results always have a fixed output ordering.

`sort_by_label` uses [natural sort
order](https://en.wikipedia.org/wiki/Natural_sort_order).

## `sort_by_label_desc()`

**This function has to be enabled via the [feature
flag](/docs/prometheus/latest/feature_flags/#experimental-promql-functions)
`--enable-feature=promql-experimental-functions`.**

Same as `sort_by_label`, but sorts in descending order.

## `sqrt()`

`sqrt(v instant-vector)` calculates the square root of all float samples in
`v`. Histogram samples in the input vector are ignored silently.

## `time()`

`time()` returns the number of seconds since January 1, 1970 UTC. Note that
this does not actually return the current time, but the time at which the
expression is to be evaluated.

## `timestamp()`

`timestamp(v instant-vector)` returns the timestamp of each of the samples of
the given vector as the number of seconds since January 1, 1970 UTC. It acts on
float and histogram samples in the same way.

## `vector()`

`vector(s scalar)` converts the scalar `s` to a float sample and returns it as
a single-element instant vector with no labels.

## `year()`

`year(v=vector(time()) instant-vector)` returns the year for each of the given
times in UTC. Histogram samples in the input vector are ignored silently.

## `<aggregation>_over_time()`

The following functions allow aggregating each series of a given range vector
over time and return an instant vector with per-series aggregation results:

* `avg_over_time(range-vector)`: the average value of all float or histogram samples in the specified interval (see details below).
* `min_over_time(range-vector)`: the minimum value of all float samples in the specified interval.
* `max_over_time(range-vector)`: the maximum value of all float samples in the specified interval.
* `sum_over_time(range-vector)`: the sum of all float or histogram samples in the specified interval (see details below).
* `count_over_time(range-vector)`: the count of all samples in the specified interval.
* `quantile_over_time(scalar, range-vector)`: the φ-quantile (0 ≤ φ ≤ 1) of all float samples in the specified interval.
* `stddev_over_time(range-vector)`: the population standard deviation of all float samples in the specified interval.
* `stdvar_over_time(range-vector)`: the population variance of all float samples in the specified interval.
* `last_over_time(range-vector)`: the most recent sample in the specified interval.
* `present_over_time(range-vector)`: the value 1 for any series in the specified interval.

If the [feature flag](/docs/prometheus/latest/feature_flags/#experimental-promql-functions)
`--enable-feature=promql-experimental-functions` is set, the following
additional functions are available:

* `mad_over_time(range-vector)`: the median absolute deviation of all float
  samples in the specified interval.
* `ts_of_min_over_time(range-vector)`: the timestamp of the last float sample
  that has the minimum value of all float samples in the specified interval.
* `ts_of_max_over_time(range-vector)`: the timestamp of the last float sample
  that has the maximum value of all float samples in the specified interval.
* `ts_of_last_over_time(range-vector)`: the timestamp of last sample in the
  specified interval.
* `first_over_time(range-vector)`: the oldest sample in the specified interval.
* `ts_of_first_over_time(range-vector)`: the timestamp of earliest sample in the
  specified interval.

Note that all values in the specified interval have the same weight in the
aggregation even if the values are not equally spaced throughout the interval.

These functions act on histograms in the following way:

* `count_over_time`, `first_over_time`, `last_over_time`, and
  `present_over_time()` act on float and histogram samples in the same way.
* `avg_over_time()` and `sum_over_time()` act on histogram samples in a way
  that corresponds to the respective aggregation operators. If a series
  contains a mix of float samples and histogram samples within the range, the
  corresponding result is removed entirely from the output vector. Such a
  removal is flagged by a warn-level annotation.
* All other functions ignore histogram samples in the following way: Input
  ranges containing only histogram samples are silently removed from the
  output. For ranges with a mix of histogram and float samples, only the float
  samples are processed and the omission of the histogram samples is flagged by
  an info-level annotation.

`first_over_time(m[1m])` differs from `m offset 1m` in that the former will
select the first sample of `m` *within* the 1m range, where `m offset 1m` will
select the most recent sample within the lookback interval *outside and prior
to* the 1m offset. This is particularly useful with `first_over_time(m[step()])`
in range queries (available when `--enable-feature=promql-duration-expr` is set)
to ensure that the sample selected is within the range step.

## Trigonometric Functions

The trigonometric functions work in radians. They ignore histogram samples in
the input vector.

* `acos(v instant-vector)`: calculates the arccosine of all float samples in `v` ([special cases](https://pkg.go.dev/math#Acos)).
* `acosh(v instant-vector)`: calculates the inverse hyperbolic cosine of all float samples in `v` ([special cases](https://pkg.go.dev/math#Acosh)).
* `asin(v instant-vector)`: calculates the arcsine of all float samples in `v` ([special cases](https://pkg.go.dev/math#Asin)).
* `asinh(v instant-vector)`: calculates the inverse hyperbolic sine of all float samples in `v` ([special cases](https://pkg.go.dev/math#Asinh)).
* `atan(v instant-vector)`: calculates the arctangent of all float samples in `v` ([special cases](https://pkg.go.dev/math#Atan)).
* `atanh(v instant-vector)`: calculates the inverse hyperbolic tangent of all float samples in `v` ([special cases](https://pkg.go.dev/math#Atanh)).
* `cos(v instant-vector)`: calculates the cosine of all float samples in `v` ([special cases](https://pkg.go.dev/math#Cos)).
* `cosh(v instant-vector)`: calculates the hyperbolic cosine of all float samples in `v` ([special cases](https://pkg.go.dev/math#Cosh)).
* `sin(v instant-vector)`: calculates the sine of all float samples in `v` ([special cases](https://pkg.go.dev/math#Sin)).
* `sinh(v instant-vector)`: calculates the hyperbolic sine of all float samples in `v` ([special cases](https://pkg.go.dev/math#Sinh)).
* `tan(v instant-vector)`: calculates the tangent of all float samples in `v` ([special cases](https://pkg.go.dev/math#Tan)).
* `tanh(v instant-vector)`: calculates the hyperbolic tangent of all float samples in `v` ([special cases](https://pkg.go.dev/math#Tanh)).

The following are useful for converting between degrees and radians:

* `deg(v instant-vector)`: converts radians to degrees for all float samples in `v`.
* `pi()`: returns pi.
* `rad(v instant-vector)`: converts degrees to radians for all float samples in `v`.

On this page

---

## Bibliography

1. [Querying basics](https://prometheus.io/docs/prometheus/latest/querying/basics/)
2. [Overview](https://prometheus.io/docs/introduction/overview/)
3. [Metric types](https://prometheus.io/docs/concepts/metric_types/)
4. [Operators](https://prometheus.io/docs/prometheus/latest/querying/operators/)
5. [Query functions](https://prometheus.io/docs/prometheus/latest/querying/functions/)