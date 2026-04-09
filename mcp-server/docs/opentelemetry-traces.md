html{background:Canvas;color:CanvasText}@media(prefers-color-scheme:dark){html{background:#0b0d12;color:#e6e6e6}}html[data-theme-init] \*{transition:none!important}(function(){const t="td-color-theme",n=localStorage.getItem(t);let e=n||(window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light");e==="auto"&&(e=window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light"),document.documentElement.setAttribute("data-bs-theme",e)})()Traces | OpenTelemetryvar doNotTrack=!1,dnt=navigator.doNotTrack||window.doNotTrack||navigator.msDoNotTrack,doNotTrack=dnt=="1"||dnt=="yes";if(!doNotTrack){window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag("js",new Date),gtag("config","G-QZHM7YEG07")}

[The OpenTelemetry Logosvg{enable-background:new 0 0 985.5 345.7}OpenTelemetry](/)

* [Docs](/docs/)
* [Ecosystem](/ecosystem/)
* [Status](/status/)
* [Community](/community/)
* [Training](/training/)
* [Blog](/blog/)
* [English
  EN](#)
  + [বাংলা](/bn/docs/concepts/signals/traces/)
  + English
  + [Español](/es/docs/concepts/signals/traces/)
  + [Français](/fr/docs/concepts/signals/traces/)
  + [日本語](/ja/docs/concepts/signals/traces/)
  + [Polski](/pl/docs/concepts/signals/traces/)
  + [Português](/pt/docs/concepts/signals/traces/)
  + [Română](/ro/docs/concepts/signals/traces/)
  + [Українська](/uk/docs/concepts/signals/traces/)
  + [中文](/zh/docs/concepts/signals/traces/)
* + Light
  + Dark
  + Auto

$(function(){$("#td-section-nav a").removeClass("active"),$("#td-section-nav #m-docsconceptssignalstraces").addClass("active"),$("#td-section-nav #m-docsconceptssignalstraces-li span").addClass("td-sidebar-nav-active-item"),$("#td-section-nav #m-docsconceptssignalstraces").parents("li").addClass("active-path"),$("#td-section-nav li.active-path").addClass("show"),$("#td-section-nav li.active-path").children("input").prop("checked",!0),$("#td-section-nav #m-docsconceptssignalstraces-li").siblings("li").addClass("show"),$("#td-section-nav #m-docsconceptssignalstraces-li").children("ul").children("li").addClass("show"),$("#td-sidebar-menu").toggleClass("d-none")})

* [Docs](/docs/ "Documentation")
  + [What is OpenTelemetry?](/docs/what-is-opentelemetry/)
  + [Getting Started](/docs/getting-started/)
    - [Dev](/docs/getting-started/dev/ "Getting started for Developers")
    - [Ops](/docs/getting-started/ops/ "Getting started for Ops")
  + [Concepts](/docs/concepts/ "OpenTelemetry Concepts")
    - [Observability primer](/docs/concepts/observability-primer/)
    - [Context propagation](/docs/concepts/context-propagation/)
    - [Signals](/docs/concepts/signals/)
      * [Traces](/docs/concepts/signals/traces/)
      * [Metrics](/docs/concepts/signals/metrics/)
      * [Logs](/docs/concepts/signals/logs/)
      * [Baggage](/docs/concepts/signals/baggage/)
      * [Profiles](/docs/concepts/signals/profiles/)
    - [Instrumentation](/docs/concepts/instrumentation/)
      * [Zero-code](/docs/concepts/instrumentation/zero-code/)
      * [Code-based](/docs/concepts/instrumentation/code-based/)
      * [Libraries](/docs/concepts/instrumentation/libraries/)
    - [Components](/docs/concepts/components/)
    - [Semantic Conventions](/docs/concepts/semantic-conventions/)
    - [Resources](/docs/concepts/resources/)
    - [Instrumentation scope](/docs/concepts/instrumentation-scope/)
    - [Sampling](/docs/concepts/sampling/)
    - [Distributions](/docs/concepts/distributions/)
    - [Glossary](/docs/concepts/glossary/)
  + [Demo](/docs/demo/ "OpenTelemetry Demo Docs")
    - [Architecture](/docs/demo/architecture/ "Demo Architecture")
    - [Collector Data Flow Dashboard](/docs/demo/collector-data-flow-dashboard/)
    - [Development](/docs/demo/development/)
    - [Docker](/docs/demo/docker-deployment/ "Docker deployment")
    - [Feature Flags](/docs/demo/feature-flags/)
      * [Diagnosing memory leaks](/docs/demo/feature-flags/recommendation-cache/ "Using Metrics and Traces to diagnose a memory leak")
    - [Forking](/docs/demo/forking/ "Forking the demo repository")
    - [Kubernetes](/docs/demo/kubernetes-deployment/ "Kubernetes deployment")
    - [Requirements](/docs/demo/requirements/ "Demo Requirements")
      * [Application](/docs/demo/requirements/application/ "Application Requirements")
      * [Architecture](/docs/demo/requirements/architecture/ "Architecture Requirements")
      * [OTel Requirements](/docs/demo/requirements/opentelemetry/ "OpenTelemetry Requirements")
      * [System](/docs/demo/requirements/system/ "System Requirements")
    - [Screenshots](/docs/demo/screenshots/ "Demo Screenshots")
    - [Services](/docs/demo/services/)
      * [Accounting](/docs/demo/services/accounting/ "Accounting Service")
      * [Ad](/docs/demo/services/ad/ "Ad Service")
      * [Cart](/docs/demo/services/cart/ "Cart Service")
      * [Checkout](/docs/demo/services/checkout/ "Checkout Service")
      * [Currency](/docs/demo/services/currency/ "Currency Service")
      * [Email](/docs/demo/services/email/ "Email Service")
      * [Flagd-UI](/docs/demo/services/flagd-ui/ "Flagd-UI Service")
      * [Fraud Detection](/docs/demo/services/fraud-detection/ "Fraud Detection Service")
      * [Frontend](/docs/demo/services/frontend/)
      * [Frontend Proxy](/docs/demo/services/frontend-proxy/ "Frontend Proxy (Envoy)")
      * [Image Provider](/docs/demo/services/image-provider/ "Image Provider Service")
      * [Kafka](/docs/demo/services/kafka/)
      * [Load Generator](/docs/demo/services/load-generator/)
      * [Payment](/docs/demo/services/payment/ "Payment Service")
      * [Product Catalog](/docs/demo/services/product-catalog/ "Product Catalog Service")
      * [Product Reviews](/docs/demo/services/product-reviews/ "Product Reviews Service")
      * [Quote](/docs/demo/services/quote/ "Quote Service")
      * [React Native App](/docs/demo/services/react-native-app/)
      * [Recommendation](/docs/demo/services/recommendation/ "Recommendation Service")
      * [Shipping](/docs/demo/services/shipping/ "Shipping Service")
    - [Telemetry Features](/docs/demo/telemetry-features/)
      * [Log Coverage](/docs/demo/telemetry-features/log-coverage/ "Log Coverage by Service")
      * [Manual Span Attributes](/docs/demo/telemetry-features/manual-span-attributes/)
      * [Metric Coverage](/docs/demo/telemetry-features/metric-coverage/ "Metric Coverage by Service")
      * [Trace Coverage](/docs/demo/telemetry-features/trace-coverage/ "Trace Coverage by Service")
    - [Tests](/docs/demo/tests/)
  + [Language APIs & SDKs](/docs/languages/)
    - [SDK Config](/docs/languages/sdk-configuration/ "SDK Configuration")
      * [General](/docs/languages/sdk-configuration/general/ "General SDK Configuration")
      * [OTLP Exporter](/docs/languages/sdk-configuration/otlp-exporter/ "OTLP Exporter Configuration")
      * [Declarative configuration](/docs/languages/sdk-configuration/declarative-configuration/)
    - [C++](/docs/languages/cpp/)
      * [Getting Started](/docs/languages/cpp/getting-started/)
      * [Instrumentation](/docs/languages/cpp/instrumentation/)
      * [Libraries](/docs/languages/cpp/library/ "Using instrumentation libraries")
      * [Exporters](/docs/languages/cpp/exporters/)
      * [API](/docs/languages/cpp/api/ "API reference")
      * [Examples](/docs/languages/cpp/examples/)
      * [Registry](/docs/languages/cpp/registry/)
    - [.NET](/docs/languages/dotnet/)
      * [Getting Started](/docs/languages/dotnet/getting-started/)
      * [Traces](/docs/languages/dotnet/traces/ "OpenTelemetry .NET traces")
        + [Console](/docs/languages/dotnet/traces/getting-started-console/ "Getting started with traces - Console")
        + [ASP.NET Core](/docs/languages/dotnet/traces/getting-started-aspnetcore/ "Getting started with traces - ASP.NET Core")
        + [Stratified sampling](/docs/languages/dotnet/traces/stratified-sampling/)
        + [Tail-based sampling](/docs/languages/dotnet/traces/tail-based-sampling/)
        + [Export to Jaeger](/docs/languages/dotnet/traces/jaeger/)
        + [Exceptions](/docs/languages/dotnet/traces/reporting-exceptions/ "Reporting exceptions")
        + [Links](/docs/languages/dotnet/traces/links-creation/ "Creating links between traces")
        + [Links-based sampling](/docs/languages/dotnet/traces/links-based-sampler/)
        + [Best practices](/docs/languages/dotnet/traces/best-practices/)
      * [Metrics](/docs/languages/dotnet/metrics/ "OpenTelemetry .NET metrics")
        + [Console](/docs/languages/dotnet/metrics/getting-started-console/ "Getting started with metrics - Console")
        + [ASP.NET Core](/docs/languages/dotnet/metrics/getting-started-aspnetcore/ "Getting started with metrics - ASP.NET Core")
        + [Export to Prometheus](/docs/languages/dotnet/metrics/getting-started-prometheus-grafana/ "Export to Prometheus and Grafana")
        + [Exemplars](/docs/languages/dotnet/metrics/exemplars/ "Using exemplars")
        + [Instruments](/docs/languages/dotnet/metrics/instruments/ "Metric instruments")
        + [Best practices](/docs/languages/dotnet/metrics/best-practices/)
      * [Logs](/docs/languages/dotnet/logs/ "OpenTelemetry .NET logs")
        + [Console](/docs/languages/dotnet/logs/getting-started-console/ "Getting started with logs - Console")
        + [ASP.NET Core](/docs/languages/dotnet/logs/getting-started-aspnetcore/ "Getting started with logs - ASP.NET Core")
        + [Complex objects](/docs/languages/dotnet/logs/complex-objects/ "Logging complex objects")
        + [Correlation](/docs/languages/dotnet/logs/correlation/ "Log correlation")
        + [Dedicated pipeline](/docs/languages/dotnet/logs/dedicated-pipeline/ "Setting up a dedicated logging pipeline")
        + [Redaction](/docs/languages/dotnet/logs/redaction/ "Log redaction")
        + [Best practices](/docs/languages/dotnet/logs/best-practices/)
      * [Instrumentation](/docs/languages/dotnet/instrumentation/)
      * [Libraries](/docs/languages/dotnet/libraries/ "Using instrumentation libraries")
      * [Resources](/docs/languages/dotnet/resources/ "Resources in OpenTelemetry .NET")
      * [Exporters](/docs/languages/dotnet/exporters/)
      * [.NET Framework](/docs/languages/dotnet/netframework/ ".NET Framework instrumentation configuration")
      * [Troubleshooting](/docs/languages/dotnet/troubleshooting/)
      * [Tracing Shim](/docs/languages/dotnet/shim/ "OpenTelemetry Tracing Shim")
      * [API - tracing](/docs/languages/dotnet/traces-api/ "Tracing API reference")
      * [API - metrics](/docs/languages/dotnet/metrics-api/ "Metrics API reference")
      * [Examples](/docs/languages/dotnet/examples/)
      * [Registry](/docs/languages/dotnet/registry/)
    - [Erlang/Elixir](/docs/languages/erlang/)
      * [Getting Started](/docs/languages/erlang/getting-started/)
      * [Instrumentation](/docs/languages/erlang/instrumentation/)
      * [Libraries](/docs/languages/erlang/libraries/ "Using instrumentation libraries")
      * [Exporters](/docs/languages/erlang/exporters/)
      * [Propagation](/docs/languages/erlang/propagation/)
      * [Resources](/docs/languages/erlang/resources/)
      * [Sampling](/docs/languages/erlang/sampling/)
      * [Testing](/docs/languages/erlang/testing/)
      * [API](/docs/languages/erlang/api/ "API reference")
      * [Examples](/docs/languages/erlang/examples/)
      * [Registry](/docs/languages/erlang/registry/)
    - [Go](/docs/languages/go/)
      * [Getting Started](/docs/languages/go/getting-started/)
      * [Instrumentation](/docs/languages/go/instrumentation/)
      * [Libraries](/docs/languages/go/libraries/ "Using instrumentation libraries")
      * [Exporters](/docs/languages/go/exporters/)
      * [Resources](/docs/languages/go/resources/)
      * [Sampling](/docs/languages/go/sampling/)
      * [API](/docs/languages/go/api/ "API reference")
      * [Examples](/docs/languages/go/examples/)
      * [Registry](/docs/languages/go/registry/)
    - [Java](/docs/languages/java/)
      * [Intro to OpenTelemetry Java](/docs/languages/java/intro/)
      * [Getting Started by Example](/docs/languages/java/getting-started/)
      * [Instrumentation ecosystem](/docs/languages/java/instrumentation/)
      * [Record Telemetry with API](/docs/languages/java/api/)
      * [Manage Telemetry with SDK](/docs/languages/java/sdk/)
      * [Configure the SDK](/docs/languages/java/configuration/)
      * [Examples](/docs/languages/java/examples/)
      * [Registry](/docs/languages/java/registry/)
    - [JavaScript](/docs/languages/js/)
      * [Getting Started](/docs/languages/js/getting-started/)
        + [Node.js](/docs/languages/js/getting-started/nodejs/)
        + [Browser](/docs/languages/js/getting-started/browser/)
      * [Instrumentation](/docs/languages/js/instrumentation/)
      * [Libraries](/docs/languages/js/libraries/ "Using instrumentation libraries")
      * [Exporters](/docs/languages/js/exporters/)
      * [Context](/docs/languages/js/context/)
      * [Propagation](/docs/languages/js/propagation/)
      * [Resources](/docs/languages/js/resources/)
      * [Sampling](/docs/languages/js/sampling/)
      * [Serverless](/docs/languages/js/serverless/)
      * [Benchmarks](/docs/languages/js/benchmarks/)
      * [API](/docs/languages/js/api/ "API reference")
      * [Examples](/docs/languages/js/examples/)
      * [Registry](/docs/languages/js/registry/)
    - [Kotlin](/docs/languages/kotlin/)
      * [Examples](/docs/languages/kotlin/examples/)
      * [Registry](/docs/languages/kotlin/registry/)
    - [PHP](/docs/languages/php/)
      * [Getting Started](/docs/languages/php/getting-started/)
      * [Instrumentation](/docs/languages/php/instrumentation/)
      * [Libraries](/docs/languages/php/libraries/ "Using instrumentation libraries")
      * [Exporters](/docs/languages/php/exporters/)
      * [Context](/docs/languages/php/context/)
      * [Propagation](/docs/languages/php/propagation/)
      * [Resources](/docs/languages/php/resources/)
      * [SDK](/docs/languages/php/sdk/)
      * [API](/docs/languages/php/api/ "API reference")
      * [Examples](/docs/languages/php/examples/)
      * [Registry](/docs/languages/php/registry/)
    - [Python](/docs/languages/python/)
      * [Getting Started](/docs/languages/python/getting-started/)
      * [Instrumentation](/docs/languages/python/instrumentation/)
      * [Libraries](/docs/languages/python/libraries/ "Using instrumentation libraries")
      * [Exporters](/docs/languages/python/exporters/)
      * [Propagation](/docs/languages/python/propagation/)
      * [Cookbook](/docs/languages/python/cookbook/)
      * [Distro](/docs/languages/python/distro/ "OpenTelemetry Distro")
      * [Using mypy](/docs/languages/python/mypy/)
      * [Benchmarks](/docs/languages/python/benchmarks/)
      * [API](/docs/languages/python/api/ "API reference")
      * [Examples](/docs/languages/python/examples/)
      * [Registry](/docs/languages/python/registry/)
    - [Ruby](/docs/languages/ruby/)
      * [Getting Started](/docs/languages/ruby/getting-started/)
      * [Instrumentation](/docs/languages/ruby/instrumentation/)
      * [Libraries](/docs/languages/ruby/libraries/ "Using instrumentation libraries")
      * [Exporters](/docs/languages/ruby/exporters/)
      * [Sampling](/docs/languages/ruby/sampling/)
      * [API](/docs/languages/ruby/api/ "API reference")
      * [Examples](/docs/languages/ruby/examples/)
      * [Registry](/docs/languages/ruby/registry/)
    - [Rust](/docs/languages/rust/)
      * [Getting Started](/docs/languages/rust/getting-started/)
      * [Libraries](/docs/languages/rust/libraries/ "Using instrumentation libraries")
      * [Exporters](/docs/languages/rust/exporters/)
      * [API](/docs/languages/rust/api/ "API reference")
      * [Examples](/docs/languages/rust/examples/)
      * [Registry](/docs/languages/rust/registry/)
    - [Swift](/docs/languages/swift/)
      * [Getting Started](/docs/languages/swift/getting-started/)
      * [Instrumentation](/docs/languages/swift/instrumentation/)
      * [Libraries](/docs/languages/swift/libraries/ "Instrumentation Libraries")
      * [Examples](/docs/languages/swift/examples/)
      * [Registry](/docs/languages/swift/registry/)
    - [Other](/docs/languages/other/ "Other languages")
  + [Platforms](/docs/platforms/ "Platforms and environments")
    - [Client-side Apps](/docs/platforms/client-apps/)
      * [Android](/docs/platforms/client-apps/android/)
      * [iOS](/docs/platforms/client-apps/ios/)
      * [Web](/docs/platforms/client-apps/web/)
    - [FaaS](/docs/platforms/faas/ "Functions as a Service")
      * [Lambda Auto-Instrumentation](/docs/platforms/faas/lambda-auto-instrument/)
      * [Lambda Collector Config](/docs/platforms/faas/lambda-collector/ "Lambda Collector Configuration")
      * [Lambda Manual Instrumentation](/docs/platforms/faas/lambda-manual-instrument/)
    - [Kubernetes](/docs/platforms/kubernetes/ "OpenTelemetry with Kubernetes")
      * [Getting Started](/docs/platforms/kubernetes/getting-started/)
      * [Collector](/docs/platforms/kubernetes/collector/ "OpenTelemetry Collector and Kubernetes")
        + [Components](/docs/platforms/kubernetes/collector/components/ "Important Components for Kubernetes")
      * [Helm Charts](/docs/platforms/kubernetes/helm/ "OpenTelemetry Helm Charts")
        + [Collector Chart](/docs/platforms/kubernetes/helm/collector/ "OpenTelemetry Collector Chart")
        + [Demo Chart](/docs/platforms/kubernetes/helm/demo/ "OpenTelemetry Demo Chart")
        + [Operator Chart](/docs/platforms/kubernetes/helm/operator/ "OpenTelemetry Operator Chart")
      * [Kubernetes Operator](/docs/platforms/kubernetes/operator/ "OpenTelemetry Operator for Kubernetes")
        + [Auto-instrumentation](/docs/platforms/kubernetes/operator/automatic/ "Injecting Auto-instrumentation")
        + [Horizontal Pod Autoscaling](/docs/platforms/kubernetes/operator/horizontal-pod-autoscaling/)
        + [Target Allocator](/docs/platforms/kubernetes/operator/target-allocator/)
        + [Troubleshooting](/docs/platforms/kubernetes/operator/troubleshooting/ "Troubleshooting the OpenTelemetry Operator for Kubernetes")
          - [Auto-instrumentation](/docs/platforms/kubernetes/operator/troubleshooting/automatic/)
          - [Prometheus Alerts Runbooks](/docs/platforms/kubernetes/operator/troubleshooting/prometheus-alerts-runbooks/)
          - [Target Allocator](/docs/platforms/kubernetes/operator/troubleshooting/target-allocator/)
  + [Zero-code Instrumentation](/docs/zero-code/)
    - [OBI](/docs/zero-code/obi/ "OpenTelemetry eBPF Instrumentation")
      * [Configure](/docs/zero-code/obi/configure/ "Configure OBI")
        + [Export modes](/docs/zero-code/obi/configure/export-modes/ "Configure OBI export modes")
        + [Global properties](/docs/zero-code/obi/configure/options/ "OBI global configuration properties")
        + [Export data](/docs/zero-code/obi/configure/export-data/ "Configure OBI Prometheus and OpenTelemetry data export")
        + [Service discovery](/docs/zero-code/obi/configure/service-discovery/ "Configure OBI service discovery")
        + [Metrics attributes](/docs/zero-code/obi/configure/metrics-traces-attributes/ "Configure OBI metrics and traces attributes")
        + [Filter data](/docs/zero-code/obi/configure/filter-metrics-traces/ "Filter metrics and traces by attribute values")
        + [Routes decorator](/docs/zero-code/obi/configure/routes-decorator/ "Configure OBI routes decorator")
        + [Metrics histograms](/docs/zero-code/obi/configure/metrics-histograms/ "Configure OBI Prometheus and OpenTelemetry metrics histograms")
        + [Sample traces](/docs/zero-code/obi/configure/sample-traces/ "Configure OBI OpenTelemetry trace sampling")
        + [Collector receiver](/docs/zero-code/obi/configure/collector-receiver/ "OBI as OpenTelemetry Collector receiver")
        + [Internal metrics reporter](/docs/zero-code/obi/configure/internal-metrics-reporter/ "Configure the OBI internal metrics reporter")
        + [Tune performance](/docs/zero-code/obi/configure/tune-performance/ "Configure OBI performance")
        + [YAML example](/docs/zero-code/obi/configure/example/ "OBI configuration YAML example")
      * [Network](/docs/zero-code/obi/network/ "Network metrics")
        + [Measure traffic between Cloud availability zones](/docs/zero-code/obi/network/inter-az/)
        + [Quickstart](/docs/zero-code/obi/network/quickstart/ "OBI network metrics quickstart")
        + [Configuration](/docs/zero-code/obi/network/config/ "OBI Network Metrics configuration options")
      * [Setup](/docs/zero-code/obi/setup/ "Set up OBI")
        + [Helm chart](/docs/zero-code/obi/setup/kubernetes-helm/ "Deploy OBI in Kubernetes with Helm")
        + [Docker](/docs/zero-code/obi/setup/docker/ "Run OBI as a Docker container")
        + [Kubernetes](/docs/zero-code/obi/setup/kubernetes/ "Deploy OBI in Kubernetes")
        + [Standalone](/docs/zero-code/obi/setup/standalone/ "Run OBI as a standalone process")
      * [Exported metrics](/docs/zero-code/obi/metrics/ "OBI exported metrics")
      * [Distributed traces](/docs/zero-code/obi/distributed-traces/ "Distributed traces with OBI")
      * [Request times](/docs/zero-code/obi/requesttime/ "Measuring total request times, instead of service times")
      * [Security](/docs/zero-code/obi/security/ "OBI security, permissions, and capabilities")
      * [Troubleshooting](/docs/zero-code/obi/troubleshooting/)
      * [Cilium compatibility](/docs/zero-code/obi/cilium-compatibility/ "OBI and Cilium compatibility")
      * [Metrics cardinality](/docs/zero-code/obi/cardinality/ "OBI metrics cardinality")
      * [Trace-log correlation](/docs/zero-code/obi/trace-log-correlation/)
    - [Go](/docs/zero-code/go/ "Go zero-code instrumentation")
      * [Auto SDK](/docs/zero-code/go/autosdk/ "Go Instrumentation Auto SDK")
    - [.NET](/docs/zero-code/dotnet/ ".NET zero-code instrumentation")
      * [Getting Started](/docs/zero-code/dotnet/getting-started/)
      * [Instrumentations](/docs/zero-code/dotnet/instrumentations/ "Available instrumentations")
      * [Configuration](/docs/zero-code/dotnet/configuration/ "Configuration and settings")
      * [Custom instrumentation](/docs/zero-code/dotnet/custom/ "Create custom traces and metrics")
      * [NuGet Packages](/docs/zero-code/dotnet/nuget-packages/ "Using the OpenTelemetry.AutoInstrumentation NuGet packages")
      * [Troubleshooting](/docs/zero-code/dotnet/troubleshooting/ "Troubleshooting .NET automatic instrumentation issues")
    - [PHP](/docs/zero-code/php/ "PHP zero-code instrumentation")
    - [Python](/docs/zero-code/python/ "Python zero-code instrumentation")
      * [Configuration](/docs/zero-code/python/configuration/ "Agent Configuration")
      * [Example](/docs/zero-code/python/example/ "Auto-Instrumentation Example")
      * [Logs Example](/docs/zero-code/python/logs-example/ "Logs Auto-Instrumentation Example")
      * [Operator](/docs/zero-code/python/operator/ "Using the OpenTelemetry Operator to Inject Auto-Instrumentation")
      * [Troubleshooting](/docs/zero-code/python/troubleshooting/ "Troubleshooting Python automatic instrumentation issues")
    - [Java](/docs/zero-code/java/ "Java zero-code instrumentation")
      * [Agent](/docs/zero-code/java/agent/ "Java Agent")
        + [Getting started](/docs/zero-code/java/agent/getting-started/)
        + [Configuration](/docs/zero-code/java/agent/configuration/)
        + [Declarative configuration](/docs/zero-code/java/agent/declarative-configuration/ "Java Agent Declarative configuration")
        + [Supported Libraries](/docs/zero-code/java/agent/supported-libraries/)
        + [Suppressing instrumentation](/docs/zero-code/java/agent/disable/ "Suppressing specific instrumentation")
        + [Annotations](/docs/zero-code/java/agent/annotations/)
        + [Extend with the API](/docs/zero-code/java/agent/api/ "Extending instrumentations with the API")
        + [Instrumentation config](/docs/zero-code/java/agent/instrumentation/ "Instrumentation configuration")
          - [HTTP](/docs/zero-code/java/agent/instrumentation/http/ "HTTP instrumentation configuration")
        + [App server config](/docs/zero-code/java/agent/server-config/ "Application server configuration")
        + [Extensions](/docs/zero-code/java/agent/extensions/)
        + [Performance](/docs/zero-code/java/agent/performance/)
      * [Quarkus](/docs/zero-code/java/quarkus/ "Quarkus instrumentation")
      * [Spring Boot starter](/docs/zero-code/java/spring-boot-starter/)
        + [Getting started](/docs/zero-code/java/spring-boot-starter/getting-started/)
        + [Extend with the API](/docs/zero-code/java/spring-boot-starter/api/ "Extending instrumentations with the API")
        + [SDK configuration](/docs/zero-code/java/spring-boot-starter/sdk-configuration/)
        + [Out of the box instrumentation](/docs/zero-code/java/spring-boot-starter/out-of-the-box-instrumentation/)
        + [Annotations](/docs/zero-code/java/spring-boot-starter/annotations/)
        + [Additional instrumentation](/docs/zero-code/java/spring-boot-starter/additional-instrumentations/)
        + [Other Spring autoconfiguration](/docs/zero-code/java/spring-boot-starter/other-spring-autoconfig/)
    - [JavaScript](/docs/zero-code/js/ "JavaScript zero-code instrumentation")
      * [Configuration](/docs/zero-code/js/configuration/ "Zero-Code Instrumentation Configuration")
  + [Collector](/docs/collector/)
    - [Quick start](/docs/collector/quick-start/)
    - [Install](/docs/collector/install/ "Install the Collector")
      * [Docker](/docs/collector/install/docker/ "Install the Collector with Docker")
      * [Kubernetes](/docs/collector/install/kubernetes/ "Install the Collector with Kubernetes")
      * [Binary](/docs/collector/install/binary/ "Install from a Collector binary")
        + [Linux](/docs/collector/install/binary/linux/ "Install the Collector on Linux")
        + [macOS](/docs/collector/install/binary/macos/ "Install the Collector on macOS")
        + [Windows](/docs/collector/install/binary/windows/ "Install the Collector on Windows")
    - [Deploy](/docs/collector/deploy/ "Deploy the Collector")
      * [Agent pattern](/docs/collector/deploy/agent/ "Agent deployment pattern")
      * [Gateway pattern](/docs/collector/deploy/gateway/ "Gateway deployment pattern")
      * [Other patterns](/docs/collector/deploy/other/ "Other deployment patterns")
        + [No Collector](/docs/collector/deploy/other/no-collector/)
    - [Configuration](/docs/collector/configuration/)
    - [Components](/docs/collector/components/)
      * [Receivers](/docs/collector/components/receiver/)
      * [Processors](/docs/collector/components/processor/)
      * [Exporters](/docs/collector/components/exporter/)
      * [Connectors](/docs/collector/components/connector/)
      * [Extensions](/docs/collector/components/extension/)
    - [Management](/docs/collector/management/)
    - [Distributions](/docs/collector/distributions/)
    - [Internal telemetry](/docs/collector/internal-telemetry/)
    - [Troubleshooting](/docs/collector/troubleshooting/)
    - [Scaling the Collector](/docs/collector/scaling/)
    - [Transforming telemetry](/docs/collector/transforming-telemetry/)
    - [Architecture](/docs/collector/architecture/)
    - [Extend](/docs/collector/extend/ "Extend the Collector")
      * [Build from source](/docs/collector/extend/build-from-source/)
      * [Build a custom Collector](/docs/collector/extend/ocb/ "Build a custom Collector with OpenTelemetry Collector Builder")
      * [Build custom components](/docs/collector/extend/custom-component/)
        + [Receivers](/docs/collector/extend/custom-component/receiver/ "Build a receiver")
        + [Connectors](/docs/collector/extend/custom-component/connector/ "Build a connector")
        + [Extensions](/docs/collector/extend/custom-component/extension/ "Build an extension")
          - [Authenticator](/docs/collector/extend/custom-component/extension/authenticator/ "Build an authenticator extension")
    - [Benchmarks](/docs/collector/benchmarks/)
    - [Registry](/docs/collector/registry/)
    - [Resiliency](/docs/collector/resiliency/)
  + [Blueprints and reference implementations](/docs/guidance/)
    - [Blueprints](/docs/guidance/blueprints/)
    - [Reference implementations](/docs/guidance/reference-implementations/)
  + [Compatibility](/docs/compatibility/)
    - [Migration](/docs/compatibility/migration/)
      * [OpenTracing](/docs/compatibility/migration/opentracing/ "Migrating from OpenTracing")
      * [OpenCensus](/docs/compatibility/migration/opencensus/ "Migrating from OpenCensus")
  + [Specs](/docs/specs/ "Specifications")
    - [Status](/docs/specs/status/ "Specification Status Summary")
    - [OTel 1.55.0](/docs/specs/otel/ "OpenTelemetry Specification 1.55.0")
      * [Overview](/docs/specs/otel/overview/)
      * [Baggage](/docs/specs/otel/baggage/)
        + [API](/docs/specs/otel/baggage/api/ "Baggage API")
      * [Client Design Principles](/docs/specs/otel/library-guidelines/ "OpenTelemetry Client Design Principles")
      * [Common concepts](/docs/specs/otel/common/ "Common specification concepts")
        + [Attribute Naming](/docs/specs/otel/common/attribute-naming/)
        + [Attribute Requirement Levels](/docs/specs/otel/common/attribute-requirement-level/ "Attribute Requirement Levels for Semantic Conventions")
        + [Instrumentation Scope](/docs/specs/otel/common/instrumentation-scope/)
        + [Mapping to AnyValue](/docs/specs/otel/common/attribute-type-mapping/ "Mapping Arbitrary Data to OTLP AnyValue")
        + [Mapping to non-OTLP Formats](/docs/specs/otel/common/mapping-to-non-otlp/ "OpenTelemetry Transformation to non-OTLP Formats")
      * [Compatibility](/docs/specs/otel/compatibility/)
        + [OpenCensus](/docs/specs/otel/compatibility/opencensus/ "OpenCensus Compatibility")
        + [OpenTracing](/docs/specs/otel/compatibility/opentracing/ "OpenTracing Compatibility")
        + [Prometheus and OpenMetrics](/docs/specs/otel/compatibility/prometheus_and_openmetrics/ "Prometheus and OpenMetrics Compatibility")
        + [Trace Context in non-OTLP Log Formats](/docs/specs/otel/compatibility/logging_trace_context/)
      * [Configuration](/docs/specs/otel/configuration/)
        + [API](/docs/specs/otel/configuration/api/ "Instrumentation Configuration API")
        + [Data Model](/docs/specs/otel/configuration/data-model/ "Configuration Data Model")
        + [SDK](/docs/specs/otel/configuration/sdk/ "Configuration SDK")
        + [Common](/docs/specs/otel/configuration/common/ "Common Configuration Specification")
        + [Env var](/docs/specs/otel/configuration/sdk-environment-variables/ "Environment Variable Specification")
        + [Supplementary Guidelines](/docs/specs/otel/configuration/supplementary-guidelines/)
      * [Context](/docs/specs/otel/context/)
        + [Environment Variables as Context Propagation Carriers](/docs/specs/otel/context/env-carriers/)
        + [Propagators API](/docs/specs/otel/context/api-propagators/)
      * [Definitions of Document Statuses](/docs/specs/otel/document-status/)
      * [Entities](/docs/specs/otel/entities/)
        + [Data Model](/docs/specs/otel/entities/data-model/ "Entity Data Model")
        + [Entity Propagation](/docs/specs/otel/entities/entity-propagation/)
      * [Error handling in OpenTelemetry](/docs/specs/otel/error-handling/)
      * [Glossary](/docs/specs/otel/glossary/)
      * [Logs](/docs/specs/otel/logs/ "OpenTelemetry Logging")
        + [API](/docs/specs/otel/logs/api/ "Logs API")
        + [Data Model](/docs/specs/otel/logs/data-model/ "Logs Data Model")
        + [SDK](/docs/specs/otel/logs/sdk/ "Logs SDK")
        + [Data Model Appendix](/docs/specs/otel/logs/data-model-appendix/)
        + [Exporters](/docs/specs/otel/logs/sdk_exporters/ "Logs Exporters")
          - [Stdout](/docs/specs/otel/logs/sdk_exporters/stdout/ "Logs Exporter - Standard output")
        + [No-Op](/docs/specs/otel/logs/noop/ "Logs API No-Op Implementation")
        + [Supplementary Guidelines](/docs/specs/otel/logs/supplementary-guidelines/)
      * [Metrics](/docs/specs/otel/metrics/ "OpenTelemetry Metrics")
        + [API](/docs/specs/otel/metrics/api/ "Metrics API")
        + [Data Model](/docs/specs/otel/metrics/data-model/ "Metrics Data Model")
        + [SDK](/docs/specs/otel/metrics/sdk/ "Metrics SDK")
        + [Exporters](/docs/specs/otel/metrics/sdk_exporters/ "Metrics Exporters")
          - [In-memory](/docs/specs/otel/metrics/sdk_exporters/in-memory/ "Metrics Exporter - In-memory")
          - [OTLP](/docs/specs/otel/metrics/sdk_exporters/otlp/ "Metrics Exporter - OTLP")
          - [Prometheus](/docs/specs/otel/metrics/sdk_exporters/prometheus/ "Metrics Exporter - Prometheus")
          - [Stdout](/docs/specs/otel/metrics/sdk_exporters/stdout/ "Metrics Exporter - Standard output")
        + [Metric Requirement Levels](/docs/specs/otel/metrics/metric-requirement-level/ "Metric Requirement Levels for Semantic Conventions")
        + [No-Op](/docs/specs/otel/metrics/noop/ "Metrics No-Op API Implementation")
        + [Supplementary Guidelines](/docs/specs/otel/metrics/supplementary-guidelines/)
      * [Performance and Blocking of OpenTelemetry API](/docs/specs/otel/performance/)
      * [Performance Benchmark of OpenTelemetry API](/docs/specs/otel/performance-benchmark/)
      * [Profiles](/docs/specs/otel/profiles/ "OpenTelemetry Profiles")
        + [Mappings](/docs/specs/otel/profiles/mappings/)
        + [Pprof](/docs/specs/otel/profiles/pprof/)
      * [Project Package Layout](/docs/specs/otel/library-layout/ "OpenTelemetry Project Package Layout")
      * [Protocol](/docs/specs/otel/protocol/ "OpenTelemetry Protocol")
        + [Specification 1.10.0](/docs/specs/otel/protocol/otlp/ "OpenTelemetry Protocol Specification")
        + [Design Goals](/docs/specs/otel/protocol/design-goals/ "Design Goals for OpenTelemetry Wire Protocol")
        + [Exporter](/docs/specs/otel/protocol/exporter/ "OpenTelemetry Protocol Exporter")
        + [File Exporter](/docs/specs/otel/protocol/file-exporter/ "OpenTelemetry Protocol File Exporter")
        + [Requirements](/docs/specs/otel/protocol/requirements/ "OpenTelemetry Protocol Requirements")
      * [Resource](/docs/specs/otel/resource/)
        + [Data Model](/docs/specs/otel/resource/data-model/ "Resource Data Model")
        + [SDK](/docs/specs/otel/resource/sdk/ "Resource SDK")
      * [Schemas](/docs/specs/otel/schemas/ "Telemetry Schemas")
        + [1.0.0](/docs/specs/otel/schemas/file_format_v1.0.0/ "Schema File Format 1.0.0")
        + [1.1.0](/docs/specs/otel/schemas/file_format_v1.1.0/ "Schema File Format 1.1.0")
      * [Semantic Conventions](/docs/specs/otel/semantic-conventions/)
      * [Specification Principles](/docs/specs/otel/specification-principles/)
      * [Telemetry Stability](/docs/specs/otel/telemetry-stability/)
      * [The OpenTelemetry approach to upgrading](/docs/specs/otel/upgrading/)
      * [Trace](/docs/specs/otel/trace/)
        + [API](/docs/specs/otel/trace/api/ "Tracing API")
        + [SDK](/docs/specs/otel/trace/sdk/ "Tracing SDK")
        + [Exceptions](/docs/specs/otel/trace/exceptions/)
        + [Exporters](/docs/specs/otel/trace/sdk_exporters/ "Trace Exporters")
          - [Stdout](/docs/specs/otel/trace/sdk_exporters/stdout/ "Span Exporter - Standard output")
          - [Zipkin](/docs/specs/otel/trace/sdk_exporters/zipkin/ "OpenTelemetry to Zipkin Transformation")
        + [Probability Sampling](/docs/specs/otel/trace/tracestate-probability-sampling/ "TraceState: Probability Sampling")
        + [TraceState](/docs/specs/otel/trace/tracestate-handling/ "TraceState Handling")
      * [Vendors](/docs/specs/otel/vendors/)
      * [Versioning and stability for OpenTelemetry clients](/docs/specs/otel/versioning-and-stability/)
    - [OTLP 1.10.0](/docs/specs/otlp/ "OTLP Specification 1.10.0")
    - [OpAMP](/docs/specs/opamp/ "Open Agent Management Protocol")
    - [Semantic conventions 1.40.0](/docs/specs/semconv/ "OpenTelemetry semantic conventions 1.40.0")
      * [Registry](/docs/specs/semconv/registry/)
        + [Attributes](/docs/specs/semconv/registry/attributes/ "Attribute registry")
          - [Android](/docs/specs/semconv/registry/attributes/android/)
          - [App](/docs/specs/semconv/registry/attributes/app/)
          - [Artifact](/docs/specs/semconv/registry/attributes/artifact/)
          - [Aspnetcore](/docs/specs/semconv/registry/attributes/aspnetcore/)
          - [AWS](/docs/specs/semconv/registry/attributes/aws/)
          - [Azure](/docs/specs/semconv/registry/attributes/azure/)
          - [Browser](/docs/specs/semconv/registry/attributes/browser/)
          - [Cassandra](/docs/specs/semconv/registry/attributes/cassandra/)
          - [CICD](/docs/specs/semconv/registry/attributes/cicd/)
          - [Client](/docs/specs/semconv/registry/attributes/client/)
          - [Cloud](/docs/specs/semconv/registry/attributes/cloud/)
          - [CloudEvents](/docs/specs/semconv/registry/attributes/cloudevents/)
          - [CloudFoundry](/docs/specs/semconv/registry/attributes/cloudfoundry/)
          - [Code](/docs/specs/semconv/registry/attributes/code/)
          - [Container](/docs/specs/semconv/registry/attributes/container/)
          - [CPU](/docs/specs/semconv/registry/attributes/cpu/)
          - [CPython](/docs/specs/semconv/registry/attributes/cpython/)
          - [DB](/docs/specs/semconv/registry/attributes/db/)
          - [Deployment](/docs/specs/semconv/registry/attributes/deployment/)
          - [Destination](/docs/specs/semconv/registry/attributes/destination/)
          - [Device](/docs/specs/semconv/registry/attributes/device/)
          - [Disk](/docs/specs/semconv/registry/attributes/disk/)
          - [DNS](/docs/specs/semconv/registry/attributes/dns/)
          - [Dotnet](/docs/specs/semconv/registry/attributes/dotnet/)
          - [Elasticsearch](/docs/specs/semconv/registry/attributes/elasticsearch/)
          - [Enduser](/docs/specs/semconv/registry/attributes/enduser/)
          - [Error](/docs/specs/semconv/registry/attributes/error/)
          - [Event](/docs/specs/semconv/registry/attributes/event/)
          - [Exception](/docs/specs/semconv/registry/attributes/exception/)
          - [Faas](/docs/specs/semconv/registry/attributes/faas/)
          - [Feature flag](/docs/specs/semconv/registry/attributes/feature-flag/)
          - [File](/docs/specs/semconv/registry/attributes/file/)
          - [GCP](/docs/specs/semconv/registry/attributes/gcp/)
          - [Gen AI](/docs/specs/semconv/registry/attributes/gen-ai/)
          - [Geo](/docs/specs/semconv/registry/attributes/geo/)
          - [Go](/docs/specs/semconv/registry/attributes/go/)
          - [GraphQL](/docs/specs/semconv/registry/attributes/graphql/)
          - [Hardware](/docs/specs/semconv/registry/attributes/hardware/)
          - [Heroku](/docs/specs/semconv/registry/attributes/heroku/)
          - [Host](/docs/specs/semconv/registry/attributes/host/)
          - [HTTP](/docs/specs/semconv/registry/attributes/http/)
          - [iOS](/docs/specs/semconv/registry/attributes/ios/)
          - [JSONRPC](/docs/specs/semconv/registry/attributes/jsonrpc/)
          - [JVM](/docs/specs/semconv/registry/attributes/jvm/)
          - [K8s](/docs/specs/semconv/registry/attributes/k8s/)
          - [Linux](/docs/specs/semconv/registry/attributes/linux/)
          - [Log](/docs/specs/semconv/registry/attributes/log/)
          - [Mainframe](/docs/specs/semconv/registry/attributes/mainframe/)
          - [MCP](/docs/specs/semconv/registry/attributes/mcp/)
          - [Messaging](/docs/specs/semconv/registry/attributes/messaging/)
          - [Network](/docs/specs/semconv/registry/attributes/network/)
          - [NFS](/docs/specs/semconv/registry/attributes/nfs/)
          - [NodeJS](/docs/specs/semconv/registry/attributes/nodejs/)
          - [OCI](/docs/specs/semconv/registry/attributes/oci/)
          - [ONC RPC](/docs/specs/semconv/registry/attributes/onc-rpc/)
          - [OpenAI](/docs/specs/semconv/registry/attributes/openai/)
          - [Openshift](/docs/specs/semconv/registry/attributes/openshift/)
          - [OpenTracing](/docs/specs/semconv/registry/attributes/opentracing/)
          - [Oracle cloud](/docs/specs/semconv/registry/attributes/oracle-cloud/)
          - [OracleDB](/docs/specs/semconv/registry/attributes/oracledb/)
          - [OS](/docs/specs/semconv/registry/attributes/os/)
          - [OTel](/docs/specs/semconv/registry/attributes/otel/)
          - [Peer](/docs/specs/semconv/registry/attributes/peer/)
          - [Pprof](/docs/specs/semconv/registry/attributes/pprof/)
          - [Process](/docs/specs/semconv/registry/attributes/process/)
          - [Profile](/docs/specs/semconv/registry/attributes/profile/)
          - [RPC](/docs/specs/semconv/registry/attributes/rpc/)
          - [Security rule](/docs/specs/semconv/registry/attributes/security-rule/)
          - [Server](/docs/specs/semconv/registry/attributes/server/)
          - [Service](/docs/specs/semconv/registry/attributes/service/)
          - [Session](/docs/specs/semconv/registry/attributes/session/)
          - [SignalR](/docs/specs/semconv/registry/attributes/signalr/)
          - [Source](/docs/specs/semconv/registry/attributes/source/)
          - [System](/docs/specs/semconv/registry/attributes/system/)
          - [Telemetry](/docs/specs/semconv/registry/attributes/telemetry/)
          - [Test](/docs/specs/semconv/registry/attributes/test/)
          - [Thread](/docs/specs/semconv/registry/attributes/thread/)
          - [TLS](/docs/specs/semconv/registry/attributes/tls/)
          - [URL](/docs/specs/semconv/registry/attributes/url/)
          - [User](/docs/specs/semconv/registry/attributes/user/)
          - [User agent](/docs/specs/semconv/registry/attributes/user-agent/)
          - [V8js](/docs/specs/semconv/registry/attributes/v8js/)
          - [VCS](/docs/specs/semconv/registry/attributes/vcs/)
          - [Webengine](/docs/specs/semconv/registry/attributes/webengine/)
          - [zOS](/docs/specs/semconv/registry/attributes/zos/)
        + [Entities](/docs/specs/semconv/registry/entities/ "Entity registry")
          - [Android](/docs/specs/semconv/registry/entities/android/)
          - [App](/docs/specs/semconv/registry/entities/app/)
          - [AWS](/docs/specs/semconv/registry/entities/aws/)
          - [Browser](/docs/specs/semconv/registry/entities/browser/)
          - [CICD](/docs/specs/semconv/registry/entities/cicd/)
          - [Cloud](/docs/specs/semconv/registry/entities/cloud/)
          - [CloudFoundry](/docs/specs/semconv/registry/entities/cloudfoundry/)
          - [Container](/docs/specs/semconv/registry/entities/container/)
          - [Deployment](/docs/specs/semconv/registry/entities/deployment/)
          - [Device](/docs/specs/semconv/registry/entities/device/)
          - [Faas](/docs/specs/semconv/registry/entities/faas/)
          - [GCP](/docs/specs/semconv/registry/entities/gcp/)
          - [Heroku](/docs/specs/semconv/registry/entities/heroku/)
          - [Host](/docs/specs/semconv/registry/entities/host/)
          - [K8s](/docs/specs/semconv/registry/entities/k8s/)
          - [Openshift](/docs/specs/semconv/registry/entities/openshift/)
          - [OS](/docs/specs/semconv/registry/entities/os/)
          - [OTel](/docs/specs/semconv/registry/entities/otel/)
          - [Process](/docs/specs/semconv/registry/entities/process/)
          - [Service](/docs/specs/semconv/registry/entities/service/)
          - [Telemetry](/docs/specs/semconv/registry/entities/telemetry/)
          - [VCS](/docs/specs/semconv/registry/entities/vcs/)
          - [Webengine](/docs/specs/semconv/registry/entities/webengine/)
          - [zOS](/docs/specs/semconv/registry/entities/zos/)
      * [General](/docs/specs/semconv/general/ "General semantic conventions")
        + [Attribute requirement levels](/docs/specs/semconv/general/attribute-requirement-level/)
        + [Attributes](/docs/specs/semconv/general/attributes/ "General attributes")
        + [Events](/docs/specs/semconv/general/events/ "Semantic conventions for events")
        + [Logs](/docs/specs/semconv/general/logs/ "General logs attributes")
        + [Metric requirement levels](/docs/specs/semconv/general/metric-requirement-level/)
        + [Metrics](/docs/specs/semconv/general/metrics/ "Metrics semantic conventions")
        + [Naming](/docs/specs/semconv/general/naming/)
        + [Profiles](/docs/specs/semconv/general/profiles/ "Profiles attributes")
        + [Recording errors](/docs/specs/semconv/general/recording-errors/)
        + [Semantic convention groups](/docs/specs/semconv/general/semantic-convention-groups/)
        + [Session](/docs/specs/semconv/general/session/ "Semantic conventions for session")
        + [Trace](/docs/specs/semconv/general/trace/ "Trace semantic conventions")
        + [Tracing compatibility](/docs/specs/semconv/general/trace-compatibility/ "Semantic conventions for tracing compatibility components")
      * [.NET](/docs/specs/semconv/dotnet/ "Semantic conventions for .NET")
        + [ASP.NET Core](/docs/specs/semconv/dotnet/dotnet-aspnetcore-metrics/ "Semantic conventions for ASP.NET Core metrics")
        + [DNS](/docs/specs/semconv/dotnet/dotnet-dns-metrics/ "Semantic conventions for DNS metrics emitted by .NET")
        + [HTTP](/docs/specs/semconv/dotnet/dotnet-http-metrics/ "Semantic conventions for HTTP client and server metrics emitted by .NET")
        + [HTTP request and connection spans](/docs/specs/semconv/dotnet/dotnet-network-traces/ "Semantic Conventions for network spans emitted by .NET")
        + [Kestrel](/docs/specs/semconv/dotnet/dotnet-kestrel-metrics/ "Semantic conventions for Kestrel web server metrics")
        + [SignalR](/docs/specs/semconv/dotnet/dotnet-signalr-metrics/ "Semantic conventions for SignalR server metrics")
      * [App](/docs/specs/semconv/app/ "Semantic conventions for Apps")
        + [Events](/docs/specs/semconv/app/app-events/ "App Events")
      * [Azure](/docs/specs/semconv/azure/ "Semantic conventions for Azure resource logs")
        + [Events](/docs/specs/semconv/azure/azure-events/ "Semantic conventions for Azure resource log events")
      * [Browser](/docs/specs/semconv/browser/ "Semantic conventions for Browser")
        + [Events](/docs/specs/semconv/browser/browser-events/ "Semantic conventions for browser events")
      * [CICD](/docs/specs/semconv/cicd/ "Semantic conventions for CICD")
        + [Logs](/docs/specs/semconv/cicd/cicd-logs/ "Semantic conventions for CICD logs")
        + [Metrics](/docs/specs/semconv/cicd/cicd-metrics/ "Semantic conventions for CICD metrics")
        + [Spans](/docs/specs/semconv/cicd/cicd-spans/ "Semantic conventions for CICD spans")
      * [CLI programs](/docs/specs/semconv/cli/ "Semantic conventions for CLI programs")
        + [Spans](/docs/specs/semconv/cli/cli-spans/ "Semantic conventions for CLI (command line interface) programs")
      * [Cloud providers](/docs/specs/semconv/cloud-providers/ "Semantic conventions for cloud providers")
        + [AWS SDK](/docs/specs/semconv/cloud-providers/aws-sdk/ "Semantic conventions for AWS SDK client spans")
      * [CloudEvents](/docs/specs/semconv/cloudevents/ "Semantic conventions for CloudEvents")
        + [Spans](/docs/specs/semconv/cloudevents/cloudevents-spans/ "Semantic conventions for CloudEvents spans")
      * [Database](/docs/specs/semconv/db/ "Semantic conventions for database calls and systems")
        + [Cassandra](/docs/specs/semconv/db/cassandra/ "Semantic conventions for Cassandra client operations")
        + [Cosmos DB](/docs/specs/semconv/db/cosmosdb/ "Semantic conventions for Microsoft Azure Cosmos DB client operations")
        + [CouchDB](/docs/specs/semconv/db/couchdb/ "Semantic conventions for CouchDB client operations")
        + [DynamoDB](/docs/specs/semconv/db/dynamodb/ "Semantic conventions for AWS DynamoDB client operations")
        + [Elasticsearch](/docs/specs/semconv/db/elasticsearch/ "Semantic conventions for Elasticsearch client operations")
        + [Exceptions](/docs/specs/semconv/db/database-exceptions/ "Semantic conventions for database exceptions")
        + [HBase](/docs/specs/semconv/db/hbase/ "Semantic conventions for HBase client operations")
        + [MariaDB](/docs/specs/semconv/db/mariadb/ "Semantic conventions for MariaDB client operations")
        + [Metrics](/docs/specs/semconv/db/database-metrics/ "Semantic conventions for database client metrics")
        + [MongoDB](/docs/specs/semconv/db/mongodb/ "Semantic conventions for MongoDB client operations")
        + [MySQL](/docs/specs/semconv/db/mysql/ "Semantic conventions for MySQL client operations")
        + [Oracle Database](/docs/specs/semconv/db/oracledb/ "Semantic conventions for Oracle Database")
        + [PostgreSQL](/docs/specs/semconv/db/postgresql/ "Semantic conventions for PostgreSQL client operations")
        + [Redis](/docs/specs/semconv/db/redis/ "Semantic conventions for Redis client operations")
        + [Spans](/docs/specs/semconv/db/database-spans/ "Semantic conventions for database client spans")
        + [SQL](/docs/specs/semconv/db/sql/ "Semantic conventions for SQL databases client operations")
        + [SQL Server](/docs/specs/semconv/db/sql-server/ "Semantic conventions for Microsoft SQL Server client operations")
      * [DNS](/docs/specs/semconv/dns/ "Semantic conventions for DNS")
        + [Metrics](/docs/specs/semconv/dns/dns-metrics/ "Semantic conventions for DNS queries")
      * [Exceptions](/docs/specs/semconv/exceptions/ "Semantic conventions for exceptions")
        + [Logs](/docs/specs/semconv/exceptions/exceptions-logs/ "Semantic conventions for exceptions in logs")
        + [Spans](/docs/specs/semconv/exceptions/exceptions-spans/ "Semantic conventions for exceptions on spans")
      * [FaaS](/docs/specs/semconv/faas/ "Semantic conventions for Function-as-a-Service")
        + [AWS Lambda](/docs/specs/semconv/faas/aws-lambda/ "Instrumenting AWS Lambda")
        + [Metrics](/docs/specs/semconv/faas/faas-metrics/ "Semantic conventions for FaaS metrics")
        + [Spans](/docs/specs/semconv/faas/faas-spans/ "Semantic conventions for FaaS spans")
      * [Feature flags](/docs/specs/semconv/feature-flags/ "Semantic conventions for feature flags")
        + [Events](/docs/specs/semconv/feature-flags/feature-flags-events/ "Semantic conventions for feature flags in events")
      * [Generative AI](/docs/specs/semconv/gen-ai/ "Semantic conventions for generative AI systems")
        + [Agent spans](/docs/specs/semconv/gen-ai/gen-ai-agent-spans/ "Semantic Conventions for GenAI agent and framework spans")
        + [Anthropic](/docs/specs/semconv/gen-ai/anthropic/ "Semantic conventions for Anthropic client operations")
        + [AWS Bedrock](/docs/specs/semconv/gen-ai/aws-bedrock/ "Semantic conventions for AWS Bedrock operations")
        + [Azure AI Inference](/docs/specs/semconv/gen-ai/azure-ai-inference/ "Semantic conventions for Azure AI Inference client operations")
        + [Events](/docs/specs/semconv/gen-ai/gen-ai-events/ "Semantic conventions for Generative AI events")
        + [LLM call examples](/docs/specs/semconv/gen-ai/non-normative/examples-llm-calls/)
        + [Metrics](/docs/specs/semconv/gen-ai/gen-ai-metrics/ "Semantic conventions for generative AI metrics")
        + [Model Context Protocol](/docs/specs/semconv/gen-ai/mcp/ "Semantic conventions for Model Context Protocol (MCP)")
        + [OpenAI](/docs/specs/semconv/gen-ai/openai/ "Semantic conventions for OpenAI client operations")
        + [Spans](/docs/specs/semconv/gen-ai/gen-ai-spans/ "Semantic conventions for generative client AI spans")
      * [GraphQL](/docs/specs/semconv/graphql/ "Semantic conventions for GraphQL")
        + [GraphQL server](/docs/specs/semconv/graphql/graphql-spans/ "Semantic conventions for GraphQL server spans")
      * [Hardware](/docs/specs/semconv/hardware/ "Semantic conventions for hardware")
        + [Battery](/docs/specs/semconv/hardware/battery/ "Semantic conventions for battery metrics")
        + [CPU](/docs/specs/semconv/hardware/cpu/ "Semantic conventions for CPU metrics")
        + [Disk Controller](/docs/specs/semconv/hardware/disk-controller/ "Semantic conventions for disk controller metrics")
        + [Enclosure](/docs/specs/semconv/hardware/enclosure/ "Semantic conventions for enclosure metrics")
        + [Fan](/docs/specs/semconv/hardware/fan/ "Semantic conventions for fan metrics")
        + [GPU](/docs/specs/semconv/hardware/gpu/ "Semantic conventions for GPU metrics")
        + [Logical Disk](/docs/specs/semconv/hardware/logical-disk/ "Semantic conventions for logical disk metrics")
        + [Memory](/docs/specs/semconv/hardware/memory/ "Semantic conventions for memory metrics")
        + [Metrics](/docs/specs/semconv/hardware/common/ "Semantic conventions for common hardware metrics")
        + [Network](/docs/specs/semconv/hardware/network/ "Semantic conventions for network metrics")
        + [Physical Disk](/docs/specs/semconv/hardware/physical-disk/ "Semantic conventions for physical disk metrics")
        + [Physical host](/docs/specs/semconv/hardware/host/ "Semantic conventions for physical host metrics")
        + [Power Supply](/docs/specs/semconv/hardware/power-supply/ "Semantic conventions for power supply metrics")
        + [Tape Drive](/docs/specs/semconv/hardware/tape-drive/ "Semantic conventions for tape drive metrics")
        + [Temperature](/docs/specs/semconv/hardware/temperature/ "Semantic conventions for temperature metrics")
        + [Voltage](/docs/specs/semconv/hardware/voltage/ "Semantic conventions for voltage metrics")
      * [How to write conventions](/docs/specs/semconv/how-to-write-conventions/ "How to write semantic conventions")
        + [Resource and Entities](/docs/specs/semconv/how-to-write-conventions/resource-and-entities/)
        + [Status Metrics](/docs/specs/semconv/how-to-write-conventions/status-metrics/ "State Metrics")
        + [T-shaped Signals](/docs/specs/semconv/how-to-write-conventions/t-shaped-signals/)
      * [HTTP](/docs/specs/semconv/http/ "Semantic conventions for HTTP")
        + [Exceptions](/docs/specs/semconv/http/http-exceptions/ "Semantic conventions for HTTP exceptions")
        + [Metrics](/docs/specs/semconv/http/http-metrics/ "Semantic conventions for HTTP metrics")
        + [Spans](/docs/specs/semconv/http/http-spans/ "Semantic conventions for HTTP spans")
      * [Messaging](/docs/specs/semconv/messaging/ "Semantic conventions for messaging systems")
        + [AWS SNS](/docs/specs/semconv/messaging/sns/ "Semantic conventions for AWS SNS")
        + [AWS SQS](/docs/specs/semconv/messaging/sqs/ "Semantic conventions for AWS SQS")
        + [Azure](/docs/specs/semconv/messaging/azure-messaging/ "Semantic conventions for Azure messaging systems")
        + [Google Cloud Pub/Sub](/docs/specs/semconv/messaging/gcp-pubsub/ "Semantic conventions for Google Cloud Pub/Sub")
        + [Kafka](/docs/specs/semconv/messaging/kafka/ "Semantic conventions for Kafka")
        + [Metrics](/docs/specs/semconv/messaging/messaging-metrics/ "Semantic conventions for messaging client metrics")
        + [RabbitMQ](/docs/specs/semconv/messaging/rabbitmq/ "Semantic conventions for RabbitMQ")
        + [RocketMQ](/docs/specs/semconv/messaging/rocketmq/ "Semantic conventions for RocketMQ")
        + [Spans](/docs/specs/semconv/messaging/messaging-spans/ "Semantic conventions for messaging spans")
      * [Mobile](/docs/specs/semconv/mobile/ "Semantic conventions for mobile platform")
        + [Events](/docs/specs/semconv/mobile/mobile-events/ "Semantic conventions for mobile events")
      * [NFS](/docs/specs/semconv/nfs/ "Semantic conventions for NFS")
        + [NFS](/docs/specs/semconv/nfs/nfs-metrics/ "Semantic conventions for NFS metrics")
      * [Non-normative](/docs/specs/semconv/non-normative/ "Non-normative supplementary information")
        + [Code attributes migration](/docs/specs/semconv/non-normative/code-attrs-migration/ "Code attributes semantic convention stability migration guide")
        + [Compatibility](/docs/specs/semconv/non-normative/compatibility/)
          - [AWS](/docs/specs/semconv/non-normative/compatibility/aws/ "Compatibility considerations for AWS")
          - [gRPC](/docs/specs/semconv/non-normative/compatibility/grpc/ "Compatibility between OpenTelemetry and gRPC semantic conventions")
        + [Database migration](/docs/specs/semconv/non-normative/db-migration/ "Database semantic convention stability migration guide")
        + [Generating semantic convention libraries](/docs/specs/semconv/non-normative/code-generation/)
        + [HTTP migration](/docs/specs/semconv/non-normative/http-migration/ "HTTP semantic convention stability migration")
        + [K8s attributes](/docs/specs/semconv/non-normative/k8s-attributes/ "Specify resource attributes using Kubernetes annotations")
        + [K8s migration](/docs/specs/semconv/non-normative/k8s-migration/ "K8s semantic convention stability migration")
        + [Naming known exceptions](/docs/specs/semconv/non-normative/naming-known-exceptions/ "Kubernetes naming exceptions")
        + [Recommended vs Opt-In CPU Metrics](/docs/specs/semconv/non-normative/groups/system/cpu-metrics-guidelines/)
        + [RPC migration](/docs/specs/semconv/non-normative/rpc-migration/ "RPC semantic convention stability migration guide")
        + [System semantic conventions: instrumentation design philosophy](/docs/specs/semconv/non-normative/groups/system/design-philosophy/)
        + [System use cases](/docs/specs/semconv/non-normative/groups/system/use-cases/ "System semantic conventions: general use cases")
      * [Object stores](/docs/specs/semconv/object-stores/ "Semantic conventions for object stores")
        + [S3](/docs/specs/semconv/object-stores/s3/ "Semantic conventions for AWS S3 client spans")
      * [OpenTelemetry SDK](/docs/specs/semconv/otel/ "Semantic conventions for OpenTelemetry SDK")
        + [SDK Metrics](/docs/specs/semconv/otel/sdk-metrics/ "Semantic conventions for OpenTelemetry SDK metrics")
      * [Resource](/docs/specs/semconv/resource/ "Resource semantic conventions")
        + [Android](/docs/specs/semconv/resource/android/)
        + [Browser](/docs/specs/semconv/resource/browser/)
        + [CICD](/docs/specs/semconv/resource/cicd/)
        + [Cloud](/docs/specs/semconv/resource/cloud/)
        + [Cloud provider](/docs/specs/semconv/resource/cloud-provider/)
          - [AWS](/docs/specs/semconv/resource/cloud-provider/aws/ "AWS semantic conventions")
            * [ECS](/docs/specs/semconv/resource/cloud-provider/aws/ecs/ "AWS ECS")
            * [EKS](/docs/specs/semconv/resource/cloud-provider/aws/eks/ "AWS EKS")
            * [Logs](/docs/specs/semconv/resource/cloud-provider/aws/logs/ "AWS logs")
          - [GCP](/docs/specs/semconv/resource/cloud-provider/gcp/ "GCP semantic conventions")
            * [Google Cloud AppHub](/docs/specs/semconv/resource/cloud-provider/gcp/apphub/)
            * [Google Cloud Run](/docs/specs/semconv/resource/cloud-provider/gcp/cloud-run/)
            * [Google Compute Engine](/docs/specs/semconv/resource/cloud-provider/gcp/gce/)
          - [Heroku](/docs/specs/semconv/resource/cloud-provider/heroku/)
        + [CloudFoundry](/docs/specs/semconv/resource/cloudfoundry/)
        + [Container](/docs/specs/semconv/resource/container/)
        + [Deployment](/docs/specs/semconv/resource/deployment-environment/)
        + [Device](/docs/specs/semconv/resource/device/)
        + [FaaS](/docs/specs/semconv/resource/faas/ "Function as a Service")
        + [Host](/docs/specs/semconv/resource/host/)
        + [Kubernetes](/docs/specs/semconv/resource/k8s/)
          - [Openshift](/docs/specs/semconv/resource/k8s/openshift/)
        + [Operating system](/docs/specs/semconv/resource/os/)
        + [Process](/docs/specs/semconv/resource/process/ "Process and process runtime resources")
        + [Service](/docs/specs/semconv/resource/service/ "Service semantic conventions")
        + [Webengine](/docs/specs/semconv/resource/webengine/)
        + [z/OS software](/docs/specs/semconv/resource/zos/)
      * [RPC](/docs/specs/semconv/rpc/ "Semantic conventions for RPC")
        + [Connect](/docs/specs/semconv/rpc/connect-rpc/ "Semantic conventions for Connect RPC")
        + [Dubbo](/docs/specs/semconv/rpc/dubbo/ "Semantic conventions for Apache Dubbo")
        + [Exceptions](/docs/specs/semconv/rpc/rpc-exceptions/ "Semantic conventions for RPC exceptions")
        + [gRPC](/docs/specs/semconv/rpc/grpc/ "Semantic conventions for gRPC")
        + [JSON-RPC](/docs/specs/semconv/rpc/json-rpc/ "Semantic conventions for JSON-RPC")
        + [Metrics](/docs/specs/semconv/rpc/rpc-metrics/ "Semantic conventions for RPC metrics")
        + [Spans](/docs/specs/semconv/rpc/rpc-spans/ "Semantic conventions for RPC spans")
      * [Runtime environment](/docs/specs/semconv/runtime/ "Semantic conventions for runtime environment")
        + [.NET](/docs/specs/semconv/runtime/dotnet-metrics/ "Semantic conventions for .NET Common Language Runtime (CLR) metrics")
        + [CPython](/docs/specs/semconv/runtime/cpython-metrics/ "Semantic conventions for CPython runtime metrics")
        + [Go](/docs/specs/semconv/runtime/go-metrics/ "Semantic conventions for Go runtime metrics")
        + [JVM](/docs/specs/semconv/runtime/jvm-metrics/ "Semantic conventions for JVM metrics")
        + [Node.js](/docs/specs/semconv/runtime/nodejs-metrics/ "Semantic conventions for Node.js runtime metrics")
        + [V8 JS engine](/docs/specs/semconv/runtime/v8js-metrics/ "Semantic conventions for V8 JS engine runtime metrics")
      * [System](/docs/specs/semconv/system/ "System semantic conventions")
        + [Container](/docs/specs/semconv/system/container-metrics/ "Semantic conventions for container metrics")
        + [Kubernetes](/docs/specs/semconv/system/k8s-metrics/ "Semantic conventions for Kubernetes metrics")
        + [OpenShift](/docs/specs/semconv/system/openshift-metrics/ "Semantic conventions for OpenShift metrics")
        + [OS process](/docs/specs/semconv/system/process-metrics/ "Semantic conventions for OS process metrics")
        + [System](/docs/specs/semconv/system/system-metrics/ "Semantic conventions for system metrics")
      * [URL](/docs/specs/semconv/url/ "Semantic conventions for URL")
  + [Security](/docs/security/)
    - [Common Vulnerabilities and Exposures](/docs/security/cve/)
    - [Handling sensitive data](/docs/security/handling-sensitive-data/)
    - [Community incident response guidelines](/docs/security/security-response/)
    - [Collector configuration](/docs/security/config-best-practices/ "Collector configuration best practices")
    - [Collector hosting](/docs/security/hosting-best-practices/ "Collector hosting best practices")
  + [Contributing](/docs/contributing/)
    - [Prerequisites](/docs/contributing/prerequisites/)
    - [Issues](/docs/contributing/issues/)
    - [Submitting content](/docs/contributing/pull-requests/)
    - [Style guide](/docs/contributing/style-guide/ "Documentation style guide")
    - [Localization](/docs/contributing/localization/ "Site localization")
    - [Blog](/docs/contributing/blog/)
    - [Pull request checks](/docs/contributing/pr-checks/)
    - [Announcements](/docs/contributing/announcements/)
    - [Dev setup and more](/docs/contributing/development/ "Development setup and commands to build, serve, and more")
    - [SIG practices](/docs/contributing/sig-practices/ "SIG practices for approver and maintainers")
    - [Acknowledgements](/docs/contributing/acknowledgements/)

[View Markdown](/docs/concepts/signals/traces/index.md)
 [View page source](https://github.com/open-telemetry/opentelemetry.io/tree/main/content/en/docs/concepts/signals/traces.md)
 [Edit this page](https://github.com/open-telemetry/opentelemetry.io/edit/main/content/en/docs/concepts/signals/traces.md)
 [Create child page](https://github.com/open-telemetry/opentelemetry.io/new/main/content/en/docs/concepts/signals?filename=change-me.md&value=---%0Atitle%3A+%22Long+Page+Title%22%0AlinkTitle%3A+%22Short+Nav+Title%22%0Aweight%3A+100%0Adescription%3A+%3E-%0A+++++Page+description+for+heading+and+indexes.%0A---%0A%0A%23%23+Heading%0A%0AEdit+this+template+to+create+your+new+page.%0A%0A%2A+Give+it+a+good+name%2C+ending+in+%60.md%60+-+e.g.+%60get-started.md%60%0A%2A+Edit+the+%22front+matter%22+section+at+the+top+of+the+page+%28weight+controls+how+its+ordered+amongst+other+pages+in+the+same+directory%3B+lowest+number+first%29.%0A%2A+Add+a+good+commit+message+at+the+bottom+of+the+page+%28%3C80+characters%3B+use+the+extended+description+field+for+more+detail%29.%0A%2A+Create+a+new+branch+so+you+can+preview+your+new+file+and+request+a+review+via+Pull+Request.%0A)
 [Create documentation issue](https://github.com/open-telemetry/opentelemetry.io/issues/new?title=Traces)

On this page

* [Tracer Provider](#tracer-provider)
* [Tracer](#tracer)
* [Trace Exporters](#trace-exporters)
* [Context Propagation](#context-propagation)
* [Spans](#spans)
  + [Span Context](#span-context)
  + [Attributes](#attributes)
  + [Span Events](#span-events)
    - [When to use span events versus span attributes](#when-to-use-span-events-versus-span-attributes)
  + [Span Links](#span-links)
  + [Span Status](#span-status)
  + [Span Kind](#span-kind)
    - [Client](#client)
    - [Server](#server)
    - [Internal](#internal)
    - [Producer](#producer)
    - [Consumer](#consumer)
* [Specification](#specification)

1. [Docs](/docs/)
2. [Concepts](/docs/concepts/)
3. [Signals](/docs/concepts/signals/)
4. Traces

# Traces

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

.feedback--answer{display:inline-block}.feedback--answer-no{margin-left:1em}.feedback--response{display:none;margin-top:1em}.feedback--response\_\_visible{display:block}

## Feedback

Was this page helpful?

Yes
No

Thank you. Your feedback is appreciated!

Please let us know [how we can improve this page](https://github.com/open-telemetry/opentelemetry.io/issues/new?template=PAGE_FEEDBACK.yml&title=[Page+feedback]%3A+ADD+A+SUMMARY+OF+YOUR+FEEDBACK+HERE). Your feedback is appreciated!

const yesButton=document.querySelector(".feedback--answer-yes"),noButton=document.querySelector(".feedback--answer-no"),yesResponse=document.querySelector(".feedback--response-yes"),noResponse=document.querySelector(".feedback--response-no"),disableButtons=()=>{yesButton.disabled=!0,noButton.disabled=!0},sendFeedback=e=>{if(typeof gtag!="function")return;gtag("event","page\_helpful",{event\_category:"Helpful",event\_label:window.location.pathname,value:e})};yesButton.addEventListener("click",()=>{yesResponse.classList.add("feedback--response\_\_visible"),disableButtons(),sendFeedback(100)}),noButton.addEventListener("click",()=>{noResponse.classList.add("feedback--response\_\_visible"),disableButtons(),sendFeedback(0)})  

Last modified January 14, 2026: [Convert all `en` page Note alerts to markdown syntax (#8894) (6bf06ddb)](https://github.com/open-telemetry/opentelemetry.io/commit/6bf06ddb9fc057dd6e8092f26d988ffe7b1af5ed)

©
2019–present
OpenTelemetry Authors | Docs [CC BY 4.0](https://creativecommons.org/licenses/by/4.0)All Rights Reserved