Sidecar Pattern - Azure Architecture Center | Microsoft Learn

 

var msDocs = {
"environment": {
"accessLevel": "online",
"azurePortalHostname": "portal.azure.com",
"reviewFeatures": false,
"supportLevel": "production",
"systemContent": true,
"siteName": "learn",
"legacyHosting": false
},
"data": {
"contentLocale": "en-us",
"contentDir": "ltr",
"userLocale": "en-us",
"userDir": "ltr",
"pageTemplate": "Conceptual",
"brand": "azure",
"context": {},
"standardFeedback": true,
"showFeedbackReport": false,
"feedbackHelpLinkType": "",
"feedbackHelpLinkUrl": "",
"feedbackSystem": "Standard",
"feedbackGitHubRepo": "MicrosoftDocs/architecture-center",
"feedbackProductUrl": "",
"extendBreadcrumb": false,
"isEditDisplayable": true,
"isPrivateUnauthorized": false,
"hideViewSource": false,
"isPermissioned": false,
"hasRecommendations": true,
"contributors": [
{
"name": "claytonsiemens77",
"url": "https://github.com/claytonsiemens77"
},
{
"name": "v-ccolin",
"url": "https://github.com/v-ccolin"
},
{
"name": "jmart1428",
"url": "https://github.com/jmart1428"
},
{
"name": "v-federicoar",
"url": "https://github.com/v-federicoar"
},
{
"name": "ShannonLeavitt",
"url": "https://github.com/ShannonLeavitt"
},
{
"name": "TimShererWithAquent",
"url": "https://github.com/TimShererWithAquent"
},
{
"name": "alexbuckgit",
"url": "https://github.com/alexbuckgit"
},
{
"name": "dsk-2015",
"url": "https://github.com/dsk-2015"
},
{
"name": "ardalis",
"url": "https://github.com/ardalis"
},
{
"name": "ketan-chawda-msft",
"url": "https://github.com/ketan-chawda-msft"
},
{
"name": "v-wimarc",
"url": "https://github.com/v-wimarc"
}
]
},
"functions": {}
};;

[Skip to main content](#main)
[Skip to Ask Learn chat experience](#)

This browser is no longer supported.

Upgrade to Microsoft Edge to take advantage of the latest features, security updates, and technical support.

[Download Microsoft Edge](https://go.microsoft.com/fwlink/p/?LinkID=2092881 )
[More info about Internet Explorer and Microsoft Edge](https://learn.microsoft.com/en-us/lifecycle/faq/internet-explorer-microsoft-edge)

Table of contents 

Exit editor mode

Ask Learn

Ask Learn

Focus mode

Table of contents
[Read in English](#)

Add

Add to plan
[Edit](https://github.com/microsoftdocs/architecture-center/blob/main/docs/patterns/sidecar.md)

---

#### Share via

[Facebook](#)
[x.com](#)
[LinkedIn](#)
[Email](#)

---

Copy Markdown

Print

---

Note

Access to this page requires authorization. You can try [signing in](#) or changing directories.

Access to this page requires authorization. You can try changing directories.

# Sidecar pattern

Feedback

Summarize this article for me

## In this article

Deploy application components into a process or container separate from the main application to provide isolation and encapsulation. This pattern lets you build applications from diverse components and technologies.

Like a motorcycle sidecar, these components attach to a parent application and share its life cycle, so you create and retire them together. This pattern is also known as the *Sidekick pattern* and supports application decomposition.

## Context and problem

Applications and services often require related functionality, like monitoring, logging, configuration, and networking services. You can implement these peripheral tasks as separate components or services.

Tightly integrated components run in the same process and efficiently use shared resources, but they lack isolation. An outage in one component can affect the entire application. They also require implementation in the parent application's language, which creates interdependence.

If you decompose the application into services, you can build each service by using different languages and technologies. This approach provides more flexibility. But each component has its own dependencies and requires language-specific libraries to access the platform and shared resources. When you deploy these features as separate services, you add latency. Language-specific code and dependencies also increase complexity for hosting and deployment.

## Solution

Deploy a cohesive set of tasks alongside the primary application in a separate process or container. This approach provides a consistent interface for platform services across languages.

[The diagram shows the primary application and sidecar linked together. The application handles core functionality, and the sidecar handles peripheral tasks, like platform abstraction, proxy to remote services, logging, and configuration. Both the application and sidecar reside in a host.](_images/sidecar.png#lightbox)

A sidecar service connects to the application without being part of it and deploys alongside it. Each application instance gets its own sidecar instance that shares its life cycle.

The Sidecar pattern provides the following advantages:

* **Language independence:** The sidecar runs independently from the primary application's runtime environment and programming language. You can use one sidecar implementation across applications written in different languages.
* **Shared resource access:** The sidecar can access the same resources as the primary application. For example, the sidecar can monitor system resources that both components use.
* **Low latency:** The sidecar's proximity to the primary application minimizes communication latency.
* **Enhanced extensibility:** You can extend applications that lack native extensibility mechanisms by attaching a sidecar as a separate process on the same host or subcontainer.

The most common implementation of this pattern uses containers, which are also called *sidecar containers* or *sidekick containers*.

## Problems and considerations

Consider the following points when you implement this pattern:

* Consider the deployment and packaging format to deploy services, processes, or containers. Containers work well for the Sidecar pattern.
* When you design a sidecar service, carefully choose the interprocess communication mechanism. Use language-agnostic or framework-agnostic technologies unless performance requirements make that approach impractical.
* Before you add functionality to a sidecar, evaluate whether it works better as a separate service or a traditional daemon.
* Consider whether to implement the functionality as a library or through a traditional extension mechanism. Language-specific libraries provide deeper integration and less network overhead.

## When to use this pattern

Use this pattern when:

* Your primary application uses diverse languages and frameworks. Sidecars provide a consistent interface that different applications can use regardless of their language or framework.
* A separate team or external partner owns a component.
* You must deploy a component or feature on the same host as the application.
* You need a service that shares the overall life cycle of your main application but that you can update independently.
* You need fine-grained control over resource limits for a specific resource or component. For example, you can deploy a component as a sidecar to restrict and manage its memory usage independently of the main application.

This pattern might not be suitable when:

* You need to optimize interprocess communication. Sidecars add overhead, especially latency, which makes them unsuitable for applications with frequent communication between components.
* Your application is small. The resource cost of deploying a sidecar for each instance might outweigh the isolation benefits.
* You need to scale the component independently. If you must scale the component differently from the main application, deploy it as a separate service instead.
* Your platform provides equivalent functionality. If your application platform already provides the needed capabilities natively, sidecars add unnecessary complexity.

## Workload design

Evaluate how to use the Sidecar pattern in a workload's design to address the goals and principles covered in the [Azure Well-Architected Framework pillars](/en-us/azure/well-architected/pillars). The following table provides guidance about how this pattern supports the goals of each pillar.

| Pillar | How this pattern supports pillar goals |
| --- | --- |
| [Security](/en-us/azure/well-architected/security/checklist) design decisions help ensure the **confidentiality**, **integrity**, and **availability** of your workload's data and systems. | When you encapsulate these tasks and deploy them in separate processes, you reduce the attack surface to only the necessary code. You can also use sidecars to add cross-cutting security controls to application components that lack native support for these features.    - [SE:04 Segmentation](/en-us/azure/well-architected/security/segmentation)   - [SE:07 Encryption](/en-us/azure/well-architected/security/encryption) |
| [Operational Excellence](/en-us/azure/well-architected/operational-excellence/checklist) helps deliver **workload quality** through **standardized processes** and team cohesion. | This pattern lets you flexibly integrate observability tools without adding dependencies to your application code. You can update and maintain the sidecar independently of the application.    - [OE:04 Tools and processes](/en-us/azure/well-architected/operational-excellence/tools-processes)   - [OE:07 Monitoring system](/en-us/azure/well-architected/operational-excellence/observability) |
| [Performance Efficiency](/en-us/azure/well-architected/performance-efficiency/checklist) helps your workload **efficiently meet demands** through optimizations in scaling, data, and code. | This pattern lets you centralize cross-cutting tasks in sidecars that scale across multiple application instances. You don't need to deploy duplicate functionality for each application instance.    - [PE:07 Code and infrastructure](/en-us/azure/well-architected/performance-efficiency/optimize-code-infrastructure) |

If this pattern introduces trade-offs within a pillar, consider them against the goals of the other pillars.

## Example

You can apply the Sidecar pattern to many scenarios. Consider the following examples:

* **Dependency abstraction:** Deploy a custom service alongside each application to provide access to shared dependency capabilities through a consistent API. This approach replaces language-specific client libraries with a sidecar that handles concerns like logging, configuration, service discovery, state management, and health checks.

  The [Distributed Application Runtime (Dapr) sidecar](https://docs.dapr.io/concepts/dapr-services/sidecar/) exemplifies this use case.
* **Service mesh data plane:** Deploy a sidecar proxy alongside each service instance to handle cross-cutting networking concerns like traffic routing, retries, mutual Transport Layer Security (mTLS), policy enforcement, and telemetry.

  Service meshes like [Istio](https://istio.io/latest/about/service-mesh/) use sidecar proxies to implement these capabilities without requiring changes to application code.
* **Ambassador sidecar:** Deploy an <ambassador> service as a sidecar. The application routes calls through the ambassador, which handles request logging, routing, circuit breaking, and other connectivity features.
* **Protocol adapters:** Deploy a sidecar to translate between incompatible protocols or data formats, or to [bridge messaging systems](messaging-bridge). This approach lets the application use simpler or legacy interfaces.
* **Telemetry enrichment:** Deploy a sidecar to preprocess or enrich telemetry data, like metrics, logs, and traces, before it forwards the data to external monitoring systems. Components like the [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/deploy/agent/) can run as sidecars to normalize, enrich, or route telemetry separately from the application.

## Next steps

* [Microservice APIs that use Dapr](/en-us/azure/container-apps/dapr-overview): Learn how Azure Container Apps uses Dapr sidecars to help you build simple, portable, resilient, and secure microservices.
* [Native sidecar mode for Istio-based service mesh feature in Azure Kubernetes Service (AKS)](/en-us/azure/aks/istio-native-sidecar): Learn how the Istio service mesh feature for AKS uses the Sidecar pattern to address distributed architecture challenges.

## Related resource

* [Ambassador pattern](ambassador)

---

## Feedback

Was this page helpful?

Yes

No

No

Need help with this topic?

Want to try using Ask Learn to clarify or guide you through this topic?

Ask Learn

Ask Learn

 Suggest a fix?

---

## Additional resources

---

* Last updated on 
  2026-02-18

### In this article

Was this page helpful?

Yes

No

No

Need help with this topic?

Want to try using Ask Learn to clarify or guide you through this topic?

Ask Learn

Ask Learn

 Suggest a fix?

[en-us](#)

[Your Privacy Choices](https://aka.ms/yourcaliforniaprivacychoices)

Theme

* Light
* Dark
* High contrast

* [AI Disclaimer](https://learn.microsoft.com/en-us/principles-for-ai-generated-content)
* [Previous Versions](https://learn.microsoft.com/en-us/previous-versions/)
* [Blog](https://techcommunity.microsoft.com/t5/microsoft-learn-blog/bg-p/MicrosoftLearnBlog)
* [Contribute](https://learn.microsoft.com/en-us/contribute)
* [Privacy](https://go.microsoft.com/fwlink/?LinkId=521839)
* [Consumer Health Privacy](https://go.microsoft.com/fwlink/?linkid=2259814)
* [Terms of Use](https://learn.microsoft.com/en-us/legal/termsofuse)
* [Trademarks](https://www.microsoft.com/legal/intellectualproperty/Trademarks/)
* © Microsoft 2026