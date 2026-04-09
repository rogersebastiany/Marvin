AWS PrivateLink concepts - Amazon Virtual Private Cloud 

AWS PrivateLink concepts - Amazon Virtual Private Cloud
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
"name" : "Amazon VPC",
"item" : "https://docs.aws.amazon.com/vpc/index.html"
},
{
"@type" : "ListItem",
"position" : 3,
"name" : "AWS PrivateLink",
"item" : "https://docs.aws.amazon.com/vpc/latest/privatelink"
},
{
"@type" : "ListItem",
"position" : 4,
"name" : "What is AWS PrivateLink?",
"item" : "https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html"
},
{
"@type" : "ListItem",
"position" : 5,
"name" : "AWS PrivateLink concepts",
"item" : "https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html"
}
]
}

[Documentation](/index.html)[Amazon VPC](/vpc/index.html)[AWS PrivateLink](what-is-privatelink.html)

[Architecture diagram](#architecture-diagram)[Providers](#concepts-service-providers)[Service or resource consumers](#concepts-service-consumers)[AWS PrivateLink connections](#privatelink-connections)[Private hosted zones](#concepts-private-hosted-zones)

# AWS PrivateLink concepts

You can use Amazon VPC to define a virtual private cloud (VPC), which is a logically
isolated virtual network. You can allow the clients in your VPC to connect to
destinations outside that VPC. For example, add an internet gateway to the VPC to allow
access to the internet, or add a VPN connection to allow access to your on-premises
network. Alternatively, use AWS PrivateLink to allow the clients in your VPC to connect to
services and resources in other VPCs using private IP addresses, as if those services
and resources were hosted directly in your VPC.

The following are important concepts to understand as you get started using
AWS PrivateLink.

###### Contents

* [Architecture diagram](#architecture-diagram)
* [Providers](#concepts-service-providers)
* [Service or resource consumers](#concepts-service-consumers)
* [AWS PrivateLink connections](#privatelink-connections)
* [Private hosted zones](#concepts-private-hosted-zones)

## Architecture diagram

The following diagram provides a high-level overview of how AWS PrivateLink works.
Consumers create VPC endpoints to connect to endpoint services and resources that
are hosted by providers.

## Providers

Understand the concepts related to a provider.

### Service provider

The owner of a service is the *service provider*. Service
providers include AWS, AWS Partners, and other AWS accounts. Service
providers can host their services using AWS resources, such as EC2 instances,
or using on-premises servers.

### Resource provider

The owner of a resource, for example a database or an Amazon EC2 instance, is the
resource provider. Resource providers include AWS services, AWS Partners,
and other AWS accounts. Resource providers can host their resources in VPCs or
on-premises.

###### Concepts

* [Endpoint services](#concepts-endpoint-services)
* [Service names](#concepts-service-names)
* [Service states](#concepts-service-states)
* [Resource configuration](#concepts-resource-configuration)
* [Resource gateway](#concepts-resource-gateway)

### Endpoint services

A service provider creates an *endpoint service* to make
their service available in a Region. A service provider must specify a load
balancer when creating an endpoint service. The load balancer receives requests
from service consumers and routes them to your service.

By default, your endpoint service is not available to service consumers. You
must add permissions that allow specific AWS principals to connect to your
endpoint service.

### Service names

Each endpoint service is identified by a service name. A service consumer must
specify the name of the service when creating a VPC endpoint. Service consumers
can query the service names for AWS services. Service providers must share the
names of their services with service consumers.

### Service states

The following are the possible states for an endpoint service:

* Pending - The endpoint service is being created.
* Available - The endpoint service is available.
* Failed - The endpoint service could not be
  created.
* Deleting - The service provider deleted the endpoint
  service and deletion is in progress.
* Deleted - The endpoint service is deleted.

### Resource configuration

The resource provider creates a *resource configuration* to
share a resource. A resource configuration is a logical object that represents
either a single resource such as a database, or a group of resources. A resource
can be an IP address, a domain-name target, or an [Amazon Relational Database Service](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html) (Amazon RDS)
database.

When sharing with other accounts, the resource provider must share the
resource through a [AWS Resource Access Manager](https://docs.aws.amazon.com/ram/latest/userguide/what-is.html) (AWS RAM) resource
share to allow specific AWS principals in the other account to connect to the
resource through a resource VPC endpoint.

Resource configurations can be associated with a service network which
principals connect to through a service-network VPC endpoint.

### Resource gateway

A resource gateway is a point of ingress into a VPC from where a resource is
being shared. The provider creates a resource gateway to share resources from
the VPC.

## Service or resource consumers

The user of a service or resource is a *consumer*. Consumers
can access endpoint services and resources from their VPCs or from
on-premises.

###### Concepts

* [VPC endpoints](#concepts-vpc-endpoints)
* [Endpoint network interfaces](#concepts-endpoint-network-interfaces)
* [Endpoint policies](#concepts-endpoint-policies)
* [Endpoint states](#concepts-endpoint-states)

### VPC endpoints

A consumer creates a *VPC endpoint* to connect their VPC to
an endpoint service or resource. A consumer must specify the endpoint service,
resource, or service network when creating a VPC endpoint. There are multiple
types of VPC endpoints. You must create the type of VPC endpoint that you
require.

* `Interface` - Create an *interface
  endpoint* to send TCP or UDP traffic to an endpoint
  service. Traffic destined for the endpoint service is resolved using
  DNS.
* `GatewayLoadBalancer` - Create a
  *Gateway Load Balancer endpoint* to send traffic to a fleet of virtual
  appliances using private IP addresses. You route traffic from your VPC
  to the Gateway Load Balancer endpoint using route tables. The Gateway Load Balancer distributes traffic to the
  virtual appliances and can scale with demand.
* `Resource` - Create a *resource
  endpoint* to access a resource that was shared with you
  and resides in another VPC. A resource endpoint lets you privately and
  securely access resources such as a database, an Amazon EC2 instance, an
  application endpoint, a domain-name target, or an IP address that may be
  in a private subnet in another VPC or in an on premise environment.
  Resource endpoints don't require a load balancer, and lets you access
  the resource directly.
* `Service network` - Create a *service-network
  endpoint* to access a service network that you created or
  was shared with you. You can use a single service-network endpoint to
  privately and securely access multiple resources and services that are
  associated to a service network.

There is another type of VPC endpoint, `Gateway`, which creates a
*gateway endpoint* to send traffic to Amazon S3 or DynamoDB.
Gateway endpoints do not use AWS PrivateLink, unlike the other types of VPC
endpoints. For more information, see [Gateway endpoints](./gateway-endpoints.html).

### Endpoint network interfaces

An *endpoint network interface* is a requester-managed
network interface that serves as an entry point for traffic destined to an
endpoint service, resource, or service network. For each subnet that you specify
when you create a VPC endpoint, we create an endpoint network interface in the
subnet.

If a VPC endpoint supports IPv4, its endpoint network interfaces have IPv4
addresses. If a VPC endpoint supports IPv6, its endpoint network interfaces have
IPv6 addresses. The IPv6 address for an endpoint network interface is
unreachable from the internet. When you describe an endpoint network interface
with an IPv6 address, notice that `denyAllIgwTraffic` is
enabled.

### Endpoint policies

A *VPC endpoint policy* is an IAM resource policy that
you attach to a VPC endpoint. It determines which principals can use the VPC
endpoint to access the endpoint service. The default VPC endpoint policy allows
all actions by all principals on all resources over the VPC endpoint.

### Endpoint states

When you create an interface VPC endpoint, the endpoint service receives a
connection request. The service provider can accept or reject the request. If
the service provider accepts the request, the service consumer can use the VPC
endpoint after it enters the Available state.

The following are the possible states for a VPC endpoint:

* PendingAcceptance - The connection request is pending.
  This is the initial state if requests are manually accepted.
* Pending - The service provider accepted the connection
  request. This is the initial state if requests are automatically
  accepted. The VPC endpoint returns to this state if the service consumer
  modifies the VPC endpoint.
* Available - The VPC endpoint is available for use.
* Rejected - The service provider rejected the connection
  request. The service provider can also reject a connection after it is
  available for use.
* Expired - The connection request expired.
* Failed - The VPC endpoint could not be made
  available.
* Deleting - The service consumer deleted the VPC endpoint
  and deletion is in progress.
* Deleted - The VPC endpoint is deleted.

The AWS PrivateLink API returns the possible states using camel case.

## AWS PrivateLink connections

Traffic from your VPC is sent to an endpoint service or resource using a
connection between the VPC endpoint and the endpoint service or resource. Traffic
between a VPC endpoint and an endpoint service or resource stays within the AWS
network, without traversing the public internet.

A service provider adds [permissions](./configure-endpoint-service.html#add-remove-permissions)
so that service consumers can access the endpoint service. The service consumer
initiates the connection and the service provider accepts or rejects the connection
request. A resource owner or service network owner shares a resource configuration
or service network with consumers through AWS Resource Access Manager so that consumers can access the
resource or service network.

With interface VPC endpoints, consumers can use [endpoint policies](./vpc-endpoints-access.html) to control which IAM
principals can use a VPC endpoint to access an endpoint service or resource.

## Private hosted zones

A *hosted zone* is a container for DNS records that define how
to route traffic for a domain or subdomain. With a *public hosted
zone*, the records specify how to route traffic on the internet. With
a *private hosted zone*, the records specify how to route traffic
in your VPCs.

You can configure Amazon Route 53 to route domain traffic to a VPC endpoint. For more
information, see [Routing traffic to a VPC endpoint using your domain name](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-to-vpc-interface-endpoint.html).

You can use Route 53 to configure split-horizon DNS, where you use the same domain
name for both a public website and an endpoint service powered by AWS PrivateLink. DNS
requests for the public hostname from the consumer VPC resolve to the private IP
addresses of the endpoint network interfaces, but requests from outside the VPC
continue to resolve to the public endpoints. For more information, see [DNS Mechanisms for Routing Traffic and Enabling Failover for AWS PrivateLink
Deployments](https://aws.amazon.com/blogs/apn/reviewing-dns-mechanisms-for-routing-traffic-and-enabling-failover-for-aws-privatelink-deployments/).

**Javascript is disabled or is unavailable in your browser.**

To use the Amazon Web Services Documentation, Javascript must be enabled. Please refer to your browser's Help pages for instructions.

[Document Conventions](/general/latest/gr/docconventions.html)

What is AWS PrivateLink?

Get started

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.