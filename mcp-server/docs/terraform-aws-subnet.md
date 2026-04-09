---
subcategory: "VPC (Virtual Private Cloud)"
layout: "aws"
page\_title: "AWS: aws\_subnet"
description: |-
Provides an VPC Subnet resource.
---
# Resource: aws\_subnet
Provides an VPC subnet resource.
~> \*\*NOTE:\*\* Due to [AWS Lambda improved VPC networking changes that began deploying in September 2019](https://aws.amazon.com/blogs/compute/announcing-improved-vpc-networking-for-aws-lambda-functions/), subnets associated with Lambda Functions can take up to 45 minutes to successfully delete. Terraform AWS Provider version 2.31.0 and later automatically handles this increased timeout, however prior versions require setting the [customizable deletion timeout](#timeouts) to 45 minutes (`delete = "45m"`). AWS and HashiCorp are working together to reduce the amount of time required for resource deletion and updates can be tracked in this [GitHub issue](https://github.com/hashicorp/terraform-provider-aws/issues/10329).
## Example Usage
### Basic Usage
```terraform
resource "aws\_subnet" "main" {
vpc\_id = aws\_vpc.main.id
cidr\_block = "10.0.1.0/24"
tags = {
Name = "Main"
}
}
```
### Subnets In Secondary VPC CIDR Blocks
When managing subnets in one of a VPC's secondary CIDR blocks created using a [`aws\_vpc\_ipv4\_cidr\_block\_association`](vpc\_ipv4\_cidr\_block\_association.html)
resource, it is recommended to reference that resource's `vpc\_id` attribute to ensure correct dependency ordering.
```terraform
resource "aws\_vpc\_ipv4\_cidr\_block\_association" "secondary\_cidr" {
vpc\_id = aws\_vpc.main.id
cidr\_block = "172.20.0.0/16"
}
resource "aws\_subnet" "in\_secondary\_cidr" {
vpc\_id = aws\_vpc\_ipv4\_cidr\_block\_association.secondary\_cidr.vpc\_id
cidr\_block = "172.20.0.0/24"
}
```
### IPAM-Managed Subnets
```terraform
data "aws\_region" "current" {}
resource "aws\_vpc\_ipam" "test" {
operating\_regions {
region\_name = data.aws\_region.current.region
}
}
resource "aws\_vpc\_ipam\_pool" "test" {
address\_family = "ipv4"
ipam\_scope\_id = aws\_vpc\_ipam.test.private\_default\_scope\_id
locale = data.aws\_region.current.name
}
resource "aws\_vpc\_ipam\_pool\_cidr" "test" {
ipam\_pool\_id = aws\_vpc\_ipam\_pool.test.id
cidr = "10.0.0.0/16"
}
resource "aws\_vpc" "test" {
ipv4\_ipam\_pool\_id = aws\_vpc\_ipam\_pool.test.id
ipv4\_netmask\_length = 24
depends\_on = [aws\_vpc\_ipam\_pool\_cidr.test]
}
resource "aws\_vpc\_ipam\_pool" "vpc" {
address\_family = "ipv4"
ipam\_scope\_id = aws\_vpc\_ipam.test.private\_default\_scope\_id
locale = data.aws\_region.current.name
source\_ipam\_pool\_id = aws\_vpc\_ipam\_pool.test.id
source\_resource {
resource\_id = aws\_vpc.test.id
resource\_owner = data.aws\_caller\_identity.current.account\_id
resource\_region = data.aws\_region.current.name
resource\_type = "vpc"
}
}
resource "aws\_vpc\_ipam\_pool\_cidr" "vpc" {
ipam\_pool\_id = aws\_vpc\_ipam\_pool.vpc.id
cidr = aws\_vpc.test.cidr\_block
}
resource "aws\_subnet" "test" {
vpc\_id = aws\_vpc.test.id
ipv4\_ipam\_pool\_id = aws\_vpc\_ipam\_pool.vpc.id
ipv4\_netmask\_length = 28
availability\_zone = data.aws\_availability\_zones.available.names[0]
depends\_on = [aws\_vpc\_ipam\_pool\_cidr.vpc]
}
```
## Argument Reference
This resource supports the following arguments:
\* `region` - (Optional) Region where this resource will be [managed](https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints). Defaults to the Region set in the [provider configuration](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference).
\* `assign\_ipv6\_address\_on\_creation` - (Optional) Specify true to indicate
that network interfaces created in the specified subnet should be
assigned an IPv6 address. Default is `false`
\* `availability\_zone` - (Optional) AZ for the subnet.
\* `availability\_zone\_id` - (Optional) AZ ID of the subnet. This argument is not supported in all regions or partitions. If necessary, use `availability\_zone` instead.
\* `cidr\_block` - (Optional) The IPv4 CIDR block for the subnet.
\* `customer\_owned\_ipv4\_pool` - (Optional) The customer owned IPv4 address pool. Typically used with the `map\_customer\_owned\_ip\_on\_launch` argument. The `outpost\_arn` argument must be specified when configured.
\* `enable\_dns64` - (Optional) Indicates whether DNS queries made to the Amazon-provided DNS Resolver in this subnet should return synthetic IPv6 addresses for IPv4-only destinations. Default: `false`.
\* `enable\_lni\_at\_device\_index` - (Optional) Indicates the device position for local network interfaces in this subnet. For example, 1 indicates local network interfaces in this subnet are the secondary network interface (eth1). A local network interface cannot be the primary network interface (eth0).
\* `enable\_resource\_name\_dns\_aaaa\_record\_on\_launch` - (Optional) Indicates whether to respond to DNS queries for instance hostnames with DNS AAAA records. Default: `false`.
\* `enable\_resource\_name\_dns\_a\_record\_on\_launch` - (Optional) Indicates whether to respond to DNS queries for instance hostnames with DNS A records. Default: `false`.
\* `ipv6\_cidr\_block` - (Optional) The IPv6 network range for the subnet,
in CIDR notation. The subnet size must use a /64 prefix length. If the existing IPv6 subnet was created with `assign\_ipv6\_address\_on\_creation = true`, changing this value will force resource recreation.
\* `ipv6\_native` - (Optional) Indicates whether to create an IPv6-only subnet. Default: `false`.
\* `ipv4\_ipam\_pool\_id` - (Optional) ID of an IPv4 VPC Resource Planning IPAM Pool. The CIDR of this pool is used to allocate the CIDR for the subnet.
\* `ipv4\_netmask\_length` - (Optional) Netmask. Requires specifying a `ipv4\_ipam\_pool\_id`.
\* `ipv6\_ipam\_pool\_id` - (Optional) ID of an IPv6 VPC Resource Planning IPAM Pool. The CIDR of this pool is used to allocate the CIDR for the subnet.
\* `ipv6\_netmask\_length` - (Optional) Netmask. Requires specifying a `ipv6\_ipam\_pool\_id`. Valid values are from 44 to 64 in increments of 4.
\* `map\_customer\_owned\_ip\_on\_launch` - (Optional) Specify `true` to indicate that network interfaces created in the subnet should be assigned a customer owned IP address. The `customer\_owned\_ipv4\_pool` and `outpost\_arn` arguments must be specified when set to `true`. Default is `false`.
\* `map\_public\_ip\_on\_launch` - (Optional) Specify true to indicate that instances launched into the subnet should be assigned a public IP address. Default is `false`.
\* `outpost\_arn` - (Optional) The Amazon Resource Name (ARN) of the Outpost.
\* `private\_dns\_hostname\_type\_on\_launch` - (Optional) The type of hostnames to assign to instances in the subnet at launch. For IPv6-only subnets, an instance DNS name must be based on the instance ID. For dual-stack and IPv4-only subnets, you can specify whether DNS names use the instance IPv4 address or the instance ID. Valid values: `ip-name`, `resource-name`.
\* `vpc\_id` - (Required) The VPC ID.
\* `tags` - (Optional) A map of tags to assign to the resource. If configured with a provider [`default\_tags` configuration block](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#default\_tags-configuration-block) present, tags with matching keys will overwrite those defined at the provider-level.
## Attribute Reference
This resource exports the following attributes in addition to the arguments above:
\* `id` - The ID of the subnet
\* `arn` - The ARN of the subnet.
\* `ipv6\_cidr\_block\_association\_id` - The association ID for the IPv6 CIDR block.
\* `owner\_id` - The ID of the AWS account that owns the subnet.
\* `tags\_all` - A map of tags assigned to the resource, including those inherited from the provider [`default\_tags` configuration block](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#default\_tags-configuration-block).
## Timeouts
[Configuration options](https://developer.hashicorp.com/terraform/language/resources/syntax#operation-timeouts):
- `create` - (Default `10m`)
- `delete` - (Default `20m`)
## Import
In Terraform v1.12.0 and later, the [`import` block](https://developer.hashicorp.com/terraform/language/import) can be used with the `identity` attribute. For example:
```terraform
import {
to = aws\_subnet.example
identity = {
id = "subnet-9d4a7b6c"
}
}
resource "aws\_subnet" "example" {
### Configuration omitted for brevity ###
}
```
### Identity Schema
#### Required
\* `id` (String) ID of the subnet.
#### Optional
\* `account\_id` (String) AWS Account where this resource is managed.
\* `region` (String) Region where this resource is managed.
In Terraform v1.5.0 and later, use an [`import` block](https://developer.hashicorp.com/terraform/language/import) to import subnets using the subnet `id`. For example:
```terraform
import {
to = aws\_subnet.example
id = "subnet-9d4a7b6c"
}
```
Using `terraform import`, import subnets using the subnet `id`. For example:
```console
% terraform import aws\_subnet.example subnet-9d4a7b6c
```