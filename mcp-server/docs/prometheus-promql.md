Querying basics | Prometheustry {
var \_colorScheme = window.localStorage.getItem("mantine-color-scheme-value");
var colorScheme = \_colorScheme === "light" || \_colorScheme === "dark" || \_colorScheme === "auto" ? \_colorScheme : "auto";
var computedColorScheme = colorScheme !== "auto" ? colorScheme : window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
document.documentElement.setAttribute("data-mantine-color-scheme", computedColorScheme);
} catch (e) {}
:root{--mantine-color-black: var(--mantine-color-gray-8);--mantine-font-family-headings: var(--font-inter);--mantine-primary-color-filled: var(--mantine-color-prometheusColor-filled);--mantine-primary-color-filled-hover: var(--mantine-color-prometheusColor-filled-hover);--mantine-primary-color-light: var(--mantine-color-prometheusColor-light);--mantine-primary-color-light-hover: var(--mantine-color-prometheusColor-light-hover);--mantine-primary-color-light-color: var(--mantine-color-prometheusColor-light-color);--mantine-primary-color-0: var(--mantine-color-prometheusColor-0);--mantine-primary-color-1: var(--mantine-color-prometheusColor-1);--mantine-primary-color-2: var(--mantine-color-prometheusColor-2);--mantine-primary-color-3: var(--mantine-color-prometheusColor-3);--mantine-primary-color-4: var(--mantine-color-prometheusColor-4);--mantine-primary-color-5: var(--mantine-color-prometheusColor-5);--mantine-primary-color-6: var(--mantine-color-prometheusColor-6);--mantine-primary-color-7: var(--mantine-color-prometheusColor-7);--mantine-primary-color-8: var(--mantine-color-prometheusColor-8);--mantine-primary-color-9: var(--mantine-color-prometheusColor-9);--mantine-color-prometheusColor-0: #ffede6;--mantine-color-prometheusColor-1: #ffdad2;--mantine-color-prometheusColor-2: #f6b5a4;--mantine-color-prometheusColor-3: #f08e74;--mantine-color-prometheusColor-4: #ea6b4b;--mantine-color-prometheusColor-5: #e75630;--mantine-color-prometheusColor-6: #e64a22;--mantine-color-prometheusColor-7: #cc3b16;--mantine-color-prometheusColor-8: #b73311;--mantine-color-prometheusColor-9: #a02709;}:root[data-mantine-color-scheme="dark"]{--mantine-color-anchor: var(--mantine-color-prometheusColor-4);--mantine-color-prometheusColor-text: var(--mantine-color-prometheusColor-4);--mantine-color-prometheusColor-filled: var(--mantine-color-prometheusColor-8);--mantine-color-prometheusColor-filled-hover: var(--mantine-color-prometheusColor-9);--mantine-color-prometheusColor-light: rgba(230, 74, 34, 0.15);--mantine-color-prometheusColor-light-hover: rgba(230, 74, 34, 0.2);--mantine-color-prometheusColor-light-color: var(--mantine-color-prometheusColor-3);--mantine-color-prometheusColor-outline: var(--mantine-color-prometheusColor-4);--mantine-color-prometheusColor-outline-hover: rgba(234, 107, 75, 0.05);}:root[data-mantine-color-scheme="light"]{--mantine-color-text: var(--mantine-color-gray-8);--mantine-color-anchor: var(--mantine-color-prometheusColor-6);--mantine-color-prometheusColor-text: var(--mantine-color-prometheusColor-filled);--mantine-color-prometheusColor-filled: var(--mantine-color-prometheusColor-6);--mantine-color-prometheusColor-filled-hover: var(--mantine-color-prometheusColor-7);--mantine-color-prometheusColor-light: rgba(230, 74, 34, 0.1);--mantine-color-prometheusColor-light-hover: rgba(230, 74, 34, 0.12);--mantine-color-prometheusColor-light-color: var(--mantine-color-prometheusColor-6);--mantine-color-prometheusColor-outline: var(--mantine-color-prometheusColor-6);--mantine-color-prometheusColor-outline-hover: rgba(230, 74, 34, 0.05);}@media (max-width: 35.99375em) {.mantine-visible-from-xs {display: none !important;}}@media (min-width: 36em) {.mantine-hidden-from-xs {display: none !important;}}@media (max-width: 47.99375em) {.mantine-visible-from-sm {display: none !important;}}@media (min-width: 48em) {.mantine-hidden-from-sm {display: none !important;}}@media (max-width: 61.99375em) {.mantine-visible-from-md {display: none !important;}}@media (min-width: 62em) {.mantine-hidden-from-md {display: none !important;}}@media (max-width: 74.99375em) {.mantine-visible-from-lg {display: none !important;}}@media (min-width: 75em) {.mantine-hidden-from-lg {display: none !important;}}@media (max-width: 87.99375em) {.mantine-visible-from-xl {display: none !important;}}@media (min-width: 88em) {.mantine-hidden-from-xl {display: none !important;}}:root{--app-shell-header-height:var(--header-height);--app-shell-header-offset:var(--header-height);--app-shell-padding:0px;}

.\_\_m\_\_-\_R\_2lmtb\_{padding-inline:var(--mantine-spacing-md);}@media(min-width: 36em){.\_\_m\_\_-\_R\_2lmtb\_{padding-inline:var(--mantine-spacing-xl);}}

[Prometheus](/)

[Docs](/docs/introduction/overview/)[Download](/download/)[Community](/community/)[Support & Training](/support-training/)[Blog](/blog/)

Ctrl + K

.\_\_m\_\_-\_R\_mmtb\_{padding-inline:var(--mantine-spacing-md);}@media(min-width: 36em){.\_\_m\_\_-\_R\_mmtb\_{padding-inline:var(--mantine-spacing-xl);}}

Show nav

[Introduction](#required-for-focus)

[Overview](/docs/introduction/overview/)[First steps](/docs/introduction/first_steps/)[Comparison to alternatives](/docs/introduction/comparison/)[FAQ](/docs/introduction/faq/)[Roadmap](/docs/introduction/roadmap/)[Design documents](/docs/introduction/design-doc/)[Media](/docs/introduction/media/)[Glossary](/docs/introduction/glossary/)[Long-term support](/docs/introduction/release-cycle/)

[Concepts](#required-for-focus)

[Data model](/docs/concepts/data_model/)[Metric types](/docs/concepts/metric_types/)[Jobs and instances](/docs/concepts/jobs_instances/)

[Prometheus Server](#required-for-focus)

[Getting started](/docs/prometheus/latest/getting_started/)[Installation](/docs/prometheus/latest/installation/)[Configuration](#required-for-focus)

[Configuration](/docs/prometheus/latest/configuration/configuration/)[Recording rules](/docs/prometheus/latest/configuration/recording_rules/)[Alerting rules](/docs/prometheus/latest/configuration/alerting_rules/)[Template examples](/docs/prometheus/latest/configuration/template_examples/)[Template reference](/docs/prometheus/latest/configuration/template_reference/)[HTTP configuration for promtool](/docs/prometheus/latest/configuration/promtool/)[Unit testing for rules](/docs/prometheus/latest/configuration/unit_testing_rules/)[HTTPS and authentication](/docs/prometheus/latest/configuration/https/)

[Agent Mode](/docs/prometheus/latest/prometheus_agent/)[Querying](#required-for-focus)

[Basics](/docs/prometheus/latest/querying/basics/)[Operators](/docs/prometheus/latest/querying/operators/)[Functions](/docs/prometheus/latest/querying/functions/)[Examples](/docs/prometheus/latest/querying/examples/)[HTTP API](/docs/prometheus/latest/querying/api/)[Remote Read API](/docs/prometheus/latest/querying/remote_read_api/)

[Storage](/docs/prometheus/latest/storage/)[Federation](/docs/prometheus/latest/federation/)[HTTP SD](/docs/prometheus/latest/http_sd/)[Management API](/docs/prometheus/latest/management_api/)[Command Line](#required-for-focus)

[prometheus](/docs/prometheus/latest/command-line/prometheus/)[promtool](/docs/prometheus/latest/command-line/promtool/)

[Migration](/docs/prometheus/latest/migration/)[API stability](/docs/prometheus/latest/stability/)[Feature flags](/docs/prometheus/latest/feature_flags/)

[Visualization](#required-for-focus)

[Expression browser](/docs/visualization/browser/)[Grafana](/docs/visualization/grafana/)[Perses](/docs/visualization/perses/)[Console templates](/docs/visualization/consoles/)

[Instrumenting](#required-for-focus)

[Client libraries](/docs/instrumenting/clientlibs/)[Writing client libraries](/docs/instrumenting/writing_clientlibs/)[Pushing metrics](/docs/instrumenting/pushing/)[Exporters and integrations](/docs/instrumenting/exporters/)[Writing exporters](/docs/instrumenting/writing_exporters/)[Exposition formats](/docs/instrumenting/exposition_formats/)[UTF-8 escaping schemes](/docs/instrumenting/escaping_schemes/)[Content negotiation](/docs/instrumenting/content_negotiation/)

[Operating](#required-for-focus)

[Security](/docs/operating/security/)[Integrations](/docs/operating/integrations/)

[Alertmanager](#required-for-focus)

[Alerting overview](/docs/alerting/latest/overview/)[Alertmanager](/docs/alerting/latest/alertmanager/)[Configuration](/docs/alerting/latest/configuration/)[High Availability](/docs/alerting/latest/high_availability/)[Notification Integrations](/docs/alerting/latest/integrations/)[Alerts API](/docs/alerting/latest/alerts_api/)[Notification template reference](/docs/alerting/latest/notifications/)[Notification template examples](/docs/alerting/latest/notification_examples/)[Management API](/docs/alerting/latest/management_api/)[HTTPS and authentication](/docs/alerting/latest/https/)

[Best practices](#required-for-focus)

[Metric and label naming](/docs/practices/naming/)[Consoles and dashboards](/docs/practices/consoles/)[Instrumentation](/docs/practices/instrumentation/)[Histograms and summaries](/docs/practices/histograms/)[Alerting](/docs/practices/alerting/)[Recording rules](/docs/practices/rules/)[When to use the Pushgateway](/docs/practices/pushing/)[Remote write tuning](/docs/practices/remote_write/)[The Zen of Prometheus](/docs/practices/the_zen/)

[Guides](#required-for-focus)

[Basic auth](/docs/guides/basic-auth/)[Monitoring Docker container metrics using cAdvisor](/docs/guides/cadvisor/)[Use file-based service discovery to discover scrape targets](/docs/guides/file-sd/)[Instrumenting a Go application](/docs/guides/go-application/)[Understanding and using the multi-target exporter pattern](/docs/guides/multi-target-exporter/)[Monitoring Linux host metrics with the Node Exporter](/docs/guides/node-exporter/)[OpenTelemetry](/docs/guides/opentelemetry/)[UTF-8 in Prometheus](/docs/guides/utf8/)[Docker Swarm](/docs/guides/dockerswarm/)[OpenMetrics 2.0 Migration Guide for Client Libraries](/docs/guides/open_metrics_2_0_migration/)[Query log](/docs/guides/query-log/)[TLS encryption](/docs/guides/tls-encryption/)

[Tutorials](#required-for-focus)

[Getting started with Prometheus](/docs/tutorials/getting_started/)[Understanding metric types](/docs/tutorials/understanding_metric_types/)[Instrumenting HTTP server written in Go](/docs/tutorials/instrumenting_http_server_in_go/)[Visualizing metrics using Grafana](/docs/tutorials/visualizing_metrics_using_grafana/)[Alerting based on metrics](/docs/tutorials/alerting_based_on_metrics/)

[Specifications](#required-for-focus)

[Native Histograms](/docs/specs/native_histograms/)[OpenMetrics](#required-for-focus)

[1.0](/docs/specs/om/open_metrics_spec/)[2.0](/docs/specs/om/open_metrics_spec_2_0/)

[Remote Write](#required-for-focus)

[1.0](/docs/specs/prw/remote_write_spec/)[2.0](/docs/specs/prw/remote_write_spec_2_0/)

# Querying basics

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
`{__name__="http_requests_total"}`. Matchers other than `=` (`!=`, `=~`, `!~`) may also be used.
The following expression selects all metrics that have a name starting with `job:`:

```
{__name__=~"job:.*"}
```

The metric name must not be one of the keywords `bool`, `on`, `ignoring`, `group_left` and `group_right`. The following expression is illegal:

```
on{} # Bad!
```

A workaround for this restriction is to use the `__name__` label:

```
{__name__="on"} # Good!
```

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

[Previous

Agent Mode](/docs/prometheus/latest/prometheus_agent/)

[Edit

Edit this page](https://github.com/prometheus/prometheus/blob/main/docs/querying/basics.md)[Issue

Report an issue](https://github.com/prometheus/prometheus/issues/new?title=docs%3A%20Issue%20with%20%22Querying%20basics%22&body=**Page%3A**%20https%3A%2F%2Fprometheus.io%2Fdocs%2Fprometheus%2Flatest%2Fquerying%2Fbasics%2F%0A%0A**Describe%20the%20issue%3A**%0A%0A)

[Next

Operators](/docs/prometheus/latest/querying/operators/)

On this page

.\_\_m\_\_-\_R\_3mtb\_{padding-inline:var(--mantine-spacing-md);}@media(min-width: 36em){.\_\_m\_\_-\_R\_3mtb\_{padding-inline:var(--mantine-spacing-xl);}}

© Prometheus Authors 2014-2026 | Documentation Distributed under CC-BY-4.0

© 2026 The Linux Foundation. All rights reserved. The Linux Foundation has registered trademarks and uses trademarks. For a list of trademarks of The Linux Foundation, please see our [Trademark Usage](https://www.linuxfoundation.org/trademark-usage) page.

(self.\_\_next\_f=self.\_\_next\_f||[]).push([0])self.\_\_next\_f.push([1,"1:\"$Sreact.fragment\"\n2:I[90533,[\"545\",\"static/chunks/c16f53c3-e2edfe54eba3117f.js\",\"341\",\"static/chunks/341-0544a5ed99d6b02e.js\",\"619\",\"static/chunks/619-f072ac750404f9da.js\",\"582\",\"static/chunks/app/docs/%5B...slug%5D/page-1b753d14db7f06db.js\"],\"ColorSchemeScript\"]\n3:I[3601,[\"545\",\"static/chunks/c16f53c3-e2edfe54eba3117f.js\",\"341\",\"static/chunks/341-0544a5ed99d6b02e.js\",\"619\",\"static/chunks/619-f072ac750404f9da.js\",\"582\",\"static/chunks/app/docs/%5B...slug%5D/page-1b753d14db7f06db.js\"],\"MantineProvider\"]\n4:I[75802,[\"545\",\"static/chunks/c16f53c3-e2edfe54eba3117f.js\",\"341\",\"static/chunks/341-0544a5ed99d6b02e.js\",\"619\",\"static/chunks/619-f072ac750404f9da.js\",\"582\",\"static/chunks/app/docs/%5B...slug%5D/page-1b753d14db7f06db.js\"],\"AppShell\"]\n5:I[93116,[\"545\",\"static/chunks/c16f53c3-e2edfe54eba3117f.js\",\"341\",\"static/chunks/341-0544a5ed99d6b02e.js\",\"619\",\"static/chunks/619-f072ac750404f9da.js\",\"728\",\"static/chunks/728-61b6b69bb6f20ba3.js\",\"687\",\"static/chunks/687-55fda7d9c0abd233.js\",\"177\",\"static/chunks/app/layout-a67ecb9d553d80eb.js\"],\"Header\"]\n6:I[44190,[\"545\",\"static/chunks/c16f53c3-e2edfe54eba3117f.js\",\"341\",\"static/chunks/341-0544a5ed99d6b02e.js\",\"619\",\"static/chunks/619-f072ac750404f9da.js\",\"582\",\"static/chunks/app/docs/%5B...slug%5D/page-1b753d14db7f06db.js\"],\"AppShellMain\"]\n7:I[13877,[\"545\",\"static/chunks/c16f53c3-e2edfe54eba3117f.js\",\"341\",\"static/chunks/341-0544a5ed99d6b02e.js\",\"619\",\"static/chunks/619-f072ac750404f9da.js\",\"582\",\"static/chunks/app/docs/%5B...slug%5D/page-1b753d14db7f06db.js\"],\"Container\"]\n8:I[9766,[],\"\"]\n9:I[98924,[],\"\"]\na:I[69772,[\"545\",\"static/chunks/c16f53c3-e2edfe54eba3117f.js\",\"341\",\"static/chunks/341-0544a5ed99d6b02e.js\",\"619\",\"static/chunks/619-f072ac750404f9da.js\",\"582\",\"static/chunks/app/docs/%5B...slug%5D/page-1b753d14db7f06db.js\"],\"Space\"]\nb:I[67661,[\"545\",\"static/chunks/c16f53c3-e2edfe54eba3117f.js\",\"341\",\"static/chunks/341-0544a5ed99d6b02e.js\",\"619\",\"static/chunks/619-f072ac750404f9da.js\",\"582\",\"static/chunks/app/docs/%5B...slug%5D/page-1b753d14db7f06db.js\"],\"Group\"]\nc:I[70305,["])self.\_\_next\_f.push([1,"\"545\",\"static/chunks/c16f53c3-e2edfe54eba3117f.js\",\"341\",\"static/chunks/341-0544a5ed99d6b02e.js\",\"619\",\"static/chunks/619-f072ac750404f9da.js\",\"582\",\"static/chunks/app/docs/%5B...slug%5D/page-1b753d14db7f06db.js\"],\"Text\"]\nd:I[77147,[\"545\",\"static/chunks/c16f53c3-e2edfe54eba3117f.js\",\"341\",\"static/chunks/341-0544a5ed99d6b02e.js\",\"619\",\"static/chunks/619-f072ac750404f9da.js\",\"582\",\"static/chunks/app/docs/%5B...slug%5D/page-1b753d14db7f06db.js\"],\"Anchor\"]\ne:I[68332,[\"545\",\"static/chunks/c16f53c3-e2edfe54eba3117f.js\",\"341\",\"static/chunks/341-0544a5ed99d6b02e.js\",\"619\",\"static/chunks/619-f072ac750404f9da.js\",\"728\",\"static/chunks/728-61b6b69bb6f20ba3.js\",\"687\",\"static/chunks/687-55fda7d9c0abd233.js\",\"177\",\"static/chunks/app/layout-a67ecb9d553d80eb.js\"],\"GoogleAnalytics\"]\nf:I[58421,[\"545\",\"static/chunks/c16f53c3-e2edfe54eba3117f.js\",\"341\",\"static/chunks/341-0544a5ed99d6b02e.js\",\"619\",\"static/chunks/619-f072ac750404f9da.js\",\"582\",\"static/chunks/app/docs/%5B...slug%5D/page-1b753d14db7f06db.js\"],\"Popover\"]\n10:I[36538,[\"545\",\"static/chunks/c16f53c3-e2edfe54eba3117f.js\",\"341\",\"static/chunks/341-0544a5ed99d6b02e.js\",\"619\",\"static/chunks/619-f072ac750404f9da.js\",\"582\",\"static/chunks/app/docs/%5B...slug%5D/page-1b753d14db7f06db.js\"],\"PopoverTarget\"]\n11:I[96778,[\"545\",\"static/chunks/c16f53c3-e2edfe54eba3117f.js\",\"341\",\"static/chunks/341-0544a5ed99d6b02e.js\",\"619\",\"static/chunks/619-f072ac750404f9da.js\",\"582\",\"static/chunks/app/docs/%5B...slug%5D/page-1b753d14db7f06db.js\"],\"Button\"]\n12:I[79770,[\"545\",\"static/chunks/c16f53c3-e2edfe54eba3117f.js\",\"341\",\"static/chunks/341-0544a5ed99d6b02e.js\",\"619\",\"static/chunks/619-f072ac750404f9da.js\",\"582\",\"static/chunks/app/docs/%5B...slug%5D/page-1b753d14db7f06db.js\"],\"PopoverDropdown\"]\n13:I[18845,[\"545\",\"static/chunks/c16f53c3-e2edfe54eba3117f.js\",\"341\",\"static/chunks/341-0544a5ed99d6b02e.js\",\"619\",\"static/chunks/619-f072ac750404f9da.js\",\"582\",\"static/chunks/app/docs/%5B...slug%5D/page-1b753d14db7f06db.js\"],\"ScrollAreaAutosize\"]\n1a:I[57150,[],\"\"]\n:HL[\"/\_next/static/media/155cae559bbd1a77-s.p."])self.\_\_next\_f.push([1,"woff2\",\"font\",{\"crossOrigin\":\"\",\"type\":\"font/woff2\"}]\n:HL[\"/\_next/static/media/e4af272ccee01ff0-s.p.woff2\",\"font\",{\"crossOrigin\":\"\",\"type\":\"font/woff2\"}]\n:HL[\"/\_next/static/css/0566b04bc4104246.css\",\"style\"]\n:HL[\"/\_next/static/css/12996fad8d583efc.css\",\"style\"]\n:HL[\"/\_next/static/css/afedc5bb723d1741.css\",\"style\"]\n"])self.\_\_next\_f.push([1,"0:{\"P\":null,\"b\":\"x7aRXbMcsvSWTolTY3uxv\",\"p\":\"\",\"c\":[\"\",\"docs\",\"prometheus\",\"latest\",\"querying\",\"basics\",\"\"],\"i\":false,\"f\":[[[\"\",{\"children\":[\"docs\",{\"children\":[[\"slug\",\"prometheus/latest/querying/basics\",\"c\"],{\"children\":[\"\_\_PAGE\_\_\",{}]}]}]},\"$undefined\",\"$undefined\",true],[\"\",[\"$\",\"$1\",\"c\",{\"children\":[[[\"$\",\"link\",\"0\",{\"rel\":\"stylesheet\",\"href\":\"/\_next/static/css/0566b04bc4104246.css\",\"precedence\":\"next\",\"crossOrigin\":\"$undefined\",\"nonce\":\"$undefined\"}],[\"$\",\"link\",\"1\",{\"rel\":\"stylesheet\",\"href\":\"/\_next/static/css/12996fad8d583efc.css\",\"precedence\":\"next\",\"crossOrigin\":\"$undefined\",\"nonce\":\"$undefined\"}],[\"$\",\"link\",\"2\",{\"rel\":\"stylesheet\",\"href\":\"/\_next/static/css/afedc5bb723d1741.css\",\"precedence\":\"next\",\"crossOrigin\":\"$undefined\",\"nonce\":\"$undefined\"}]],[\"$\",\"html\",null,{\"lang\":\"en\",\"suppressHydrationWarning\":true,\"data-mantine-color-scheme\":\"light\",\"className\":\"\_\_variable\_f367f3 \_\_variable\_d0e872\",\"style\":{\"--header-height\":\"72px\"},\"children\":[[\"$\",\"head\",null,{\"children\":[\"$\",\"$L2\",null,{\"defaultColorScheme\":\"auto\"}]}],[\"$\",\"body\",null,{\"children\":[\"$\",\"$L3\",null,{\"theme\":{\"colors\":{\"prometheusColor\":[\"#ffede6\",\"#ffdad2\",\"#f6b5a4\",\"#f08e74\",\"#ea6b4b\",\"#e75630\",\"#e64a22\",\"#cc3b16\",\"#b73311\",\"#a02709\"]},\"black\":\"var(--mantine-color-gray-8)\",\"primaryColor\":\"prometheusColor\",\"headings\":{\"fontFamily\":\"var(--font-inter)\",\"sizes\":{\"h1\":{}}}},\"defaultColorScheme\":\"auto\",\"children\":[\"$\",\"$L4\",null,{\"header\":{\"height\":\"var(--header-height)\"},\"children\":[[\"$\",\"$L5\",null,{\"announcement\":\"$undefined\"}],[\"$\",\"$L6\",null,{\"children\":[\"$\",\"$L7\",null,{\"size\":\"xl\",\"mt\":\"xl\",\"px\":{\"base\":\"md\",\"xs\":\"xl\"},\"children\":[[\"$\",\"$L8\",null,{\"parallelRouterKey\":\"children\",\"error\":\"$undefined\",\"errorStyles\":\"$undefined\",\"errorScripts\":\"$undefined\",\"template\":[\"$\",\"$L9\",null,{}],\"templateStyles\":\"$undefined\",\"templateScripts\":\"$undefined\",\"notFound\":[[[\"$\",\"title\",null,{\"children\":\"404: This page could not be found.\"}],[\"$\",\"div\",null,{\"style\":{\"fontFamily\":\"system-ui,\\\"Segoe UI\\\",Roboto,Helvetica,Arial,sans-serif,\\\"Apple Color Emoji\\\",\\\"Segoe UI Emoji\\\"\",\"height\":\"100vh\",\"textAlign\":\"center\",\"display\":\"flex\",\"flexDirection\":\"column\",\"alignItems\":\"center\",\"justifyContent\":\"center\"},\"children\":[\"$\",\"div\",null,{\"children\":[[\"$\",\"style\",null,{\"dangerouslySetInnerHTML\":{\"\_\_html\":\"body{color:#000;background:#fff;margin:0}.next-error-h1{border-right:1px solid rgba(0,0,0,.3)}@media (prefers-color-scheme:dark){body{color:#fff;background:#000}.next-error-h1{border-right:1px solid rgba(255,255,255,.3)}}\"}}],[\"$\",\"h1\",null,{\"className\":\"next-error-h1\",\"style\":{\"display\":\"inline-block\",\"margin\":\"0 20px 0 0\",\"padding\":\"0 23px 0 0\",\"fontSize\":24,\"fontWeight\":500,\"verticalAlign\":\"top\",\"lineHeight\":\"49px\"},\"children\":404}],[\"$\",\"div\",null,{\"style\":{\"display\":\"inline-block\"},\"children\":[\"$\",\"h2\",null,{\"style\":{\"fontSize\":14,\"fontWeight\":400,\"lineHeight\":\"49px\",\"margin\":0},\"children\":\"This page could not be found.\"}]}]]}]}]],[]],\"forbidden\":\"$undefined\",\"unauthorized\":\"$undefined\"}],[\"$\",\"$La\",null,{\"h\":50}]]}]}],[\"$\",\"footer\",null,{\"style\":{\"backgroundColor\":\"light-dark(var(--mantine-color-gray-0), var(--mantine-color-dark-9))\"},\"children\":[\"$\",\"$L7\",null,{\"size\":\"xl\",\"px\":{\"base\":\"md\",\"xs\":\"xl\"},\"py\":\"xl\",\"children\":[\"$\",\"$Lb\",null,{\"children\":[[\"$\",\"$Lc\",null,{\"c\":\"dimmed\",\"fz\":\"sm\",\"children\":[\"© Prometheus Authors 2014-\",2026,\" | Documentation Distributed under CC-BY-4.0\"]}],[\"$\",\"$Lc\",null,{\"c\":\"dimmed\",\"fz\":\"sm\",\"children\":[\"© \",2026,\" The Linux Foundation. All rights reserved. The Linux Foundation has registered trademarks and uses trademarks. For a list of trademarks of The Linux Foundation, please see our\",\" \",[\"$\",\"$Ld\",null,{\"inherit\":true,\"href\":\"https://www.linuxfoundation.org/trademark-usage\",\"target\":\"\_blank\",\"children\":\"Trademark Usage\"}],\" \",\"page.\"]}]]}]}]}]]}]}]}],[\"$\",\"$Le\",null,{\"gaId\":\"G-80ZM8LGB96\"}]]}]]}],{\"children\":[\"docs\",[\"$\",\"$1\",\"c\",{\"children\":[null,[[\"$\",\"$Lf\",null,{\"position\":\"bottom\",\"withArrow\":true,\"shadow\":\"md\",\"children\":[[\"$\",\"$L10\",null,{\"children\":[\"$\",\"$L11\",null,{\"hiddenFrom\":\"sm\",\"variant\":\"outline\",\"mb\":\"lg\",\"leftSection\":[\"$\",\"svg\",null,{\"ref\":\"$undefined\",\"xmlns\":\"http://www.w3.org/2000/svg\",\"width\":24,\"height\":24,\"viewBox\":\"0 0 24 24\",\"fill\":\"none\",\"stroke\":\"currentColor\",\"strokeWidth\":1.5,\"strokeLinecap\":\"round\",\"strokeLinejoin\":\"round\",\"className\":\"tabler-icon tabler-icon-menu-2 \",\"children\":[\"$undefined\",[\"$\",\"path\",\"svg-0\",{\"d\":\"M4 6l16 0\"}],[\"$\",\"path\",\"svg-1\",{\"d\":\"M4 12l16 0\"}],[\"$\",\"path\",\"svg-2\",{\"d\":\"M4 18l16 0\"}],\"$undefined\"]}],\"color\":\"light-dark(var(--mantine-color-gray-7), var(--mantine-color-gray-4))\",\"fw\":\"normal\",\"bd\":\"1px solid var(--mantine-color-gray-5)\",\"children\":\"Show nav\"}]}],[\"$\",\"$L12\",null,{\"mah\":\"calc(100vh - var(--header-height) - var(--header-to-content-margin))\",\"children\":[\"$\",\"$L13\",null,{\"mah\":\"calc(80vh - var(--header-height))\",\"type\":\"never\",\"children\":\"$L14\"}]}]]}],\"$L15\",\"$L16\"]]}],{\"children\":[[\"slug\",\"prometheus/latest/querying/basics\",\"c\"],\"$L17\",{\"children\":[\"\_\_PAGE\_\_\",\"$L18\",{},null,false]},null,false]},null,false]},null,false],\"$L19\",false]],\"m\":\"$undefined\",\"G\":[\"$1a\",[]],\"s\":false,\"S\":true}\n"])self.\_\_next\_f.push([1,"1b:I[32968,[\"545\",\"static/chunks/c16f53c3-e2edfe54eba3117f.js\",\"341\",\"static/chunks/341-0544a5ed99d6b02e.js\",\"619\",\"static/chunks/619-f072ac750404f9da.js\",\"499\",\"static/chunks/app/docs/layout-56c3c649b197c5c2.js\"],\"default\"]\n1c:I[67623,[\"545\",\"static/chunks/c16f53c3-e2edfe54eba3117f.js\",\"341\",\"static/chunks/341-0544a5ed99d6b02e.js\",\"619\",\"static/chunks/619-f072ac750404f9da.js\",\"582\",\"static/chunks/app/docs/%5B...slug%5D/page-1b753d14db7f06db.js\"],\"Box\"]\n1d:I[18845,[\"545\",\"static/chunks/c16f53c3-e2edfe54eba3117f.js\",\"341\",\"static/chunks/341-0544a5ed99d6b02e.js\",\"619\",\"static/chunks/619-f072ac750404f9da.js\",\"582\",\"static/chunks/app/docs/%5B...slug%5D/page-1b753d14db7f06db.js\"],\"ScrollArea\"]\n1e:I[12409,[\"545\",\"static/chunks/c16f53c3-e2edfe54eba3117f.js\",\"341\",\"static/chunks/341-0544a5ed99d6b02e.js\",\"619\",\"static/chunks/619-f072ac750404f9da.js\",\"499\",\"static/chunks/app/docs/layout-56c3c649b197c5c2.js\"],\"default\"]\n1f:I[648,[\"545\",\"static/chunks/c16f53c3-e2edfe54eba3117f.js\",\"341\",\"static/chunks/341-0544a5ed99d6b02e.js\",\"619\",\"static/chunks/619-f072ac750404f9da.js\",\"499\",\"static/chunks/app/docs/layout-56c3c649b197c5c2.js\"],\"AnchorScroller\"]\n21:I[24431,[],\"OutletBoundary\"]\n23:I[15278,[],\"AsyncMetadataOutlet\"]\n25:I[24431,[],\"ViewportBoundary\"]\n27:I[24431,[],\"MetadataBoundary\"]\n28:\"$Sreact.suspense\"\n14:[\"$\",\"$L1b\",null,{}]\n"])self.\_\_next\_f.push([1,"15:[\"$\",\"$Lb\",null,{\"wrap\":\"nowrap\",\"align\":\"flex-start\",\"gap\":50,\"children\":[[\"$\",\"$L1c\",null,{\"component\":\"nav\",\"w\":250,\"flex\":\"0 0 auto\",\"h\":\"calc(100vh - var(--header-height) - var(--header-to-content-margin))\",\"pos\":\"sticky\",\"top\":\"calc(var(--header-height) + var(--header-to-content-margin))\",\"visibleFrom\":\"sm\",\"style\":{\"borderInlineEnd\":\"1px solid light-dark(var(--mantine-color-gray-3), var(--mantine-color-gray-7))\"},\"mx\":\"calc(var(--mantine-spacing-xs) \* -1)\",\"children\":[\"$\",\"$L1d\",null,{\"h\":\"calc(100vh - var(--header-height) - var(--header-to-content-margin))\",\"type\":\"never\",\"children\":[\"$\",\"$L1c\",null,{\"px\":\"xs\",\"children\":[\"$\",\"$L1b\",null,{}]}]}]}],[\"$\",\"div\",null,{\"style\":{\"minWidth\":0},\"children\":[\"$\",\"$L8\",null,{\"parallelRouterKey\":\"children\",\"error\":\"$undefined\",\"errorStyles\":\"$undefined\",\"errorScripts\":\"$undefined\",\"template\":[\"$\",\"$L9\",null,{}],\"templateStyles\":\"$undefined\",\"templateScripts\":\"$undefined\",\"notFound\":\"$undefined\",\"forbidden\":\"$undefined\",\"unauthorized\":\"$undefined\"}]}],[\"$\",\"$L1e\",null,{\"maw\":230,\"wrapperProps\":{\"visibleFrom\":\"lg\"},\"scrollSpyOptions\":{\"selector\":\".markdown-content :is(h2, h3), .markdown-content h1:not(:first-of-type)\"}}]]}]\n"])self.\_\_next\_f.push([1,"16:[\"$\",\"$L1f\",null,{}]\n17:[\"$\",\"$1\",\"c\",{\"children\":[null,[\"$\",\"$L8\",null,{\"parallelRouterKey\":\"children\",\"error\":\"$undefined\",\"errorStyles\":\"$undefined\",\"errorScripts\":\"$undefined\",\"template\":[\"$\",\"$L9\",null,{}],\"templateStyles\":\"$undefined\",\"templateScripts\":\"$undefined\",\"notFound\":\"$undefined\",\"forbidden\":\"$undefined\",\"unauthorized\":\"$undefined\"}]]}]\n18:[\"$\",\"$1\",\"c\",{\"children\":[\"$L20\",null,[\"$\",\"$L21\",null,{\"children\":[\"$L22\",[\"$\",\"$L23\",null,{\"promise\":\"$@24\"}]]}]]}]\n19:[\"$\",\"$1\",\"h\",{\"children\":[null,[[\"$\",\"$L25\",null,{\"children\":\"$L26\"}],[\"$\",\"meta\",null,{\"name\":\"next-size-adjust\",\"content\":\"\"}]],[\"$\",\"$L27\",null,{\"children\":[\"$\",\"div\",null,{\"hidden\":true,\"children\":[\"$\",\"$28\",null,{\"fallback\":null,\"children\":\"$L29\"}]}]}]]}]\n"])self.\_\_next\_f.push([1,"26:[[\"$\",\"meta\",\"0\",{\"charSet\":\"utf-8\"}],[\"$\",\"meta\",\"1\",{\"name\":\"viewport\",\"content\":\"width=device-width, initial-scale=1\"}]]\n22:null\n"])self.\_\_next\_f.push([1,"2a:I[80622,[],\"IconMark\"]\n"])self.\_\_next\_f.push([1,"24:{\"metadata\":[[\"$\",\"title\",\"0\",{\"children\":\"Querying basics | Prometheus\"}],[\"$\",\"meta\",\"1\",{\"name\":\"description\",\"content\":\"Prometheus project documentation for Querying basics\"}],[\"$\",\"meta\",\"2\",{\"name\":\"keywords\",\"content\":\"prometheus,monitoring,monitoring system,time series,time series database,alerting,metrics,telemetry\"}],[\"$\",\"link\",\"3\",{\"rel\":\"canonical\",\"href\":\"https://prometheus.io/docs/prometheus/latest/querying/basics/\"}],[\"$\",\"meta\",\"4\",{\"property\":\"og:title\",\"content\":\"Querying basics | Prometheus\"}],[\"$\",\"meta\",\"5\",{\"property\":\"og:description\",\"content\":\"Prometheus project documentation for Querying basics\"}],[\"$\",\"meta\",\"6\",{\"property\":\"og:url\",\"content\":\"https://prometheus.io/docs/prometheus/latest/querying/basics/\"}],[\"$\",\"meta\",\"7\",{\"name\":\"twitter:card\",\"content\":\"summary\_large\_image\"}],[\"$\",\"meta\",\"8\",{\"name\":\"twitter:title\",\"content\":\"Querying basics | Prometheus\"}],[\"$\",\"meta\",\"9\",{\"name\":\"twitter:description\",\"content\":\"Prometheus project documentation for Querying basics\"}],[\"$\",\"meta\",\"10\",{\"name\":\"twitter:image:type\",\"content\":\"image/png\"}],[\"$\",\"meta\",\"11\",{\"name\":\"twitter:image:width\",\"content\":\"1200\"}],[\"$\",\"meta\",\"12\",{\"name\":\"twitter:image:height\",\"content\":\"1200\"}],[\"$\",\"meta\",\"13\",{\"name\":\"twitter:image\",\"content\":\"https://prometheus.io/twitter-image.png?b370f6418ef38b42\"}],[\"$\",\"link\",\"14\",{\"rel\":\"icon\",\"href\":\"/icon.svg?7aa022e51797bcef\",\"type\":\"image/svg+xml\",\"sizes\":\"any\"}],[\"$\",\"$L2a\",\"15\",{}]],\"error\":null,\"digest\":\"$undefined\"}\n"])self.\_\_next\_f.push([1,"29:\"$24:metadata\"\n"])self.\_\_next\_f.push([1,"2b:I[74264,[\"545\",\"static/chunks/c16f53c3-e2edfe54eba3117f.js\",\"341\",\"static/chunks/341-0544a5ed99d6b02e.js\",\"619\",\"static/chunks/619-f072ac750404f9da.js\",\"582\",\"static/chunks/app/docs/%5B...slug%5D/page-1b753d14db7f06db.js\"],\"Title\"]\n2d:I[71165,[\"545\",\"static/chunks/c16f53c3-e2edfe54eba3117f.js\",\"341\",\"static/chunks/341-0544a5ed99d6b02e.js\",\"619\",\"static/chunks/619-f072ac750404f9da.js\",\"582\",\"static/chunks/app/docs/%5B...slug%5D/page-1b753d14db7f06db.js\"],\"Divider\"]\n2e:I[52619,[\"545\",\"static/chunks/c16f53c3-e2edfe54eba3117f.js\",\"341\",\"static/chunks/341-0544a5ed99d6b02e.js\",\"619\",\"static/chunks/619-f072ac750404f9da.js\",\"582\",\"static/chunks/app/docs/%5B...slug%5D/page-1b753d14db7f06db.js\"],\"\"]\n2f:I[2369,[\"545\",\"static/chunks/c16f53c3-e2edfe54eba3117f.js\",\"341\",\"static/chunks/341-0544a5ed99d6b02e.js\",\"619\",\"static/chunks/619-f072ac750404f9da.js\",\"582\",\"static/chunks/app/docs/%5B...slug%5D/page-1b753d14db7f06db.js\"],\"Stack\"]\n"])self.\_\_next\_f.push([1,"20:[null,[\"$\",\"div\",null,{\"data-pagefind-body\":\"true\",\"data-pagefind-meta\":\"breadcrumbs:Prometheus Server \u003e Querying \u003e Basics\",\"children\":[[\"$\",\"$L2b\",null,{\"order\":1,\"children\":\"Querying basics\"}],\"$L2c\"]}],[\"$\",\"$L2d\",null,{\"my\":\"xl\"}],[\"$\",\"$Lb\",null,{\"component\":\"nav\",\"aria-label\":\"pagination\",\"justify\":\"space-between\",\"mt\":\"xl\",\"wrap\":\"nowrap\",\"gap\":\"xs\",\"children\":[[\"$\",\"$L1c\",null,{\"flex\":\"0 1 40%\",\"maw\":\"40%\",\"children\":[\"$\",\"$L11\",null,{\"w\":\"100%\",\"component\":\"$2e\",\"href\":\"/docs/prometheus/latest/prometheus\_agent/\",\"variant\":\"outline\",\"color\":\"var(--mantine-color-text)\",\"justify\":\"space-between\",\"h\":80,\"leftSection\":[\"$\",\"svg\",null,{\"ref\":\"$undefined\",\"xmlns\":\"http://www.w3.org/2000/svg\",\"width\":24,\"height\":24,\"viewBox\":\"0 0 24 24\",\"fill\":\"none\",\"stroke\":\"currentColor\",\"strokeWidth\":1.5,\"strokeLinecap\":\"round\",\"strokeLinejoin\":\"round\",\"className\":\"tabler-icon tabler-icon-arrow-left \",\"children\":[\"$undefined\",[\"$\",\"path\",\"svg-0\",{\"d\":\"M5 12l14 0\"}],[\"$\",\"path\",\"svg-1\",{\"d\":\"M5 12l6 6\"}],[\"$\",\"path\",\"svg-2\",{\"d\":\"M5 12l6 -6\"}],\"$undefined\"]}],\"ta\":\"right\",\"bd\":\"1px solid var(--mantine-color-gray-5)\",\"children\":[\"$\",\"$L2f\",null,{\"align\":\"flex-end\",\"gap\":5,\"children\":[[\"$\",\"$Lc\",null,{\"size\":\"sm\",\"fw\":700,\"children\":\"Previous\"}],[\"$\",\"$Lc\",null,{\"size\":\"sm\",\"style\":{\"whiteSpace\":\"normal\"},\"children\":\"Agent Mode\"}]]}]}]}],[\"$\",\"$Lb\",null,{\"gap\":\"xs\",\"wrap\":\"nowrap\",\"children\":[[\"$\",\"$L11\",null,{\"component\":\"a\",\"href\":\"https://github.com/prometheus/prometheus/blob/main/docs/querying/basics.md\",\"target\":\"\_blank\",\"variant\":\"subtle\",\"color\":\"var(--mantine-color-text)\",\"h\":80,\"leftSection\":[\"$\",\"svg\",null,{\"ref\":\"$undefined\",\"xmlns\":\"http://www.w3.org/2000/svg\",\"width\":18,\"height\":18,\"viewBox\":\"0 0 24 24\",\"fill\":\"none\",\"stroke\":\"currentColor\",\"strokeWidth\":1.5,\"strokeLinecap\":\"round\",\"strokeLinejoin\":\"round\",\"className\":\"tabler-icon tabler-icon-pencil \",\"children\":[\"$undefined\",[\"$\",\"path\",\"svg-0\",{\"d\":\"M4 20h4l10.5 -10.5a2.828 2.828 0 1 0 -4 -4l-10.5 10.5v4\"}],[\"$\",\"path\",\"svg-1\",{\"d\":\"M13.5 6.5l4 4\"}],\"$undefined\"]}],\"fw\":\"normal\",\"visibleFrom\":\"xs\",\"children\":[[\"$\",\"$Lc\",null,{\"inherit\":true,\"hiddenFrom\":\"md\",\"children\":\"Edit\"}],[\"$\",\"$Lc\",null,{\"inherit\":true,\"visibleFrom\":\"md\",\"children\":\"Edit this page\"}]]}],[\"$\",\"$L11\",null,{\"component\":\"a\",\"href\":\"https://github.com/prometheus/prometheus/issues/new?title=docs%3A%20Issue%20with%20%22Querying%20basics%22\u0026body=\*\*Page%3A\*\*%20https%3A%2F%2Fprometheus.io%2Fdocs%2Fprometheus%2Flatest%2Fquerying%2Fbasics%2F%0A%0A\*\*Describe%20the%20issue%3A\*\*%0A%0A\",\"target\":\"\_blank\",\"variant\":\"subtle\",\"color\":\"var(--mantine-color-text)\",\"h\":80,\"leftSection\":[\"$\",\"svg\",null,{\"ref\":\"$undefined\",\"xmlns\":\"http://www.w3.org/2000/svg\",\"width\":18,\"height\":18,\"viewBox\":\"0 0 24 24\",\"fill\":\"none\",\"stroke\":\"currentColor\",\"strokeWidth\":1.5,\"strokeLinecap\":\"round\",\"strokeLinejoin\":\"round\",\"className\":\"tabler-icon tabler-icon-bug \",\"children\":[\"$undefined\",[\"$\",\"path\",\"svg-0\",{\"d\":\"M9 9v-1a3 3 0 0 1 6 0v1\"}],[\"$\",\"path\",\"svg-1\",{\"d\":\"M8 9h8a6 6 0 0 1 1 3v3a5 5 0 0 1 -10 0v-3a6 6 0 0 1 1 -3\"}],[\"$\",\"path\",\"svg-2\",{\"d\":\"M3 13l4 0\"}],[\"$\",\"path\",\"svg-3\",{\"d\":\"M17 13l4 0\"}],[\"$\",\"path\",\"svg-4\",{\"d\":\"M12 20l0 -6\"}],[\"$\",\"path\",\"svg-5\",{\"d\":\"M4 19l3.35 -2\"}],[\"$\",\"path\",\"svg-6\",{\"d\":\"M20 19l-3.35 -2\"}],[\"$\",\"path\",\"svg-7\",{\"d\":\"M4 7l3.75 2.4\"}],[\"$\",\"path\",\"svg-8\",{\"d\":\"M20 7l-3.75 2.4\"}],\"$undefined\"]}],\"fw\":\"normal\",\"visibleFrom\":\"xs\",\"children\":[[\"$\",\"$Lc\",null,{\"inherit\":true,\"hiddenFrom\":\"md\",\"children\":\"Issue\"}],[\"$\",\"$Lc\",null,{\"inherit\":true,\"visibleFrom\":\"md\",\"children\":\"Report an issue\"}]]}]]}],[\"$\",\"$L1c\",null,{\"flex\":\"0 1 40%\",\"maw\":\"40%\",\"ta\":\"right\",\"children\":[\"$\",\"$L11\",null,{\"w\":\"100%\",\"component\":\"$2e\",\"href\":\"/docs/prometheus/latest/querying/operators/\",\"variant\":\"outline\",\"color\":\"var(--mantine-color-text)\",\"justify\":\"space-between\",\"h\":80,\"rightSection\":[\"$\",\"svg\",null,{\"ref\":\"$undefined\",\"xmlns\":\"http://www.w3.org/2000/svg\",\"width\":24,\"height\":24,\"viewBox\":\"0 0 24 24\",\"fill\":\"none\",\"stroke\":\"currentColor\",\"strokeWidth\":1.5,\"strokeLinecap\":\"round\",\"strokeLinejoin\":\"round\",\"className\":\"tabler-icon tabler-icon-arrow-right \",\"children\":[\"$undefined\",[\"$\",\"path\",\"svg-0\",{\"d\":\"M5 12l14 0\"}],[\"$\",\"path\",\"svg-1\",{\"d\":\"M13 18l6 -6\"}],[\"$\",\"path\",\"svg-2\",{\"d\":\"M13 6l6 6\"}],\"$undefined\"]}],\"ta\":\"left\",\"bd\":\"1px solid var(--mantine-color-gray-5)\",\"children\":[\"$\",\"$L2f\",null,{\"gap\":5,\"children\":[[\"$\",\"$Lc\",null,{\"size\":\"sm\",\"fw\":700,\"children\":\"Next\"}],[\"$\",\"$Lc\",null,{\"size\":\"sm\",\"style\":{\"whiteSpace\":\"normal\"},\"children\":\"Operators\"}]]}]}]}]]}]]\n"])self.\_\_next\_f.push([1,"2c:[\"$\",\"div\",null,{\"className\":\"markdown-content\",\"children\":\"$L30\"}]\n"])self.\_\_next\_f.push([1,"30:[[\"$\",\"p\",\"p-0\",{\"children\":\"Prometheus provides a functional query language called PromQL (Prometheus Query\\nLanguage) that lets the user select and aggregate time series data in real\\ntime.\"}],\"\\n\",[\"$\",\"p\",\"p-1\",{\"children\":[\"When you send a query request to Prometheus, it can be an \",[\"$\",\"em\",\"em-0\",{\"children\":\"instant query\"}],\", evaluated at one point in time,\\nor a \",[\"$\",\"em\",\"em-1\",{\"children\":\"range query\"}],\" at equally-spaced steps between a start and an end time. PromQL works exactly the same\\nin each case; the range query is just like an instant query run multiple times at different timestamps.\"]}],\"\\n\",[\"$\",\"p\",\"p-2\",{\"children\":\"In the Prometheus UI, the \\\"Table\\\" tab is for instant queries and the \\\"Graph\\\" tab is for range queries.\"}],\"\\n\",[\"$\",\"p\",\"p-3\",{\"children\":[\"Other programs can fetch the result of a PromQL expression via the \",[\"$\",\"$Ld\",\"a-0\",{\"inherit\":true,\"c\":\"var(--secondary-link-color)\",\"component\":\"$2e\",\"href\":\"/docs/prometheus/latest/querying/api\",\"children\":\"HTTP API\"}],\".\"]}],\"\\n\",[\"$\",\"$L2b\",\"h2-0\",{\"order\":2,\"id\":\"examples\",\"children\":[\"Examples\",[\"$\",\"a\",\"a-0\",{\"className\":\"header-auto-link\",\"href\":\"#examples\",\"children\":[\"$\",\"svg\",null,{\"ref\":\"$undefined\",\"xmlns\":\"http://www.w3.org/2000/svg\",\"width\":\"0.875em\",\"height\":\"0.875em\",\"viewBox\":\"0 0 24 24\",\"fill\":\"none\",\"stroke\":\"currentColor\",\"strokeWidth\":2,\"strokeLinecap\":\"round\",\"strokeLinejoin\":\"round\",\"className\":\"tabler-icon tabler-icon-link \",\"children\":[\"$undefined\",[\"$\",\"path\",\"svg-0\",{\"d\":\"M9 15l6 -6\"}],[\"$\",\"path\",\"svg-1\",{\"d\":\"M11 6l.463 -.536a5 5 0 0 1 7.071 7.072l-.534 .464\"}],[\"$\",\"path\",\"svg-2\",{\"d\":\"M13 18l-.397 .534a5.068 5.068 0 0 1 -7.127 0a4.972 4.972 0 0 1 0 -7.071l.524 -.463\"}],\"$undefined\"]}]}]]}],\"\\n\",[\"$\",\"p\",\"p-4\",{\"children\":[\"This document is a Prometheus basic language reference. For learning, it may be easier to\\nstart with a couple of \",[\"$\",\"$Ld\",\"a-0\",{\"inherit\":true,\"c\":\"var(--secondary-link-color)\",\"component\":\"$2e\",\"href\":\"/docs/prometheus/latest/querying/examples\",\"children\":\"examples\"}],\".\"]}],\"\\n\",[\"$\",\"$L2b\",\"h2-1\",{\"order\":2,\"id\":\"samples\",\"children\":[\"Samples\",[\"$\",\"a\",\"a-0\",{\"className\":\"header-auto-link\",\"href\":\"#samples\",\"children\":[\"$\",\"svg\",null,{\"ref\":\"$undefined\",\"xmlns\":\"http://www.w3.org/2000/svg\",\"width\":\"0.875em\",\"height\":\"0.875em\",\"viewBox\":\"0 0 24 24\",\"fill\":\"none\",\"stroke\":\"currentColor\",\"strokeWidth\":2,\"strokeLinecap\":\"round\",\"strokeLinejoin\":\"round\",\"className\":\"tabler-icon tabler-icon-link \",\"children\":[\"$undefined\",[\"$\",\"path\",\"svg-0\",{\"d\":\"M9 15l6 -6\"}],[\"$\",\"path\",\"svg-1\",{\"d\":\"M11 6l.463 -.536a5 5 0 0 1 7.071 7.072l-.534 .464\"}],[\"$\",\"path\",\"svg-2\",{\"d\":\"M13 18l-.397 .534a5.068 5.068 0 0 1 -7.127 0a4.972 4.972 0 0 1 0 -7.071l.524 -.463\"}],\"$undefined\"]}]}]]}],\"\\n\",[\"$\",\"p\",\"p-5\",{\"children\":[\"The value of a sample at a given timestamp returned by PromQL may be a float or\\na \",[\"$\",\"$Ld\",\"a-0\",{\"inherit\":true,\"c\":\"var(--secondary-link-color)\",\"component\":\"$2e\",\"href\":\"/docs/specs/native\_histograms\",\"children\":\"native histogram\"}],\". A\\nfloat sample is a simple floating point number, whereas a native histograms\\nsample contains a full histogram including count, sum, and buckets.\"]}],\"\\n\",[\"$\",\"p\",\"p-6\",{\"children\":[\"Note that the term “histogram sample” in the PromQL documentation always refers\\nto a native histogram. The term \\\"classic histogram\\\" refers to a set of time\\nseries containing float samples with the \",[\"$\",\"code\",\"code-0\",{\"children\":\"\_bucket\"}],\", \",[\"$\",\"code\",\"code-1\",{\"children\":\"\_count\"}],\", and \",[\"$\",\"code\",\"code-2\",{\"children\":\"\_sum\"}],\"\\nsuffixes that together describe a histogram. From the perspective of PromQL,\\nthese contain just float samples, there are no “classic histogram samples”.\"]}],\"\\n\",[\"$\",\"p\",\"p-7\",{\"children\":[\"Both float samples and histogram samples can have a counter or a gauge “flavor”.\\nFloat samples with a counter or gauge flavor are generally simply called\\n“counters” or “gauges”, respectively, while their histogram counterparts are\\ncalled “counter histograms” or “gauge histograms”. Float samples do not store\\ntheir flavor, leaving it to the user to take their flavor into account when\\nwriting PromQL queries. (By convention, time series containing float counters\\nhave a name ending on \",\"$L31\",\" to help with the distinction.)\"]}],\"\\n\",\"$L32\",\"\\n\",\"$L33\",\"\\n\",\"$L34\",\"\\n\",\"$L35\",\"\\n\",\"$L36\",\"\\n\",\"$L37\",\"\\n\",\"$L38\",\"\\n\",\"$L39\",\"\\n\",\"$L3a\",\"\\n\",\"$L3b\",\"\\n\",\"$L3c\",\"\\n\",\"$L3d\",\"\\n\",\"$L3e\",\"\\n\",\"$L3f\",\"\\n\",\"$L40\",\"\\n\",\"$L41\",\"\\n\",\"$L42\",\"\\n\",\"$L43\",\"\\n\",\"$L44\",\"\\n\",\"$L45\",\"\\n\",\"$L46\",\"\\n\",\"$L47\",\"\\n\",\"$L48\",\"\\n\",\"$L49\",\"\\n\",\"$L4a\",\"\\n\",\"$L4b\",\"\\n\",\"$L4c\",\"\\n\",\"$L4d\",\"\\n\",\"$L4e\",\"\\n\",\"$L4f\",\"\\n\",\"$L50\",\"\\n\",\"$L51\",\"\\n\",\"$L52\",\"\\n\",\"$L53\",\"\\n\",\"$L54\",\"\\n\",\"$L55\",\"\\n\",\"$L56\",\"\\n\",\"$L57\",\"\\n\",\"$L58\",\"\\n\",\"$L59\",\"\\n\",\"$L5a\",\"\\n\",\"$L5b\",\"\\n\",\"$L5c\",\"\\n\",\"$L5d\",\"\\n\",\"$L5e\",\"\\n\",\"$L5f\",\"\\n\",\"$L60\",\"\\n\",\"$L61\",\"\\n\",\"$L62\",\"\\n\",\"$L63\",\"\\n\",\"$L64\",\"\\n\",\"$L65\",\"\\n\",\"$L66\",\"\\n\",\"$L67\",\"\\n\",\"$L68\",\"\\n\",\"$L69\",\"\\n\",\"$L6a\",\"\\n\",\"$L6b\",\"\\n\",\"$L6c\",\"\\n\",\"$L6d\",\"\\n\",\"$L6e\",\"\\n\",\"$L6f\",\"\\n\",\"$L70\",\"\\n\",\"$L71\",\"\\n\",\"$L72\",\"\\n\",\"$L73\",\"\\n\",\"$L74\",\"\\n\",\"$L75\",\"\\n\",\"$L76\",\"\\n\",\"$L77\",\"\\n\",\"$L78\",\"\\n\",\"$L79\",\"\\n\",\"$L7a\",\"\\n\",\"$L7b\",\"\\n\",\"$L7c\",\"\\n\",\"$L7d\",\"\\n\",\"$L7e\",\"\\n\",\"$L7f\",\"\\n\",\"$L80\",\"\\n\",\"$L81\",\"\\n\",\"$L82\",\"\\n\",\"$L83\",\"\\n\",\"$L84\",\"\\n\",\"$L85\",\"\\n\",\"$L86\",\"\\n\",\"$L87\",\"\\n\",\"$L88\",\"\\n\",\"$L89\",\"\\n\",\"$L8a\",\"\\n\",\"$L8b\",\"\\n\",\"$L8c\",\"\\n\",\"$L8d\",\"\\n\",\"$L8e\",\"\\n\",\"$L8f\",\"\\n\",\"$L90\",\"\\n\",\"$L91\",\"\\n\",\"$L92\",\"\\n\",\"$L93\",\"\\n\",\"$L94\",\"\\n\",\"$L95\",\"\\n\",\"$L96\",\"\\n\",\"$L97\",\"\\n\",\"$L98\",\"\\n\",\"$L99\",\"\\n\",\"$L9a\",\"\\n\",\"$L9b\",\"\\n\",\"$L9c\",\"\\n\",\"$L9d\",\"\\n\",\"$L9e\",\"\\n\",\"$L9f\",\"\\n\",\"$La0\",\"\\n\",\"$La1\",\"\\n\",\"$La2\",\"\\n\",\"$La3\",\"\\n\",\"$La4\",\"\\n\",\"$La5\",\"\\n\",\"$La6\",\"\\n\",\"$La7\",\"\\n\",\"$La8\",\"\\n\",\"$La9\",\"\\n\",\"$Laa\",\"\\n\",\"$Lab\",\"\\n\",\"$Lac\",\"\\n\",\"$Lad\",\"\\n\",\"$Lae\",\"\\n\",\"$Laf\",\"\\n\",\"$Lb0\",\"\\n\",\"$Lb1\",\"\\n\",\"$Lb2\",\"\\n\",\"$Lb3\",\"\\n\",\"$Lb4\"]\n"])self.\_\_next\_f.push([1,"31:[\"$\",\"code\",\"code-0\",{\"children\":\"\_total\"}]\n32:[\"$\",\"p\",\"p-8\",{\"children\":[\"Since histogram samples “know” their counter or gauge flavor, this allows\\nreliable warnings about mismatched operations. For example, applying the \",[\"$\",\"code\",\"code-0\",{\"children\":\"rate\"}],\"\\nfunction to gauge floats will most likely produce a\\nnonsensical result, but the query will be processed without complains. However,\\nif applied to gauge histograms, the result of the query will be\\nannotated with a warning.\"]}]\n"])self.\_\_next\_f.push([1,"33:[\"$\",\"$L2b\",\"h2-2\",{\"order\":2,\"id\":\"expression-language-data-types\",\"children\":[\"Expression language data types\",[\"$\",\"a\",\"a-0\",{\"className\":\"header-auto-link\",\"href\":\"#expression-language-data-types\",\"children\":[\"$\",\"svg\",null,{\"ref\":\"$undefined\",\"xmlns\":\"http://www.w3.org/2000/svg\",\"width\":\"0.875em\",\"height\":\"0.875em\",\"viewBox\":\"0 0 24 24\",\"fill\":\"none\",\"stroke\":\"currentColor\",\"strokeWidth\":2,\"strokeLinecap\":\"round\",\"strokeLinejoin\":\"round\",\"className\":\"tabler-icon tabler-icon-link \",\"children\":[\"$undefined\",[\"$\",\"path\",\"svg-0\",{\"d\":\"M9 15l6 -6\"}],[\"$\",\"path\",\"svg-1\",{\"d\":\"M11 6l.463 -.536a5 5 0 0 1 7.071 7.072l-.534 .464\"}],[\"$\",\"path\",\"svg-2\",{\"d\":\"M13 18l-.397 .534a5.068 5.068 0 0 1 -7.127 0a4.972 4.972 0 0 1 0 -7.071l.524 -.463\"}],\"$undefined\"]}]}]]}]\n"])self.\_\_next\_f.push([1,"34:[\"$\",\"p\",\"p-9\",{\"children\":\"In Prometheus's expression language, an expression or sub-expression can\\nevaluate to one of four types:\"}]\n"])self.\_\_next\_f.push([1,"35:[\"$\",\"ul\",\"ul-0\",{\"children\":[\"\\n\",[\"$\",\"li\",\"li-0\",{\"children\":[[\"$\",\"strong\",\"strong-0\",{\"children\":\"Instant vector\"}],\" - a set of time series containing a single sample for each time series, all sharing the same timestamp\"]}],\"\\n\",[\"$\",\"li\",\"li-1\",{\"children\":[[\"$\",\"strong\",\"strong-0\",{\"children\":\"Range vector\"}],\" - a set of time series containing a range of data points over time for each time series\"]}],\"\\n\",[\"$\",\"li\",\"li-2\",{\"children\":[[\"$\",\"strong\",\"strong-0\",{\"children\":\"Scalar\"}],\" - a simple numeric floating point value\"]}],\"\\n\",[\"$\",\"li\",\"li-3\",{\"children\":[[\"$\",\"strong\",\"strong-0\",{\"children\":\"String\"}],\" - a simple string value; currently unused\"]}],\"\\n\"]}]\n"])self.\_\_next\_f.push([1,"36:[\"$\",\"p\",\"p-10\",{\"children\":[\"Depending on the use case (e.g. when graphing vs. displaying the output of an\\nexpression), only some of these types are legal as the result of a\\nuser-specified expression.\\nFor \",[\"$\",\"$Ld\",\"a-0\",{\"inherit\":true,\"c\":\"var(--secondary-link-color)\",\"component\":\"$2e\",\"href\":\"/docs/prometheus/latest/querying/api#instant-queries\",\"children\":\"instant queries\"}],\", any of the above data types are allowed as the root of the expression.\\n\",[\"$\",\"$Ld\",\"a-1\",{\"inherit\":true,\"c\":\"var(--secondary-link-color)\",\"component\":\"$2e\",\"href\":\"/docs/prometheus/latest/querying/api#range-queries\",\"children\":\"Range queries\"}],\" only support scalar-typed and instant-vector-typed expressions.\"]}]\n"])self.\_\_next\_f.push([1,"37:[\"$\",\"p\",\"p-11\",{\"children\":\"Both vectors and time series may contain a mix of float samples and histogram\\nsamples.\"}]\n"])self.\_\_next\_f.push([1,"38:[\"$\",\"$L2b\",\"h2-3\",{\"order\":2,\"id\":\"reconciliation-of-histogram-bucket-layouts\",\"children\":[\"Reconciliation of histogram bucket layouts\",[\"$\",\"a\",\"a-0\",{\"className\":\"header-auto-link\",\"href\":\"#reconciliation-of-histogram-bucket-layouts\",\"children\":[\"$\",\"svg\",null,{\"ref\":\"$undefined\",\"xmlns\":\"http://www.w3.org/2000/svg\",\"width\":\"0.875em\",\"height\":\"0.875em\",\"viewBox\":\"0 0 24 24\",\"fill\":\"none\",\"stroke\":\"currentColor\",\"strokeWidth\":2,\"strokeLinecap\":\"round\",\"strokeLinejoin\":\"round\",\"className\":\"tabler-icon tabler-icon-link \",\"children\":[\"$undefined\",[\"$\",\"path\",\"svg-0\",{\"d\":\"M9 15l6 -6\"}],[\"$\",\"path\",\"svg-1\",{\"d\":\"M11 6l.463 -.536a5 5 0 0 1 7.071 7.072l-.534 .464\"}],[\"$\",\"path\",\"svg-2\",{\"d\":\"M13 18l-.397 .534a5.068 5.068 0 0 1 -7.127 0a4.972 4.972 0 0 1 0 -7.071l.524 -.463\"}],\"$undefined\"]}]}]]}]\n"])self.\_\_next\_f.push([1,"39:[\"$\",\"p\",\"p-12\",{\"children\":\"Native histograms can have different bucket layouts, but they are generally\\nconvertible to compatible versions to apply binary and aggregation operations\\nto them. Functions acting on range vectors that are applicable to native\\nhistograms also perform such reconciliation. In binary operations this\\nreconciliation is performed pairwise, in aggregation operations and functions\\nall histogram samples are reconciled to one compatible bucket layout.\"}]\n3a:[\"$\",\"p\",\"p-13\",{\"children\":[\"Not all bucket layouts can be reconciled, if incompatible histograms are\\nencountered in an operation, the corresponding output vector element is removed\\nfrom the result, flagged with a warn-level annotation.\\nMore details can be found in the\\n\",[\"$\",\"$Ld\",\"a-0\",{\"inherit\":true,\"c\":\"var(--secondary-link-color)\",\"component\":\"$2e\",\"href\":\"/docs/specs/native\_histograms/#compatibility-between-histograms\",\"children\":\"native histogram specification\"}],\".\"]}]\n"])self.\_\_next\_f.push([1,"3b:[\"$\",\"$L2b\",\"h2-4\",{\"order\":2,\"id\":\"literals\",\"children\":[\"Literals\",[\"$\",\"a\",\"a-0\",{\"className\":\"header-auto-link\",\"href\":\"#literals\",\"children\":[\"$\",\"svg\",null,{\"ref\":\"$undefined\",\"xmlns\":\"http://www.w3.org/2000/svg\",\"width\":\"0.875em\",\"height\":\"0.875em\",\"viewBox\":\"0 0 24 24\",\"fill\":\"none\",\"stroke\":\"currentColor\",\"strokeWidth\":2,\"strokeLinecap\":\"round\",\"strokeLinejoin\":\"round\",\"className\":\"tabler-icon tabler-icon-link \",\"children\":[\"$undefined\",[\"$\",\"path\",\"svg-0\",{\"d\":\"M9 15l6 -6\"}],[\"$\",\"path\",\"svg-1\",{\"d\":\"M11 6l.463 -.536a5 5 0 0 1 7.071 7.072l-.534 .464\"}],[\"$\",\"path\",\"svg-2\",{\"d\":\"M13 18l-.397 .534a5.068 5.068 0 0 1 -7.127 0a4.972 4.972 0 0 1 0 -7.071l.524 -.463\"}],\"$undefined\"]}]}]]}]\n"])self.\_\_next\_f.push([1,"3c:[\"$\",\"p\",\"p-14\",{\"children\":\"The following section describes literal values of various kinds.\\nNote that there is no “histogram literal”.\"}]\n"])self.\_\_next\_f.push([1,"3d:[\"$\",\"$L2b\",\"h3-0\",{\"order\":3,\"id\":\"string-literals\",\"children\":[\"String literals\",[\"$\",\"a\",\"a-0\",{\"className\":\"header-auto-link\",\"href\":\"#string-literals\",\"children\":[\"$\",\"svg\",null,{\"ref\":\"$undefined\",\"xmlns\":\"http://www.w3.org/2000/svg\",\"width\":\"0.875em\",\"height\":\"0.875em\",\"viewBox\":\"0 0 24 24\",\"fill\":\"none\",\"stroke\":\"currentColor\",\"strokeWidth\":2,\"strokeLinecap\":\"round\",\"strokeLinejoin\":\"round\",\"className\":\"tabler-icon tabler-icon-link \",\"children\":[\"$undefined\",[\"$\",\"path\",\"svg-0\",{\"d\":\"M9 15l6 -6\"}],[\"$\",\"path\",\"svg-1\",{\"d\":\"M11 6l.463 -.536a5 5 0 0 1 7.071 7.072l-.534 .464\"}],[\"$\",\"path\",\"svg-2\",{\"d\":\"M13 18l-.397 .534a5.068 5.068 0 0 1 -7.127 0a4.972 4.972 0 0 1 0 -7.071l.524 -.463\"}],\"$undefined\"]}]}]]}]\n"])self.\_\_next\_f.push([1,"3e:[\"$\",\"p\",\"p-15\",{\"children\":\"String literals are designated by single quotes, double quotes or backticks.\"}]\n"])self.\_\_next\_f.push([1,"3f:[\"$\",\"p\",\"p-16\",{\"children\":[\"PromQL follows the same \",[\"$\",\"$Ld\",\"a-0\",{\"inherit\":true,\"c\":\"var(--secondary-link-color)\",\"href\":\"https://golang.org/ref/spec#String\_literals\",\"target\":\"\_blank\",\"rel\":\"noopener\",\"children\":[\"$\",\"span\",null,{\"children\":[\"escaping rules as\\nGo\",\" \",[\"$\",\"svg\",null,{\"ref\":\"$undefined\",\"xmlns\":\"http://www.w3.org/2000/svg\",\"width\":\"0.9em\",\"height\":\"0.9em\",\"viewBox\":\"0 0 24 24\",\"fill\":\"none\",\"stroke\":\"currentColor\",\"strokeWidth\":2,\"strokeLinecap\":\"round\",\"strokeLinejoin\":\"round\",\"className\":\"tabler-icon tabler-icon-external-link \",\"style\":{\"marginBottom\":-1.5},\"children\":[\"$undefined\",[\"$\",\"path\",\"svg-0\",{\"d\":\"M12 6h-6a2 2 0 0 0 -2 2v10a2 2 0 0 0 2 2h10a2 2 0 0 0 2 -2v-6\"}],[\"$\",\"path\",\"svg-1\",{\"d\":\"M11 13l9 -9\"}],[\"$\",\"path\",\"svg-2\",{\"d\":\"M15 4h5v5\"}],\"$undefined\"]}]]}]}],\". For string literals in single or double quotes, a\\nbackslash begins an escape sequence, which may be followed by \",[\"$\",\"code\",\"code-0\",{\"children\":\"a\"}],\", \",[\"$\",\"code\",\"code-1\",{\"children\":\"b\"}],\", \",[\"$\",\"code\",\"code-2\",{\"children\":\"f\"}],\",\\n\",[\"$\",\"code\",\"code-3\",{\"children\":\"n\"}],\", \",[\"$\",\"code\",\"code-4\",{\"children\":\"r\"}],\", \",[\"$\",\"code\",\"code-5\",{\"children\":\"t\"}],\", \",[\"$\",\"code\",\"code-6\",{\"children\":\"v\"}],\" or \",[\"$\",\"code\",\"code-7\",{\"children\":\"\\\\\"}],\". Specific characters can be provided using octal\\n(\",[\"$\",\"code\",\"code-8\",{\"children\":\"\\\\nnn\"}],\") or hexadecimal (\",[\"$\",\"code\",\"code-9\",{\"children\":\"\\\\xnn\"}],\", \",[\"$\",\"code\",\"code-10\",{\"children\":\"\\\\unnnn\"}],\" and \",[\"$\",\"code\",\"code-11\",{\"children\":\"\\\\Unnnnnnnn\"}],\") notations.\"]}]\n"])self.\_\_next\_f.push([1,"40:[\"$\",\"p\",\"p-17\",{\"children\":\"Conversely, escape characters are not parsed in string literals designated by backticks. It is important to note that, unlike Go, Prometheus does not discard newlines inside backticks.\"}]\n41:[\"$\",\"p\",\"p-18\",{\"children\":\"Example:\"}]\n42:[\"$\",\"pre\",\"pre-0\",{\"style\":{\"fontSize\":14,\"backgroundColor\":\"light-dark(var(--mantine-color-gray-0), var(--mantine-color-dark-6))\",\"lineHeight\":1.7,\"display\":\"block\",\"padding\":\"1em\",\"borderRadius\":\"0.5em\",\"overflow\":\"auto\"},\"children\":[\"$\",\"code\",\"code-0\",{\"children\":\"\\\"this is a string\\\"\\n'these are unescaped: \\\\n \\\\\\\\ \\\\t'\\n`these are not unescaped: \\\\n ' \\\" \\\\t`\\n\"}]}]\n"])self.\_\_next\_f.push([1,"43:[\"$\",\"$L2b\",\"h3-1\",{\"order\":3,\"id\":\"float-literals-and-time-durations\",\"children\":[\"Float literals and time durations\",[\"$\",\"a\",\"a-0\",{\"className\":\"header-auto-link\",\"href\":\"#float-literals-and-time-durations\",\"children\":[\"$\",\"svg\",null,{\"ref\":\"$undefined\",\"xmlns\":\"http://www.w3.org/2000/svg\",\"width\":\"0.875em\",\"height\":\"0.875em\",\"viewBox\":\"0 0 24 24\",\"fill\":\"none\",\"stroke\":\"currentColor\",\"strokeWidth\":2,\"strokeLinecap\":\"round\",\"strokeLinejoin\":\"round\",\"className\":\"tabler-icon tabler-icon-link \",\"children\":[\"$undefined\",[\"$\",\"path\",\"svg-0\",{\"d\":\"M9 15l6 -6\"}],[\"$\",\"path\",\"svg-1\",{\"d\":\"M11 6l.463 -.536a5 5 0 0 1 7.071 7.072l-.534 .464\"}],[\"$\",\"path\",\"svg-2\",{\"d\":\"M13 18l-.397 .534a5.068 5.068 0 0 1 -7.127 0a4.972 4.972 0 0 1 0 -7.071l.524 -.463\"}],\"$undefined\"]}]}]]}]\n"])self.\_\_next\_f.push([1,"44:[\"$\",\"p\",\"p-19\",{\"children\":\"Scalar float values can be written as literal integer or floating-point numbers\\nin the format (whitespace only included for better readability):\"}]\n45:[\"$\",\"pre\",\"pre-1\",{\"style\":{\"fontSize\":14,\"backgroundColor\":\"light-dark(var(--mantine-color-gray-0), var(--mantine-color-dark-6))\",\"lineHeight\":1.7,\"display\":\"block\",\"padding\":\"1em\",\"borderRadius\":\"0.5em\",\"overflow\":\"auto\"},\"children\":[\"$\",\"code\",\"code-0\",{\"children\":\"[-+]?(\\n [0-9]\*\\\\.?[0-9]+([eE][-+]?[0-9]+)?\\n | 0[xX][0-9a-fA-F]+\\n | [nN][aA][nN]\\n | [iI][nN][fF]\\n)\\n\"}]}]\n46:[\"$\",\"p\",\"p-20\",{\"children\":\"Examples:\"}]\n47:[\"$\",\"pre\",\"pre-2\",{\"style\":{\"fontSize\":14,\"backgroundColor\":\"light-dark(var(--mantine-color-gray-0), var(--mantine-color-dark-6))\",\"lineHeight\":1.7,\"display\":\"block\",\"padding\":\"1em\",\"borderRadius\":\"0.5em\",\"overflow\":\"auto\"},\"children\":[\"$\",\"code\",\"code-0\",{\"children\":\"23\\n-2.43\\n3.4e-9\\n0x8f\\n-Inf\\nNaN\\n\"}]}]\n48:[\"$\",\"p\",\"p-21\",{\"children\":[\"Additionally, underscores (\",[\"$\",\"code\",\"code-0\",{\"children\":\"\_\"}],\") can be used in between decimal or hexadecimal\\ndigits to improve readability.\"]}]\n49:[\"$\",\"p\",\"p-22\",{\"children\":\"Examples:\"}]\n4a:[\"$\",\"pre\",\"pre-3\",{\"style\":{\"fontSize\":14,\"backgroundColor\":\"light-dark(var(--mantine-color-gray-0), var(--mantine-color-dark-6))\",\"lineHeight\":1.7,\"display\":\"block\",\"padding\":\"1em\",\"borderRadius\":\"0.5em\",\"overflow\":\"auto\"},\"children\":[\"$\",\"code\",\"code-0\",{\"children\":\"1\_000\_000\\n.123\_456\_789\\n0x\_53\_AB\_F3\_82\\n\"}]}]\n4b:[\"$\",\"p\",\"p-23\",{\"children\":\"Float literals are also used to specify durations in seconds. For convenience,\\ndecimal integer numbers may be combined with the following\\ntime units:\"}]\n"])self.\_\_next\_f.push([1,"4c:[\"$\",\"ul\",\"ul-1\",{\"children\":[\"\\n\",[\"$\",\"li\",\"li-0\",{\"children\":[[\"$\",\"code\",\"code-0\",{\"children\":\"ms\"}],\" – milliseconds\"]}],\"\\n\",[\"$\",\"li\",\"li-1\",{\"children\":[[\"$\",\"code\",\"code-0\",{\"children\":\"s\"}],\" – seconds – 1s equals 1000ms\"]}],\"\\n\",[\"$\",\"li\",\"li-2\",{\"children\":[[\"$\",\"code\",\"code-0\",{\"children\":\"m\"}],\" – minutes – 1m equals 60s (ignoring leap seconds)\"]}],\"\\n\",[\"$\",\"li\",\"li-3\",{\"children\":[[\"$\",\"code\",\"code-0\",{\"children\":\"h\"}],\" – hours – 1h equals 60m\"]}],\"\\n\",[\"$\",\"li\",\"li-4\",{\"children\":[[\"$\",\"code\",\"code-0\",{\"children\":\"d\"}],\" – days – 1d equals 24h (ignoring so-called daylight saving time)\"]}],\"\\n\",[\"$\",\"li\",\"li-5\",{\"children\":[[\"$\",\"code\",\"code-0\",{\"children\":\"w\"}],\" – weeks – 1w equals 7d\"]}],\"\\n\",[\"$\",\"li\",\"li-6\",{\"children\":[[\"$\",\"code\",\"code-0\",{\"children\":\"y\"}],\" – years – 1y equals 365d (ignoring leap days)\"]}],\"\\n\"]}]\n"])self.\_\_next\_f.push([1,"4d:[\"$\",\"p\",\"p-24\",{\"children\":\"Suffixing a decimal integer number with one of the units above is a different\\nrepresentation of the equivalent number of seconds as a bare float literal.\"}]\n4e:[\"$\",\"p\",\"p-25\",{\"children\":\"Examples:\"}]\n4f:[\"$\",\"pre\",\"pre-4\",{\"style\":{\"fontSize\":14,\"backgroundColor\":\"light-dark(var(--mantine-color-gray-0), var(--mantine-color-dark-6))\",\"lineHeight\":1.7,\"display\":\"block\",\"padding\":\"1em\",\"borderRadius\":\"0.5em\",\"overflow\":\"auto\"},\"children\":[\"$\",\"code\",\"code-0\",{\"children\":\"1s # Equivalent to 1.\\n2m # Equivalent to 120.\\n1ms # Equivalent to 0.001.\\n-2h # Equivalent to -7200.\\n\"}]}]\n50:[\"$\",\"p\",\"p-26\",{\"children\":[\"The following examples do \",[\"$\",\"em\",\"em-0\",{\"children\":\"not\"}],\" work:\"]}]\n51:[\"$\",\"pre\",\"pre-5\",{\"style\":{\"fontSize\":14,\"backgroundColor\":\"light-dark(var(--mantine-color-gray-0), var(--mantine-color-dark-6))\",\"lineHeight\":1.7,\"display\":\"block\",\"padding\":\"1em\",\"borderRadius\":\"0.5em\",\"overflow\":\"auto\"},\"children\":[\"$\",\"code\",\"code-0\",{\"children\":\"0xABm # No suffixing of hexadecimal numbers.\\n1.5h # Time units cannot be combined with a floating point.\\n+Infd # No suffixing of ±Inf or NaN.\\n\"}]}]\n52:[\"$\",\"p\",\"p-27\",{\"children\":\"Multiple units can be combined by concatenation of suffixed integers. Units\\nmust be ordered from the longest to the shortest. A given unit must only appear\\nonce per float literal.\"}]\n53:[\"$\",\"p\",\"p-28\",{\"children\":\"Examples:\"}]\n54:[\"$\",\"pre\",\"pre-6\",{\"style\":{\"fontSize\":14,\"backgroundColor\":\"light-dark(var(--mantine-color-gray-0), var(--mantine-color-dark-6))\",\"lineHeight\":1.7,\"display\":\"block\",\"padding\":\"1em\",\"borderRadius\":\"0.5em\",\"overflow\":\"auto\"},\"children\":[\"$\",\"code\",\"code-0\",{\"children\":\"1h30m # Equivalent to 5400s and thus 5400.\\n12h34m56s # Equivalent to 45296s and thus 45296.\\n54s321ms # Equivalent to 54.321.\\n\"}]}]\n"])self.\_\_next\_f.push([1,"55:[\"$\",\"$L2b\",\"h2-5\",{\"order\":2,\"id\":\"time-series-selectors\",\"children\":[\"Time series selectors\",[\"$\",\"a\",\"a-0\",{\"className\":\"header-auto-link\",\"href\":\"#time-series-selectors\",\"children\":[\"$\",\"svg\",null,{\"ref\":\"$undefined\",\"xmlns\":\"http://www.w3.org/2000/svg\",\"width\":\"0.875em\",\"height\":\"0.875em\",\"viewBox\":\"0 0 24 24\",\"fill\":\"none\",\"stroke\":\"currentColor\",\"strokeWidth\":2,\"strokeLinecap\":\"round\",\"strokeLinejoin\":\"round\",\"className\":\"tabler-icon tabler-icon-link \",\"children\":[\"$undefined\",[\"$\",\"path\",\"svg-0\",{\"d\":\"M9 15l6 -6\"}],[\"$\",\"path\",\"svg-1\",{\"d\":\"M11 6l.463 -.536a5 5 0 0 1 7.071 7.072l-.534 .464\"}],[\"$\",\"path\",\"svg-2\",{\"d\":\"M13 18l-.397 .534a5.068 5.068 0 0 1 -7.127 0a4.972 4.972 0 0 1 0 -7.071l.524 -.463\"}],\"$undefined\"]}]}]]}]\n"])self.\_\_next\_f.push([1,"56:[\"$\",\"p\",\"p-29\",{\"children\":\"These are the basic building-blocks that instruct PromQL what data to fetch.\"}]\n"])self.\_\_next\_f.push([1,"57:[\"$\",\"$L2b\",\"h3-2\",{\"order\":3,\"id\":\"instant-vector-selectors\",\"children\":[\"Instant vector selectors\",[\"$\",\"a\",\"a-0\",{\"className\":\"header-auto-link\",\"href\":\"#instant-vector-selectors\",\"children\":[\"$\",\"svg\",null,{\"ref\":\"$undefined\",\"xmlns\":\"http://www.w3.org/2000/svg\",\"width\":\"0.875em\",\"height\":\"0.875em\",\"viewBox\":\"0 0 24 24\",\"fill\":\"none\",\"stroke\":\"currentColor\",\"strokeWidth\":2,\"strokeLinecap\":\"round\",\"strokeLinejoin\":\"round\",\"className\":\"tabler-icon tabler-icon-link \",\"children\":[\"$undefined\",[\"$\",\"path\",\"svg-0\",{\"d\":\"M9 15l6 -6\"}],[\"$\",\"path\",\"svg-1\",{\"d\":\"M11 6l.463 -.536a5 5 0 0 1 7.071 7.072l-.534 .464\"}],[\"$\",\"path\",\"svg-2\",{\"d\":\"M13 18l-.397 .534a5.068 5.068 0 0 1 -7.127 0a4.972 4.972 0 0 1 0 -7.071l.524 -.463\"}],\"$undefined\"]}]}]]}]\n"])self.\_\_next\_f.push([1,"58:[\"$\",\"p\",\"p-30\",{\"children\":\"Instant vector selectors allow the selection of a set of time series and a\\nsingle sample value for each at a given timestamp (point in time). In the simplest\\nform, only a metric name is specified, which results in an instant vector\\ncontaining elements for all time series that have this metric name.\"}]\n"])self.\_\_next\_f.push([1,"59:[\"$\",\"p\",\"p-31\",{\"children\":[\"The value returned will be that of the most recent sample at or before the\\nquery's evaluation timestamp (in the case of an\\n\",[\"$\",\"$Ld\",\"a-0\",{\"inherit\":true,\"c\":\"var(--secondary-link-color)\",\"component\":\"$2e\",\"href\":\"/docs/prometheus/latest/querying/api#instant-queries\",\"children\":\"instant query\"}],\")\\nor the current step within the query (in the case of a\\n\",[\"$\",\"$Ld\",\"a-1\",{\"inherit\":true,\"c\":\"var(--secondary-link-color)\",\"component\":\"$2e\",\"href\":\"/docs/prometheus/latest/querying/api#range-queries\",\"children\":\"range query\"}],\").\\nThe \",[\"$\",\"$Ld\",\"a-2\",{\"inherit\":true,\"c\":\"var(--secondary-link-color)\",\"component\":\"$2e\",\"href\":\"#modifier\",\"children\":[[\"$\",\"code\",\"code-0\",{\"children\":\"@\"}],\" modifier\"]}],\" allows overriding the timestamp relative to which\\nthe selection takes place. Time series are only returned if their most recent sample is less than the \",[\"$\",\"$Ld\",\"a-3\",{\"inherit\":true,\"c\":\"var(--secondary-link-color)\",\"component\":\"$2e\",\"href\":\"#staleness\",\"children\":\"lookback period\"}],\" ago.\"]}]\n"])self.\_\_next\_f.push([1,"5a:[\"$\",\"p\",\"p-32\",{\"children\":[\"This example selects all time series that have the \",[\"$\",\"code\",\"code-0\",{\"children\":\"http\_requests\_total\"}],\" metric\\nname, returning the most recent sample for each:\"]}]\n5b:[\"$\",\"pre\",\"pre-7\",{\"style\":{\"fontSize\":14,\"backgroundColor\":\"light-dark(var(--mantine-color-gray-0), var(--mantine-color-dark-6))\",\"lineHeight\":1.7,\"display\":\"block\",\"padding\":\"1em\",\"borderRadius\":\"0.5em\",\"overflow\":\"auto\"},\"children\":[\"$\",\"code\",\"code-0\",{\"children\":\"http\_requests\_total\\n\"}]}]\n5c:[\"$\",\"p\",\"p-33\",{\"children\":[\"It is possible to filter these time series further by appending a comma-separated list of label\\nmatchers in curly braces (\",[\"$\",\"code\",\"code-0\",{\"children\":\"{}\"}],\").\"]}]\n5d:[\"$\",\"p\",\"p-34\",{\"children\":[\"This example selects only those time series with the \",[\"$\",\"code\",\"code-0\",{\"children\":\"http\_requests\_total\"}],\"\\nmetric name that also have the \",[\"$\",\"code\",\"code-1\",{\"children\":\"job\"}],\" label set to \",[\"$\",\"code\",\"code-2\",{\"children\":\"prometheus\"}],\" and their\\n\",[\"$\",\"code\",\"code-3\",{\"children\":\"group\"}],\" label set to \",[\"$\",\"code\",\"code-4\",{\"children\":\"canary\"}],\":\"]}]\n5e:[\"$\",\"pre\",\"pre-8\",{\"style\":{\"fontSize\":14,\"backgroundColor\":\"light-dark(var(--mantine-color-gray-0), var(--mantine-color-dark-6))\",\"lineHeight\":1.7,\"display\":\"block\",\"padding\":\"1em\",\"borderRadius\":\"0.5em\",\"overflow\":\"auto\"},\"children\":[\"$\",\"code\",\"code-0\",{\"children\":\"http\_requests\_total{job=\\\"prometheus\\\",group=\\\"canary\\\"}\\n\"}]}]\n5f:[\"$\",\"p\",\"p-35\",{\"children\":\"It is also possible to negatively match a label value, or to match label values\\nagainst regular expressions. The following label matching operators exist:\"}]\n60:[\"$\",\"ul\",\"ul-2\",{\"children\":[\"\\n\",[\"$\",\"li\",\"li-0\",{\"children\":[[\"$\",\"code\",\"code-0\",{\"children\":\"=\"}],\": Select labels that are exactly equal to the provided string.\"]}],\"\\n\",[\"$\",\"li\",\"li-1\",{\"children\":[[\"$\",\"code\",\"code-0\",{\"children\":\"!=\"}],\": Select labels that are not equal to the provided string.\"]}],\"\\n\",[\"$\",\"li\",\"li-2\",{\"children\":[[\"$\",\"code\",\"code-0\",{\"children\":\"=~\"}],\": Sel"])self.\_\_next\_f.push([1,"ect labels that regex-match the provided string.\"]}],\"\\n\",[\"$\",\"li\",\"li-3\",{\"children\":[[\"$\",\"code\",\"code-0\",{\"children\":\"!~\"}],\": Select labels that do not regex-match the provided string.\"]}],\"\\n\"]}]\n61:[\"$\",\"p\",\"p-36\",{\"children\":[[\"$\",\"$Ld\",\"a-0\",{\"inherit\":true,\"c\":\"var(--secondary-link-color)\",\"component\":\"$2e\",\"href\":\"#regular-expressions\",\"children\":\"Regex\"}],\" matches are fully anchored. A match of \",[\"$\",\"code\",\"code-0\",{\"children\":\"env=~\\\"foo\\\"\"}],\" is treated as \",[\"$\",\"code\",\"code-1\",{\"children\":\"env=~\\\"^foo$\\\"\"}],\".\"]}]\n62:[\"$\",\"p\",\"p-37\",{\"children\":[\"For example, this selects all \",[\"$\",\"code\",\"code-0\",{\"children\":\"http\_requests\_total\"}],\" time series for \",[\"$\",\"code\",\"code-1\",{\"children\":\"staging\"}],\",\\n\",[\"$\",\"code\",\"code-2\",{\"children\":\"testing\"}],\", and \",[\"$\",\"code\",\"code-3\",{\"children\":\"development\"}],\" environments and HTTP methods other than \",[\"$\",\"code\",\"code-4\",{\"children\":\"GET\"}],\".\"]}]\n63:[\"$\",\"pre\",\"pre-9\",{\"style\":{\"fontSize\":14,\"backgroundColor\":\"light-dark(var(--mantine-color-gray-0), var(--mantine-color-dark-6))\",\"lineHeight\":1.7,\"display\":\"block\",\"padding\":\"1em\",\"borderRadius\":\"0.5em\",\"overflow\":\"auto\"},\"children\":[\"$\",\"code\",\"code-0\",{\"children\":\"http\_requests\_total{environment=~\\\"staging|testing|development\\\",method!=\\\"GET\\\"}\\n\"}]}]\n64:[\"$\",\"p\",\"p-38\",{\"children\":\"Label matchers that match empty label values also select all time series that\\ndo not have the specific label set at all. It is possible to have multiple matchers for the same label name.\"}]\n65:[\"$\",\"p\",\"p-39\",{\"children\":\"For example, given the dataset:\"}]\n66:[\"$\",\"pre\",\"pre-10\",{\"style\":{\"fontSize\":14,\"backgroundColor\":\"light-dark(var(--mantine-color-gray-0), var(--mantine-color-dark-6))\",\"lineHeight\":1.7,\"display\":\"block\",\"padding\":\"1em\",\"borderRadius\":\"0.5em\",\"overflow\":\"auto\"},\"children\":[\"$\",\"code\",\"code-0\",{\"children\":\"http\_requests\_total\\nhttp\_requests\_total{replica=\\\"rep-a\\\"}\\nhttp\_requests\_total{replica=\\\"rep-b\\\"}\\nhttp\_requests\_total{environment=\\\"development\\\"}\\n\"}]}]\n67:[\"$\",\"p\",\"p-40\",{\"children\":[\"The"])self.\_\_next\_f.push([1," query \",[\"$\",\"code\",\"code-0\",{\"children\":\"http\_requests\_total{environment=\\\"\\\"}\"}],\" would match and return:\"]}]\n68:[\"$\",\"pre\",\"pre-11\",{\"style\":{\"fontSize\":14,\"backgroundColor\":\"light-dark(var(--mantine-color-gray-0), var(--mantine-color-dark-6))\",\"lineHeight\":1.7,\"display\":\"block\",\"padding\":\"1em\",\"borderRadius\":\"0.5em\",\"overflow\":\"auto\"},\"children\":[\"$\",\"code\",\"code-0\",{\"children\":\"http\_requests\_total\\nhttp\_requests\_total{replica=\\\"rep-a\\\"}\\nhttp\_requests\_total{replica=\\\"rep-b\\\"}\\n\"}]}]\n69:[\"$\",\"p\",\"p-41\",{\"children\":\"and would exclude:\"}]\n6a:[\"$\",\"pre\",\"pre-12\",{\"style\":{\"fontSize\":14,\"backgroundColor\":\"light-dark(var(--mantine-color-gray-0), var(--mantine-color-dark-6))\",\"lineHeight\":1.7,\"display\":\"block\",\"padding\":\"1em\",\"borderRadius\":\"0.5em\",\"overflow\":\"auto\"},\"children\":[\"$\",\"code\",\"code-0\",{\"children\":\"http\_requests\_total{environment=\\\"development\\\"}\\n\"}]}]\n6b:[\"$\",\"p\",\"p-42\",{\"children\":\"Multiple matchers can be used for the same label name; they all must pass for a result to be returned.\"}]\n6c:[\"$\",\"p\",\"p-43\",{\"children\":\"The query:\"}]\n6d:[\"$\",\"pre\",\"pre-13\",{\"style\":{\"fontSize\":14,\"backgroundColor\":\"light-dark(var(--mantine-color-gray-0), var(--mantine-color-dark-6))\",\"lineHeight\":1.7,\"display\":\"block\",\"padding\":\"1em\",\"borderRadius\":\"0.5em\",\"overflow\":\"auto\"},\"children\":[\"$\",\"code\",\"code-0\",{\"children\":\"http\_requests\_total{replica!=\\\"rep-a\\\",replica=~\\\"rep.\*\\\"}\\n\"}]}]\n6e:[\"$\",\"p\",\"p-44\",{\"children\":\"Would then match:\"}]\n6f:[\"$\",\"pre\",\"pre-14\",{\"style\":{\"fontSize\":14,\"backgroundColor\":\"light-dark(var(--mantine-color-gray-0), var(--mantine-color-dark-6))\",\"lineHeight\":1.7,\"display\":\"block\",\"padding\":\"1em\",\"borderRadius\":\"0.5em\",\"overflow\":\"auto\"},\"children\":[\"$\",\"code\",\"code-0\",{\"children\":\"http\_requests\_total{replica=\\\"rep-b\\\"}\\n\"}]}]\n70:[\"$\",\"p\",\"p-45\",{\"children\":\"Vector selectors must either specify a name or at least one label matcher\\nthat does not match the empty string. The following expression is illegal:\"}]\n71:[\"$\",\"pre\",\"pre-15\",{\"style\":{\"fontSize\":14,\"backgroundColor\":\"light-dark(var(--mant"])self.\_\_next\_f.push([1,"ine-color-gray-0), var(--mantine-color-dark-6))\",\"lineHeight\":1.7,\"display\":\"block\",\"padding\":\"1em\",\"borderRadius\":\"0.5em\",\"overflow\":\"auto\"},\"children\":[\"$\",\"code\",\"code-0\",{\"children\":\"{job=~\\\".\*\\\"} # Bad!\\n\"}]}]\n72:[\"$\",\"p\",\"p-46\",{\"children\":\"In contrast, these expressions are valid as they both have a selector that does not\\nmatch empty label values.\"}]\n73:[\"$\",\"pre\",\"pre-16\",{\"style\":{\"fontSize\":14,\"backgroundColor\":\"light-dark(var(--mantine-color-gray-0), var(--mantine-color-dark-6))\",\"lineHeight\":1.7,\"display\":\"block\",\"padding\":\"1em\",\"borderRadius\":\"0.5em\",\"overflow\":\"auto\"},\"children\":[\"$\",\"code\",\"code-0\",{\"children\":\"{job=~\\\".+\\\"} # Good!\\n{job=~\\\".\*\\\",method=\\\"get\\\"} # Good!\\n\"}]}]\n"])self.\_\_next\_f.push([1,"74:[\"$\",\"p\",\"p-47\",{\"children\":[\"Label matchers can also be applied to metric names by matching against the internal\\n\",[\"$\",\"code\",\"code-0\",{\"children\":\"\_\_name\_\_\"}],\" label. For example, the expression \",[\"$\",\"code\",\"code-1\",{\"children\":\"http\_requests\_total\"}],\" is equivalent to\\n\",[\"$\",\"code\",\"code-2\",{\"children\":\"{\_\_name\_\_=\\\"http\_requests\_total\\\"}\"}],\". Matchers other than \",[\"$\",\"code\",\"code-3\",{\"children\":\"=\"}],\" (\",[\"$\",\"code\",\"code-4\",{\"children\":\"!=\"}],\", \",[\"$\",\"code\",\"code-5\",{\"children\":\"=~\"}],\", \",[\"$\",\"code\",\"code-6\",{\"children\":\"!~\"}],\") may also be used.\\nThe following expression selects all metrics that have a name starting with \",[\"$\",\"code\",\"code-7\",{\"children\":\"job:\"}],\":\"]}]\n"])self.\_\_next\_f.push([1,"75:[\"$\",\"pre\",\"pre-17\",{\"style\":{\"fontSize\":14,\"backgroundColor\":\"light-dark(var(--mantine-color-gray-0), var(--mantine-color-dark-6))\",\"lineHeight\":1.7,\"display\":\"block\",\"padding\":\"1em\",\"borderRadius\":\"0.5em\",\"overflow\":\"auto\"},\"children\":[\"$\",\"code\",\"code-0\",{\"children\":\"{\_\_name\_\_=~\\\"job:.\*\\\"}\\n\"}]}]\n76:[\"$\",\"p\",\"p-48\",{\"children\":[\"The metric name must not be one of the keywords \",[\"$\",\"code\",\"code-0\",{\"children\":\"bool\"}],\", \",[\"$\",\"code\",\"code-1\",{\"children\":\"on\"}],\", \",[\"$\",\"code\",\"code-2\",{\"children\":\"ignoring\"}],\", \",[\"$\",\"code\",\"code-3\",{\"children\":\"group\_left\"}],\" and \",[\"$\",\"code\",\"code-4\",{\"children\":\"group\_right\"}],\". The following expression is illegal:\"]}]\n77:[\"$\",\"pre\",\"pre-18\",{\"style\":{\"fontSize\":14,\"backgroundColor\":\"light-dark(var(--mantine-color-gray-0), var(--mantine-color-dark-6))\",\"lineHeight\":1.7,\"display\":\"block\",\"padding\":\"1em\",\"borderRadius\":\"0.5em\",\"overflow\":\"auto\"},\"children\":[\"$\",\"code\",\"code-0\",{\"children\":\"on{} # Bad!\\n\"}]}]\n78:[\"$\",\"p\",\"p-49\",{\"children\":[\"A workaround for this restriction is to use the \",[\"$\",\"code\",\"code-0\",{\"children\":\"\_\_name\_\_\"}],\" label:\"]}]\n79:[\"$\",\"pre\",\"pre-19\",{\"style\":{\"fontSize\":14,\"backgroundColor\":\"light-dark(var(--mantine-color-gray-0), var(--mantine-color-dark-6))\",\"lineHeight\":1.7,\"display\":\"block\",\"padding\":\"1em\",\"borderRadius\":\"0.5em\",\"overflow\":\"auto\"},\"children\":[\"$\",\"code\",\"code-0\",{\"children\":\"{\_\_name\_\_=\\\"on\\\"} # Good!\\n\"}]}]\n"])self.\_\_next\_f.push([1,"7a:[\"$\",\"$L2b\",\"h3-3\",{\"order\":3,\"id\":\"range-vector-selectors\",\"children\":[\"Range Vector Selectors\",[\"$\",\"a\",\"a-0\",{\"className\":\"header-auto-link\",\"href\":\"#range-vector-selectors\",\"children\":[\"$\",\"svg\",null,{\"ref\":\"$undefined\",\"xmlns\":\"http://www.w3.org/2000/svg\",\"width\":\"0.875em\",\"height\":\"0.875em\",\"viewBox\":\"0 0 24 24\",\"fill\":\"none\",\"stroke\":\"currentColor\",\"strokeWidth\":2,\"strokeLinecap\":\"round\",\"strokeLinejoin\":\"round\",\"className\":\"tabler-icon tabler-icon-link \",\"children\":[\"$undefined\",[\"$\",\"path\",\"svg-0\",{\"d\":\"M9 15l6 -6\"}],[\"$\",\"path\",\"svg-1\",{\"d\":\"M11 6l.463 -.536a5 5 0 0 1 7.071 7.072l-.534 .464\"}],[\"$\",\"path\",\"svg-2\",{\"d\":\"M13 18l-.397 .534a5.068 5.068 0 0 1 -7.127 0a4.972 4.972 0 0 1 0 -7.071l.524 -.463\"}],\"$undefined\"]}]}]]}]\n"])self.\_\_next\_f.push([1,"7b:[\"$\",\"p\",\"p-50\",{\"children\":[\"Range vector literals work like instant vector literals, except that they\\nselect a range of samples back from the current instant. Syntactically, a\\n\",[\"$\",\"$Ld\",\"a-0\",{\"inherit\":true,\"c\":\"var(--secondary-link-color)\",\"component\":\"$2e\",\"href\":\"#float-literals-and-time-durations\",\"children\":\"float literal\"}],\" is appended in square\\nbrackets (\",[\"$\",\"code\",\"code-0\",{\"children\":\"[]\"}],\") at the end of a vector selector to specify for how many seconds\\nback in time values should be fetched for each resulting range vector element.\\nCommonly, the float literal uses the syntax with one or more time units, e.g.\\n\",[\"$\",\"code\",\"code-1\",{\"children\":\"[5m]\"}],\". The range is a left-open and right-closed interval, i.e. samples with\\ntimestamps coinciding with the left boundary of the range are excluded from the\\nselection, while samples coinciding with the right boundary of the range are\\nincluded in the selection.\"]}]\n"])self.\_\_next\_f.push([1,"7c:[\"$\",\"p\",\"p-51\",{\"children\":[\"In this example, we select all the values recorded less than 5m ago for all\\ntime series that have the metric name \",[\"$\",\"code\",\"code-0\",{\"children\":\"http\_requests\_total\"}],\" and a \",[\"$\",\"code\",\"code-1\",{\"children\":\"job\"}],\" label\\nset to \",[\"$\",\"code\",\"code-2\",{\"children\":\"prometheus\"}],\":\"]}]\n7d:[\"$\",\"pre\",\"pre-20\",{\"style\":{\"fontSize\":14,\"backgroundColor\":\"light-dark(var(--mantine-color-gray-0), var(--mantine-color-dark-6))\",\"lineHeight\":1.7,\"display\":\"block\",\"padding\":\"1em\",\"borderRadius\":\"0.5em\",\"overflow\":\"auto\"},\"children\":[\"$\",\"code\",\"code-0\",{\"children\":\"http\_requests\_total{job=\\\"prometheus\\\"}[5m]\\n\"}]}]\n"])self.\_\_next\_f.push([1,"7e:[\"$\",\"$L2b\",\"h3-4\",{\"order\":3,\"id\":\"offset-modifier\",\"children\":[\"Offset modifier\",[\"$\",\"a\",\"a-0\",{\"className\":\"header-auto-link\",\"href\":\"#offset-modifier\",\"children\":[\"$\",\"svg\",null,{\"ref\":\"$undefined\",\"xmlns\":\"http://www.w3.org/2000/svg\",\"width\":\"0.875em\",\"height\":\"0.875em\",\"viewBox\":\"0 0 24 24\",\"fill\":\"none\",\"stroke\":\"currentColor\",\"strokeWidth\":2,\"strokeLinecap\":\"round\",\"strokeLinejoin\":\"round\",\"className\":\"tabler-icon tabler-icon-link \",\"children\":[\"$undefined\",[\"$\",\"path\",\"svg-0\",{\"d\":\"M9 15l6 -6\"}],[\"$\",\"path\",\"svg-1\",{\"d\":\"M11 6l.463 -.536a5 5 0 0 1 7.071 7.072l-.534 .464\"}],[\"$\",\"path\",\"svg-2\",{\"d\":\"M13 18l-.397 .534a5.068 5.068 0 0 1 -7.127 0a4.972 4.972 0 0 1 0 -7.071l.524 -.463\"}],\"$undefined\"]}]}]]}]\n"])self.\_\_next\_f.push([1,"7f:[\"$\",\"p\",\"p-52\",{\"children\":[\"The \",[\"$\",\"code\",\"code-0\",{\"children\":\"offset\"}],\" modifier allows changing the time offset for individual\\ninstant and range vectors in a query.\"]}]\n80:[\"$\",\"p\",\"p-53\",{\"children\":[\"For example, the following expression returns the value of\\n\",[\"$\",\"code\",\"code-0\",{\"children\":\"http\_requests\_total\"}],\" 5 minutes in the past relative to the current\\nquery evaluation time:\"]}]\n81:[\"$\",\"pre\",\"pre-21\",{\"style\":{\"fontSize\":14,\"backgroundColor\":\"light-dark(var(--mantine-color-gray-0), var(--mantine-color-dark-6))\",\"lineHeight\":1.7,\"display\":\"block\",\"padding\":\"1em\",\"borderRadius\":\"0.5em\",\"overflow\":\"auto\"},\"children\":[\"$\",\"code\",\"code-0\",{\"children\":\"http\_requests\_total offset 5m\\n\"}]}]\n82:[\"$\",\"p\",\"p-54\",{\"children\":[\"Note that the \",[\"$\",\"code\",\"code-0\",{\"children\":\"offset\"}],\" modifier always needs to follow the selector\\nimmediately, i.e. the following would be correct:\"]}]\n83:[\"$\",\"pre\",\"pre-22\",{\"style\":{\"fontSize\":14,\"backgroundColor\":\"light-dark(var(--mantine-color-gray-0), var(--mantine-color-dark-6))\",\"lineHeight\":1.7,\"display\":\"block\",\"padding\":\"1em\",\"borderRadius\":\"0.5em\",\"overflow\":\"auto\"},\"children\":[\"$\",\"code\",\"code-0\",{\"children\":\"sum(http\_requests\_total{method=\\\"GET\\\"} offset 5m) // GOOD.\\n\"}]}]\n84:[\"$\",\"p\",\"p-55\",{\"children\":[\"While the following would be \",[\"$\",\"em\",\"em-0\",{\"children\":\"incorrect\"}],\":\"]}]\n85:[\"$\",\"pre\",\"pre-23\",{\"style\":{\"fontSize\":14,\"backgroundColor\":\"light-dark(var(--mantine-color-gray-0), var(--mantine-color-dark-6))\",\"lineHeight\":1.7,\"display\":\"block\",\"padding\":\"1em\",\"borderRadius\":\"0.5em\",\"overflow\":\"auto\"},\"children\":[\"$\",\"code\",\"code-0\",{\"children\":\"sum(http\_requests\_total{method=\\\"GET\\\"}) offset 5m // INVALID.\\n\"}]}]\n86:[\"$\",\"p\",\"p-56\",{\"children\":[\"The same works for range vectors. This returns the 5-minute \",[\"$\",\"$Ld\",\"a-0\",{\"inherit\":true,\"c\":\"var(--secondary-link-color)\",\"component\":\"$2e\",\"href\":\"/docs/prometheus/latest/querying/functions#rate\",\"children\":\"rate\"}],\"\\nthat \",[\"$\",\"code\",\"code-0\",{\"children\":\"http\_requests\_total\"}],\" had a"])self.\_\_next\_f.push([1," week ago:\"]}]\n87:[\"$\",\"pre\",\"pre-24\",{\"style\":{\"fontSize\":14,\"backgroundColor\":\"light-dark(var(--mantine-color-gray-0), var(--mantine-color-dark-6))\",\"lineHeight\":1.7,\"display\":\"block\",\"padding\":\"1em\",\"borderRadius\":\"0.5em\",\"overflow\":\"auto\"},\"children\":[\"$\",\"code\",\"code-0\",{\"children\":\"rate(http\_requests\_total[5m] offset 1w)\\n\"}]}]\n88:[\"$\",\"p\",\"p-57\",{\"children\":\"When querying for samples in the past, a negative offset will enable temporal comparisons forward in time:\"}]\n89:[\"$\",\"pre\",\"pre-25\",{\"style\":{\"fontSize\":14,\"backgroundColor\":\"light-dark(var(--mantine-color-gray-0), var(--mantine-color-dark-6))\",\"lineHeight\":1.7,\"display\":\"block\",\"padding\":\"1em\",\"borderRadius\":\"0.5em\",\"overflow\":\"auto\"},\"children\":[\"$\",\"code\",\"code-0\",{\"children\":\"rate(http\_requests\_total[5m] offset -1w)\\n\"}]}]\n8a:[\"$\",\"p\",\"p-58\",{\"children\":\"Note that this allows a query to look ahead of its evaluation time.\"}]\n"])self.\_\_next\_f.push([1,"8b:[\"$\",\"$L2b\",\"h3-5\",{\"order\":3,\"id\":\"-modifier\",\"children\":[\"@ modifier\",[\"$\",\"a\",\"a-0\",{\"className\":\"header-auto-link\",\"href\":\"#-modifier\",\"children\":[\"$\",\"svg\",null,{\"ref\":\"$undefined\",\"xmlns\":\"http://www.w3.org/2000/svg\",\"width\":\"0.875em\",\"height\":\"0.875em\",\"viewBox\":\"0 0 24 24\",\"fill\":\"none\",\"stroke\":\"currentColor\",\"strokeWidth\":2,\"strokeLinecap\":\"round\",\"strokeLinejoin\":\"round\",\"className\":\"tabler-icon tabler-icon-link \",\"children\":[\"$undefined\",[\"$\",\"path\",\"svg-0\",{\"d\":\"M9 15l6 -6\"}],[\"$\",\"path\",\"svg-1\",{\"d\":\"M11 6l.463 -.536a5 5 0 0 1 7.071 7.072l-.534 .464\"}],[\"$\",\"path\",\"svg-2\",{\"d\":\"M13 18l-.397 .534a5.068 5.068 0 0 1 -7.127 0a4.972 4.972 0 0 1 0 -7.071l.524 -.463\"}],\"$undefined\"]}]}]]}]\n"])self.\_\_next\_f.push([1,"8c:[\"$\",\"p\",\"p-59\",{\"children\":[\"The \",[\"$\",\"code\",\"code-0\",{\"children\":\"@\"}],\" modifier allows changing the evaluation time for individual instant\\nand range vectors in a query. The time supplied to the \",[\"$\",\"code\",\"code-1\",{\"children\":\"@\"}],\" modifier\\nis a Unix timestamp and described with a float literal.\"]}]\n8d:[\"$\",\"p\",\"p-60\",{\"children\":[\"For example, the following expression returns the value of\\n\",[\"$\",\"code\",\"code-0\",{\"children\":\"http\_requests\_total\"}],\" at \",[\"$\",\"code\",\"code-1\",{\"children\":\"2021-01-04T07:40:00+00:00\"}],\":\"]}]\n8e:[\"$\",\"pre\",\"pre-26\",{\"style\":{\"fontSize\":14,\"backgroundColor\":\"light-dark(var(--mantine-color-gray-0), var(--mantine-color-dark-6))\",\"lineHeight\":1.7,\"display\":\"block\",\"padding\":\"1em\",\"borderRadius\":\"0.5em\",\"overflow\":\"auto\"},\"children\":[\"$\",\"code\",\"code-0\",{\"children\":\"http\_requests\_total @ 1609746000\\n\"}]}]\n8f:[\"$\",\"p\",\"p-61\",{\"children\":[\"Note that the \",[\"$\",\"code\",\"code-0\",{\"children\":\"@\"}],\" modifier always needs to follow the selector\\nimmediately, i.e. the following would be correct:\"]}]\n90:[\"$\",\"pre\",\"pre-27\",{\"style\":{\"fontSize\":14,\"backgroundColor\":\"light-dark(var(--mantine-color-gray-0), var(--mantine-color-dark-6))\",\"lineHeight\":1.7,\"display\":\"block\",\"padding\":\"1em\",\"borderRadius\":\"0.5em\",\"overflow\":\"auto\"},\"children\":[\"$\",\"code\",\"code-0\",{\"children\":\"sum(http\_requests\_total{method=\\\"GET\\\"} @ 1609746000) // GOOD.\\n\"}]}]\n91:[\"$\",\"p\",\"p-62\",{\"children\":[\"While the following would be \",[\"$\",\"em\",\"em-0\",{\"children\":\"incorrect\"}],\":\"]}]\n92:[\"$\",\"pre\",\"pre-28\",{\"style\":{\"fontSize\":14,\"backgroundColor\":\"light-dark(var(--mantine-color-gray-0), var(--mantine-color-dark-6))\",\"lineHeight\":1.7,\"display\":\"block\",\"padding\":\"1em\",\"borderRadius\":\"0.5em\",\"overflow\":\"auto\"},\"children\":[\"$\",\"code\",\"code-0\",{\"children\":\"sum(http\_requests\_total{method=\\\"GET\\\"}) @ 1609746000 // INVALID.\\n\"}]}]\n93:[\"$\",\"p\",\"p-63\",{\"children\":[\"The same works for range vectors. This returns the 5-minute rate that\\n\",[\"$\",\"code\",\"code-0\",{\"children\":\"http\_requests\_total\"}],\" had at \",[\"$\",\"code\",\"code-1"])self.\_\_next\_f.push([1,"\",{\"children\":\"2021-01-04T07:40:00+00:00\"}],\":\"]}]\n94:[\"$\",\"pre\",\"pre-29\",{\"style\":{\"fontSize\":14,\"backgroundColor\":\"light-dark(var(--mantine-color-gray-0), var(--mantine-color-dark-6))\",\"lineHeight\":1.7,\"display\":\"block\",\"padding\":\"1em\",\"borderRadius\":\"0.5em\",\"overflow\":\"auto\"},\"children\":[\"$\",\"code\",\"code-0\",{\"children\":\"rate(http\_requests\_total[5m] @ 1609746000)\\n\"}]}]\n95:[\"$\",\"p\",\"p-64\",{\"children\":[\"The \",[\"$\",\"code\",\"code-0\",{\"children\":\"@\"}],\" modifier supports all representations of numeric literals described above.\\nIt works with the \",[\"$\",\"code\",\"code-1\",{\"children\":\"offset\"}],\" modifier where the offset is applied relative to the \",[\"$\",\"code\",\"code-2\",{\"children\":\"@\"}],\"\\nmodifier time. The results are the same irrespective of the order of the modifiers.\"]}]\n96:[\"$\",\"p\",\"p-65\",{\"children\":\"For example, these two queries will produce the same result:\"}]\n97:[\"$\",\"pre\",\"pre-30\",{\"style\":{\"fontSize\":14,\"backgroundColor\":\"light-dark(var(--mantine-color-gray-0), var(--mantine-color-dark-6))\",\"lineHeight\":1.7,\"display\":\"block\",\"padding\":\"1em\",\"borderRadius\":\"0.5em\",\"overflow\":\"auto\"},\"children\":[\"$\",\"code\",\"code-0\",{\"children\":\"# offset after @\\nhttp\_requests\_total @ 1609746000 offset 5m\\n# offset before @\\nhttp\_requests\_total offset 5m @ 1609746000\\n\"}]}]\n98:[\"$\",\"p\",\"p-66\",{\"children\":[\"Additionally, \",[\"$\",\"code\",\"code-0\",{\"children\":\"start()\"}],\" and \",[\"$\",\"code\",\"code-1\",{\"children\":\"end()\"}],\" can also be used as values for the \",[\"$\",\"code\",\"code-2\",{\"children\":\"@\"}],\" modifier as special values.\"]}]\n99:[\"$\",\"p\",\"p-67\",{\"children\":\"For a range query, they resolve to the start and end of the range query respectively and remain the same for all steps.\"}]\n9a:[\"$\",\"p\",\"p-68\",{\"children\":[\"For an instant query, \",[\"$\",\"code\",\"code-0\",{\"children\":\"start()\"}],\" and \",[\"$\",\"code\",\"code-1\",{\"children\":\"end()\"}],\" both resolve to the evaluation time.\"]}]\n9b:[\"$\",\"pre\",\"pre-31\",{\"style\":{\"fontSize\":14,\"backgroundColor\":\"light-dark(var(--mantine-color-gray-0), var(--mantine-color-dark-6))\",\"lineHeight\":1.7,\"di"])self.\_\_next\_f.push([1,"splay\":\"block\",\"padding\":\"1em\",\"borderRadius\":\"0.5em\",\"overflow\":\"auto\"},\"children\":[\"$\",\"code\",\"code-0\",{\"children\":\"http\_requests\_total @ start()\\nrate(http\_requests\_total[5m] @ end())\\n\"}]}]\n9c:[\"$\",\"p\",\"p-69\",{\"children\":[\"Note that the \",[\"$\",\"code\",\"code-0\",{\"children\":\"@\"}],\" modifier allows a query to look ahead of its evaluation time.\"]}]\n"])self.\_\_next\_f.push([1,"9d:[\"$\",\"$L2b\",\"h2-6\",{\"order\":2,\"id\":\"subquery\",\"children\":[\"Subquery\",[\"$\",\"a\",\"a-0\",{\"className\":\"header-auto-link\",\"href\":\"#subquery\",\"children\":[\"$\",\"svg\",null,{\"ref\":\"$undefined\",\"xmlns\":\"http://www.w3.org/2000/svg\",\"width\":\"0.875em\",\"height\":\"0.875em\",\"viewBox\":\"0 0 24 24\",\"fill\":\"none\",\"stroke\":\"currentColor\",\"strokeWidth\":2,\"strokeLinecap\":\"round\",\"strokeLinejoin\":\"round\",\"className\":\"tabler-icon tabler-icon-link \",\"children\":[\"$undefined\",[\"$\",\"path\",\"svg-0\",{\"d\":\"M9 15l6 -6\"}],[\"$\",\"path\",\"svg-1\",{\"d\":\"M11 6l.463 -.536a5 5 0 0 1 7.071 7.072l-.534 .464\"}],[\"$\",\"path\",\"svg-2\",{\"d\":\"M13 18l-.397 .534a5.068 5.068 0 0 1 -7.127 0a4.972 4.972 0 0 1 0 -7.071l.524 -.463\"}],\"$undefined\"]}]}]]}]\n"])self.\_\_next\_f.push([1,"9e:[\"$\",\"p\",\"p-70\",{\"children\":\"Subquery allows you to run an instant query for a given range and resolution. The result of a subquery is a range vector.\"}]\n9f:[\"$\",\"p\",\"p-71\",{\"children\":[\"Syntax: \",[\"$\",\"code\",\"code-0\",{\"children\":\"\u003cinstant\_query\u003e '[' \u003crange\u003e ':' [\u003cresolution\u003e] ']' [ @ \u003cfloat\_literal\u003e ] [ offset \u003cfloat\_literal\u003e ]\"}]]}]\na0:[\"$\",\"ul\",\"ul-3\",{\"children\":[\"\\n\",[\"$\",\"li\",\"li-0\",{\"children\":[[\"$\",\"code\",\"code-0\",{\"id\":\"resolution\",\"children\":\"\u003cresolution\u003e\"}],\" is optional. Default is the global evaluation interval.\"]}],\"\\n\"]}]\n"])self.\_\_next\_f.push([1,"a1:[\"$\",\"$L2b\",\"h2-7\",{\"order\":2,\"id\":\"operators\",\"children\":[\"Operators\",[\"$\",\"a\",\"a-0\",{\"className\":\"header-auto-link\",\"href\":\"#operators\",\"children\":[\"$\",\"svg\",null,{\"ref\":\"$undefined\",\"xmlns\":\"http://www.w3.org/2000/svg\",\"width\":\"0.875em\",\"height\":\"0.875em\",\"viewBox\":\"0 0 24 24\",\"fill\":\"none\",\"stroke\":\"currentColor\",\"strokeWidth\":2,\"strokeLinecap\":\"round\",\"strokeLinejoin\":\"round\",\"className\":\"tabler-icon tabler-icon-link \",\"children\":[\"$undefined\",[\"$\",\"path\",\"svg-0\",{\"d\":\"M9 15l6 -6\"}],[\"$\",\"path\",\"svg-1\",{\"d\":\"M11 6l.463 -.536a5 5 0 0 1 7.071 7.072l-.534 .464\"}],[\"$\",\"path\",\"svg-2\",{\"d\":\"M13 18l-.397 .534a5.068 5.068 0 0 1 -7.127 0a4.972 4.972 0 0 1 0 -7.071l.524 -.463\"}],\"$undefined\"]}]}]]}]\n"])self.\_\_next\_f.push([1,"a2:[\"$\",\"p\",\"p-72\",{\"children\":[\"Prometheus supports many binary and aggregation operators. These are described\\nin detail in the \",[\"$\",\"$Ld\",\"a-0\",{\"inherit\":true,\"c\":\"var(--secondary-link-color)\",\"component\":\"$2e\",\"href\":\"/docs/prometheus/latest/querying/operators\",\"children\":\"expression language operators\"}],\" page.\"]}]\n"])self.\_\_next\_f.push([1,"a3:[\"$\",\"$L2b\",\"h2-8\",{\"order\":2,\"id\":\"functions\",\"children\":[\"Functions\",[\"$\",\"a\",\"a-0\",{\"className\":\"header-auto-link\",\"href\":\"#functions\",\"children\":[\"$\",\"svg\",null,{\"ref\":\"$undefined\",\"xmlns\":\"http://www.w3.org/2000/svg\",\"width\":\"0.875em\",\"height\":\"0.875em\",\"viewBox\":\"0 0 24 24\",\"fill\":\"none\",\"stroke\":\"currentColor\",\"strokeWidth\":2,\"strokeLinecap\":\"round\",\"strokeLinejoin\":\"round\",\"className\":\"tabler-icon tabler-icon-link \",\"children\":[\"$undefined\",[\"$\",\"path\",\"svg-0\",{\"d\":\"M9 15l6 -6\"}],[\"$\",\"path\",\"svg-1\",{\"d\":\"M11 6l.463 -.536a5 5 0 0 1 7.071 7.072l-.534 .464\"}],[\"$\",\"path\",\"svg-2\",{\"d\":\"M13 18l-.397 .534a5.068 5.068 0 0 1 -7.127 0a4.972 4.972 0 0 1 0 -7.071l.524 -.463\"}],\"$undefined\"]}]}]]}]\n"])self.\_\_next\_f.push([1,"a4:[\"$\",\"p\",\"p-73\",{\"children\":[\"Prometheus supports several functions to operate on data. These are described\\nin detail in the \",[\"$\",\"$Ld\",\"a-0\",{\"inherit\":true,\"c\":\"var(--secondary-link-color)\",\"component\":\"$2e\",\"href\":\"/docs/prometheus/latest/querying/functions\",\"children\":\"expression language functions\"}],\" page.\"]}]\n"])self.\_\_next\_f.push([1,"a5:[\"$\",\"$L2b\",\"h2-9\",{\"order\":2,\"id\":\"comments\",\"children\":[\"Comments\",[\"$\",\"a\",\"a-0\",{\"className\":\"header-auto-link\",\"href\":\"#comments\",\"children\":[\"$\",\"svg\",null,{\"ref\":\"$undefined\",\"xmlns\":\"http://www.w3.org/2000/svg\",\"width\":\"0.875em\",\"height\":\"0.875em\",\"viewBox\":\"0 0 24 24\",\"fill\":\"none\",\"stroke\":\"currentColor\",\"strokeWidth\":2,\"strokeLinecap\":\"round\",\"strokeLinejoin\":\"round\",\"className\":\"tabler-icon tabler-icon-link \",\"children\":[\"$undefined\",[\"$\",\"path\",\"svg-0\",{\"d\":\"M9 15l6 -6\"}],[\"$\",\"path\",\"svg-1\",{\"d\":\"M11 6l.463 -.536a5 5 0 0 1 7.071 7.072l-.534 .464\"}],[\"$\",\"path\",\"svg-2\",{\"d\":\"M13 18l-.397 .534a5.068 5.068 0 0 1 -7.127 0a4.972 4.972 0 0 1 0 -7.071l.524 -.463\"}],\"$undefined\"]}]}]]}]\n"])self.\_\_next\_f.push([1,"a6:[\"$\",\"p\",\"p-74\",{\"children\":[\"PromQL supports line comments that start with \",[\"$\",\"code\",\"code-0\",{\"children\":\"#\"}],\". Example:\"]}]\na7:[\"$\",\"pre\",\"pre-32\",{\"style\":{\"fontSize\":14,\"backgroundColor\":\"light-dark(var(--mantine-color-gray-0), var(--mantine-color-dark-6))\",\"lineHeight\":1.7,\"display\":\"block\",\"padding\":\"1em\",\"borderRadius\":\"0.5em\",\"overflow\":\"auto\"},\"children\":[\"$\",\"code\",\"code-0\",{\"children\":\" # This is a comment\\n\"}]}]\n"])self.\_\_next\_f.push([1,"a8:[\"$\",\"$L2b\",\"h2-10\",{\"order\":2,\"id\":\"regular-expressions\",\"children\":[\"Regular expressions\",[\"$\",\"a\",\"a-0\",{\"className\":\"header-auto-link\",\"href\":\"#regular-expressions\",\"children\":[\"$\",\"svg\",null,{\"ref\":\"$undefined\",\"xmlns\":\"http://www.w3.org/2000/svg\",\"width\":\"0.875em\",\"height\":\"0.875em\",\"viewBox\":\"0 0 24 24\",\"fill\":\"none\",\"stroke\":\"currentColor\",\"strokeWidth\":2,\"strokeLinecap\":\"round\",\"strokeLinejoin\":\"round\",\"className\":\"tabler-icon tabler-icon-link \",\"children\":[\"$undefined\",[\"$\",\"path\",\"svg-0\",{\"d\":\"M9 15l6 -6\"}],[\"$\",\"path\",\"svg-1\",{\"d\":\"M11 6l.463 -.536a5 5 0 0 1 7.071 7.072l-.534 .464\"}],[\"$\",\"path\",\"svg-2\",{\"d\":\"M13 18l-.397 .534a5.068 5.068 0 0 1 -7.127 0a4.972 4.972 0 0 1 0 -7.071l.524 -.463\"}],\"$undefined\"]}]}]]}]\n"])self.\_\_next\_f.push([1,"a9:[\"$\",\"p\",\"p-75\",{\"children\":[\"All regular expressions in Prometheus use \",[\"$\",\"$Ld\",\"a-0\",{\"inherit\":true,\"c\":\"var(--secondary-link-color)\",\"href\":\"https://github.com/google/re2/wiki/Syntax\",\"target\":\"\_blank\",\"rel\":\"noopener\",\"children\":[\"$\",\"span\",null,{\"children\":[\"RE2 syntax\",\" \",[\"$\",\"svg\",null,{\"ref\":\"$undefined\",\"xmlns\":\"http://www.w3.org/2000/svg\",\"width\":\"0.9em\",\"height\":\"0.9em\",\"viewBox\":\"0 0 24 24\",\"fill\":\"none\",\"stroke\":\"currentColor\",\"strokeWidth\":2,\"strokeLinecap\":\"round\",\"strokeLinejoin\":\"round\",\"className\":\"tabler-icon tabler-icon-external-link \",\"style\":{\"marginBottom\":-1.5},\"children\":[\"$undefined\",[\"$\",\"path\",\"svg-0\",{\"d\":\"M12 6h-6a2 2 0 0 0 -2 2v10a2 2 0 0 0 2 2h10a2 2 0 0 0 2 -2v-6\"}],[\"$\",\"path\",\"svg-1\",{\"d\":\"M11 13l9 -9\"}],[\"$\",\"path\",\"svg-2\",{\"d\":\"M15 4h5v5\"}],\"$undefined\"]}]]}]}],\".\"]}]\n"])self.\_\_next\_f.push([1,"aa:[\"$\",\"p\",\"p-76\",{\"children\":\"Regex matches are always fully anchored.\"}]\n"])self.\_\_next\_f.push([1,"ab:[\"$\",\"$L2b\",\"h2-11\",{\"order\":2,\"id\":\"gotchas\",\"children\":[\"Gotchas\",[\"$\",\"a\",\"a-0\",{\"className\":\"header-auto-link\",\"href\":\"#gotchas\",\"children\":[\"$\",\"svg\",null,{\"ref\":\"$undefined\",\"xmlns\":\"http://www.w3.org/2000/svg\",\"width\":\"0.875em\",\"height\":\"0.875em\",\"viewBox\":\"0 0 24 24\",\"fill\":\"none\",\"stroke\":\"currentColor\",\"strokeWidth\":2,\"strokeLinecap\":\"round\",\"strokeLinejoin\":\"round\",\"className\":\"tabler-icon tabler-icon-link \",\"children\":[\"$undefined\",[\"$\",\"path\",\"svg-0\",{\"d\":\"M9 15l6 -6\"}],[\"$\",\"path\",\"svg-1\",{\"d\":\"M11 6l.463 -.536a5 5 0 0 1 7.071 7.072l-.534 .464\"}],[\"$\",\"path\",\"svg-2\",{\"d\":\"M13 18l-.397 .534a5.068 5.068 0 0 1 -7.127 0a4.972 4.972 0 0 1 0 -7.071l.524 -.463\"}],\"$undefined\"]}]}]]}]\n"])self.\_\_next\_f.push([1,"ac:[\"$\",\"$L2b\",\"h3-6\",{\"order\":3,\"id\":\"staleness\",\"children\":[\"Staleness\",[\"$\",\"a\",\"a-0\",{\"className\":\"header-auto-link\",\"href\":\"#staleness\",\"children\":[\"$\",\"svg\",null,{\"ref\":\"$undefined\",\"xmlns\":\"http://www.w3.org/2000/svg\",\"width\":\"0.875em\",\"height\":\"0.875em\",\"viewBox\":\"0 0 24 24\",\"fill\":\"none\",\"stroke\":\"currentColor\",\"strokeWidth\":2,\"strokeLinecap\":\"round\",\"strokeLinejoin\":\"round\",\"className\":\"tabler-icon tabler-icon-link \",\"children\":[\"$undefined\",[\"$\",\"path\",\"svg-0\",{\"d\":\"M9 15l6 -6\"}],[\"$\",\"path\",\"svg-1\",{\"d\":\"M11 6l.463 -.536a5 5 0 0 1 7.071 7.072l-.534 .464\"}],[\"$\",\"path\",\"svg-2\",{\"d\":\"M13 18l-.397 .534a5.068 5.068 0 0 1 -7.127 0a4.972 4.972 0 0 1 0 -7.071l.524 -.463\"}],\"$undefined\"]}]}]]}]\n"])self.\_\_next\_f.push([1,"ad:[\"$\",\"p\",\"p-77\",{\"children\":[\"The timestamps at which to sample data, during a query, are selected\\nindependently of the actual present time series data. This is mainly to support\\ncases like aggregation (\",[\"$\",\"code\",\"code-0\",{\"children\":\"sum\"}],\", \",[\"$\",\"code\",\"code-1\",{\"children\":\"avg\"}],\", and so on), where multiple aggregated\\ntime series do not precisely align in time. Because of their independence,\\nPrometheus needs to assign a value at those timestamps for each relevant time\\nseries. It does so by taking the newest sample that is less than the lookback period ago.\\nThe lookback period is 5 minutes by default, but can be\\n\",[\"$\",\"$Ld\",\"a-0\",{\"inherit\":true,\"c\":\"var(--secondary-link-color)\",\"component\":\"$2e\",\"href\":\"/docs/prometheus/latest/command-line/prometheus\",\"children\":[\"set with the \",[\"$\",\"code\",\"code-0\",{\"children\":\"--query.lookback-delta\"}],\" flag\"]}],\"\\nor overridden on an individual query via the \",[\"$\",\"code\",\"code-2\",{\"children\":\"lookback\_delta\"}],\" parameter.\"]}]\n"])self.\_\_next\_f.push([1,"ae:[\"$\",\"p\",\"p-78\",{\"children\":\"If a target scrape or rule evaluation no longer returns a sample for a time\\nseries that was previously present, this time series will be marked as stale.\\nIf a target is removed, the previously retrieved time series will be marked as\\nstale soon after removal.\"}]\naf:[\"$\",\"p\",\"p-79\",{\"children\":\"If a query is evaluated at a sampling timestamp after a time series is marked\\nas stale, then no value is returned for that time series. If new samples are\\nsubsequently ingested for that time series, they will be returned as expected.\"}]\nb0:[\"$\",\"p\",\"p-80\",{\"children\":\"A time series will go stale when it is no longer exported, or the target no\\nlonger exists. Such time series will disappear from graphs\\nat the times of their latest collected sample, and they will not be returned\\nin queries after they are marked stale.\"}]\nb1:[\"$\",\"p\",\"p-81\",{\"children\":[\"Some exporters, which put their own timestamps on samples, get a different behaviour:\\nseries that stop being exported take the last value for (by default) 5 minutes before\\ndisappearing. The \",[\"$\",\"code\",\"code-0\",{\"children\":\"track\_timestamps\_staleness\"}],\" setting can change this.\"]}]\n"])self.\_\_next\_f.push([1,"b2:[\"$\",\"$L2b\",\"h3-7\",{\"order\":3,\"id\":\"avoiding-slow-queries-and-overloads\",\"children\":[\"Avoiding slow queries and overloads\",[\"$\",\"a\",\"a-0\",{\"className\":\"header-auto-link\",\"href\":\"#avoiding-slow-queries-and-overloads\",\"children\":[\"$\",\"svg\",null,{\"ref\":\"$undefined\",\"xmlns\":\"http://www.w3.org/2000/svg\",\"width\":\"0.875em\",\"height\":\"0.875em\",\"viewBox\":\"0 0 24 24\",\"fill\":\"none\",\"stroke\":\"currentColor\",\"strokeWidth\":2,\"strokeLinecap\":\"round\",\"strokeLinejoin\":\"round\",\"className\":\"tabler-icon tabler-icon-link \",\"children\":[\"$undefined\",[\"$\",\"path\",\"svg-0\",{\"d\":\"M9 15l6 -6\"}],[\"$\",\"path\",\"svg-1\",{\"d\":\"M11 6l.463 -.536a5 5 0 0 1 7.071 7.072l-.534 .464\"}],[\"$\",\"path\",\"svg-2\",{\"d\":\"M13 18l-.397 .534a5.068 5.068 0 0 1 -7.127 0a4.972 4.972 0 0 1 0 -7.071l.524 -.463\"}],\"$undefined\"]}]}]]}]\n"])self.\_\_next\_f.push([1,"b3:[\"$\",\"p\",\"p-82\",{\"children\":[\"If a query needs to operate on a substantial amount of data, graphing it might\\ntime out or overload the server or browser. Thus, when constructing queries\\nover unknown data, always start building the query in the tabular view of\\nPrometheus's expression browser until the result set seems reasonable\\n(hundreds, not thousands, of time series at most). Only when you have filtered\\nor aggregated your data sufficiently, switch to graph mode. If the expression\\nstill takes too long to graph ad-hoc, pre-record it via a \",[\"$\",\"$Ld\",\"a-0\",{\"inherit\":true,\"c\":\"var(--secondary-link-color)\",\"component\":\"$2e\",\"href\":\"/docs/prometheus/latest/configuration/recording\_rules#recording-rules\",\"children\":\"recording\\nrule\"}],\".\"]}]\n"])self.\_\_next\_f.push([1,"b4:[\"$\",\"p\",\"p-83\",{\"children\":[\"This is especially relevant for Prometheus's query language, where a bare\\nmetric name selector like \",[\"$\",\"code\",\"code-0\",{\"children\":\"api\_http\_requests\_total\"}],\" could expand to thousands\\nof time series with different labels. Also, keep in mind that expressions that\\naggregate over many time series will generate load on the server even if the\\noutput is only a small number of time series. This is similar to how it would\\nbe slow to sum all values of a column in a relational database, even if the\\noutput value is only a single number.\"]}]\n"])