What is a Network Load Balancer? - Elastic Load Balancing 

What is a Network Load Balancer? - Elastic Load Balancing
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
"name" : "Elastic Load Balancing",
"item" : "https://docs.aws.amazon.com/elasticloadbalancing/index.html"
},
{
"@type" : "ListItem",
"position" : 3,
"name" : "Network Load Balancers",
"item" : "https://docs.aws.amazon.com/elasticloadbalancing/latest/network"
},
{
"@type" : "ListItem",
"position" : 4,
"name" : "What is a Network Load Balancer?",
"item" : "https://docs.aws.amazon.com/elasticloadbalancing/latest/network/introduction.html"
}
]
}

[Documentation](/index.html)[Elastic Load Balancing](/elasticloadbalancing/index.html)[Network Load Balancers](introduction.html)

[Network Load Balancer components](#network-load-balancer-components)[Network Load Balancer overview](#network-load-balancer-overview)[Benefits of migrating from a Classic Load Balancer](#network-load-balancer-benefits)[Getting started](#network-load-balancer-get-started)[Pricing](#network-load-balancer-pricing)

# What is a Network Load Balancer?

Elastic Load Balancing automatically distributes your incoming traffic across multiple targets, such as EC2
instances, containers, and IP addresses, in one or more Availability Zones. It monitors the
health of its registered targets, and routes traffic only to the healthy targets. Elastic Load Balancing
scales your load balancer as your incoming traffic changes over time. It can automatically
scale to the vast majority of workloads.

Elastic Load Balancing supports the following load balancers: Application Load Balancers, Network Load Balancers, Gateway Load Balancers, and Classic Load Balancers.
You can select the type of load balancer that best suits your needs. This guide
discusses Network Load Balancers. For more information about the other load balancers, see the
[User Guide for Application Load Balancers](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/), the [User Guide for Gateway Load Balancers](https://docs.aws.amazon.com/elasticloadbalancing/latest/gateway/), and the [User Guide for Classic Load Balancers](https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/).

## Network Load Balancer components

A *load balancer* serves as the single point of contact for
clients. The load balancer distributes incoming traffic across multiple targets, such as
Amazon EC2 instances. This increases the availability of your application. You add one or
more listeners to your load balancer.

A *listener* checks for connection requests from clients, using the
protocol and port that you configure, and forwards requests to a target group.

A *target group* routes requests to one or more registered
targets, such as EC2 instances, using the protocol and the port number that you
specify. Network Load Balancer target groups support the TCP, UDP, TCP\_UDP, TLS, QUIC, and TCP\_QUIC protocols. You can register a
target with multiple target groups. You can configure health checks on a per target group
basis. Health checks are performed on all targets registered to the target groups that are
specified in the default action for your load balancer.

For more information, see the following documentation:

* [Load balancers](./network-load-balancers.html)
* [Listeners](./load-balancer-listeners.html)
* [Target groups](./load-balancer-target-groups.html)

## Network Load Balancer overview

A Network Load Balancer functions at the fourth layer of the Open Systems Interconnection (OSI) model.
It can handle millions of requests per second. After the load balancer receives a
request from a client, it selects a target from a target group in the default action.
It attempts to send the request to the selected target using the protocol and port
that you specified.

When you enable an Availability Zone for the load balancer, Elastic Load Balancing creates a load
balancer node in the Availability Zone. By default, each load balancer node distributes
traffic across the registered targets in its Availability Zone only. If you enable
cross-zone load balancing, each load balancer node distributes traffic across the
registered targets in all enabled Availability Zones. For more information, see [Update the Availability Zones for your Network Load Balancer](./availability-zones.html).

To increase the fault tolerance of your applications, you can enable multiple
Availability Zones for your load balancer and ensure that each target group has at least
one target in each enabled Availability Zone. For example, if one or more target groups
does not have a healthy target in an Availability Zone, we remove the IP address for the
corresponding subnet from DNS, but the load balancer nodes in the other Availability
Zones are still available to route traffic. If a client doesn't honor the time-to-live
(TTL) and sends requests to the IP address after it is removed from DNS, the requests
fail.

For TCP traffic, the load balancer selects a target using a flow hash algorithm based
on the protocol, source IP address, source port, destination IP address, destination
port, and TCP sequence number. The TCP connections from a client have different source
ports and sequence numbers, and can be routed to different targets. Each individual TCP
connection is routed to a single target for the life of the connection.

For UDP traffic, the load balancer selects a target using a flow hash algorithm based
on the protocol, source IP address, source port, destination IP address, and destination
port. A UDP flow has the same source and destination, so it is consistently routed to a
single target throughout its lifetime. Different UDP flows have different source IP
addresses and ports, so they can be routed to different targets.

For QUIC traffic, the load balancer selects a target using the Server ID specified in the Connection ID (CID).
For initial connection attempts that lack a Server ID, a flow hash algorithm based on the protocol,
source IP address, source port, destination IP address, and destination port is used. Once a Connection ID is established
traffic for this CID gets routed to the same target for the lifetime of the CID.

Elastic Load Balancing creates a network interface for each Availability Zone you enable. Each load
balancer node in the Availability Zone uses this network interface to get a static IP
address. When you create an Internet-facing load balancer, you can optionally associate
one Elastic IP address per subnet.

When you create a target group, you specify its target type, which determines how you
register targets. For example, you can register instance IDs, IP addresses, or an Application Load Balancer.
The target type also affects whether the client IP addresses are preserved.
For more information, see [Client IP preservation](./edit-target-group-attributes.html#client-ip-preservation).

You can add and remove targets from your load balancer as your needs change, without
disrupting the overall flow of requests to your application. Elastic Load Balancing scales your load
balancer as traffic to your application changes over time. Elastic Load Balancing can scale to the vast
majority of workloads automatically.

You can configure health checks, which are used to monitor the health of the
registered targets so that the load balancer can send requests only to the healthy
targets.

For more information, see [How Elastic Load Balancing works](https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/how-elastic-load-balancing-works.html) in
the *Elastic Load Balancing User Guide*.

## Benefits of migrating from a Classic Load Balancer

Using a Network Load Balancer instead of a Classic Load Balancer has the following benefits:

* Ability to handle volatile workloads and scale to millions of requests per
  second.
* Support for static IP addresses for the load balancer. You can also assign one
  Elastic IP address per subnet enabled for the load balancer.
* Support for registering targets by IP address, including targets outside the
  VPC for the load balancer.
* Support for routing requests to multiple applications on a single EC2
  instance. You can register each instance or IP address with the same target
  group using multiple ports.
* Support for containerized applications. Amazon Elastic Container Service (Amazon ECS) can select an unused
  port when scheduling a task and register the task with a target group using this
  port. This enables you to make efficient use of your clusters.
* Support for monitoring the health of each service independently, as health
  checks are defined at the target group level and many Amazon CloudWatch metrics are
  reported at the target group level. Attaching a target group to an Auto Scaling group
  enables you to scale each service dynamically based on demand.
* Support for the QUIC and TCP\_QUIC protocols with advanced congestion control,
  fewer round trip connection establishment, built in TLS, and connection migration across networks.

For more information about the features supported by each load
balancer type, see [Product comparisons](https://aws.amazon.com/elasticloadbalancing/features/#Product_comparisons)
for Elastic Load Balancing.

## Getting started

To create a Network Load Balancer using the AWS Management Console, AWS CLI, or AWS CloudFormation, see
[Create a Network Load Balancer](./create-network-load-balancer.html).

For demos of common load balancer configurations, see [Elastic Load Balancing Demos](https://exampleloadbalancer.com/).

## Pricing

For more information, see [Elastic Load Balancing pricing](https://aws.amazon.com/elasticloadbalancing/pricing/).

**Javascript is disabled or is unavailable in your browser.**

To use the Amazon Web Services Documentation, Javascript must be enabled. Please refer to your browser's Help pages for instructions.

[Document Conventions](/general/latest/gr/docconventions.html)

Network Load Balancers

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.