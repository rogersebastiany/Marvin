# Cloud Architecture Patterns


---

## 1. Retry pattern

Azure

Enable an application to handle transient failures when it tries to connect to a service or network resource, by transparently retrying a failed operation. This can improve the stability of the application.

## Context and problem

An application that communicates with elements running in the cloud has to be sensitive to the transient faults that can occur in this environment. Faults include the momentary loss of network connectivity to components and services, the temporary unavailability of a service, or timeouts that occur when a service is busy.

These faults are typically self-correcting, and if the action that triggered a fault is repeated after a suitable delay it's likely to be successful. For example, a database service that's processing a large number of concurrent requests can implement a [throttling strategy](/en-us/azure/architecture/patterns/throttling) that temporarily rejects any further requests until its workload has eased. An application trying to access the database might fail to connect, but if it tries again after a delay it might succeed.

## Solution

In the cloud, transient faults should be expected and an application should be designed to handle them elegantly and transparently. Doing so minimizes the effects faults can have on the business tasks the application is performing. The most common design pattern to address is to introduce a retry mechanism.

The diagram above illustrates invoking an operation in a hosted service using a retry mechanism. If the request is unsuccessful after a predefined number of attempts, the application should treat the fault as an exception and handle it accordingly.

Note

Due to the commonplace nature of transient faults, built-in retry mechanisms are now available in many client libraries and cloud services, with some degree of configurability for the number of maximum retries, the delay between retries, and other parameters. The [Microsoft Entity Framework](/en-us/ef) provides facilities to retry [failed database operations](/en-us/ef/core/miscellaneous/connection-resiliency).

### Retry strategies

If an application detects a failure when it tries to send a request to a remote service, it can handle the failure using the following strategies:

* **Cancel**. If the fault indicates that the failure isn't transient or is unlikely to be successful if repeated, the application should cancel the operation and report an exception.
* **Retry immediately**. If the specific fault reported is unusual or rare, like a network packet becoming corrupted while it was being transmitted, the best course of action might be to immediately retry the request.
* **Retry after delay**. If the fault is caused by one of the more commonplace connectivity or busy failures, the network or service might need a short period while the connectivity issues are corrected or the backlog of work is cleared, so programmatically delaying the retry is a good strategy. In many cases, the period between retries should be chosen to spread requests from multiple instances of the application as evenly as possible to reduce the chance of a busy service continuing to be overloaded.

If the request still fails, the application can wait and make another attempt. If necessary, this process can be repeated with increasing delays between retry attempts, until some maximum number of requests have been attempted. The delay can be increased incrementally or exponentially, depending on the type of failure and the probability that it'll be corrected during this time.

The application should wrap all attempts to access a remote service in code that implements a retry policy matching one of the strategies listed above. Requests sent to different services can be subject to different policies.

An application should log the details of faults and failing operations. This information is useful to operators. That being said, in order to avoid flooding operators with alerts on operations where subsequently retried attempts were successful, it is best to log early failures as *informational entries* and only the failure of the last of the retry attempts as an actual error. Here is an [example of how this logging model would look like](https://docs.particular.net/nservicebus/recoverability/#retry-logging).

If a service is frequently unavailable or busy, it's often because the service has exhausted its resources. You can reduce the frequency of these faults by scaling out the service. For example, if a database service is continually overloaded, it might be beneficial to partition the database and spread the load across multiple servers.

## Issues and considerations

You should consider the following points when deciding how to implement this pattern.

### Impact on performance

The retry policy should be tuned to match the business requirements of the application and the nature of the failure. For some noncritical operations, it's better to fail fast rather than retry several times and affect the throughput of the application. For example, in an interactive web application accessing a remote service, it's better to fail after a smaller number of retries with only a short delay between retry attempts, and display a suitable message to the user (for example, "please try again later"). For a batch application, it might be more appropriate to increase the number of retry attempts with an exponentially increasing delay between attempts.

An aggressive retry policy with minimal delay between attempts, and a large number of retries, could further degrade a busy service that's running close to or at capacity. This retry policy could also affect the responsiveness of the application if it's continually trying to perform a failing operation.

If a request still fails after a significant number of retries, it's better for the application to prevent further requests going to the same resource and report a failure immediately. When the period expires, the application can tentatively allow one or more requests through to see whether they're successful. For more information about this strategy, see [Circuit Breaker pattern](/en-us/azure/architecture/patterns/circuit-breaker).

### Idempotency

Consider whether the operation is idempotent. If so, it's inherently safe to retry. Otherwise, retries could cause the operation to be executed more than once, with unintended side effects. For example, a service might receive the request, process the request successfully, but fail to send a response. At that point, the retry logic might re-send the request, assuming that the first request wasn't received.

### Exception type

A request to a service can fail for various reasons raising different exceptions depending on the nature of the failure. Some exceptions indicate a failure that can be resolved quickly, while others indicate that the failure is longer lasting. It's useful for the retry policy to adjust the time between retry attempts based on the type of the exception.

### Transaction consistency

Consider how retrying an operation that's part of a transaction will affect the overall transaction consistency. Fine tune the retry policy for transactional operations to maximize the chance of success and reduce the need to undo all the transaction steps.

## General guidance

* Ensure that all retry code is fully tested against various failure conditions. Check that it doesn't severely affect the performance or reliability of the application, cause excessive load on services and resources, or generate race conditions or bottlenecks.
* Implement retry logic only where the full context of a failing operation is understood. For example, if a task that contains a retry policy invokes another task that also contains a retry policy, this extra layer of retries can add long delays to the processing. It might be better to configure the lower-level task to fail fast and report the reason for the failure back to the task that invoked it. This higher-level task can then handle the failure based on its own policy.
* Log all connectivity failures that cause a retry so that underlying problems with the application, services, or resources can be identified.
* Investigate the faults that are most likely to occur for a service or a resource to discover if they're likely to be long lasting or terminal. If they are, it's better to handle the fault as an exception. The application can report or log the exception, and then try to continue either by invoking an alternative service (if one is available), or by offering degraded functionality. For more information on how to detect and handle long-lasting faults, see the [Circuit Breaker pattern](/en-us/azure/architecture/patterns/circuit-breaker).

## When to use this pattern

Use this pattern when an application could experience transient faults as it interacts with a remote service or accesses a remote resource. These faults are expected to be short lived, and repeating a request that has previously failed could succeed on a subsequent attempt.

This pattern might not be useful:

* When a fault is likely to be long lasting, because this can affect the responsiveness of an application. The application might be wasting time and resources trying to repeat a request that's likely to fail.
* For handling failures that aren't due to transient faults, such as internal exceptions caused by errors in the business logic of an application.
* As an alternative to addressing scalability issues in a system. If an application experiences frequent busy faults, it's often a sign that the service or resource being accessed should be scaled up.

## Workload design

An architect should evaluate how the Retry pattern can be used in their workload's design to address the goals and principles covered in the [Azure Well-Architected Framework pillars](/en-us/azure/well-architected/pillars). For example:

| Pillar | How this pattern supports pillar goals |
| --- | --- |
| [Reliability](/en-us/azure/well-architected/reliability/checklist) design decisions help your workload become **resilient** to malfunction and to ensure that it **recovers** to a fully functioning state after a failure occurs. | Mitigating transient faults in a distributed system is a core technique for improving a workload's resilience.   - [RE:07 Self-preservation](/en-us/azure/well-architected/reliability/self-preservation)  - [RE:07 Transient faults](/en-us/azure/well-architected/reliability/handle-transient-faults) |

As with any design decision, consider any tradeoffs against the goals of the other pillars that might be introduced with this pattern.

## Example

Refer to the [Implement a retry policy with .NET](/en-us/azure/storage/blobs/storage-retry-policy) guide for a detailed example using the Azure SDK with built-in retry mechanism support.

## Next steps

* Before writing custom retry logic, consider using a general framework such as [Polly](https://www.pollydocs.org/) for .NET or [Resilience4j](https://resilience4j.readme.io/docs/getting-started) for Java.
* When processing commands that change business data, be aware that retries can result in the action being performed twice, which could be problematic if that action is something like charging a customer's credit card. Using the Idempotence pattern described in [this blog post](https://particular.net/blog/what-does-idempotent-mean) can help deal with these situations.

## Related resources

* [Reliable web app pattern](/en-us/azure/architecture/web-apps/guides/enterprise-app-patterns/overview#reliable-web-app-pattern) shows you how to apply the retry pattern to web applications converging on the cloud.
* For most Azure services, the client SDKs include built-in retry logic.
* [Circuit Breaker pattern](/en-us/azure/architecture/patterns/circuit-breaker). If a failure is expected to be more long lasting, it might be more appropriate to implement the Circuit Breaker pattern. Combining the Retry and Circuit Breaker patterns provides a comprehensive approach to handling faults.

---

## 2. Throttling pattern

Azure

Control the consumption of resources used by an instance of an application, an individual tenant, or an entire service. This can allow the system to continue to function and meet service-level objectives (SLOs), even when an increase in demand places an extreme load on resources.

## Context and problem

The load on a cloud application typically varies over time based on the number of active users or the types of activities they're performing. For example, more users are likely to be active during business hours, or the system might be required to perform computationally expensive analytics at the end of each month. There might also be sudden and unanticipated bursts in activity. If the processing requirements of the system exceed the capacity of the resources that are available, it'll experience poor performance and can even fail. If the system has to meet an agreed level of service, such failure could be unacceptable.

There are many strategies available for handling varying load in the cloud, depending on the business goals for the application. One strategy is to use [autoscaling](/en-us/azure/architecture/best-practices/auto-scaling) to match the provisioned resources to the user needs at any given time. This has the potential to consistently meet user demand, while optimizing running costs. However, while autoscaling can trigger the provisioning of more resources, this provisioning isn't immediate. If demand grows quickly, there can be a window of time where there's a resource deficit.

## Solution

An alternative strategy to autoscaling is to allow applications to use resources only up to a limit, and then throttle them when this limit is reached. The system should monitor how it's using resources so that, when usage exceeds the threshold, it can throttle requests from one or more users. This enables the system to continue functioning and meet any service-level objectives (SLOs) that are in place. For more information on monitoring resource usage, see the [Instrumentation and Telemetry Guidance](/en-us/previous-versions/msp-n-p/dn589775(v=pandp.10)).

The system could implement several throttling strategies, including:

* Rejecting requests from an individual user who's already accessed system APIs more than n times per second over a given period of time. This requires the system to meter the use of resources for each tenant or user running an application. For more information, see the [Service Metering Guidance](/en-us/previous-versions/msp-n-p/dn589796(v=pandp.10)).
* Disabling or degrading the functionality of selected nonessential services so that essential services can run unimpeded with sufficient resources. For example, if the application is streaming video output, it could switch to a lower resolution.
* Using load leveling to smooth the volume of activity (this approach is covered in more detail by the [Queue-based Load Leveling pattern](/en-us/azure/architecture/patterns/queue-based-load-leveling)). In a multitenant environment, this approach will reduce the performance for every tenant. If the system must support a mix of tenants with different SLAs, the work for high-value tenants might be performed immediately. Requests for other tenants can be held back, and handled when the backlog has eased. The [Priority Queue pattern](/en-us/azure/architecture/patterns/priority-queue) could be used to help implement this approach, as could exposing different endpoints for the different service levels/priorities.
* Deferring operations being performed on behalf of lower priority applications or tenants. These operations can be suspended or limited, with an exception generated to inform the tenant that the system is busy and that the operation should be retried later.
* You should be careful when integrating with some 3rd-party services that might become unavailable or return errors. Reduce the number of concurrent requests being processed so that the logs do not unnecessarily fill up with errors. You also avoid the costs that are associated with needlessly retrying the processing of requests that would fail because of that 3rd-party service. Then, when requests are processed successfully, go back to regular unthrottled request processing. One library that implements this functionality is [NServiceBus](https://docs.particular.net/nservicebus/recoverability/#automatic-rate-limiting).

The figure shows an area graph for resource use (a combination of memory, CPU, bandwidth, and other factors) against time for applications that are making use of three features. A feature is an area of functionality, such as a component that performs a specific set of tasks, a piece of code that performs a complex calculation, or an element that provides a service such as an in-memory cache. These features are labeled A, B, and C.

> The area immediately below the line for a feature indicates the resources that are used by applications when they invoke this feature. For example, the area below the line for Feature A shows the resources used by applications that are making use of Feature A, and the area between the lines for Feature A and Feature B indicates the resources used by applications invoking Feature B. Aggregating the areas for each feature shows the total resource use of the system.

The previous figure shows the effects of deferring operations. Just before time T1, the total resources allocated to all applications that use these features reach a threshold. That threshold represents the limit of resource use. At this point, the applications are in danger of exhausting the resources available. In this system, Feature B is less critical than Feature A or Feature C, so it's temporarily disabled and the resources that it was using are released. Between times T1 and T2, the applications using Feature A and Feature C continue running as normal. Eventually, the resource use of these two features diminishes to the point when, at time T2, there is sufficient capacity to enable Feature B again.

The autoscaling and throttling approaches can also be combined to help keep the applications responsive and within SLAs. If the demand is expected to remain high, throttling provides a temporary solution while the system scales out. At this point, the full functionality of the system can be restored.

The next figure shows an area graph of the overall resource use by all applications running in a system against time, and illustrates how throttling can be combined with autoscaling.

At time T1, the threshold specifying the soft limit of resource use is reached. At this point, the system can start to scale out. However, if the new resources don't become available quickly enough, then the existing resources might be exhausted and the system could fail. To prevent this from occurring, the system is temporarily throttled, as described earlier. When autoscaling has completed and the extra resources are available, throttling can be relaxed.

## Issues and considerations

You should consider the following points when deciding how to implement this pattern:

* Throttling an application, and the strategy to use, is an architectural decision that affects the entire design of a system. Throttling should be considered early in the application design process because it isn't easy to add once a system has been implemented.
* Throttling must be performed quickly. The system must be capable of detecting an increase in activity and react accordingly. The system must also be able to revert to its original state quickly after the load has eased. This requires that the appropriate performance data is continually captured and monitored.
* If a service needs to deny a user request temporarily, it should return a specific error code like 429 ("Too many requests") and 503 ("Server Too Busy") so the client application can understand that the reason for the refusal to serve a request is due to throttling.

  + HTTP 429 indicates the calling application sent too many requests in a time window and exceeded a predetermined limit.
  + HTTP 503 indicates the service isn't ready to handle the request. The common cause is that the service is experiencing more temporary load spikes than expected.

The client application can wait for a period before retrying the request. A `Retry-After` HTTP header should be included, to support the client in choosing the retry strategy.

* Throttling can be used as a temporary measure while a system autoscales. In some cases, it's better to throttle rather than scale if a burst in activity is sudden and not expected to last because scaling can add considerably to running costs.
* If throttling is being used as a temporary measure while a system autoscales, and if resource demands grow very quickly, the system might not be able to continue functioning—even when operating in a throttled mode. If this isn't acceptable, consider maintaining larger capacity reserves and configuring more aggressive autoscaling.
* Normalize resource costs for different operations as they generally don't carry equal execution costs. For example, throttling limits might be lower for read operations and higher for write operations. Not considering the cost of an operation can result in exhausted capacity and exposing a potential attack vector.
* Dynamic configuration change of throttling behavior at runtime is desirable. If a system faces an abnormal load that the applied configuration cannot handle, throttling limits might need to increase or decrease to stabilize the system and keep up with the current traffic. Expensive, risky, and slow deployments are not desirable at this point. Using the [External Configuration Store pattern](/en-us/azure/architecture/patterns/external-configuration-store) throttling configuration is externalized and can be changed and applied without deployments.

## When to use this pattern

Use this pattern:

* To ensure that a system continues to meet service-level objectives (SLOs).
* To prevent a single tenant from monopolizing the resources provided by an application.
* To handle bursts in activity.
* To help cost-optimize a system by limiting the maximum resource levels needed to keep it functioning.
* To reduce low value compute processing during periods of high carbon intensity in the energy grid.

## Workload design

An architect should evaluate how the Throttling pattern can be used in their workload's design to address the goals and principles covered in the [Azure Well-Architected Framework pillars](/en-us/azure/well-architected/pillars). For example:

| Pillar | How this pattern supports pillar goals |
| --- | --- |
| [Reliability](/en-us/azure/well-architected/reliability/checklist) design decisions help your workload become **resilient** to malfunction and to ensure that it **recovers** to a fully functioning state after a failure occurs. | You design the limits to help prevent resource exhaustion that might lead to malfunctions. You can also use this pattern as a control mechanism in a graceful degradation plan.   - [RE:07 Self-preservation](/en-us/azure/well-architected/reliability/self-preservation) |
| [Security](/en-us/azure/well-architected/security/checklist) design decisions help ensure the **confidentiality**, **integrity**, and **availability** of your workload's data and systems. | You can design the limits to help prevent resource exhaustion that could result from automated abuse of the system.   - [SE:06 Network controls](/en-us/azure/well-architected/security/networking)  - [SE:08 Hardening resources](/en-us/azure/well-architected/security/harden-resources) |
| [Cost Optimization](/en-us/azure/well-architected/cost-optimization/checklist) is focused on **sustaining and improving** your workload's **return on investment**. | The enforced limits can inform cost modeling and can even be directly tied to the business model of your application. They also put clear upper bounds on utilization, which can be factored into resource sizing.   - [CO:02 Cost model](/en-us/azure/well-architected/cost-optimization/cost-model)  - [CO:12 Scaling costs](/en-us/azure/well-architected/cost-optimization/optimize-scaling-costs) |
| [Performance Efficiency](/en-us/azure/well-architected/performance-efficiency/checklist) helps your workload **efficiently meet demands** through optimizations in scaling, data, code. | When the system is under high demand, this pattern helps mitigate congestion that can lead to performance bottlenecks. You can also use it to proactively avoid noisy neighbor scenarios.   - [PE:02 Capacity planning](/en-us/azure/well-architected/performance-efficiency/capacity-planning)  - [PE:05 Scaling and partitioning](/en-us/azure/well-architected/performance-efficiency/scale-partition) |

As with any design decision, consider any tradeoffs against the goals of the other pillars that might be introduced with this pattern.

## Example

The final figure illustrates how throttling can be implemented in a multitenant system. Users from each of the tenant organizations access a cloud-hosted application where they fill out and submit surveys. The application contains instrumentation that monitors the rate at which these users are submitting requests to the application.

In order to prevent the users from one tenant affecting the responsiveness and availability of the application for all other users, a limit is applied to the number of requests per second the users from any one tenant can submit. The application blocks requests that exceed this limit.

## Next steps

The following guidance might also be relevant when implementing this pattern:

* [Instrumentation and Telemetry Guidance](/en-us/previous-versions/msp-n-p/dn589775(v=pandp.10)). Throttling depends on gathering information about how heavily a service is being used. Describes how to generate and capture custom monitoring information.
* [Service Metering Guidance](/en-us/previous-versions/msp-n-p/dn589796(v=pandp.10)). Describes how to meter the use of services in order to gain an understanding of how they're used. This information can be useful in determining how to throttle a service.
* [Autoscaling Guidance](/en-us/previous-versions/msp-n-p/dn589774(v=pandp.10)). Throttling can be used as an interim measure while a system autoscales, or to remove the need for a system to autoscale. Contains information on autoscaling strategies.

## Related resources

The following patterns might also be relevant when implementing this pattern:

* [Queue-based Load Leveling pattern](/en-us/azure/architecture/patterns/queue-based-load-leveling). Queue-based load leveling is a commonly used mechanism for implementing throttling. A queue can act as a buffer that helps to even out the rate at which requests sent by an application are delivered to a service.
* [Priority Queue pattern](/en-us/azure/architecture/patterns/priority-queue). A system can use priority queuing as part of its throttling strategy to maintain performance for critical or higher value applications, while reducing the performance of less important applications.
* [External Configuration Store pattern](/en-us/azure/architecture/patterns/external-configuration-store). Centralizing and externalizing the throttling policies provides the capability to change the configuration at runtime without the need for a redeployment. Services can subscribe to configuration changes, which applies the new configuration immediately, to stabilize a system.

---

## 3. Sidecar pattern

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

## 4. Saga distributed transactions pattern

Azure

The Saga design pattern helps maintain data consistency in distributed systems by coordinating transactions across multiple services. A saga is a sequence of local transactions where each service performs its operation and initiates the next step through events or messages. If a step in the sequence fails, the saga performs compensating transactions to undo the completed steps. This approach helps maintain data consistency.

## Context and problem

A *transaction* represents a unit of work, which can include multiple operations. Within a transaction, an *event* refers to a state change that affects an entity. A *command* encapsulates all information needed to perform an action or trigger a subsequent event.

Transactions must adhere to the principles of atomicity, consistency, isolation, and durability (ACID).

* **Atomicity:** All operations succeed or no operations succeed.
* **Consistency:** Data transitions from one valid state to another valid state.
* **Isolation:** Concurrent transactions yield the same results as sequential transactions.
* **Durability:** Changes persist after they're committed, even when failures occur.

In a single service, transactions follow ACID principles because they operate within a single database. However, it can be more complex to achieve ACID compliance across multiple services.

### Challenges in microservices architectures

Microservices architectures typically assign a [dedicated database to each microservice](/en-us/dotnet/architecture/cloud-native/distributed-data#database-per-microservice-why). This approach provides several benefits:

* Each service encapsulates its own data.
* Each service can use the most suitable database technology and schema for its specific needs.
* Databases for each service can be scaled independently.
* Failures in one service are isolated from other services.

Despite these advantages, this architecture complicates cross-service data consistency. Traditional database guarantees like ACID aren't directly applicable to multiple independently managed data stores. Because of these limitations, architectures that rely on interprocess communication, or traditional transaction models like two-phase commit protocol, are often better suited for the Saga pattern.

## Solution

The Saga pattern manages transactions by breaking them into a sequence of *local transactions*.

Each local transaction:

1. Completes its work atomically within a single service.
2. Updates the service's database.
3. Initiates the next transaction via an event or message.

If a local transaction fails, the saga performs a series of *compensating transactions* to reverse the changes that the preceding local transactions made.

### Key concepts in the Saga pattern

* **Compensable transactions** can be undone or compensated for by other transactions with the opposite effect. If a step in the saga fails, compensating transactions undo the changes that the compensable transactions made.
* **Pivot transactions** serve as the point of no return in the saga. After a pivot transaction succeeds, compensable transactions are no longer relevant. All subsequent actions must be completed for the system to achieve a consistent final state. A pivot transaction can assume different roles, depending on the flow of the saga:

  + **Irreversible or noncompensable transactions** can't be undone or retried.
  + **The boundary between reversible and committed** means that the pivot transaction can be the last undoable, or compensable, transaction. Or it can be the first retryable operation in the saga.
* **Retryable transactions** follow the pivot transaction. Retryable transactions are idempotent and help ensure that the saga can reach its final state, even if temporary failures occur. They help the saga eventually achieve a consistent state.

### Saga implementation approaches

The two typical saga implementation approaches are *choreography* and *orchestration*. Each approach has its own set of challenges and technologies to coordinate the workflow.

#### Choreography

In the choreography approach, services exchange events without a centralized controller. With choreography, each local transaction publishes domain events that trigger local transactions in other services.

| Benefits of choreography | Drawbacks of choreography |
| --- | --- |
| Good for simple workflows that have few services and don't need a coordination logic. | Workflow can be confusing when you add new steps. It's difficult to track which commands each saga participant responds to. |
| No other service is required for coordination. | There's a risk of cyclic dependency between saga participants because they have to consume each other's commands. |
| Doesn't introduce a single point of failure because the responsibilities are distributed across the saga participants. | Integration testing is difficult because all services must run to simulate a transaction. |

#### Orchestration

In orchestration, a centralized controller, or *orchestrator*, handles all the transactions and tells the participants which operation to perform based on events. The orchestrator performs saga requests, stores and interprets the states of each task, and handles failure recovery by using compensating transactions.

| Benefits of orchestration | Drawbacks of orchestration |
| --- | --- |
| Better suited for complex workflows or when you add new services. | Other design complexity requires an implementation of a coordination logic. |
| Avoids cyclic dependencies because the orchestrator manages the flow. | Introduces a point of failure because the orchestrator manages the complete workflow. |
| Clear separation of responsibilities simplifies service logic. |  |

## Problems and considerations

Consider the following points as you decide how to implement this pattern:

* **Shift in design thinking:** Adopting the Saga pattern requires a different mindset. It requires you to focus on transaction coordination and data consistency across multiple microservices.
* **Complexity of debugging sagas:** Debugging sagas can be complex, specifically as the number of participating services grows.
* **Irreversible local database changes:** Data can't be rolled back because saga participants commit changes to their respective databases.
* **Handling transient failures and idempotence:** The system must handle transient failures effectively and ensure idempotence, when repeating the same operation doesn't alter the outcome. For more information, see [Idempotent message processing](/en-us/azure/architecture/reference-architectures/containers/aks-mission-critical/mission-critical-data-platform#idempotent-message-processing).
* **Need for monitoring and tracking sagas:** Monitoring and tracking the workflow of a saga are essential tasks to maintain operational oversight.
* **Limitations of compensating transactions:** Compensating transactions might not always succeed, which can leave the system in an inconsistent state.

### Potential data anomalies in sagas

Data anomalies are inconsistencies that can occur when sagas operate across multiple services. Because each service manages its own data, called *participant data*, there's no built-in isolation across services. This setup can result in data inconsistencies or durability problems, such as partially applied updates or conflicts between services. Typical problems include:

* **Lost updates:** When one saga modifies data without considering changes made by another saga, it results in overwritten or missing updates.
* **Dirty reads:** When a saga or transaction reads data that another saga has modified, but the modification isn't complete.
* **Fuzzy, or nonrepeatable, reads:** When different steps in a saga read inconsistent data because updates occur between the reads.

### Strategies to address data anomalies

To reduce or prevent these anomalies, consider the following countermeasures:

* **Semantic lock:** Use application-level locks when a saga's compensable transaction uses a semaphore to indicate that an update is in progress.
* **Commutative updates:** Design updates so that they can be applied in any order while still producing the same result. This approach helps reduce conflicts between sagas.
* **Pessimistic view:** Reorder the sequence of the saga so that data updates occur in retryable transactions to eliminate dirty reads. Otherwise, one saga could read dirty data, or *uncommitted changes*, while another saga simultaneously performs a compensable transaction to roll back its updates.
* **Reread values:** Confirm that data remains unchanged before you make updates. If data changes, stop the current step and restart the saga as needed.
* **Version files:** Maintain a log of all operations performed on a record and ensure that they're performed in the correct sequence to prevent conflicts.
* **Risk-based concurrency based on value:** Dynamically choose the appropriate concurrency mechanism based on the potential business risk. For example, use sagas for low-risk updates and distributed transactions for high-risk updates.

## When to use this pattern

Use this pattern when:

* You need to ensure data consistency in a distributed system without tight coupling.
* You need to roll back or compensate if one of the operations in the sequence fails.

This pattern might not be suitable when:

* Transactions are tightly coupled.
* Compensating transactions occur in earlier participants.
* There are cyclic dependencies.

## Next step

## Related resources

The following patterns might be relevant when you implement this pattern:

* The [Choreography pattern](/en-us/azure/architecture/patterns/choreography) has each component of the system participate in the decision-making process about the workflow of a business transaction, instead of relying on a central point of control.
* The [Compensating Transaction pattern](/en-us/azure/architecture/patterns/compensating-transaction) undoes work performed by a series of steps, and eventually defines a consistent operation if one or more steps fail. Cloud-hosted applications that implement complex business processes and workflows often follow this *eventual consistency model*.
* The [Retry pattern](/en-us/azure/architecture/patterns/retry) lets an application handle transient failures when it tries to connect to a service or network resource by transparently retrying the failed operation. This pattern can improve the stability of the application.
* The [Circuit Breaker pattern](/en-us/azure/architecture/patterns/circuit-breaker) handles faults that take a variable amount of time to recover from, when you connect to a remote service or resource. This pattern can improve the stability and resiliency of an application.
* The [Health Endpoint Monitoring pattern](/en-us/azure/architecture/patterns/health-endpoint-monitoring) implements functional checks in an application that external tools can access through exposed endpoints at regular intervals. This pattern can help you verify that applications and services are performing correctly.

---

## 5. Circuit Breaker pattern

The Circuit Breaker pattern helps handle faults that might take varying amounts of time to recover from when an application connects to a remote service or resource. A circuit breaker temporarily blocks access to a faulty service after it detects failures. This action prevents repeated unsuccessful attempts so that the system can recover effectively. This pattern can improve the stability and resiliency of an application.

## Context and problem

In a distributed environment, calls to remote resources and services can fail because of transient faults. Transient faults include overcommitted or temporarily unavailable resources, slow network connections, or time-outs. These faults typically correct themselves after a short period of time. To help manage these faults, you should design a cloud application to use a strategy, such as the [Retry pattern](retry).

Unanticipated events can create faults that take longer to fix. These faults can range in severity from a partial loss of connectivity to a complete service failure. In these situations, an application shouldn't continually retry an operation that's unlikely to succeed. Instead, the application should quickly recognize the failed operation and handle the failure accordingly.

If a service is busy, failure in one part of the system might lead to cascading failures. For example, you can configure an operation that invokes a service to implement a time-out. If the service fails to respond within this period, the operation replies with a failure message.

However, this strategy can block concurrent requests to the same operation until the time-out period expires. These blocked requests might hold critical system resources, such as memory, threads, and database connections. This problem can exhaust resources, which might fail other unrelated parts of the system that need to use the same resources.

In these situations, an operation should fail immediately and only attempt to invoke the service if it's likely to succeed. To resolve this problem, set a shorter time-out. But ensure that the time-out is long enough for the operation to succeed most of the time.

## Solution

The Circuit Breaker pattern helps prevent an application from repeatedly trying to run an operation that's likely to fail. This pattern enables the application to continue running without waiting for the fault to be fixed or wasting CPU cycles on determining that the fault is persistent. The Circuit Breaker pattern also enables an application to detect when the fault is resolved. If the fault is resolved, the application can try to invoke the operation again.

Note

The Circuit Breaker pattern serves a different purpose than the Retry pattern. The Retry pattern enables an application to retry an operation with the expectation that it eventually succeeds. The Circuit Breaker pattern prevents an application from performing an operation that's likely to fail. An application can combine these two patterns by using the Retry pattern to invoke an operation through a circuit breaker. However, the retry logic should be sensitive to any exceptions that the circuit breaker returns and stop retry attempts if the circuit breaker indicates that a fault isn't transient.

A circuit breaker acts as a proxy for operations that might fail. The proxy should monitor the number of recent failures and use this information to decide whether to allow the operation to proceed or to return an exception immediately.

You can implement the proxy as a state machine that includes the following states. These states mimic the functionality of an electrical circuit breaker:

* **Closed:** The request from the application is routed to the operation. The proxy maintains a count of the number of recent failures. If the call to the operation is unsuccessful, the proxy increments this count. If the number of recent failures exceeds a specified threshold within a given time period, the proxy is placed into the **Open** state and starts a time-out timer. When the timer expires, the proxy is placed into the **Half-Open** state.

  Note

  During the time-out, the system tries to fix the problem that caused the failure before it allows the application to attempt the operation again.
* **Open:** The request from the application fails immediately and an exception is returned to the application.
* **Half-Open:** A limited number of requests from the application are allowed to pass through and invoke the operation. If these requests are successful, the circuit breaker assumes that the fault that caused the failure is fixed, and the circuit breaker switches to the **Closed** state. The failure counter is reset. If any request fails, the circuit breaker assumes that the fault is still present, so it reverts to the **Open** state. It restarts the time-out timer so that the system can recover from the failure.

  Note

  The **Half-Open** state helps prevent a recovering service from suddenly being flooded with requests. As a service recovers, it might be able to support a limited volume of requests until the recovery is complete. But while recovery is in progress, a flood of work can cause the service to time out or fail again.

The following diagram shows the counter operations for each state.

[The diagram shows three sections that are labeled closed, half-open, and open. The closed state includes the action to reset the failure counter. If the operation succeeds, it returns a result, otherwise the increment failure counter returns a failure. The half-open state includes the action to reset the success counter. If the operation succeeds, the increment success counter returns a result, otherwise it returns a failure. The open state includes the actions to start the time-out timer and then return a failure. An arrow from the closed to open state indicates that the failure threshold is reached. An arrow from the open to half-open state indicates that the time-out timer expired. An arrow from the half-open to closed state indicates that the success count threshold is reached. An arrow from the half-open to open state indicates that the operation failed.](_images/circuit-breaker-diagram.png#lightbox)

The failure counter for the **Closed** state is time based. It automatically resets at periodic intervals. This design helps prevent the circuit breaker from entering the **Open** state if it experiences occasional failures. The failure threshold triggers the **Open** state only when a specified number of failures occur during a specified interval.

The success counter for the **Half-Open** state records the number of successful attempts to invoke the operation. The circuit breaker reverts to the **Closed** state after a specified number of successful, consecutive operation invocations. If any invocation fails, the circuit breaker enters the **Open** state immediately and the success counter resets the next time it enters the **Half-Open** state.

Note

System recovery is based on external operations, such as restoring or restarting a failed component or repairing a network connection.

The Circuit Breaker pattern provides stability while the system recovers from a failure and minimizes the impact on performance. It can help maintain the response time of the system. This pattern quickly rejects a request for an operation that's likely to fail, rather than waiting for the operation to time out or never return. If the circuit breaker raises an event each time it changes state, this information can help monitor the health of the protected system component or alert an administrator when a circuit breaker switches to the **Open** state.

You can customize and adapt this pattern to different types of failures. For example, you can apply an increasing time-out timer to a circuit breaker. You can place the circuit breaker in the **Open** state for a few seconds initially. If the failure isn't resolved, increase the time-out to a few minutes and adjust accordingly. In some cases, rather than returning a failure and raising an exception, the **Open** state can return a default value that's meaningful to the application.

Note

Traditionally, circuit breakers relied on preconfigured thresholds, such as failure count and time-out duration. This approach resulted in a deterministic but sometimes suboptimal behavior.

Adaptive techniques that use AI and machine learning can dynamically adjust thresholds based on real-time traffic patterns, anomalies, and historical failure rates. This approach improves resiliency and efficiency.

## Problems and considerations

Consider the following factors when you implement this pattern:

* **Exception handling:** An application that invokes an operation through a circuit breaker must be able to handle the exceptions if the operation is unavailable. Exception management is based on the application. For example, an application might temporarily degrade its functionality, invoke an alternative operation to try to perform the same task or obtain the same data, or report the exception to the user and ask them to try again later.
* **Types of exceptions:** The reasons for a request failure can vary in severity. For example, a request might fail because a remote service crashes and requires several minutes to recover, or because an overloaded service causes a time-out. A circuit breaker might be able to examine the types of exceptions that occur and adjust its strategy based on the nature of these exceptions. For example, it might require a larger number of time-out exceptions to trigger the circuit breaker to the **Open** state compared to the number of failures caused by the unavailable service.
* **Monitoring:** A circuit breaker should provide clear observability into both failed and successful requests so that operations teams can assess system health. Use distributed tracing for end-to-end visibility across services.
* **Recoverability:** You should configure the circuit breaker to match the likely recovery pattern of the operation that it protects. For example, if the circuit breaker remains in the **Open** state for a long period, it can raise exceptions even if the reason for the failure is resolved. Similarly, a circuit breaker can fluctuate and reduce the response times of applications if it switches from the **Open** state to the **Half-Open** state too quickly.
* **Failed operations testing:** In the **Open** state, rather than using a timer to determine when to switch to the **Half-Open** state, a circuit breaker can periodically ping the remote service or resource to determine whether it's available. This ping can either attempt to invoke a previously failed operation or use a special health-check operation that the remote service provides. For more information, see [Health Endpoint Monitoring pattern](health-endpoint-monitoring).
* **Manual override:** If the recovery time for a failing operation is extremely variable, you should provide a manual reset option that enables an administrator to close a circuit breaker and reset the failure counter. Similarly, an administrator can force a circuit breaker into the **Open** state and restart the time-out timer if the protected operation is temporarily unavailable.
* **Concurrency:** A large number of concurrent instances of an application can access the same circuit breaker. The implementation shouldn't block concurrent requests or add excessive overhead to each call to an operation.
* **Resource differentiation:** Be careful when you use a single circuit breaker for one type of resource if there might be multiple underlying independent providers. For example, in a data store that contains multiple shards, one shard might be fully accessible while another experiences a temporary problem. If the error responses in these scenarios are merged, an application might try to access some shards even when failure is likely. And access to other shards might be blocked even though it's likely to succeed.
* **Accelerated circuit breaking:** Sometimes a failure response can contain enough information for the circuit breaker to trip immediately and stay tripped for a minimum amount of time. For example, the error response from a shared resource that's overloaded can indicate that the application should instead try again in a few minutes, instead of immediately retrying.
* **Multiregion deployments:** You can design a circuit breaker for single region or multiregion deployments. To design for multiregion deployments, use global load balancers or custom region-aware circuit breaking strategies that help ensure controlled failover, latency optimization, and regulatory compliance.
* **Service mesh circuit breakers:** You can implement circuit breakers at the application layer or as a cross-cutting, abstracted feature. For example, service meshes often support circuit breaking as a <sidecar> or as a standalone capability without modifying application code.

  Note

  A service can return HTTP 429 (too many requests) if it's throttling the client or HTTP 503 (service unavailable) if the service isn't available. The response can include other information, such as the anticipated duration of the delay.
* **Failed request replay:** In the **Open** state, rather than failing immediately, a circuit breaker can record the details of each request in a journal and arrange for these requests to be replayed when the remote resource or service becomes available.
* **Inappropriate time-outs on external services:** A circuit breaker might not fully protect applications from failures in external services that have long time-out periods. If the time-out is too long, a thread that runs a circuit breaker might be blocked for an extended period before the circuit breaker indicates that the operation failed. During this time, many other application instances might also try to invoke the service through the circuit breaker and tie up numerous threads before they all fail.
* **Adaptability to compute diversification:** Circuit breakers should account for different compute environments, from serverless to containerized workloads, where factors like cold starts and scalability affect failure handling. Adaptive approaches can dynamically adjust strategies based on the compute type, which helps ensure resilience across heterogeneous architectures.

## When to use this pattern

Use this pattern when:

* You want to prevent cascading failures by stopping excessive remote service calls or access requests to a shared resource if these operations are likely to fail.
* You want to route traffic intelligently based on real-time failure signals to enhance multiregion resilience.
* You want to protect against slow dependencies so that you can maintain your service-level objectives and avoid performance degradation from high-latency services.
* You want to manage intermittent connectivity problems and reduce request failures in distributed environments.

This pattern might not be suitable when:

* You need to manage access to local private resources in an application, such as in-memory data structures. In this environment, a circuit breaker adds overhead to your system.
* You need to use it as a substitute for handling exceptions in the business logic of your applications.
* Well-known retry algorithms are sufficient and your dependencies are designed to handle retry mechanisms. In this scenario, a circuit breaker in your application might add unnecessary complexity to your system.
* Waiting for a circuit breaker to reset might introduce unacceptable delays.
* You have a message-driven or event-driven architecture, because they often route failed messages to a dead letter queue for manual or deferred processing. Built-in failure isolation and retry mechanisms are often sufficient.
* Failure recovery is managed at the infrastructure or platform level, such as with health checks in global load balancers or service meshes.

## Workload design

Evaluate how to use the Circuit Breaker pattern in a workload's design to address the goals and principles covered in the [Azure Well-Architected Framework pillars](/en-us/azure/well-architected/pillars). The following table provides guidance about how this pattern supports the goals of each pillar.

| Pillar | How this pattern supports pillar goals |
| --- | --- |
| [Reliability](/en-us/azure/well-architected/reliability/checklist) design decisions help your workload become **resilient** to malfunction and ensure that it **recovers** to a fully functioning state after a failure occurs. | This pattern helps prevent a faulting dependency from overloading. Use this pattern to trigger graceful degradation in the workload. Couple circuit breakers with automatic recovery to provide self-preservation and self-healing.   - [RE:03 Failure mode analysis](/en-us/azure/well-architected/reliability/failure-mode-analysis)  - [Transient faults](/en-us/azure/well-architected/reliability/handle-transient-faults)  - [RE:07 Self-preservation](/en-us/azure/well-architected/reliability/self-preservation) |
| [Performance Efficiency](/en-us/azure/well-architected/performance-efficiency/checklist) helps your workload **efficiently meet demands** through optimizations in scaling, data, and code. | This pattern avoids the retry-on-error approach, which can lead to excessive resource usage during dependency recovery and can overload performance on a dependency that's attempting recovery.   - [PE:07 Code and infrastructure](/en-us/azure/well-architected/performance-efficiency/optimize-code-infrastructure)  - [PE:11 Live-issues responses](/en-us/azure/well-architected/performance-efficiency/respond-live-performance-issues) |

If this pattern introduces trade-offs within a pillar, consider them against the goals of the other pillars.

## Example

This example implements the Circuit Breaker pattern to help prevent quota overrun by using the [Azure Cosmos DB lifetime free tier](/en-us/azure/cosmos-db/free-tier). This tier is primarily for noncritical data and operates under a capacity plan that allocates a specific quota of resource units per second. During seasonal events, demand might exceed the provided capacity, which can result in `429` responses.

When demand spikes occur, [Azure Monitor alerts with dynamic thresholds](/en-us/azure/azure-monitor/alerts/alerts-dynamic-thresholds) detect and proactively notify the operations and management teams that the database requires more capacity. Simultaneously, a circuit breaker that's tuned by using historical error patterns trips to prevent cascading failures. In this state, the application gracefully degrades by returning default or cached responses. The application informs users of the temporary unavailability of certain data while preserving overall system stability.

This strategy enhances resilience that aligns with business justification. It controls capacity surges so that workload teams can manage cost increases deliberately and maintain service quality without unexpectedly increasing operating expenses. After demand subsides or increased capacity is confirmed, the circuit breaker resets, and the application returns to full functionality that aligns with both technical and budgetary objectives.

[The diagram has three primary sections. The first section contains two web browser icons. The first icon displays a fully functional user interface, and the second icon shows a degraded user experience that has an on-screen warning to indicate the problem to users. The second section is enclosed within a dashed-line rectangle, which is divided into two groups. The top group includes the workload resources, App Service and Azure Cosmos DB. Arrows from both web browser icons point to the App Service instance, representing incoming requests from the client. Additionally, arrows from the App Service instance point to the Azure Cosmos DB, which indicate data interactions between the application services and the database. Another arrow loops from the App Service instance back to itself, symbolizing the circuit breaker time-out mechanism. This loop signifies that when a 429 Too Many Requests response is detected, the system falls back to serving cached responses, degrading the user experience until the situation resolves. The bottom group of this section focuses on observability and alerting. Azure Monitor collects data from the Azure resources in the top group. Azure Monitor also connects to an alert rule icon. The third section shows the scalability workflow that's triggered when the alert is raised. An arrow connects the alert icon to the approvers, which indicates that the notification is sent to them for review. Another arrow leads from the approvers to a development console, which signifies the approval process for scaling the database. Finally, a subsequent arrow extends from the development console to Azure Cosmos DB, which depicts the action of scaling the database in response to the overload condition.](_images/circuit-breaker-pattern.svg#lightbox)

*Download a [Visio file](https://arch-center.azureedge.net/circuit-breaker-pattern.vsdx) of this architecture.*

### Flow A: Closed state

* The system operates normally, and all requests reach the database without returning any `429` HTTP responses.
* The circuit breaker remains closed, and no default or cached responses are necessary.

### Flow B: Open state

1. When the circuit breaker receives the first `429` response, it trips to an **Open** state.
2. Subsequent requests are immediately short-circuited, which returns default or cached responses and informs users of temporary degradation. The application is protected from further overload.
3. Azure Monitor receives logs and telemetry data and evaluates them against dynamic thresholds. An alert triggers if the conditions of the alert rule are met.
4. An action group proactively notifies the operations team of the overload condition.
5. After workload team approval, the operations team can increase the provisioned throughput to alleviate overload or delay scaling if the load subsides naturally.

### Flow C: Half-Open state

1. After a predefined time-out, the circuit breaker enters a **Half-Open** state that permits a limited number of trial requests.
2. If these trial requests succeed without returning `429` responses, the breaker resets to a **Closed** state, and normal operations restore back to Flow A. If failures persist, the breaker reverts to the **Open** state, or Flow B.

### Components

* [Azure App Service](/en-us/azure/well-architected/service-guides/app-service-web-apps) hosts the web application that serves as the primary entry point for client requests. The application code implements the logic that enforces circuit breaker policies and delivers default or cached responses when the circuit is open. This architecture helps prevent overload on downstream systems and maintain the user experience during peak demand or failures.
* [Azure Cosmos DB](/en-us/azure/well-architected/service-guides/cosmos-db) is one of the application's data stores. It serves noncritical data via the free tier, which is ideal for small production workloads. The circuit breaker mechanism helps limit traffic to the database during high-demand periods.
* [Azure Monitor](/en-us/azure/well-architected/service-guides/azure-log-analytics) functions as the centralized monitoring solution. It aggregates all activity logs to help ensure comprehensive, end-to-end observability. Azure Monitor receives logs and telemetry data from App Service and key metrics from Azure Cosmos DB (like the number of `429` responses) for aggregation and analysis.
* [Azure Monitor alerts](/en-us/azure/azure-monitor/alerts/alerts-overview) weigh alert rules against [dynamic thresholds](/en-us/azure/azure-monitor/alerts/alerts-dynamic-thresholds) to identify potential outages based on historical data. Predefined alerts notify the operations team when thresholds are breached.

  Sometimes, the workload team might approve an increase in provisioned throughput, but the operations team anticipates that the system can recover on its own because the load isn't too high. In these cases, the circuit breaker time-out elapses naturally. During this time, if the `429` responses cease, the threshold calculation detects the prolonged outages and excludes them from the learning algorithm. As a result, the next time an overload occurs, the threshold waits for a higher error rate in Azure Cosmos DB, which delays the notification. This adjustment allows the circuit breaker to handle the problem without an immediate alert, which improves cost and operational efficiency.

## Related resources

* The [Reliable Web App pattern](../web-apps/guides/enterprise-app-patterns/overview#reliable-web-app-pattern) applies the Circuit Breaker pattern to web applications that converge on the cloud.
* The [Retry pattern](retry) describes how an application can handle anticipated temporary failures when it tries to connect to a service or network resource by transparently retrying an operation that previously failed.
* The [Health Endpoint Monitoring pattern](health-endpoint-monitoring) describes how a circuit breaker can test the health of a service by sending a request to an endpoint that the service exposes. The service should return information that indicates its status.

---

## 6. Event Sourcing pattern

Instead of storing only the current state of the data in a relational database, store the full series of actions taken on an object in an append-only store. The store acts as the system of record that you can use to materialize the domain objects. This approach can improve auditability and write performance in complex systems.

Important

Event sourcing is a complex pattern that introduces significant trade-offs. It changes how you store data, handle concurrency, evolve schemas, and query state. It's costly to migrate to or from an event sourcing solution, and after you adopt the pattern, it constrains future design decisions in the parts of the system that use it. Adopt event sourcing when its benefits, like auditability and historical reconstruction, justify the pattern's complexity. For most systems and most parts of a system, traditional data management is sufficient.

## Context and problem

Most applications work with data. The application typically stores the latest state of the data in a relational database and inserts or updates data as needed. For example, in the traditional create, read, update, and delete (CRUD) model, an application reads data from the store, modifies it, and updates the current state of the data with the new values, typically by using transactions that lock the data.

The CRUD approach is straightforward and fast for most scenarios. However, in high-load systems, this approach presents challenges:

* **Write contention:** Because updates require read-modify-write cycles with row-level locking, concurrent writes to the same entity degrade performance and become a bottleneck under load.
* **Auditability:** CRUD systems only store the latest state of the data. If you don't implement an auditing mechanism that records the details of each operation in a separate log, you lose data history.

## Solution

The Event Sourcing pattern defines an approach to handling operations on data that a sequence of events drive. Each event is recorded in an append-only store. Application code raises events that describe each action taken on the object. It typically sends events to a queue in which a separate process, an event handler, listens to the queue and persists the events in an event store. Each event represents a logical change to the object, such as `AddedItemToOrder` or `OrderCanceled`.

The events persist in an event store that serves as the system of record, or the authoritative data source, about the current state of the data. Extra event handlers can listen for specific events and take action as needed. For example, consumers might initiate tasks that apply operations in the events to other systems or take other associated actions required to finish the operation. The application code that generates the events is decoupled from the systems that subscribe to the events.

Each entity in an event-sourced system has its own event stream, which is the ordered sequence of events that records every change to that entity. At any point, applications can read the history of events. Applications derive the current state of an entity by replaying all the events in its stream. This process is known as *rehydration*. It can occur on demand when the application handles a request.

Applications typically implement [materialized views](materialized-view) because it's costly to read and replay events. Materialized views are read-only projections of the event store that are optimized for querying. For example, a system can maintain a materialized view of all customer orders that it uses to populate the UI. When the application adds new orders, adds or removes items in the order, or adds shipping information, the application raises events and a handler updates the materialized view.

The following diagram shows an overview of this pattern combined with the [Command Query Responsibility Segregation (CQRS) pattern](cqrs). The presentation layer reads from a separate read-only store and writes commands to command handlers. The command handlers retrieve the entity's event stream from the event store, run business logic, and push new events to a queue. Event handlers consume events from the queue and write events to the event store, update the read-only store, or integrate with external systems.

[At the top of the diagram, a box represents the presentation layer. In the upper right, an arrow labeled reads points from the presentation layer to a box labeled business object, which points to a read-only store. An arrow labeled writes points from the presentation layer to a box on the left that includes command handlers and business objects. From this box, an arrow labeled get cart events points to an event store. Another arrow points from the command handlers box to a box at the bottom labeled queue or topic that contains seven envelope icons. Alongside this arrow, envelope icons represent events like cart created, item 1 added, item 2 added, item 1 removed, and shipping information added. Three arrows point from the queue or topic box to separate event handlers. The leftmost event handler writes events to the event store. The middle event handler updates the read-only store. The rightmost event handler integrates with external systems.](_images/event-sourcing-overview.svg#lightbox)

*Download a [Visio file](https://arch-center.azureedge.net/event-sourcing-overview.vsdx) of this architecture.*

### Workflow

The following workflow corresponds to the previous diagram:

1. The presentation layer calls an object that reads from a read-only store. It uses the returned data to populate the UI.
2. The presentation layer calls command handlers to perform actions like *create a cart* or *add an item to the cart*.
3. The command handler loads the entity by retrieving its event stream from the event store. For example, it might retrieve all cart events. It replays those events against the entity to reconstruct its current state before any new action occurs.
4. The business logic runs and events are raised. In most implementations, the events are pushed to a queue or topic to decouple the event producers and event consumers.
5. Event handlers listen for specific events and take the appropriate action for that handler. In this example, the event handlers take the following actions:

   1. Write the events to the event store
   2. Update a read-only store optimized for queries
   3. Integrate with external systems

### Pattern advantages

The Event Sourcing pattern provides the following advantages:

* Events are immutable, and you can store them by using an append-only operation. The UI, workflow, or process that initiates an event can continue, and tasks that handle the events can run in the background. Write throughput improves, especially for the presentation layer, because append-only writes avoid the row-level lock contention that update-in-place systems create.
* Events are simple objects that describe an action that occurs along with any associated data required to describe the action that the event represents. Events don't directly update a data store. Event handlers pick up and process recorded events when a handler is available and the system can handle the load. Use events to help simplify implementation and management.
* Events typically have meaning for a domain expert, whereas object-relational impedance mismatch can make complex database tables hard to understand. Tables are artificial constructs that represent the current state of the system, not the events that occur.
* Event sourcing can help prevent concurrent updates from causing conflicts because it avoids the requirement to directly update objects in the data store. Command handlers rehydrate an entity from its event stream to enforce business rules before they append new events, so two handlers that load the same entity simultaneously can act on the same state.

  For example, each handler sees five remaining seats, and both handlers can accept a reservation. Event stores address this scenario by using optimistic concurrency control and reject an append if the stream changed since it was read. Upon rejection, the handler reloads the entity, reevaluates, and retries.
* Append-only event storage provides an audit trail that applications can use to monitor actions taken against a data store. It can regenerate the current state as materialized views or projections by replaying the events at any time, and it can help test and debug the system.

  The requirement to use compensating events to cancel changes can provide a history of reversed changes. If the model stores only the current state, this history doesn't exist. You can also use the list of events to analyze application performance, detect user behavior trends, and obtain other useful business information.
* The command handlers raise events, and tasks perform operations in response to those events. This decoupling of the tasks from the events provides flexibility and extensibility. Tasks know about the type of event and the event data, but not about the operation that triggers the event.

  Multiple tasks can handle each event, so they can easily integrate with other services and systems that only listen for new events that the event store raises. But the event sourcing events are typically low level, and it might be necessary to generate specific integration events instead.

Tip

Event sourcing is commonly combined with the [CQRS pattern](cqrs) by performing the data management tasks in response to the events and by materializing views from the stored events. Use this combination to independently scale reads and writes because append-only event ingestion and query-optimized projections operate separately.

## Problems and considerations

Consider the following points as you decide how to implement this pattern:

* **Event design:** Design events to capture the business intent behind each change in addition to the resulting state. For example, in the seat-reservation system, an event that records *two seats were reserved* is more valuable than an event that records *remaining seats changed to 42*. The first event tells you what happened. The second event only tells you the resulting state. State-focused events reduce the event store to a change log that has no business meaning. Intent-focused events provide more detailed projections, meaningful audit trails, and the flexibility to build new read models from historical events without having to change the write environment.
* **Eventual consistency:** The system is only eventually consistent when it creates materialized views or generates projections of data by replaying events. A delay exists between when an application handles a request and adds events to the event store, when the events publish, and when consumers handle the events. During this period, new events that describe further changes to entities might arrive at the event store. Ensure that your customers understand that data is eventually consistent and that the system is designed to account for eventual consistency in these scenarios.
* **Versioning events:** The event store is the permanent source of information, so you should never update the event data. The only way to update an entity or undo a change is to add a compensating event to the event store. A compensating event is a new event that reverses or corrects the effect of a previous event. For example, a `ReservationCanceled` event compensates for a prior `SeatsReserved` event. The original event remains in the stream, and the compensating event records that it was undone.

  This immutability also means that if a bug produces incorrect events, those events persist in the store. Fixing the bug in application code doesn't fix the historical events, so you might also need compensating events or upcasters to handle the bad data during replay. If the schema (rather than the data) of the persisted events needs to change, perhaps during a migration, it can be difficult to combine existing events in the store with the new version.

  You can use the following strategies individually or in combination:

  + **Tolerant deserialization:** Design event consumers to ignore unknown fields and use default values for missing fields. This approach handles additive, nonbreaking changes, such as adding an optional field, without requiring any transformation of stored events.
  + **Event versioning:** Include a version identifier in each event, either as metadata in the event envelope or as part of the event type name. Consumers use the version to select the appropriate handling logic.
  + **Upcasting:** Register transformation functions that convert older event schemas to the current schema during deserialization. You can chain upcasters so that the application code only needs to handle the latest version. The stored events remain unchanged, which preserves immutability.
  + **In-place migration:** Rewrite historical events to the new schema directly in the event store. This approach breaks immutability and should be a last resort because it undermines the audit trail.
* **Event ordering:** Multiple-threaded applications and multiple instances of applications might store events in the event store. The consistency of events in the event store and the order of events that affect a specific entity's current state are crucial. Adding a timestamp to every event can help you avoid problems. Another common practice is to annotate each event that results from a request with an incremental identifier. If two actions attempt to add events for the same entity at the same time, the event store can reject an event that matches an existing entity identifier and event identifier.
* **Event querying:** There's no standard approach or existing mechanisms, such as SQL queries, for reading events to obtain information. The only data that you can extract is a stream of events by using an event identifier as the criteria. The event ID typically maps to individual entities. You can determine the current state of an entity only by replaying all of the events that relate to it against the original state of that entity.
* **Event store options:** An event store can be a purpose-built database designed for append-only event streams or a general-purpose relational or document database with an append-only table.

  + Purpose-built event stores provide built-in support for tasks like reading a stream by entity, optimistic concurrency, and snapshots.
  + Relational databases are familiar and widely available but require you to build those behaviors yourself.

  Because each entity has its own independent event stream, event stores partition naturally by entity ID, which simplifies horizontal scaling or sharding when needed.

  Important

  Don't confuse an event store with an event stream message broker. Message brokers such as Apache Kafka typically lack per-entity stream queries and optimistic concurrency. They work well as a distribution layer to fan out events to projections and external consumers, but they aren't a substitute for an event store.
* **Entity state re-creation:** The length of each event stream affects how you manage and update the system. If the streams are large, replaying every event to rehydrate an entity becomes costly in both time and compute. To mitigate this cost, create snapshots at specific intervals, such as every *N* events. A snapshot is a serialized representation of the entity's state at a specific point in its event stream. To rehydrate the entity, load the most recent snapshot and replay only the events that occur after it, rather than replaying the entire stream from the beginning. When you choose a snapshot frequency, balance the storage cost of snapshots against the time saved during rehydration.

  Note

  Snapshots are an optimization, not a replacement for the event stream. The event stream remains the source of truth, and you can regenerate snapshots from it at any time.
* **Conflict handling:** Optimistic concurrency control prevents conflicting writes to the same event stream, but the application must still handle conflicts that span multiple entities. For example, an event that indicates a reduction in stock inventory might arrive in the data store while a customer places an order for that item. Design the system to reconcile these situations, such as by advising the customer or by creating a back order.
* **Idempotency requirements:** Event delivery to consumers is typically *at least once*, so consumers can receive the same event more than once. Event handlers must be idempotent so processing a duplicate event doesn't change the outcome. For example, if multiple instances of a consumer process seat-reservation events to maintain an available-seat count, a duplicated reservation event must result in only one decrement. Without idempotency, projections drift from the event stream and side effects such as payments or notifications trigger more than once. Track the last processed event sequence number for each consumer and skip duplicates, or design state mutations that are inherently safe to repeat.
* **Circular logic:** Be mindful of scenarios in which the processing of one event requires the creation of one or more new events. This sequence can result in an infinite loop.
* **Testing:** A specific testing style best suits event-sourced systems. Set up past events, issue a command, and assert on the new events produced. This *given-when-then* approach tests business logic without databases, queues, or projections. But you also need integration tests for projections, idempotency behavior, and schema evolution paths, which adds testing surface compared to CRUD systems.
* **Personal data and regulatory compliance:** The append-only, immutable nature of an event store conflicts with data protection regulations that require deletion of personal data, such as the *right to be forgotten* laws. Deleting events outright breaks stream integrity, so design for this tension from the start.

  + A common approach is to store personal data outside the event store and reference it by identifier in events. This approach allows deletion to occur independently without affecting the event stream.
  + When you can't separate personal data from events, use crypto-shredding. Encrypt personal data in events by using a per-subject key. Delete the key to render the data unrecoverable while leaving the event structure intact. This approach adds encryption overhead on every read and write and requires robust key management.

## When to use this pattern

Use this pattern when:

* You want to capture intent, purpose, or reason in the data. For example, you can capture changes to a customer entity as a series of specific event types, such as *Moved home*, *Closed account*, or *Deceased*.
* You must minimize or completely avoid conflicting updates to data.
* You want to record events that occur, to replay them to restore the state of a system, to roll back changes, or to keep a history and audit log. For example, when a task consists of multiple steps, you might need to run actions to revert updates and then replay some steps to bring the data back into a consistent state.
* The application already uses events as a natural feature of its operation, and event sourcing requires little extra development or implementation effort.
* You need to decouple the process of inputting or updating data from the tasks required to apply these actions. This change might be to improve UI performance or to distribute events to other listeners that act when the events occur. For example, you can integrate a payroll system with an expense submission website. Both the website and the payroll system consume events that the event store raises in response to data updated on the website.
* You want the flexibility to change the format of materialized models and entity data if requirements change, or when you use CQRS and you need to adapt a read model or the views that expose the data.
* You use CQRS and eventual consistency is acceptable while a read model is updated, or entity and data rehydration from an event stream results in acceptable performance reduction.

This pattern might not be suitable when:

* Systems have straightforward CRUD operations that don't require auditability, replay, or historical reconstruction of state. The operational overhead of an event store isn't justified if the only requirement is current-state reads and writes.
* Prototypes, minimum viable products (MVPs), or systems have short expected lifespans. The upfront investment in event design, schema evolution strategy, and projection infrastructure rarely yield a return in these scenarios.
* Systems require consistency and real-time updates to the views of the data. Eventual consistency between the event store and projections is inherent to event sourcing.
* Domains in which data is mostly static or for reference, such as lookup tables or catalogs. This type of data changes infrequently and doesn't benefit from change history.
* Teams don't have experience in [event-driven architectures](../guide/architecture-styles/event-driven). Event sourcing changes how you test, debug, and operate a system. Adopting it without the foundational knowledge increases the risk of antipatterns that are costly to reverse.

Tip

Event sourcing doesn't have to be an all-or-nothing decision for your entire system. Apply it selectively to the parts of your system that it benefits the most, such as a payment ledger or order-processing pipeline. Use traditional CRUD for parts when the complexity isn't justified, such as user profile management or application configuration.

## Workload design

Evaluate how to use the Event Sourcing pattern in a workload's design to address the goals and principles covered in the [Azure Well-Architected Framework pillars](/en-us/azure/well-architected/pillars). The following table provides guidance about how this pattern supports the goals of each pillar.

| Pillar | How this pattern supports pillar goals |
| --- | --- |
| [Reliability](/en-us/azure/well-architected/reliability/checklist) design decisions help your workload become **resilient** to malfunction and ensure that it **recovers** to a fully functioning state after a failure occurs. | This pattern can facilitate state reconstruction if you need to recover state stores because you capture a history of changes in complex business processes.   - [Data partitioning](/en-us/azure/well-architected/design-guides/partition-data)  - [RE:09 Disaster recovery](/en-us/azure/well-architected/reliability/disaster-recovery) |
| [Performance Efficiency](/en-us/azure/well-architected/performance-efficiency/checklist) helps your workload **efficiently meet demands** through optimizations in scaling, data, and code. | This pattern, usually combined with CQRS, an appropriate domain design, and strategic snapshotting, can improve workload performance because of atomic append-only operations and the avoidance of database locking for writes and reads.   - [PE:08 Data performance](/en-us/azure/well-architected/performance-efficiency/optimize-data-performance) |

If this pattern introduces trade-offs within a pillar, consider them against the goals of the other pillars.

## Example

A conference management system needs to track the number of completed bookings for a conference. By tracking this number, it can check for available seats when a potential attendee tries to make a booking. The system can store the total number of bookings for a conference in at least two ways:

* The system can store information about the total number of bookings as a separate entity in a database that holds booking information. As attendees make or cancel bookings, the system increases or decreases this number. This approach is simple in theory, but it can cause scalability problems if a large number of attendees attempt to book seats during a short period of time. For example, this surge typically occurs on the final day before the booking period closes.
* The system can store information about bookings and cancellations as events held in an event store. It calculates the number of available seats by replaying these events. This approach can be more scalable because of the immutability of events. The system needs to only read data from the event store or append data to the event store. It never modifies event information about bookings and cancellations.

The following diagram shows how you might use event sourcing to implement the seat reservation subsystem of the conference management system.

[At the top of the diagram, a box represents the presentation layer. An arrow labeled writes points from the presentation layer to a box that includes command handlers and business objects. An arrow labeled get seat availability events points from that box to an event store. An arrow labeled seat reserved (number of seats) points from the command handlers box to a box labeled queue or topic. An arrow points from the queue or topic box to an event handler. Another arrow points from the event handler to the event store.](_images/event-sourcing-example.svg#lightbox)

*Download a [Visio file](https://arch-center.azureedge.net/event-sourcing-example.vsdx) of this architecture.*

### Workflow

The following workflow corresponds to the previous diagram:

1. The UI issues a command to reserve seats for two attendees. A separate command handler handles the command. The command handler is a piece of logic that's decoupled from the UI and is responsible for handling requests posted as commands.
2. The system constructs an entity that contains information about all reservations for the conference by replaying the events that describe bookings and cancellations. This entity is called `SeatAvailability`, and it's contained within a domain model that exposes methods for querying and modifying the data in the entity.

   Tip

   Consider optimizations like snapshots so that you don't need to replay the full list of events to obtain the current state of the entity. Snapshots also maintain a cached copy of the entity in memory.
3. The command handler invokes a method that the domain model exposes to make the reservations.
4. The `SeatAvailability` entity raises an event that contains the number of reserved seats. The next time that the entity applies events, it uses all the reservations to compute the number of remaining seats.
5. The system appends the new event to the list of events in the event store.

If a user cancels a seat, the system follows a similar process, but the command handler issues a command that generates a seat cancellation event and appends it to the event store.

The system can provide a complete history, or audit trail, of the bookings and cancellations for a conference by using an event store. The events in the event store are the accurate record. You don't need to persist entities in any other way because the system can easily replay the events and restore the state to any point in time.

## Next step

* [CQRS pattern](cqrs): The write store that provides the permanent source of information for a CQRS implementation is typically based on an implementation of the Event Sourcing pattern. The pattern segregates the operations that read data in an application from the operations that update data by using separate interfaces.

## Community resources

* [Object-relational impedance mismatch](https://wikipedia.org/wiki/Object%E2%80%93relational_impedance_mismatch).
* [Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html), by Martin Fowler: The original 2005 description of the pattern that established the foundational vocabulary.
* [CQRS Documents (PDF)](https://cqrs.files.wordpress.com/2010/11/cqrs_documents.pdf), by Greg Young: The definitive resource about event sourcing and CQRS from the practitioner who formalized both patterns.

## Related resources

The following patterns and guidance might also be relevant when you implement this pattern:

* [Materialized View pattern](materialized-view): The data store that you use in an event sourcing system typically isn't suited for efficient querying. Instead, a common approach is to generate prepopulated views of the data at regular intervals or when the data changes.
* [Compensating Transaction pattern](compensating-transaction): The system doesn't update existing data in an event sourcing store. Instead, it adds new entries that transition the state of entities to the new values. To reverse a change, it uses compensating entries because it can't reverse the previous change. The Compensating Transaction pattern article describes how to undo the work that a previous operation performed.
* [Domain analysis for microservices](../microservices/model/tactical-domain-driven-design): In systems that use domain-driven design (DDD), the entity that owns an event stream is typically an [aggregate](../microservices/model/tactical-domain-driven-design#aggregates), a consistency boundary that receives commands, enforces business rules, and emits events.

---

## 7. CQRS pattern

Command Query Responsibility Segregation (CQRS) is a design pattern that segregates read and write operations for a data store into separate data models. This approach allows each model to be optimized independently and can improve the performance, scalability, and security of an application.

## Context and problem

In a traditional architecture, a single data model is often used for both read and write operations. This approach is straightforward and is suited for basic create, read, update, and delete (CRUD) operations.

As applications grow, it can become increasingly difficult to optimize read and write operations on a single data model. Read and write operations often have different performance and scaling requirements. A traditional CRUD architecture doesn't take this asymmetry into account, which can result in the following challenges:

* **Data mismatch:** The read and write representations of data often differ. Some fields that are required during updates might be unnecessary during read operations.
* **Lock contention:** Parallel operations on the same data set can cause lock contention.
* **Performance problems:** The traditional approach can have a negative effect on performance because of load on the data store and data access layer, and the complexity of queries required to retrieve information.
* **Security challenges:** It can be difficult to manage security when entities are subject to read and write operations. This overlap can expose data in unintended contexts.

Combining these responsibilities can result in an overly complicated model.

## Solution

Use the CQRS pattern to separate write operations, or *commands*, from read operations, or *queries*. Commands update data. Queries retrieve data. The CQRS pattern is useful in scenarios that require a clear separation between commands and reads.

* **Understand commands.** Commands should represent specific business tasks instead of low-level data updates. For example, in a hotel-booking app, use the command "Book hotel room" instead of "Set ReservationStatus to Reserved." This approach better captures the intent of the user and aligns commands with business processes. To help ensure that commands are successful, you might need to refine the user interaction flow and server-side logic and consider asynchronous processing.

  | Area of refinement | Recommendation |
  | --- | --- |
  | Client-side validation | Validate specific conditions before you send the command to prevent obvious failures. For example, if no rooms are available, disable the "Book" button and provide a clear, user-friendly message in the UI that explains why booking isn’t possible. This setup reduces unnecessary server requests and provides immediate feedback to users, which enhances their experience. |
  | Server-side logic | Enhance the business logic to handle edge cases and failures gracefully. For example, to address race conditions such as multiple users attempting to book the last available room, consider adding users to a waiting list or suggesting alternatives. |
  | Asynchronous processing | [Process commands asynchronously](/en-us/dotnet/architecture/microservices/architect-microservice-container-applications/asynchronous-message-based-communication) by placing them in a queue, instead of handling them synchronously. |
* **Understand queries.** Queries never alter data. Instead, they return data transfer objects (DTOs) that present the required data in a convenient format, without any domain logic. This distinct separation of responsibilities simplifies the design and implementation of the system.

### Separate read models and write models

Separating the read model from the write model simplifies system design and implementation by addressing specific concerns for data writes and data reads. This separation improves clarity, scalability, and performance but introduces trade-offs. For example, scaffolding tools like object-relational mapping (O/RM) frameworks can't automatically generate CQRS code from a database schema, so you need custom logic to bridge the gap.

The following sections describe two primary approaches to implement read model and write model separation in CQRS. Each approach has unique benefits and challenges, such as synchronization and consistency management.

#### Separate models in a single data store

This approach represents the foundational level of CQRS, where both the read and write models share a single underlying database but maintain distinct logic for their operations. A basic CQRS architecture allows you to delineate the write model from the read model while relying on a shared data store.

This approach improves clarity, performance, and scalability by defining distinct models for handling read and write concerns.

* **A write model** is designed to handle commands that update or persist data. It includes validation and domain logic, and helps ensure data consistency by optimizing for transactional integrity and business processes.
* **A read model** is designed to serve queries for retrieving data. It focuses on generating DTOs or projections that are optimized for the presentation layer. It enhances query performance and responsiveness by avoiding domain logic.

#### Separate models in different data stores

A more advanced CQRS implementation uses distinct data stores for the read and write models. Separation of the read and write data stores allows you to scale each model to match the load. It also enables you to use a different storage technology for each data store. You can use a document database for the read data store and a relational database for the write data store.

When you use separate data stores, you must ensure that both remain synchronized. A common pattern is to have the write model publish events when it updates the database, which the read model uses to refresh its data. For more information about how to use events, see [Event-driven architecture style](../guide/architecture-styles/event-driven). Because you usually can't enlist message brokers and databases into a single distributed transaction, challenges in consistency can occur when you update the database and publishing events. For more information, see [Idempotent message processing](/en-us/azure/architecture/reference-architectures/containers/aks-mission-critical/mission-critical-data-platform#idempotent-message-processing).

The read data store can use its own data schema that's optimized for queries. For example, it can store a [materialized view](materialized-view) of the data to avoid complex joins or O/RM mappings. The read data store can be a read-only replica of the write store or have a different structure. Deploying multiple read-only replicas can improve performance by reducing latency and increasing availability, especially in distributed scenarios.

### Benefits of CQRS

* **Independent scaling.** CQRS enables the read models and write models to scale independently. This approach can help minimize lock contention and improve system performance under load.
* **Optimized data schemas.** Read operations can use a schema that's optimized for queries. Write operations use a schema that's optimized for updates.
* **Security.** By separating reads and writes, you can ensure that only the appropriate domain entities or operations have permission to perform write actions on the data.
* **Separation of concerns.** Separating the read and write responsibilities results in cleaner, more maintainable models. The write side typically handles complex business logic. The read side can remain simple and focused on query efficiency.
* **Simpler queries.** When you store a materialized view in the read database, the application can avoid complex joins when it queries.

## Problems and considerations

Consider the following points as you decide how to implement this pattern:

* **Increased complexity.** The core concept of CQRS is straightforward, but it can introduce significant complexity into the application design, specifically when combined with the [Event Sourcing pattern](event-sourcing).
* **Messaging challenges.** Messaging isn't a requirement for CQRS, but you often use it to process commands and publish update events. When messaging is included, the system must account for potential problems such as message failures, duplicates, and retries. For more information about strategies to handle commands that have varying priorities, see [Priority queues](priority-queue).
* **Eventual consistency.** When the read databases and write databases are separated, the read data might not show the most recent changes immediately. This delay results in stale data. Ensuring that the read model store stays up-to-date with changes in the write model store can be challenging. Also, detecting and handling scenarios where a user acts on stale data requires careful consideration.

## When to use this pattern

Use this pattern when:

* **You work in collaborative environments.** In environments where multiple users access and modify the same data simultaneously, CQRS helps reduce merge conflicts. Commands can include enough granularity to prevent conflicts, and the system can resolve any conflicts that occur within the command logic.
* **You have task-based user interfaces.** Applications that guide users through complex processes as a series of steps or with complex domain models benefit from CQRS.

  + The write model has a full command-processing stack with business logic, input validation, and business validation. The write model might treat a set of associated objects as a single unit for data changes, which is known as an *aggregate* in domain-driven design terminology. The write model might also help ensure that these objects are always in a consistent state.
  + The read model has no business logic or validation stack. It returns a DTO for use in a view model. The read model is eventually consistent with the write model.
* **You need performance tuning.** Systems where the performance of data reads must be fine-tuned separately from performance of data writes benefit from CQRS. This pattern is especially beneficial when the number of reads is greater than the number of writes. The read model scales horizontally to handle large query volumes. The write model runs on fewer instances to minimize merge conflicts and maintain consistency.
* **You have separation of development concerns.** CQRS allows teams to work independently. One team implements the complex business logic in the write model, and another team develops the read model and user interface components.
* **You have evolving systems.** CQRS supports systems that evolve over time. It accommodates new model versions, frequent changes to business rules, or other modifications without affecting existing functionality.
* **You need system integration:** Systems that integrate with other subsystems, especially systems that use the Event Sourcing pattern, remain available even if a subsystem temporarily fails. CQRS isolates failures, which prevents a single component from affecting the entire system.

This pattern might not be suitable when:

* The domain or the business rules are simple.
* A simple CRUD-style user interface and data access operations are sufficient.

## Workload design

Evaluate how to use the CQRS pattern in a workload's design to address the goals and principles covered in the [Azure Well-Architected Framework pillars](/en-us/azure/well-architected/pillars). The following table provides guidance about how this pattern supports the goals of the Performance Efficiency pillar.

| Pillar | How this pattern supports pillar goals |
| --- | --- |
| [Performance Efficiency](/en-us/azure/well-architected/performance-efficiency/checklist) helps your workload efficiently meet demands through optimizations in scaling, data, and code. | The separation of read operations and write operations in high read-to-write workloads enables targeted performance and scaling optimizations for each operation's specific purpose.   - [PE:05 Scaling and partitioning](/en-us/azure/well-architected/performance-efficiency/scale-partition)  - [PE:08 Data performance](/en-us/azure/well-architected/performance-efficiency/optimize-data-performance) |

Consider any trade-offs against the goals of the other pillars that this pattern might introduce.

## Combine the Event Sourcing and CQRS patterns

Some implementations of CQRS incorporate the [Event Sourcing pattern](event-sourcing). This pattern stores the system's state as a chronological series of events. Each event captures the changes made to the data at a specific time. To determine the current state, the system replays these events in order. In this setup:

* The event store is the *write model* and the single source of truth.
* The *read model* generates materialized views from these events, typically in a highly denormalized form. These views optimize data retrieval by tailoring structures to query and display requirements.

### Benefits of combining the Event Sourcing and CQRS patterns

The same events that update the write model can serve as inputs to the read model. The read model can then build a real-time snapshot of the current state. These snapshots optimize queries by providing efficient and precomputed views of the data.

Instead of directly storing the current state, the system uses a stream of events as the write store. This approach reduces update conflicts on aggregates and enhances performance and scalability. The system can process these events asynchronously to build or update materialized views for the read data store.

Because the event store acts as the single source of truth, you can easily regenerate materialized views or adapt to changes in the read model by replaying historical events. Basically, materialized views function as a durable, read-only cache that's optimized for fast and efficient queries.

### Considerations for how to combine the Event Sourcing and CQRS patterns

Before you combine the CQRS pattern with the [Event Sourcing pattern](event-sourcing), evaluate the following considerations:

* **Eventual consistency:** Because the write and read data stores are separate, updates to the read data store might lag behind event generation. This delay results in eventual consistency.
* **Increased complexity:** Combining the CQRS pattern with the Event Sourcing pattern requires a different design approach, which can make a successful implementation more challenging. You must write code to generate, process, and handle events, and assemble or update views for the read model. However, the Event Sourcing pattern simplifies domain modeling and allows you to rebuild or create new views easily by preserving the history and intent of all data changes.
* **Performance of view generation:** Generating materialized views for the read model can consume significant time and resources. The same applies to projecting data by replaying and processing events for specific entities or collections. Complexity increases when calculations involve analyzing or summing values over long periods because all related events must be examined. Implement snapshots of the data at regular intervals. For example, store the current state of an entity or periodic snapshots of aggregated totals, which is the number of times a specific action occurs. Snapshots reduce the need to process the full event history repeatedly, which improves performance.

## Example

The following code shows extracts from an example of a CQRS implementation that uses different definitions for the read models and the write models. The model interfaces don't dictate features of the underlying data stores, and they can evolve and be fine-tuned independently because these interfaces are separate.

The following code shows the read model definition.

```
// Query interface
namespace ReadModel
{
  public interface ProductsDao
  {
    ProductDisplay FindById(int productId);
    ICollection<ProductDisplay> FindByName(string name);
    ICollection<ProductInventory> FindOutOfStockProducts();
    ICollection<ProductDisplay> FindRelatedProducts(int productId);
  }

  public class ProductDisplay
  {
    public int Id { get; set; }
    public string Name { get; set; }
    public string Description { get; set; }
    public decimal UnitPrice { get; set; }
    public bool IsOutOfStock { get; set; }
    public double UserRating { get; set; }
  }

  public class ProductInventory
  {
    public int Id { get; set; }
    public string Name { get; set; }
    public int CurrentStock { get; set; }
  }
}
```

The system allows users to rate products. The application code does this by using the `RateProduct` command shown in the following code.

```
public interface ICommand
{
  Guid Id { get; }
}

public class RateProduct : ICommand
{
  public RateProduct()
  {
    this.Id = Guid.NewGuid();
  }
  public Guid Id { get; set; }
  public int ProductId { get; set; }
  public int Rating { get; set; }
  public int UserId {get; set; }
}
```

The system uses the `ProductsCommandHandler` class to handle commands that the application sends. Clients typically send commands to the domain through a messaging system such as a queue. The command handler accepts these commands and invokes methods of the domain interface. The granularity of each command is designed to reduce the chance of conflicting requests. The following code shows an outline of the `ProductsCommandHandler` class.

```
public class ProductsCommandHandler :
    ICommandHandler<AddNewProduct>,
    ICommandHandler<RateProduct>,
    ICommandHandler<AddToInventory>,
    ICommandHandler<ConfirmItemShipped>,
    ICommandHandler<UpdateStockFromInventoryRecount>
{
  private readonly IRepository<Product> repository;

  public ProductsCommandHandler (IRepository<Product> repository)
  {
    this.repository = repository;
  }

  void Handle (AddNewProduct command)
  {
    ...
  }

  void Handle (RateProduct command)
  {
    
    if (product != null)
    {
      product.RateProduct(command.UserId, command.Rating);
      repository.Save(product);
    }
  }

  void Handle (AddToInventory command)
  {
    ...
  }

  void Handle (ConfirmItemsShipped command)
  {
    ...
  }

  void Handle (UpdateStockFromInventoryRecount command)
  {
    ...
  }
}
```

## Next step

The following information might be relevant when you implement this pattern:

* [Data partitioning guidance](../best-practices/data-partitioning) describes best practices for how to divide data into partitions that you can manage and access separately to improve scalability, reduce contention, and optimize performance.

## Related resources

* [Event Sourcing pattern](event-sourcing). This pattern describes how to simplify tasks in complex domains and improve performance, scalability, and responsiveness. It also explains how to provide consistency for transactional data while maintaining full audit trails and history that can enable compensating actions.
* [Materialized View pattern](materialized-view). This pattern creates prepopulated views, known as *materialized views*, for efficient querying and data extraction from one or more data stores. The read model of a CQRS implementation can contain materialized views of the write model data, or the read model can be used to generate materialized views.

---

## 8. Strangler Fig pattern

This pattern incrementally migrates a legacy system by gradually replacing specific pieces of functionality with new applications and services. As you replace features from the legacy system, the new system eventually comprises all of the old system's features. This approach suppresses the old system so that you can decommission it.

## Context and problem

As systems age, the development tools, hosting technology, and system architectures that they're built on can become obsolete. As new features and functionality are added, these applications become more complex, which can make them harder to maintain or extend.

Replacing an entire complex system is a huge undertaking. Instead, many teams prefer to migrate to a new system gradually and keep the old system to handle unmigrated features. However, running two separate versions of an application forces clients to track which version has individual features. Every time teams migrate a feature or service, they must direct clients to the new location. To overcome these challenges, you can adopt an approach that supports incremental migration and minimizes disruptions to clients.

## Solution

Use an incremental process to replace specific pieces of functionality with new applications and services. Customers can continue using the same interface, unaware that this migration is taking place.

The Strangler Fig pattern provides a controlled and phased approach to modernization. It allows the existing application to continue functioning during the modernization effort. A façade (proxy) intercepts requests that go to the back-end legacy system. The façade routes these requests either to the legacy application or to the new services.

This pattern reduces risks in migration by enabling your teams to move forward at a pace that suits the complexity of the project. As you migrate functionality to the new system, the legacy system becomes obsolete, and you decommission the legacy system.

1. The Strangler Fig pattern begins by introducing a façade (proxy) between the client app, the legacy system, and the new system. The façade acts as an intermediary. It allows the client app to interact with the legacy system and the new system. Initially, the façade routes most requests to the legacy system.
2. As the migration progresses, the façade incrementally shifts requests from the legacy system to the new system. With each iteration, you implement more pieces of functionality in the new system.

   This incremental approach gradually reduces the legacy system's responsibilities and expands the scope of the new system. The process is iterative. It allows the team to address complexities and dependencies in manageable stages. These stages help the system remain stable and functional.
3. After you migrate all of the functionality and there are no dependencies on the legacy system, you can decommission the legacy system. The façade routes all requests exclusively to the new system.
4. You remove the façade and reconfigure the client app to communicate directly with the new system. This step marks the completion of the migration.

## Problems and considerations

Consider the following points as you decide how to implement this pattern:

* Consider how to handle services and data stores that both the new system and the legacy system might use. Make sure that both systems can access these resources at the same time.
* Structure new applications and services so that you can easily intercept and replace them in future strangler fig migrations. For example, strive to have clear demarcations between parts of your solution so that you can migrate each part individually.
* After the migration is complete, you typically remove the strangler fig façade. Alternatively, you can maintain the façade as an adaptor for legacy clients to use while you update the core system for newer clients.
* Make sure that the façade keeps up with the migration.
* Make sure that the façade doesn't become a single point of failure or a performance bottleneck.

## When to use this pattern

Use this pattern when:

* You gradually migrate a back-end application to a new architecture, especially when replacing large systems, key components, or complex features introduces risk.
* The original system can continue to exist for an extended period of time during the migration effort.

This pattern might not be suitable when:

* Requests to the back-end system can't be intercepted.
* You migrate a small system and replacing the whole system is simple.
* You need to fully decommission the original solution quickly.

## Workload design

Evaluate how to use the Strangler Fig pattern in a workload's design to address the goals and principles of the [Azure Well-Architected Framework pillars](/en-us/azure/well-architected/pillars). The following table provides guidance about how this pattern supports the goals of each pillar.

| Pillar | How this pattern supports pillar goals |
| --- | --- |
| [Reliability](/en-us/azure/well-architected/reliability/checklist) design decisions help your workload become **resilient** to malfunction and to ensure that it **recovers** to a fully functioning state after a failure occurs. | This pattern's incremental approach can help mitigate risks during a component transition compared to making large systemic changes all at once.   - [RE:08 Testing](/en-us/azure/well-architected/reliability/testing-strategy) |
| [Cost Optimization](/en-us/azure/well-architected/cost-optimization/checklist) focuses on **sustaining and improving** your workload's **return on investment (ROI)**. | The goal of this approach is to maximize the use of existing investments in the currently running system while modernizing incrementally. It enables you to perform high-ROI replacements before low-ROI replacements.   - [CO:07 Component costs](/en-us/azure/well-architected/cost-optimization/optimize-component-costs)  - [CO:08 Environment costs](/en-us/azure/well-architected/cost-optimization/optimize-environment-costs) |
| [Operational Excellence](/en-us/azure/well-architected/operational-excellence/checklist) helps deliver **workload quality** through **standardized processes** and team cohesion. | This pattern provides a continuous improvement approach. Incremental replacements that make small changes over time are preferable to large systemic changes that are riskier to implement.   - [OE:06 Supply chain for workload development](/en-us/azure/well-architected/operational-excellence/workload-supply-chain)  - [OE:11 Safe deployment practices](/en-us/azure/well-architected/operational-excellence/safe-deployments) |

Consider any trade-offs against the goals of the other pillars that this pattern might introduce.

## Example

Legacy systems typically depend on a centralized database. Over time, a centralized database can become difficult to manage and evolve because of its many dependencies. To address these challenges, various database patterns can facilitate the transition away from such legacy systems. The Strangler Fig pattern is one of these patterns. Apply the Strangler Fig pattern as a phased approach to gradually transition from a legacy system to a new system and minimize disruption.

1. You introduce a new system, and the new system starts handling some requests from the client app. However, the new system still depends on the legacy database for all read and write operations. The legacy system remains operational, which facilitates a smooth transition without immediate structural changes.
2. In the next phase, you introduce a new database. You migrate data load history to the new database by using an extract, transform, and load (ETL) process. The ETL process synchronizes the new database with the legacy database. During this phase, the new system performs shadow writes. The new system updates both databases in parallel. The new system continues to read from the legacy database to validate consistency.
3. Finally, the new database becomes the system of record. The new database takes over all read and write operations. You can start deprecating the legacy database and legacy system. After you validate the new database, you can retire the legacy database. This retirement completes the migration process with minimal disruption.

## Next step

Read Martin Fowler's blog post about [Strangler Fig pattern application](https://martinfowler.com/bliki/StranglerFigApplication.html).

## Related resource

[Messaging Bridge pattern](messaging-bridge)

---

## 9. Bulkhead pattern

The Bulkhead pattern is a type of application design that's tolerant of failure. In a bulkhead architecture, also known as a *cell-based architecture*, elements of an application are isolated into pools so that if one fails, the other elements continue to function. The Bulkhead pattern is named after the sectioned partitions (bulkheads) of a ship's hull. If the hull of a ship is compromised, only the damaged section fills with water, which prevents the ship from sinking.

## Context and problem

A cloud-based application might include multiple services, and each service has one or more consumers. Excessive load or failure in a service affects all consumers of the service.

Also, a consumer might send requests to multiple services simultaneously and use resources for each request. When the consumer sends a request to a misconfigured or unresponsive service, the resources that the client's request uses might remain unavailable for an extended period. As requests to the service continue, those resources might be exhausted. For example, the client's connection pool might be exhausted. At that point, the consumer's requests to other services are affected. Eventually, the consumer can't send requests to any other services, not only the original unresponsive service.

Resource exhaustion affects services that have multiple consumers. Many requests from one client might exhaust available resources in the service. Resource exhaustion can mean that other consumers can't consume the service, which causes a cascading failure effect.

## Solution

Partition service instances into different groups based on consumer load and availability requirements. This design helps isolate failures. You can sustain service functionality for some consumers, even during a failure.

A consumer can also partition resources to ensure that resources used to call one service don't affect the resources used to call another service. For example, a consumer that calls multiple services might be assigned a connection pool for each service. If a service begins to fail, it only affects the connection pool assigned for that service. The consumer can continue to use other services.

This pattern provides the following benefits:

* Isolates consumers and services from cascading failures. A problem that affects a consumer or service can be isolated within its own bulkhead to prevent the entire solution from failing.
* Preserves some functionality if a service failure occurs. Other services and features of the application continue to work.
* Provides different quality of service levels for consuming applications. You can configure a high-priority consumer pool to use high-priority services.

The following diagram shows bulkheads structured around connection pools that call individual services. If Service A fails or causes a problem, the connection pool is isolated, so only workloads that use the thread pool assigned to Service A are affected. Workloads that use Service B and C aren't affected and can continue working without interruption.

Diagram that shows two workloads, Workload 1 and Workload 2, and three services, Service A, Service B, and Service C. Workload 1 uses a connection pool that's assigned to Service A. Workload 2 uses two connection pools. One connection pool is assigned to Service B, and the other is assigned to Service C. The connection pool that Workload 1 uses is isolated. The connection pools that Workload 2 uses can continue to call Service B and Service C.

The following diagram shows multiple clients that call a single service. Each client is assigned to a separate service instance. Client 1 makes too many requests and overwhelms its instance. Because each service instance is isolated from the others, the other clients can continue to make calls.

Diagram that shows three clients, Client 1, Client 2, and Client 3, and three service instances that each form a part of Service A. Each client connects to its own service instance. The service instances are isolated. If Client 1 overwhelms its instance, Clients 2 and 3 are unaffected.

## Problems and considerations

Consider the following points as you decide how to implement this pattern:

* Define partitions around the business and technical requirements of the application.
* If you use [tactical domain-driven design to design microservices](../microservices/model/tactical-domain-driven-design), partition boundaries should align with the bounded contexts.
* When you partition services or consumers into bulkheads, consider the level of isolation offered by the technology and the overhead in terms of cost, performance, and manageability.
* To provide more sophisticated fault handling, consider combining bulkheads with retry, circuit breaker, and throttling patterns.
* When you partition consumers into bulkheads, consider using processes, thread pools, and semaphores. Projects like [resilience4j](https://resilience4j.readme.io/docs/getting-started) and [Polly](https://www.pollydocs.org/) offer a framework for creating consumer bulkheads.
* When you partition services into bulkheads, consider deploying them into separate virtual machines, containers, or processes. Containers offer a good balance of resource isolation with fairly low overhead.
* Services that communicate by using asynchronous messages can be isolated through different sets of queues. Each queue can have a dedicated set of instances that process messages on the queue or a single group of instances that use an algorithm to dequeue and dispatch processing.
* Determine the level of granularity for the bulkheads. For example, if you want to distribute tenants across partitions, you can place each tenant into a separate partition or put several tenants into one partition.
* Monitor each partition's performance and service-level agreement (SLA).
* Use built-in platform controls, such as Azure API Management rate limits, Azure Cosmos DB request unit (RU) isolation, and resource limits in Azure Kubernetes Service (AKS) or Azure Container Apps. Don't re-create these throttling and isolation mechanisms in your application code.
* AI and inference workloads often require strict bulkheads because of deployment-level quotas and concurrency limits, for example, isolating Azure OpenAI deployments per workload or per tenant.

## When to use this pattern

Use this pattern when:

* You want to isolate resources for specific dependencies so that a disruption in one service doesn't affect the entire application.
* You want to isolate critical consumers from standard consumers.
* You need to protect the application from cascading failures.

This pattern might not be suitable when:

* Less efficient use of resources might not be acceptable in the project.
* The added complexity isn't necessary.

## Workload design

Evaluate how to use the Bulkhead pattern in a workload's design to address the goals and principles covered in the [Azure Well-Architected Framework pillars](/en-us/azure/well-architected/pillars). The following table provides guidance about how this pattern supports the goals of each pillar.

| Pillar | How this pattern supports pillar goals |
| --- | --- |
| [Reliability](/en-us/azure/well-architected/reliability/checklist) design decisions help your workload become **resilient** to malfunction and ensure that it **recovers** to a fully functioning state after a failure occurs. | The failure isolation strategy introduced through the intentional and complete segmentation between components attempts to contain faults to the bulkhead that experiences the problem, which prevents impact on other bulkheads.   - [RE:02 Critical flows](/en-us/azure/well-architected/reliability/identify-flows)  - [RE:07 Self-preservation](/en-us/azure/well-architected/reliability/self-preservation) |
| [Security](/en-us/azure/well-architected/security/checklist) design decisions help ensure the **confidentiality**, **integrity**, and **availability** of your workload's data and systems. | The segmentation between components helps constrain security incidents to the compromised bulkhead.   - [SE:04 Segmentation](/en-us/azure/well-architected/security/segmentation) |
| [Performance Efficiency](/en-us/azure/well-architected/performance-efficiency/checklist) helps your workload **efficiently meet demands** through optimizations in scaling, data, and code. | Each bulkhead can be individually scalable to efficiently meet the needs of the task that's encapsulated in the bulkhead.   - [PE:02 Capacity planning](/en-us/azure/well-architected/performance-efficiency/capacity-planning)  - [PE:05 Scaling and partitioning](/en-us/azure/well-architected/performance-efficiency/scale-partition) |

If this pattern introduces trade-offs within a pillar, consider them against the goals of the other pillars.

## Example

The following Kubernetes configuration file creates an isolated container to run a single service, with its own CPU and memory resources and limits.

```
apiVersion: v1
kind: Pod
metadata:
  name: drone-management
spec:
  containers:
  - name: drone-management-container
    image: drone-service
    resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "1"
```

## Next steps

* Use [API Management rate-limit policies](/en-us/azure/api-management/api-management-policies#rate-limiting-and-quotas) to control request throughput per client.
* Use [Azure Functions concurrency controls](/en-us/azure/azure-functions/functions-concurrency) to limit parallel executions.
* Set [Container Apps resource limits](/en-us/azure/container-apps/containers) to control CPU and memory per workload.
* Assign [Azure Cosmos DB RU throughput](/en-us/azure/cosmos-db/set-throughput) per container for predictable isolation.

## Related resources

* [Circuit Breaker pattern](circuit-breaker)
* [Retry pattern](retry)
* [Throttling pattern](throttling)

---

## Bibliography

1. [Retry pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/retry)
2. [Throttling pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/throttling)
3. [Sidecar pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/sidecar)
4. [Saga distributed transactions pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/saga)
5. [Circuit Breaker pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker)
6. [Event Sourcing pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing)
7. [CQRS pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs)
8. [Strangler Fig pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/strangler-fig)
9. [Bulkhead pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/bulkhead)