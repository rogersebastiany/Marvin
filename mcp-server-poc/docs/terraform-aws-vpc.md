---
subcategory: "VPC (Virtual Private Cloud)"
layout: "aws"
page\_title: "AWS: aws\_vpc"
description: |-
Provides a VPC resource.
---
# Resource: aws\_vpc
Provides a VPC resource.
## Example Usage
Basic usage:
```terraform
resource "aws\_vpc" "main" {
cidr\_block = "10.0.0.0/16"
}
```
Basic usage with tags:
```terraform
resource "aws\_vpc" "main" {
cidr\_block = "10.0.0.0/16"
instance\_tenancy = "default"
tags = {
Name = "main"
}
}
```
VPC with CIDR from AWS IPAM:
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
locale = data.aws\_region.current.region
}
resource "aws\_vpc\_ipam\_pool\_cidr" "test" {
ipam\_pool\_id = aws\_vpc\_ipam\_pool.test.id
cidr = "172.20.0.0/16"
}
resource "aws\_vpc" "test" {
ipv4\_ipam\_pool\_id = aws\_vpc\_ipam\_pool.test.id
ipv4\_netmask\_length = 28
depends\_on = [
aws\_vpc\_ipam\_pool\_cidr.test
]
}
```
## Argument Reference
This resource supports the following arguments:
\* `region` - (Optional) Region where this resource will be [managed](https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints). Defaults to the Region set in the [provider configuration](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference).
\* `cidr\_block` - (Optional) The IPv4 CIDR block for the VPC. CIDR can be explicitly set or it can be derived from IPAM using `ipv4\_netmask\_length`.
\* `instance\_tenancy` - (Optional) A tenancy option for instances launched into the VPC. Default is `default`, which ensures that EC2 instances launched in this VPC use the EC2 instance tenancy attribute specified when the EC2 instance is launched. The only other option is `dedicated`, which ensures that EC2 instances launched in this VPC are run on dedicated tenancy instances regardless of the tenancy attribute specified at launch. This has a dedicated per region fee of $2 per hour, plus an hourly per instance usage fee.
\* `ipv4\_ipam\_pool\_id` - (Optional) The ID of an IPv4 IPAM pool you want to use for allocating this VPC's CIDR. IPAM is a VPC feature that you can use to automate your IP address management workflows including assigning, tracking, troubleshooting, and auditing IP addresses across AWS Regions and accounts. Using IPAM you can monitor IP address usage throughout your AWS Organization.
\* `ipv4\_netmask\_length` - (Optional) The netmask length of the IPv4 CIDR you want to allocate to this VPC. Requires specifying a `ipv4\_ipam\_pool\_id`.
\* `ipv6\_cidr\_block` - (Optional) IPv6 CIDR block to request from an IPAM Pool. Can be set explicitly or derived from IPAM using `ipv6\_netmask\_length`.
\* `ipv6\_ipam\_pool\_id` - (Optional) IPAM Pool ID for a IPv6 pool. Conflicts with `assign\_generated\_ipv6\_cidr\_block`.
\* `ipv6\_netmask\_length` - (Optional) Netmask length to request from IPAM Pool. Conflicts with `ipv6\_cidr\_block`. This can be omitted if IPAM pool as a `allocation\_default\_netmask\_length` set. Valid values are from `44` to `60` in increments of 4.
\* `ipv6\_cidr\_block\_network\_border\_group` - (Optional) By default when an IPv6 CIDR is assigned to a VPC a default ipv6\_cidr\_block\_network\_border\_group will be set to the region of the VPC. This can be changed to restrict advertisement of public addresses to specific Network Border Groups such as LocalZones.
\* `enable\_dns\_support` - (Optional) A boolean flag to enable/disable DNS support in the VPC. Defaults to true.
\* `enable\_network\_address\_usage\_metrics` - (Optional) Indicates whether Network Address Usage metrics are enabled for your VPC. Defaults to false.
\* `enable\_dns\_hostnames` - (Optional) A boolean flag to enable/disable DNS hostnames in the VPC. Defaults false.
\* `assign\_generated\_ipv6\_cidr\_block` - (Optional) Requests an Amazon-provided IPv6 CIDR block with a /56 prefix length for the VPC. You cannot specify the range of IP addresses, or the size of the CIDR block. Default is `false`. Conflicts with `ipv6\_ipam\_pool\_id`
\* `tags` - (Optional) A map of tags to assign to the resource. If configured with a provider [`default\_tags` configuration block](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#default\_tags-configuration-block) present, tags with matching keys will overwrite those defined at the provider-level.
## Attribute Reference
This resource exports the following attributes in addition to the arguments above:
\* `arn` - Amazon Resource Name (ARN) of VPC
\* `id` - The ID of the VPC
\* `instance\_tenancy` - Tenancy of instances spin up within VPC
\* `dhcp\_options\_id` - DHCP options id of the desired VPC.
\* `enable\_dns\_support` - Whether or not the VPC has DNS support
\* `enable\_network\_address\_usage\_metrics` - Whether Network Address Usage metrics are enabled for the VPC
\* `enable\_dns\_hostnames` - Whether or not the VPC has DNS hostname support
\* `main\_route\_table\_id` - The ID of the main route table associated with
this VPC. Note that you can change a VPC's main route table by using an
[`aws\_main\_route\_table\_association`](/docs/providers/aws/r/main\_route\_table\_association.html).
\* `default\_network\_acl\_id` - The ID of the network ACL created by default on VPC creation
\* `default\_security\_group\_id` - The ID of the security group created by default on VPC creation
\* `default\_route\_table\_id` - The ID of the route table created by default on VPC creation
\* `ipv6\_association\_id` - The association ID for the IPv6 CIDR block.
\* `ipv6\_cidr\_block\_network\_border\_group` - The Network Border Group Zone name
\* `owner\_id` - The ID of the AWS account that owns the VPC.
\* `tags\_all` - A map of tags assigned to the resource, including those inherited from the provider [`default\_tags` configuration block](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#default\_tags-configuration-block).
## Import
In Terraform v1.5.0 and later, use an [`import` block](https://developer.hashicorp.com/terraform/language/import) to import VPCs using the VPC `id`. For example:
```terraform
import {
to = aws\_vpc.test\_vpc
id = "vpc-a01106c2"
}
```
Using `terraform import`, import VPCs using the VPC `id`. For example:
```console
% terraform import aws\_vpc.test\_vpc vpc-a01106c2
```