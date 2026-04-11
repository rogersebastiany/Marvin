# DevOps and API Tools


---

## 1. What is OpenAPI?

---

The OpenAPI Specification (OAS) provides a consistent means to carry information through each stage of the API lifecycle. It is a specification language for HTTP APIs that defines structure and syntax in a way that is not wedded to the programming language the API is created in. API specifications are typically written in YAML or JSON, allowing for easy sharing and consumption of the specification.

With OAS, you can quickly discover how an API works. As it is programming-language agnostic you can quickly identify and understand service capabilities. You can also use OAS to configure infrastructure, generate client code and create test cases for your APIs. OAS can therefore support your endeavors throughout the API lifecycle, and help you communicate with developer communities both inside and outside your organization.

## What is OpenAPI?

Having the ability to provide a definition of your API to other people – your colleagues, companies you partner with or organizations who you provide APIs to – is vital to doing business. The success of the API economy is predicated on doing this repeatedly, succinctly and deterministically, using a vernacular that is relevant to the API consumer.

API specification languages provide a standardized means to do this. Your APIs can be described in agnostic terms, decoupling them from any specific programming language. Consumers of your API specification do not need to understand the guts of your application or try to learn Lisp or Haskell if that’s what you chose to write it in. They can understand exactly what they need from your API specification, written in a simple and expressive language.

The OpenAPI Specification (OAS) enables exactly this transfer of knowledge from API provider to API consumer. It is an open standard for describing your APIs, allowing you to provide an API specification encoded in a JSON or YAML document. It provides a comprehensive dictionary of terms that reflects commonly-understood concepts in the world of APIs, embedding the fundamentals of HTTP and JSON. When teamed up with supporting tools it can provide a rich experience based on a simple document.

## OAS in the API Lifecycle

Providing and using an OAS document is not, however, a point-in-time activity. It is fundamental to the API lifecycle, providing affordances for all activities from the inception of the design right through to deployment and support. If an API lifecycle is a transport network then OAS should be considered an arterial road, providing the means to efficiently transfer large amounts of pertinent information quickly and efficiently.

When one considers the API lifecycle it starts to become clear how useful an OpenAPI document is. Consider the simple API lifecycle below. It is based on the idea of API-first design, where the interface is designed without writing a stitch of implementation code. OAS can be used at each stage in this lifecycle.

An API lifecycle within an organization clearly has more nuances than the steps described above, and will undoubtedly be tailored towards the software development lifecycle in use. An agile methodology may, for example, iterate over the steps shown above many times. However, for the purposes of exemplar this simplified view has merit as it shows the utility of OAS at each stage.

## Using OAS to help elicit requirements

The first step in our conceptional lifecycle is Requirements, where ideas about an API start to take shape. “Taking shape” covers a multitude of different activities – some technical, some not. Requirements gathering in most organizations stretches back into the business, working with the product team to define what the API should provide for its consumers and that support a holistic view of the product features.

Technologists working on bringing those requirements need some means to convey them. OAS provides the means to support this in an agnostic and *portable* way. It also provides the means to do this **quickly** and be able to socialize their ideas with other stakeholders with minimal set-up.

Having a sketch of your API design in OAS when gathering requirements gives you a headstart when starting design.

## OAS for design

The design stage of our conceptual API lifecycle is when we take requirements – sketched out in an OpenAPI document or not – and turn them into something tangible. Whatever your starting point – a blank sheet of (virtual) paper, stubbed and annotated controller classes in your code base, a graphical representation in your design tool of choice – being able to create an OAS for consumption of others is vitally important. Given our conceptual lifecycle is based on API-first design the tool of choice is more likely to be an OpenAPI editor or an IDE with an OpenAPI plugin. In the majority of organizations we can also add a number of artifacts that might support this activity: design patterns, Schema objects based on industry standards, organizational data models and so on.

Whatever the tool and artifacts used at the API provider, OAS provides a *tangible* output from the design process. Having a well-defined and versionable artifact to work with is critical to the accuracy and efficiency of the subsequent steps of the API lifecycle. An OpenAPI document – source controlled using an appropriate mechanism – allows this to happen in a sensible way, and provides a clear and unequivocal input to development.

## OAS in development

Once an API design has been created the time has come to write some code and create an implementation of that API in software. Acting on the output design process means working with the OpenAPI document to help bring your application to life.

Our conception lifecycle assumes an API-first design approach, where the OpenAPI document is created upfront and code is then written to create the implementation. There is, of course, the “code-first” approach where the implementation is created and then (typically) annotated so an OpenAPI document can then be generated.

The pros and cons of both approaches are beyond the scope of this post, but if you take the API first approach then having the design detailed in an OpenAPI document is critical to your implementation. The OAS has a rich tooling ecosystem and using the OpenAPI document to generate server-side code is a common approach to automating the creation of controller classes. This speeds up the delivery of the implementation and helps ensure the interface design and the implementation are closely-matched.

Implementing your API in code is, however, only one of the subsequent steps in the lifecycle. Other activities rely on OAS to be completed successfully.

## Configuring your infrastructure with OAS

The vast majority of organizations exposing APIs internally or externally use infrastructure to protect the API from malicious intent or provide standardized patterns of deployment.

API management is arguably the most common architecture component in this context. Its function is to protect the APIs of an API provider and provide lifecycle-based functions that help organizations operate their APIs seamlessly. The majority of API management tools provide support for using an OpenAPI document as an input to configuration, using it to build – for example – an API gateway configuration that observes the structure of the API and implements path and parameter validation, request body validation and provides callouts to security systems associated with the function of the APIs.

The point here is one of efficiency. Having an OpenAPI document available to facilitate this process turns it from a lengthy configuration exercise to a button-click operation. By using the same artifact created at design time OAS reduces the administration overhead for API providers, all done using a single version of the truth expressed in the OpenAPI document.

## Creating a developer experience with OAS

The point about efficiency also rings true when we talk about developer experience. Having the means to communicate to developers – publicly or with partners, internally or externally – through the same means we used to design our implementation massively accelerates our means to publish relevant information.

Many developers want just the raw OpenAPI document to use in their own tooling. Obviously this is available – often embellished with copy written documentation which can be embedded in the OpenAPI document itself – but API providers can also deliver a rich developer experience through their own choice of tools. There are countless tools compatible with OAS that can provide a developer portal from a button-click, an interactive experience to “try” a provider’s APIs and software development kits in multiple languages generated from an OpenAPI document.

OAS cannot do it all on its own of course. The majority of API providers look to create an immersive experience with content particular to their product and unique selling points. This takes the talents of many creative individuals and the tools they use. OAS does, however, provide a structure that can help bind the experience together.

## Testing with OAS

Developer experience often focuses on OAS from the perspective of the API consumer as a user of the product or service offered up by the API provider. There are, however, other consumers who can make use of an OpenAPI document to understand an API and perform activities pertinent to them.

One area of particular importance is in testing an API. API providers need assurance that the APIs they put in the market meet their acceptable levels of quality and accuracy. Testing APIs requires the same insight as consuming it due to the same need to understand the structure, parameters and request and response definitions. Writing and executing test cases relies on the same level of understanding as an API consumer.

API testing is an area where tooling has become heavily invested in OAS as an input. For example, using tools to perform contract tests to check that design and implementation match is a common activity for API providers. The same is true for security tools, which test the API footprint for weaknesses in the implementation. Having an OpenAPI document provides a definition of what is API is \*supposed\* to offer and therefore a baseline what might have been unintentionally exposed or implement weak security practices.

Testing is therefore a stage in our conceptual API lifecycle that significantly benefits from leverage OAS. Using an OpenAPI document as an input both accelerates this activity and provides a deterministic mechanism for executing tests.

## 💡 Final Thoughts

The last stage in our API cycle is about making the API available to API consumers. Deploying the API obviously covers more than just installing our software implementation. API management and the developer experience all need to come together to provide the API that an API consumers want to deliver them a particular product or service with what they need to understand how it works and what they need to do to build their software.

In this article we’ve tried to explain how useful OAS is at every stage of getting an API to this point. OAS ties the lifecycle together by providing a consistent means to carry information through each stage. When this is done right OAS provides a valuable mechanism for API providers to ensure consistency and quality in their endeavors.

Want to know more about OAS? Please check out our [Getting Started with OpenAPI Specification](https://learn.openapis.org/) guide for a detailed overview of the specification. Please also visit our [tooling catalog](https://tools.openapis.org/), which provides details of open source and commercial tools that support OAS.

---

## 2. Getting Started

Tip

This guide assumes you have a grounding in the tools that Argo CD is based on. Please read [understanding the basics](../understand_the_basics/) to learn about these tools.

## Requirements

* Installed [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) command-line tool.
* Have a [kubeconfig](https://kubernetes.io/docs/tasks/access-application-cluster/configure-access-multiple-clusters/) file (default location is `~/.kube/config`).
* CoreDNS. Can be enabled for microk8s by `microk8s enable dns && microk8s stop && microk8s start`

## 1. Install Argo CD

```
kubectlcreatenamespaceargocd
kubectlapply-nargocd--server-side--force-conflicts-fhttps://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

This will create a new `argocd` namespace where all Argo CD services and application resources will reside. It will also install Argo CD by applying the official manifests from the stable branch. Using a pinned version (like `v3.2.0`) is recommended for production.

Note

**Why `--server-side --force-conflicts`?**

The `--server-side` flag is required because some Argo CD CRDs (like ApplicationSet) exceed the 262KB annotation size limit imposed by client-side `kubectl apply`. Server-side apply avoids this limitation by not storing the `last-applied-configuration` annotation.

The `--force-conflicts` flag allows the apply operation to take ownership of fields that may have been previously managed by other tools (such as Helm or a previous `kubectl apply`). This is safe for fresh installs and necessary for upgrades. Note that any custom modifications you've made to fields that are defined in the Argo CD manifests (like `affinity`, `env`, or `probes`) will be overwritten. However, fields not specified in the manifests (like `resources` limits/requests or `tolerations`) will be preserved.

Warning

The installation manifests include `ClusterRoleBinding` resources that reference `argocd` namespace. If you are installing Argo CD into a different
namespace then make sure to update the namespace reference.

Tip

If you are not interested in UI, SSO, and multi-cluster features, then you can install only the [core](../operator-manual/core/#installing) Argo CD components.

This default installation will have a self-signed certificate and cannot be accessed without a bit of extra work.
Do one of:

* Follow the [instructions to configure a certificate](../operator-manual/tls/) (and ensure that the client OS trusts it).
* Configure the client OS to trust the self signed certificate.
* Use the --insecure flag on all Argo CD CLI operations in this guide.

Note

Default namespace for `kubectl` config must be set to `argocd`.
This is only needed for the following commands since the previous commands have -n argocd already:

```
kubectlconfigset-context--current--namespace=argocd
```

Use `argocd login --core` to [configure](../user-guide/commands/argocd_login/) CLI access and skip steps 3-5.

Note

This default installation for Redis is using password authentication. The Redis password is stored in Kubernetes secret `argocd-redis` with key `auth` in the namespace where Argo CD is installed.

If you are running Argo CD on Docker Desktop or another local Kubernetes environment, refer to the [Running Argo CD Locally](../developer-guide/running-locally/) guide for the full setup instructions and configuration steps tailored for local clusters.

## 2. Download Argo CD CLI

Download the latest Argo CD version from <https://github.com/argoproj/argo-cd/releases/latest>. More detailed installation instructions can be found via the [CLI installation documentation](../cli_installation/).

Also available in Mac, Linux and WSL Homebrew:

```
brewinstallargocd
```

## 3. Access Argo CD

By default, Argo CD isn’t exposed outside the cluster. To access Argo CD from your browser or CLI, use one of the following methods:

### Service Type Load Balancer

Change the argocd-server service type to `LoadBalancer`:

```
kubectlpatchsvcargocd-server-nargocd-p'{"spec": {"type": "LoadBalancer"}}'
```

After a short wait, your cloud provider will assign an external IP address to the service. You can retrieve this IP with:

```
kubectlgetsvcargocd-server-nargocd-o=jsonpath='{.status.loadBalancer.ingress[0].ip}'
```

### Ingress

Follow the [ingress documentation](../operator-manual/ingress/) on how to configure Argo CD with ingress.

### Port Forwarding

Kubectl port-forwarding can also be used to connect to the API server without exposing the service.

```
kubectlport-forwardsvc/argocd-server-nargocd8080:443
```

The API server can then be accessed using https://localhost:8080

## 4. Login Using The CLI

The initial password for the `admin` account is auto-generated and stored as
clear text in the field `password` in a secret named `argocd-initial-admin-secret`
in your Argo CD installation namespace. You can simply retrieve this password
using the `argocd` CLI:

```
argocdadmininitial-password-nargocd
```

Warning

You should delete the `argocd-initial-admin-secret` from the Argo CD
namespace once you changed the password. The secret serves no other
purpose than to store the initially generated password in clear and can
safely be deleted at any time. It will be re-created on demand by Argo CD
if a new admin password must be re-generated.

Using the username `admin` and the password from above, login to Argo CD's IP or hostname:

```
argocdlogin<ARGOCD_SERVER>
```

Note

The CLI environment must be able to communicate with the Argo CD API server. If it isn't directly accessible as described above in step 3, you can tell the CLI to access it using port forwarding through one of these mechanisms: 1) add `--port-forward-namespace argocd` flag to every CLI command; or 2) set `ARGOCD_OPTS` environment variable: `export ARGOCD_OPTS='--port-forward-namespace argocd'`.

Change the password using the command:

```
argocdaccountupdate-password
```

## 5. Register A Cluster To Deploy Apps To (Optional)

This step registers a cluster's credentials to Argo CD, and is only necessary when deploying to
an external cluster. When deploying internally (to the same cluster that Argo CD is running in),
https://kubernetes.default.svc should be used as the application's K8s API server address.

First list all clusters contexts in your current kubeconfig:

```
kubectlconfigget-contexts-oname
```

Choose a context name from the list and supply it to `argocd cluster add CONTEXTNAME`. For example,
for docker-desktop context, run:

```
argocdclusteradddocker-desktop
```

The above command installs a ServiceAccount (`argocd-manager`), into the kube-system namespace of
that kubectl context, and binds the service account to an admin-level ClusterRole. Argo CD uses this
service account token to perform its management tasks (i.e. deploy/monitoring).

Note

The rules of the `argocd-manager-role` role can be modified such that it only has `create`, `update`, `patch`, `delete` privileges to a limited set of namespaces, groups, kinds.
However `get`, `list`, `watch` privileges are required at the cluster-scope for Argo CD to function.

## 6. Create An Application From A Git Repository

An example repository containing a guestbook application is available at
<https://github.com/argoproj/argocd-example-apps.git> to demonstrate how Argo CD works.

Note

Note: The following example application may only be compatible with AMD64 architecture. If you are running on a different architecture (such as ARM64 or ARMv7), you may encounter issues with dependencies or container images that are not built for your platform. Consider verifying the compatibility of the application or building architecture-specific images if necessary.

### Creating Apps Via CLI

First we need to set the current namespace to argocd running the following command:

```
kubectlconfigset-context--current--namespace=argocd
```

Create the example guestbook application with the following command:

```
argocdappcreateguestbook--repohttps://github.com/argoproj/argocd-example-apps.git--pathguestbook--dest-serverhttps://kubernetes.default.svc--dest-namespacedefault
```

### Creating Apps Via UI

Open a browser to the Argo CD external UI, and login by visiting the IP/hostname in a browser and use the credentials set in step 4 or locally as explained in [Try Argo CD Locally](../try_argo_cd_locally/).

After logging in, click the **+ New App** button as shown below:

Give your app the name `guestbook`, use the project `default`, and leave the sync policy as `Manual`:

Connect the <https://github.com/argoproj/argocd-example-apps.git> repo to Argo CD by setting repository url to the github repo url, leave revision as `HEAD`, and set the path to `guestbook`:

For **Destination**, set cluster URL to `https://kubernetes.default.svc` (or `in-cluster` for cluster name) and namespace to `default`:

After filling out the information above, click **Create** at the top of the UI to create the `guestbook` application:

## 7. Sync (Deploy) The Application

### Syncing via CLI

Once the guestbook application is created, you can now view its status:

```
$argocdappgetguestbook
Name:guestbook
Server:https://kubernetes.default.svc
Namespace:default
URL:https://10.97.164.88/applications/guestbook
Repo:https://github.com/argoproj/argocd-example-apps.git
Target:
Path:guestbook
SyncPolicy:<none>
SyncStatus:OutOfSyncfrom(1ff8a67)
HealthStatus:Missing

GROUPKINDNAMESPACENAMESTATUSHEALTH
appsDeploymentdefaultguestbook-uiOutOfSyncMissing
Servicedefaultguestbook-uiOutOfSyncMissing
```

The application status is initially in `OutOfSync` state since the application has yet to be
deployed, and no Kubernetes resources have been created. To sync (deploy) the application, run:

```
argocdappsyncguestbook
```

This command retrieves the manifests from the repository and performs a `kubectl apply` of the
manifests. The guestbook app is now running and you can now view its resource components, logs,
events, and assessed health status.

### Syncing via UI

On the Applications page, click on *Sync* button of the guestbook application:

A panel will be opened and then, click on *Synchronize* button.

You can see more details by clicking at the guestbook application:

---

## 3. 

## Training Courses

Get started or level up your GraphQL skills with these trusted tutorials.

* [GraphQL-JS tutorial

  Step-by-step guide to building schemas and executing queries with GraphQL.js.](https://www.graphql-js.org/docs/)
* [Apollo Odyssey

  Interactive courses for building GraphQL applications with Apollo's toolset.](https://www.apollographql.com/tutorials/)
* [Yoga GraphQL Server Tutorial

  Open source tutorial for creating modern GraphQL Servers in Node, CF Workers, Deno and others.](https://the-guild.dev/graphql/yoga-server/tutorial/basic)
* [GraphQL Tutorials

  Real World Fullstack GraphQL tutorials for developers by Hasura.](https://hasura.io/learn/)

## Common questions

Find answers to the most common questions about GraphQL — from getting started to advanced use cases. This also covers frontend concerns and info about the official specification.

## Looking for more?

Learning is just the beginning. Discover tools and other resources — or connect with the GraphQL community around the world.

[Resources](/resources/)[Community](/community/)

---

## 4. About Grafana

Grafana Cloud
Enterprise
Open source

# About Grafana

[Grafana open source software](/oss/) enables you to query, visualize, alert on, and explore your metrics, logs, and traces wherever they are stored. Grafana OSS provides you with tools to turn your time-series database (TSDB) data into insightful graphs and visualizations. The Grafana OSS plugin framework also enables you to connect other data sources like NoSQL/SQL databases, ticketing tools like Jira or ServiceNow, and CI/CD tooling like GitLab.

After you have [installed Grafana](../setup-grafana/installation/) and set up your first dashboard using instructions in [Getting started with Grafana](../getting-started/build-first-dashboard/), you will have many options to choose from depending on your requirements. For example, if you want to view weather data and statistics about your smart home, then you can create a [playlist](../dashboards/create-manage-playlists/). If you are the administrator for an enterprise and are managing Grafana for multiple teams, then you can set up [provisioning](../administration/provisioning/) and [authentication](../setup-grafana/configure-access/configure-authentication/).

The following sections provide an overview of Grafana features and links to product documentation to help you learn more. For more guidance and ideas, check out our [Grafana Community forums](https://community.grafana.com/).

## Explore metrics, logs, and traces

Explore your data through ad-hoc queries and dynamic drilldown. Split view and compare different time ranges, queries and data sources side by side. Refer to [Explore](../explore/) for more information.

## Alerts

If you’re using Grafana Alerting, then you can have alerts sent through a number of different alert notifiers, including PagerDuty, SMS, email, VictorOps, OpsGenie, or Slack.

Alert hooks allow you to create different notifiers with a bit of code if you prefer some other channels of communication. Visually define [alert rules](../alerting/alerting-rules/) for your most important metrics.

## Annotations

Annotate graphs with rich events from different data sources. Hover over events to see the full event metadata and tags.

This feature, which shows up as a graph marker in Grafana, is useful for correlating data in case something goes wrong. You can create the annotations manually—just control-click on a graph and input some text—or you can fetch data from any data source. Refer to [Annotations](../dashboards/build-dashboards/annotate-visualizations/) for more information.

## Dashboard variables

[Template variables](../dashboards/variables/) allow you to create dashboards that can be reused for lots of different use cases. Values aren’t hard-coded with these templates, so for instance, if you have a production server and a test server, you can use the same dashboard for both.

Templating allows you to drill down into your data, say, from all data to North America data, down to Texas data, and beyond. You can also share these dashboards across teams within your organization—or if you create a great dashboard template for a popular data source, you can contribute it to the whole community to customize and use.

## Configure Grafana

If you’re a Grafana administrator, then you’ll want to thoroughly familiarize yourself with [Grafana configuration options](../setup-grafana/configure-grafana/) and the [Grafana CLI](../cli/).

Configuration covers both config files and environment variables. You can set up default ports, logging levels, email IP addresses, security, and more.

## Import dashboards and plugins

Discover hundreds of [dashboards](/grafana/dashboards) and [plugins](/grafana/plugins) in the official library. Thanks to the passion and momentum of community members, new ones are added every week.

## Authentication

Grafana supports different authentication methods, such as LDAP and OAuth, and allows you to map users to organizations. Refer to the [User authentication overview](../setup-grafana/configure-access/configure-authentication/) for more information.

In Grafana Enterprise, you can also map users to teams: If your company has its own authentication system, Grafana allows you to map the teams in your internal systems to teams in Grafana. That way, you can automatically give people access to the dashboards designated for their teams. Refer to [Grafana Enterprise](grafana-enterprise/) for more information.

## Provisioning

While it’s easy to click, drag, and drop to create a single dashboard, power users in need of many dashboards will want to automate the setup with a script. You can script anything in Grafana.

For example, if you’re spinning up a new Kubernetes cluster, you can also spin up a Grafana automatically with a script that would have the right server, IP address, and data sources preset and locked in so users cannot change them. It’s also a way of getting control over a lot of dashboards. Refer to [Provisioning](../administration/provisioning/) for more information.

## Permissions

When organizations have one Grafana and multiple teams, they often want the ability to both keep things separate and share dashboards. You can create a team of users and then set permissions on [folders and dashboards](../administration/user-management/manage-dashboard-permissions/), and down to the [data source level](../administration/data-source-management/#data-source-permissions) if you’re using [Grafana Enterprise](grafana-enterprise/).

## Other Grafana Labs OSS Projects

In addition to Grafana, Grafana Labs also provides the following open source projects:

**Grafana Loki:** Grafana Loki is an open source, set of components that can be composed into a fully featured logging stack. For more information, refer to [Grafana Loki documentation](/docs/loki/latest/).

**Grafana Tempo:** Grafana Tempo is an open source, easy-to-use and high-volume distributed tracing backend. For more information, refer to [Grafana Tempo documentation](/docs/tempo/latest/?pg=oss-tempo&plcmt=hero-txt/).

**Grafana Mimir:** Grafana Mimir is an open source software project that provides a scalable long-term storage for Prometheus. For more information about Grafana Mimir, refer to [Grafana Mimir documentation](/docs/mimir/latest/).

**Grafana Pyroscope:** Grafana Pyroscope is an open source software project for aggregating continuous profiling data. Continuous profiling is an observability signal that allows you to understand your workload’s resources (CPU, memory, for example) usage down to the line number. For more information about Grafana Pyroscope, refer to [Grafana Pyroscope documentation](/docs/pyroscope/latest/).

**Grafana Faro:** Grafana Faro is an open source JavaScript agent that embeds in web applications to collect real user monitoring (RUM) data: performance metrics, logs, exceptions, events, and traces. For more information about using Grafana Faro, refer to [Grafana Faro documentation](/docs/grafana-cloud/monitor-applications/frontend-observability/faro-web-sdk/).

**Grafana Beyla:** Grafana Beyla is an eBPF-based application auto-instrumentation tool for application observability. eBPF is used to automatically inspect application executables and the OS networking layer as well as capture basic trace spans related to web transactions and Rate-Errors-Duration (RED) metrics for Linux HTTP/S and gRPC services. All data capture occurs without any modifications to application code or configuration. For more information about Grafana Beyla, refer to [Grafana Beyla documentation](/docs/beyla/latest/).

**Grafana Alloy:** Grafana Alloy is a flexible, high performance, vendor-neutral distribution of the [OpenTelemetry](https://opentelemetry.io/) (OTel) Collector.
It’s fully compatible with the most popular open source observability standards such as OpenTelemetry (OTel) and Prometheus.
For more information about Grafana Alloy, refer to the [Grafana Alloy documentation](/docs/alloy/latest/).

**Grafana k6:** Grafana k6 is an open-source load testing tool that makes performance testing easy and productive for engineering teams. For more information about Grafana k6, refer to [Grafana k6 documentation](/docs/k6/latest/).

**Grafana OnCall:** Grafana OnCall is an open source incident response management tool built to help teams improve their collaboration and resolve incidents faster. For more information about Grafana OnCall, refer to [Grafana OnCall documentation](/docs/oncall/latest/).

## Related resources from Grafana Labs

Additional helpful documentation, links, and articles:

[Video

Getting started with managing your metrics, logs, and traces using Grafana

In this webinar, we’ll demo how to get started using the LGTM Stack: Loki for logs, Grafana for visualization, Tempo for traces, and Mimir for metrics.](/go/webinar/getting-started-with-grafana-lgtm-stack/)[Video

Getting started with Grafana dashboard design

In this webinar, you'll learn how to design stylish and easily accessible Grafana dashboards that tell a story.](/go/webinar/getting-started-with-grafana-dashboard-design/)[Video

Building advanced Grafana dashboards

In this webinar, we’ll demo how to build and format Grafana dashboards.](/go/webinar/building-advanced-grafana-dashboards/)

---

## 5. Introduction to gRPC

An introduction to gRPC and protocol buffers.

# Introduction to gRPC

An introduction to gRPC and protocol buffers.

This page introduces you to gRPC and protocol buffers. gRPC can use
protocol buffers as both its Interface Definition Language (**IDL**) and as its underlying message
interchange format. If you’re new to gRPC and/or protocol buffers, read this!
If you just want to dive in and see gRPC in action first,
[select a language](/docs/languages/) and try its **Quick start**.

## Overview

In gRPC, a client application can directly call a method on a server application
on a different machine as if it were a local object, making it easier for you to
create distributed applications and services. As in many RPC systems, gRPC is
based around the idea of defining a service, specifying the methods that can be
called remotely with their parameters and return types. On the server side, the
server implements this interface and runs a gRPC server to handle client calls.
On the client side, the client has a stub (referred to as just a client in some
languages) that provides the same methods as the server.

gRPC clients and servers can run and talk to each other in a variety of
environments - from servers inside Google to your own desktop - and can be
written in any of gRPC’s supported languages. So, for example, you can easily
create a gRPC server in Java with clients in Go, Python, or Ruby. In addition,
the latest Google APIs will have gRPC versions of their interfaces, letting you
easily build Google functionality into your applications.

### Working with Protocol Buffers

By default, gRPC uses [Protocol Buffers](https://protobuf.dev/overview), Google’s
mature open source mechanism for serializing structured data (although it
can be used with other data formats such as JSON). Here’s a quick intro to how
it works. If you’re already familiar with protocol buffers, feel free to skip
ahead to the next section.

The first step when working with protocol buffers is to define the structure
for the data you want to serialize in a *proto file*: this is an ordinary text
file with a `.proto` extension. Protocol buffer data is structured as
*messages*, where each message is a small logical record of information
containing a series of name-value pairs called *fields*. Here’s a simple
example:

```
message Person {  string name = 1;  int32 id = 2;  bool has_ponycopter = 3;}
```

Then, once you’ve specified your data structures, you use the protocol buffer
compiler `protoc` to generate data access classes in your preferred language(s)
from your proto definition. These provide simple accessors for each field,
like `name()` and `set_name()`, as well as methods to serialize/parse
the whole structure to/from raw bytes. So, for instance, if your chosen
language is C++, running the compiler on the example above will generate a
class called `Person`. You can then use this class in your application to
populate, serialize, and retrieve `Person` protocol buffer messages.

You define gRPC services
in ordinary proto files, with RPC method parameters and return types specified as
protocol buffer messages:

```
// The greeter service definition.
service Greeter {  // Sends a greeting
  rpc SayHello (HelloRequest) returns (HelloReply) {}}// The request message containing the user's name.
message HelloRequest {  string name = 1;}// The response message containing the greetings
message HelloReply {  string message = 1;}
```

gRPC uses `protoc` with a special gRPC plugin to
generate code from your proto file: you get
generated gRPC client and server code, as well as the regular protocol buffer
code for populating, serializing, and retrieving your message types. To learn more about protocol buffers, including how to install `protoc` with the
gRPC plugin in your chosen language, see the [protocol buffers documentation](https://protobuf.dev/overview).

## Protocol buffer versions

While [protocol buffers](https://protobuf.dev/overview) have been available to open source users for some time,
most examples from this site use protocol buffers version 3 (proto3), which has
a slightly simplified syntax, some useful new features, and supports more
languages. Proto3 is currently available in Java, C++, Dart, Python,
Objective-C, C#, a lite-runtime (Android Java), Ruby, and JavaScript from the
[protocol buffers GitHub repo](https://github.com/google/protobuf/releases), as well as a Go language generator from the
[golang/protobuf official package](https://pkg.go.dev/google.golang.org/protobuf), with more languages in development. You can
find out more in the [proto3 language guide](https://protobuf.dev/programming-guides/proto3) and the [reference
documentation](https://protobuf.dev/reference) available for each language. The reference documentation also
includes a [formal specification](https://protobuf.dev/reference/protobuf/proto3-spec) for the `.proto` file format.

In general, while you can use proto2 (the current default protocol buffers
version), we recommend that you use proto3 with gRPC as it lets you use the
full range of gRPC-supported languages, as well as avoiding compatibility
issues with proto2 clients talking to proto3 servers and vice versa.

Last modified November 12, 2024: [Embed YouTube videos in different webpages (#1380) (196f408)](https://github.com/grpc/grpc.io/commit/196f408ae74741605fbb66f3ccf23b81fe384667)

[View page source](https://github.com/grpc/grpc.io/tree/main/content/en/docs/what-is-grpc/introduction.md)
 [Edit this page](https://github.com/grpc/grpc.io/edit/main/content/en/docs/what-is-grpc/introduction.md)
 [Create child page](https://github.com/grpc/grpc.io/new/main/content/en/docs/what-is-grpc/introduction.md?filename=change-me.md&value=---%0Atitle%3A+%22Long+Page+Title%22%0AlinkTitle%3A+%22Short+Nav+Title%22%0Aweight%3A+100%0Adescription%3A+%3E-%0A+++++Page+description+for+heading+and+indexes.%0A---%0A%0A%23%23+Heading%0A%0AEdit+this+template+to+create+your+new+page.%0A%0A%2A+Give+it+a+good+name%2C+ending+in+%60.md%60+-+e.g.+%60getting-started.md%60%0A%2A+Edit+the+%22front+matter%22+section+at+the+top+of+the+page+%28weight+controls+how+its+ordered+amongst+other+pages+in+the+same+directory%3B+lowest+number+first%29.%0A%2A+Add+a+good+commit+message+at+the+bottom+of+the+page+%28%3C80+characters%3B+use+the+extended+description+field+for+more+detail%29.%0A%2A+Create+a+new+branch+so+you+can+preview+your+new+file+and+request+a+review+via+Pull+Request.%0A)
 [Create documentation issue](https://github.com/grpc/grpc.io/issues/new?title=Introduction%20to%20gRPC)
 [Create project issue](https://github.com/grpc/grpc.io/issues/new)

---

## Bibliography

1. [What is OpenAPI?](https://www.openapis.org/what-is-openapi)
2. [Getting Started](https://argo-cd.readthedocs.io/en/stable/getting_started/)
3. [](https://graphql.org/learn/)
4. [About Grafana](https://grafana.com/docs/grafana/latest/introduction/)
5. [Introduction to gRPC](https://grpc.io/docs/what-is-grpc/introduction/)