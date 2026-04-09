Use Service Connect to connect Amazon ECS services with short names - Amazon Elastic Container Service 

Use Service Connect to connect Amazon ECS services with short names - Amazon Elastic Container Service
{
"@context" : "https://schema.org",
"@type" : "BreadcrumbList",
"itemListElement" : [
{
"@type" : "ListItem",
"position" : 1,
"name" : "AWS",
"item" : "https://aws.amazon.com"
},
{
"@type" : "ListItem",
"position" : 2,
"name" : "Amazon ECS",
"item" : "https://docs.aws.amazon.com/ecs/index.html"
},
{
"@type" : "ListItem",
"position" : 3,
"name" : "Developer Guide",
"item" : "https://docs.aws.amazon.com/AmazonECS/latest/developerguide"
},
{
"@type" : "ListItem",
"position" : 4,
"name" : "Schedule your containers on Amazon ECS",
"item" : "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/scheduling\_tasks.html"
},
{
"@type" : "ListItem",
"position" : 5,
"name" : "Amazon ECS services",
"item" : "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs\_services.html"
},
{
"@type" : "ListItem",
"position" : 6,
"name" : "Interconnect Amazon ECS services",
"item" : "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/interconnecting-services.html"
},
{
"@type" : "ListItem",
"position" : 7,
"name" : "Use Service Connect to connect Amazon ECS services with short names",
"item" : "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/interconnecting-services.html"
}
]
}

[Documentation](/index.html)[Amazon ECS](/ecs/index.html)[Developer Guide](Welcome.html)

[Pricing](#service-connect-pricing)

# Use Service Connect to connect Amazon ECS services with short names

Amazon ECS Service Connect provides management of service-to-service communication as Amazon ECS
configuration. It builds both service discovery and a service mesh in Amazon ECS. This provides
the complete configuration inside each service that you manage by service deployments, a
unified way to refer to your services within namespaces that doesn't depend on the VPC
DNS configuration, and standardized metrics and logs to monitor all of your applications.
Service Connect only interconnects services.

The following diagram shows an example Service Connect network with 2 subnets in the VPC
and 2 services. A client service that runs WordPress with 1 task in each subnets. A server
service that runs MySQL with 1 task in each subnet. Both services are highly available and
resilient to task and Availability Zone issues because each service runs multiple tasks that
are spread out over 2 subnets. The solid arrows show a connection from WordPress to MySQL.
For example, a `mysql --host=mysql` CLI command that is run from inside the
WordPress container in the task with the IP address `172.31.16.1`. The command
uses the short name `mysql` on the default port for MySQL. This name and port
connects to the Service Connect proxy in the same task. The proxy in the WordPress task
uses round-robin load balancing and any previous failure information in outlier detection to
pick which MySQL task to connect to. As shown by the solid arrows in the diagram, the proxy
connects to the second proxy in the MySQL task with the IP Address `172.31.16.2`.
The second proxy connects to the local MySQL server in the same task. Both proxies report
connection performance that is visible in graphs in the Amazon ECS and Amazon CloudWatch consoles so that
you can get performance metrics from all kinds of applications in the same way.

The following terms are used with Service Connect.

**port name**
:   The Amazon ECS task definition configuration that assigns a name to a particular
    port mapping. This configuration is only used by Amazon ECS Service Connect.

**client alias**
:   The Amazon ECS service configuration that assigns the port number that is used in
    the endpoint. Additionally, the client alias can assign the DNS name of the
    endpoint, overriding the discovery name. If a discovery name isn't provided in
    the Amazon ECS service, the client alias name overrides the port name as the endpoint
    name. For endpoint examples, see the definition of
    *endpoint*. Multiple client aliases can be assigned to an
    Amazon ECS service. This configuration is only used by Amazon ECS Service Connect.

**discovery name**
:   The optional, intermediate name that you can create for a specified port from
    the task definition. This name is used to create a AWS Cloud Map service. If this name
    isn't provided, the port name from the task definition is used. Multiple
    discovery names can be assigned to a specific port an Amazon ECS service.
    This configuration is only used by Amazon ECS Service Connect.

    AWS Cloud Map service names must be unique within a namespace. Because of this
    limitation, you can have only one Service Connect configuration without a
    discovery name for a particular task definition in each namespace.

**endpoint**
:   The URL to connect to an API or website. The URL contains the protocol, a DNS
    name, and the port. For more information about endpoints in general, see [endpoint](https://docs.aws.amazon.com/glossary/latest/reference/glos-chap.html#endpoint) in the *AWS glossary* in the
    Amazon Web Services General Reference.

    Service Connect creates endpoints that connect to Amazon ECS services and
    configures the tasks in Amazon ECS services to connect to the endpoints. The URL
    contains the protocol, a DNS name, and the port. You select the protocol and
    port name in the task definition, as the port must match the application that is
    inside the container image. In the service, you select each port by name and can
    assign the DNS name. If you don't specify a DNS name in the Amazon ECS service
    configuration, the port name from the task definition is used by default. For
    example, a Service Connect endpoint could be `http://blog:80`,
    `grpc://checkout:8080`, or
    `http://_db.production.internal:99`.

**Service Connect service**
:   The configuration of a single endpoint in an Amazon ECS service. This is a part of
    the Service Connect configuration, consisting of a single row in the
    **Service Connect and discovery name configuration** in
    the console, or one object in the `services` list in the JSON
    configuration of an Amazon ECS service. This configuration is only used by Amazon ECS Service Connect.

    For more information, see [ServiceConnectService](https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_ServiceConnectService.html) in the Amazon Elastic Container Service API Reference.

**namespace**
:   The short name or full Amazon Resource Name (ARN) of the AWS Cloud Map namespace for use with
    Service Connect. The namespace must be in the same AWS Region as the Amazon ECS
    service and cluster. The type of namespace in AWS Cloud Map doesn't affect
    Service Connect. The namespace can be one that is shared with your AWS account using AWS Resource Access Manager (AWS RAM) in AWS Regions that AWS RAM is available in. For more information
    about shared namespaces, see [Cross-account AWS Cloud Map
    namespace sharing](https://docs.aws.amazon.com/cloud-map/latest/dg/sharing-namespaces.html) in the
    *AWS Cloud Map Developer Guide*.

    Service Connect uses the AWS Cloud Map namespace as a logical grouping of Amazon ECS
    tasks that talk to one another. Each Amazon ECS service can belong to only one
    namespace. The services within a namespace can be spread across different Amazon ECS
    clusters within the same AWS Region. If the namespace is a shared namespace,
    the services can be spread across the namespace owner and namespace consumer
    AWS accounts. You can freely organize services by any criteria.

**client service**
:   A service that runs a network client application. This service must have a
    namespace configured. Each task in the service can discover and connect to all
    of the endpoints in the namespace through a Service Connect proxy
    container.

    If any of your containers in the task need to connect to an endpoint from a
    service in a namespace, choose a client service. If a frontend, reverse proxy,
    or load balancer application receives external traffic through other methods
    such as from Elastic Load Balancing, it could use this type of Service Connect
    configuration.

**client-server service**
:   An Amazon ECS service that runs a network or web service application. This service
    must have a namespace and at least one endpoint configured. Each task in the
    service is reachable by using the endpoints. The Service Connect proxy
    container listens on the endpoint name and port to direct traffic to the app
    containers in the task.

    If any of the containers expose and listen on a port for network traffic,
    choose a client-server service. These applications don't need to connect to
    other client-server services in the same namespace, but the client configuration
    is needed. A backend, middleware, business tier, or most microservices can use
    this type of Service Connect configuration. If you want a frontend, reverse
    proxy, or load balancer application to receive traffic from other services
    configured with Service Connect in the same namespace, these services should
    use this type of Service Connect configuration.

The Service Connect feature creates a virtual network of related services. The same
service configuration can be used across multiple different namespaces to run independent
yet identical sets of applications. Service Connect defines the proxy container in the
Amazon ECS service. This way, the same task definition can be used to run identical applications
in different namespaces with different Service Connect configurations. Each task that the
service makes runs a proxy container in the task.

Service Connect is suitable for connections between Amazon ECS services within the same
namespace. For the following applications, you need to use an additional interconnection
method to connect to an Amazon ECS service that is configured with Service Connect:

* Tasks that are configured in other namespaces
* Tasks that aren’t configured for Service Connect
* Other applications outside of Amazon ECS

These applications can connect through the Service Connect proxy but can’t resolve
Service Connect endpoint names.

For these applications to resolve the IP addresses of Amazon ECS tasks, you need to use another
interconnection method.

###### Topics

* [Pricing](#service-connect-pricing)
* [Amazon ECS Service Connect components](./service-connect-concepts-deploy.html)
* [Amazon ECS Service Connect configuration overview](./service-connect-concepts.html)
* [Amazon ECS Service Connect with shared AWS Cloud Map namespaces](./service-connect-shared-namespaces.html)
* [Amazon ECS Service Connect access logs](./service-connect-envoy-access-logs.html)
* [Encrypt Amazon ECS Service Connect traffic](./service-connect-tls.html)
* [Configuring Amazon ECS Service Connect with the AWS CLI](./create-service-connect.html)

## Pricing

* Amazon ECS Service Connect pricing depends on whether you use AWS Fargate or
  Amazon EC2 infrastructure to host your containerized workloads. When using Amazon ECS on
  AWS Outposts, the pricing follows the same model that's used when you use Amazon EC2
  directly. For more information, see [Amazon ECS Pricing](https://aws.amazon.com/ecs/pricing).
* There is no additional charge for using Amazon ECS Service Connect.
* There is no additional charge for AWS Cloud Map usage when used by
  Service Connect.
* Customers pay for compute resources used by Amazon ECS Service Connect, including
  vCPU and Memory. As the Amazon ECS Service Connect agent runs inside a customer
  task, there is no additional charge for running it. The task resources are
  shared between the customer workload and the Amazon ECS Service Connect
  agent.
* When using Amazon ECS Service Connect traffic encryption functionality with AWS Private CA,
  customers pay for the private certificate authority they create and for each TLS
  certificate issued. For more details, see [AWS Private Certificate Authority pricing](https://aws.amazon.com/private-ca/pricing/).
  To estimate the monthly cost of TLS certificates, customers need to know the
  number of Amazon ECS services that have TLS enabled, multiply it by the certificate
  cost, and then multiply it by six. As Amazon ECS Service Connect automatically
  rotates TLS certificates every five days, there are six certificates issued per
  Amazon ECS service, per month, on average.

**Javascript is disabled or is unavailable in your browser.**

To use the Amazon Web Services Documentation, Javascript must be enabled. Please refer to your browser's Help pages for instructions.

[Document Conventions](/general/latest/gr/docconventions.html)

Interconnect services

Service Connect components

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.