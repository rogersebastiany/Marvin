---
subcategory: "ELB (Elastic Load Balancing)"
layout: "aws"
page\_title: "AWS: aws\_lb"
description: |-
Provides a Load Balancer resource.
---
# Resource: aws\_lb
Provides a Load Balancer resource.
~> \*\*Note:\*\* `aws\_alb` is known as `aws\_lb`. The functionality is identical.
## Example Usage
### Application Load Balancer
```terraform
resource "aws\_lb" "test" {
name = "test-lb-tf"
internal = false
load\_balancer\_type = "application"
security\_groups = [aws\_security\_group.lb\_sg.id]
subnets = [for subnet in aws\_subnet.public : subnet.id]
enable\_deletion\_protection = true
access\_logs {
bucket = aws\_s3\_bucket.lb\_logs.id
prefix = "test-lb"
enabled = true
}
tags = {
Environment = "production"
}
}
```
### Network Load Balancer
```terraform
resource "aws\_lb" "test" {
name = "test-lb-tf"
internal = false
load\_balancer\_type = "network"
subnets = [for subnet in aws\_subnet.public : subnet.id]
enable\_deletion\_protection = true
tags = {
Environment = "production"
}
}
```
### Specifying Elastic IPs
```terraform
resource "aws\_lb" "example" {
name = "example"
load\_balancer\_type = "network"
subnet\_mapping {
subnet\_id = aws\_subnet.example1.id
allocation\_id = aws\_eip.example1.id
}
subnet\_mapping {
subnet\_id = aws\_subnet.example2.id
allocation\_id = aws\_eip.example2.id
}
}
```
### Specifying private IP addresses for an internal-facing load balancer
```terraform
resource "aws\_lb" "example" {
name = "example"
load\_balancer\_type = "network"
subnet\_mapping {
subnet\_id = aws\_subnet.example1.id
private\_ipv4\_address = "10.0.1.15"
}
subnet\_mapping {
subnet\_id = aws\_subnet.example2.id
private\_ipv4\_address = "10.0.2.15"
}
}
```
## Argument Reference
This resource supports the following arguments:
\* `region` - (Optional) Region where this resource will be [managed](https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints). Defaults to the Region set in the [provider configuration](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference).
\* `access\_logs` - (Optional) Access Logs block. See below.
\* `connection\_logs` - (Optional) Connection Logs block. See below. Only valid for Load Balancers of type `application`.
\* `client\_keep\_alive` - (Optional) Client keep alive value in seconds. The valid range is 60-604800 seconds. The default is 3600 seconds.
\* `customer\_owned\_ipv4\_pool` - (Optional) ID of the customer owned ipv4 pool to use for this load balancer.
\* `desync\_mitigation\_mode` - (Optional) How the load balancer handles requests that might pose a security risk to an application due to HTTP desync. Valid values are `monitor`, `defensive` (default), `strictest`.
\* `dns\_record\_client\_routing\_policy` - (Optional) How traffic is distributed among the load balancer Availability Zones. Possible values are `any\_availability\_zone` (default), `availability\_zone\_affinity`, or `partial\_availability\_zone\_affinity`. See [Availability Zone DNS affinity](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/network-load-balancers.html#zonal-dns-affinity) for additional details. Only valid for `network` type load balancers.
\* `drop\_invalid\_header\_fields` - (Optional) Whether HTTP headers with header fields that are not valid are removed by the load balancer (true) or routed to targets (false). The default is false. Elastic Load Balancing requires that message header names contain only alphanumeric characters and hyphens. Only valid for Load Balancers of type `application`.
\* `enable\_cross\_zone\_load\_balancing` - (Optional) If true, cross-zone load balancing of the load balancer will be enabled. For `network` and `gateway` type load balancers, this feature is disabled by default (`false`). For `application` load balancer this feature is always enabled (`true`) and cannot be disabled. Defaults to `false`.
\* `enable\_deletion\_protection` - (Optional) If true, deletion of the load balancer will be disabled via the AWS API. This will prevent Terraform from deleting the load balancer. Defaults to `false`.
\* `enable\_http2` - (Optional) Whether HTTP/2 is enabled in `application` load balancers. Defaults to `true`.
\* `enable\_tls\_version\_and\_cipher\_suite\_headers` - (Optional) Whether the two headers (`x-amzn-tls-version` and `x-amzn-tls-cipher-suite`), which contain information about the negotiated TLS version and cipher suite, are added to the client request before sending it to the target. Only valid for Load Balancers of type `application`. Defaults to `false`
\* `enable\_xff\_client\_port` - (Optional) Whether the X-Forwarded-For header should preserve the source port that the client used to connect to the load balancer in `application` load balancers. Defaults to `false`.
\* `enable\_waf\_fail\_open` - (Optional) Whether to allow a WAF-enabled load balancer to route requests to targets if it is unable to forward the request to AWS WAF. Defaults to `false`.
\* `enable\_zonal\_shift` - (Optional) Whether zonal shift is enabled. Defaults to `false`.
\* `enforce\_security\_group\_inbound\_rules\_on\_private\_link\_traffic` - (Optional) Whether inbound security group rules are enforced for traffic originating from a PrivateLink. Only valid for Load Balancers of type `network`. The possible values are `on` and `off`.
\* `health\_check\_logs` - (Optional) Health Check Logs block. See below. Only valid for Load Balancers of type `application`.
\* `idle\_timeout` - (Optional) Time in seconds that the connection is allowed to be idle. Only valid for Load Balancers of type `application`. Default: 60.
\* `internal` - (Optional) If true, the LB will be internal. Defaults to `false`.
\* `ip\_address\_type` - (Optional) Type of IP addresses used by the subnets for your load balancer. The possible values depend upon the load balancer type: `ipv4` (all load balancer types), `dualstack` (all load balancer types), and `dualstack-without-public-ipv4` (type `application` only).
\* `ipam\_pools` (Optional). The IPAM pools to use with the load balancer. Only valid for Load Balancers of type `application`. See [ipam\_pools](#ipam\_pools) for more information.
\* `load\_balancer\_type` - (Optional) Type of load balancer to create. Possible values are `application`, `gateway`, or `network`. The default value is `application`.
\* `minimum\_load\_balancer\_capacity` - (Optional) Minimum capacity for a load balancer. Only valid for Load Balancers of type `application` or `network`.
\* `name` - (Optional) Name of the LB. This name must be unique within your AWS account, can have a maximum of 32 characters, must contain only alphanumeric characters or hyphens, and must not begin or end with a hyphen. If not specified, Terraform will autogenerate a name beginning with `tf-lb`.
\* `name\_prefix` - (Optional) Creates a unique name beginning with the specified prefix. Conflicts with `name`.
\* `security\_groups` - (Optional) List of security group IDs to assign to the LB. Only valid for Load Balancers of type `application` or `network`. For load balancers of type `network` security groups cannot be added if none are currently present, and cannot all be removed once added. If either of these conditions are met, this will force a recreation of the resource.
\* `preserve\_host\_header` - (Optional) Whether the Application Load Balancer should preserve the Host header in the HTTP request and send it to the target without any change. Defaults to `false`.
\* `secondary\_ips\_auto\_assigned\_per\_subnet` - (Optional) The number of secondary IP addresses to configure for your load balancer nodes. Only valid for Load Balancers of type `network`. The valid range is 0-7. When decreased, this will force a recreation of the resource. Default: `0`.
\* `subnet\_mapping` - (Optional) Subnet mapping block. See below. For Load Balancers of type `network` subnet mappings can only be added.
\* `subnets` - (Optional) List of subnet IDs to attach to the LB. For Load Balancers of type `network` subnets can only be added (see [Availability Zones](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/network-load-balancers.html#availability-zones)), deleting a subnet for load balancers of type `network` will force a recreation of the resource.
\* `tags` - (Optional) Map of tags to assign to the resource. If configured with a provider [`default\_tags` configuration block](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#default\_tags-configuration-block) present, tags with matching keys will overwrite those defined at the provider-level.
\* `xff\_header\_processing\_mode` - (Optional) Determines how the load balancer modifies the `X-Forwarded-For` header in the HTTP request before sending the request to the target. The possible values are `append`, `preserve`, and `remove`. Only valid for Load Balancers of type `application`. The default is `append`.
~> \*\*NOTE:\*\* Please note that internal LBs can only use `ipv4` as the `ip\_address\_type`. You can only change to `dualstack` `ip\_address\_type` if the selected subnets are IPv6 enabled.
~> \*\*NOTE:\*\* Please note that one of either `subnets` or `subnet\_mapping` is required.
### access\_logs
\* `bucket` - (Required) S3 bucket name to store the logs in.
\* `enabled` - (Optional) Boolean to enable / disable `access\_logs`. Defaults to `false`, even when `bucket` is specified.
\* `prefix` - (Optional) S3 bucket prefix. Logs are stored in the root if not configured.
### connection\_logs
\* `bucket` - (Required) S3 bucket name to store the logs in.
\* `enabled` - (Optional) Boolean to enable / disable `connection\_logs`. Defaults to `false`, even when `bucket` is specified.
\* `prefix` - (Optional) S3 bucket prefix. Logs are stored in the root if not configured.
### health\_check\_logs
\* `bucket` - (Required) S3 bucket name to store the logs in.
\* `enabled` - (Optional) Boolean to enable / disable `health\_check\_logs`. Defaults to `false`, even when `bucket` is specified.
\* `prefix` - (Optional) S3 bucket prefix. Logs are stored in the root if not configured.
### ipam\_pools
\* `ipv4\_ipam\_pool\_id` - (Required) The ID of the IPv4 IPAM pool.
### minimum\_load\_balancer\_capacity
\* `capacity\_units` - (Required) The number of capacity units.
### subnet\_mapping
\* `subnet\_id` - (Required) ID of the subnet of which to attach to the load balancer. You can specify only one subnet per Availability Zone.
\* `allocation\_id` - (Optional) Allocation ID of the Elastic IP address for an internet-facing load balancer.
\* `ipv6\_address` - (Optional) IPv6 address. You associate IPv6 CIDR blocks with your VPC and choose the subnets where you launch both internet-facing and internal Application Load Balancers or Network Load Balancers.
\* `private\_ipv4\_address` - (Optional) Private IPv4 address for an internal load balancer.
## Attribute Reference
This resource exports the following attributes in addition to the arguments above:
\* `arn` - ARN of the load balancer.
\* `arn\_suffix` - ARN suffix for use with CloudWatch Metrics.
\* `dns\_name` - DNS name of the load balancer.
\* `subnet\_mapping.\*.outpost\_id` - ID of the Outpost containing the load balancer.
\* `tags\_all` - Map of tags assigned to the resource, including those inherited from the provider [`default\_tags` configuration block](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#default\_tags-configuration-block).
\* `zone\_id` - Canonical hosted zone ID of the load balancer (to be used in a Route 53 Alias record).
## Timeouts
[Configuration options](https://developer.hashicorp.com/terraform/language/resources/syntax#operation-timeouts):
- `create` - (Default `10m`)
- `update` - (Default `10m`)
- `delete` - (Default `10m`)
## Import
In Terraform v1.12.0 and later, the [`import` block](https://developer.hashicorp.com/terraform/language/import) can be used with the `identity` attribute. For example:
```terraform
import {
to = aws\_lb.example
identity = {
"arn" = "arn:aws:elasticloadbalancing:us-west-2:123456789012:loadbalancer/app/my-load-balancer/50dc6c495c0c9188"
}
}
resource "aws\_lb" "example" {
### Configuration omitted for brevity ###
}
```
### Identity Schema
#### Required
- `arn` (String) Amazon Resource Name (ARN) of the load balancer.
In Terraform v1.5.0 and later, use an [`import` block](https://developer.hashicorp.com/terraform/language/import) to import LBs using their ARN. For example:
```terraform
import {
to = aws\_lb.bar
id = "arn:aws:elasticloadbalancing:us-west-2:123456789012:loadbalancer/app/my-load-balancer/50dc6c495c0c9188"
}
```
Using `terraform import`, import LBs using their ARN. For example:
```console
% terraform import aws\_lb.bar arn:aws:elasticloadbalancing:us-west-2:123456789012:loadbalancer/app/my-load-balancer/50dc6c495c0c9188
```