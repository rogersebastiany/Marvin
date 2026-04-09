NAT gateways - Amazon Virtual Private Cloud 

NAT gateways - Amazon Virtual Private Cloud
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
"name" : "User Guide",
"item" : "https://docs.aws.amazon.com/vpc/latest/userguide"
},
{
"@type" : "ListItem",
"position" : 4,
"name" : "Connect your VPC to other networks",
"item" : "https://docs.aws.amazon.com/vpc/latest/userguide/extend-intro.html"
},
{
"@type" : "ListItem",
"position" : 5,
"name" : "Connect to the internet or other networks using NAT devices",
"item" : "https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat.html"
},
{
"@type" : "ListItem",
"position" : 6,
"name" : "NAT gateways",
"item" : "https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat.html"
}
]
}

[Documentation](/index.html)[Amazon VPC](/vpc/index.html)[User Guide](what-is-amazon-vpc.html)

# NAT gateways

A NAT gateway is a Network Address Translation (NAT) service. You can use a NAT gateway
so that instances in a private subnet can connect to services outside your VPC but external
services can't initiate a connection with those instances.

When you create a NAT gateway, you specify one of the following connectivity types:

* **Public** – (Default) Instances in private subnets
  can connect to the internet through a public NAT gateway, but the instances can't receive
  unsolicited inbound connections from the internet. You create a public NAT gateway in a
  public subnet and must associate an Elastic IP address with the NAT gateway at creation. You
  route traffic from the NAT gateway to the internet gateway for the VPC. Alternatively, you
  can use a public NAT gateway to connect to other VPCs or your on-premises network. In this
  case, you route traffic from the NAT gateway through a transit gateway or a virtual private
  gateway.
* **Private** – Instances in private subnets can
  connect to other VPCs or your on-premises network through a private NAT gateway, but the
  instances can't receive unsolicited inbound connections from the other VPCs or the
  on-premises network. You can route traffic from the NAT gateway through a transit gateway or
  a virtual private gateway. You can't associate an Elastic IP address with a private NAT
  gateway. You can attach an internet gateway to a VPC with a private NAT gateway, but if you
  route traffic from the private NAT gateway to the internet gateway, the internet gateway
  drops the traffic.

A NAT gateway is for use with IPv4 or IPv6 traffic (using [DNS64 and NAT64](./nat-gateway-nat64-dns64.html)). Another option for enabling outbound-only internet
communication over IPv6 is using an [egress-only internet gateway](./egress-only-internet-gateway.html).

Both private and public NAT gateways map the source private IPv4 address of the instances to the private IPv4 address of the NAT gateway, but in the case of a public NAT gateway, the internet gateway then maps the private IPv4 address of the public
NAT gateway to the Elastic IP address associated with the NAT gateway. When sending response traffic to the instances, whether it's a
public or private NAT gateway, the NAT gateway translates the address back to the original source IP address.

###### Considerations

* Connections must always be initiated from within the VPC containing the NAT
  gateway.
* You can use either a public or private NAT gateway to route traffic to transit gateways
  and virtual private gateways.
* If you use a private NAT gateway to connect to a transit gateway or virtual private gateway,
  traffic to the destination will come from the private IP address of the private NAT gateway.
* If you use a public NAT gateway to connect to a transit gateway or virtual private
  gateway, traffic to the destination will come from the private IP address of the public NAT
  gateway. The public NAT gateway only uses its Elastic IP address as the source IP
  address when used in conjunction with an internet gateway in the same VPC.

###### Contents

* [NAT gateway basics](./nat-gateway-basics.html)
* [Work with NAT gateways](./nat-gateway-working-with.html)
* [Regional NAT gateways for automatic multi-AZ expansion](./nat-gateways-regional.html)
* [Use cases](./nat-gateway-scenarios.html)
* [DNS64 and NAT64](./nat-gateway-nat64-dns64.html)
* [Inspect traffic from NAT gateways](./nat-gateway-inspect-traffic.html)
* [CloudWatch metrics](./vpc-nat-gateway-cloudwatch.html)
* [Troubleshooting](./nat-gateway-troubleshooting.html)
* [Pricing](./nat-gateway-pricing.html)

**Javascript is disabled or is unavailable in your browser.**

To use the Amazon Web Services Documentation, Javascript must be enabled. Please refer to your browser's Help pages for instructions.

[Document Conventions](/general/latest/gr/docconventions.html)

NAT devices

NAT gateway basics

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.