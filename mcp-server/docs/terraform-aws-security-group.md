---
subcategory: "VPC (Virtual Private Cloud)"
layout: "aws"
page\_title: "AWS: aws\_security\_group"
description: |-
Provides a security group resource.
---
# Resource: aws\_security\_group
Provides a security group resource.
~> \*\*NOTE:\*\* Avoid using the `ingress` and `egress` arguments of the `aws\_security\_group` resource to configure in-line rules, as they struggle with managing multiple CIDR blocks, and, due to the historical lack of unique IDs, tags and descriptions. To avoid these problems, use the current best practice of the [`aws\_vpc\_security\_group\_egress\_rule`](vpc\_security\_group\_egress\_rule.html) and [`aws\_vpc\_security\_group\_ingress\_rule`](vpc\_security\_group\_ingress\_rule.html) resources with one CIDR block per rule.
!> \*\*WARNING:\*\* You should not use the `aws\_security\_group` resource with \_in-line rules\_ (using the `ingress` and `egress` arguments of `aws\_security\_group`) in conjunction with the [`aws\_vpc\_security\_group\_egress\_rule`](vpc\_security\_group\_egress\_rule.html) and [`aws\_vpc\_security\_group\_ingress\_rule`](vpc\_security\_group\_ingress\_rule.html) resources or the [`aws\_security\_group\_rule`](security\_group\_rule.html) resource. Doing so may cause rule conflicts, perpetual differences, and result in rules being overwritten.
~> \*\*NOTE:\*\* Referencing Security Groups across VPC peering has certain restrictions. More information is available in the [VPC Peering User Guide](https://docs.aws.amazon.com/vpc/latest/peering/vpc-peering-security-groups.html).
~> \*\*NOTE:\*\* Due to [AWS Lambda improved VPC networking changes that began deploying in September 2019](https://aws.amazon.com/blogs/compute/announcing-improved-vpc-networking-for-aws-lambda-functions/), security groups associated with Lambda Functions can take up to 45 minutes to successfully delete. Terraform AWS Provider version 2.31.0 and later automatically handles this increased timeout, however prior versions require setting the [customizable deletion timeout](#timeouts) to 45 minutes (`delete = "45m"`). AWS and HashiCorp are working together to reduce the amount of time required for resource deletion and updates can be tracked in this [GitHub issue](https://github.com/hashicorp/terraform-provider-aws/issues/10329).
~> \*\*NOTE:\*\* The `cidr\_blocks` and `ipv6\_cidr\_blocks` parameters are optional in the `ingress` and `egress` blocks. If nothing is specified, traffic will be blocked as described in \_NOTE on Egress rules\_ later.
## Example Usage
### Basic Usage
```terraform
resource "aws\_security\_group" "allow\_tls" {
name = "allow\_tls"
description = "Allow TLS inbound traffic and all outbound traffic"
vpc\_id = aws\_vpc.main.id
tags = {
Name = "allow\_tls"
}
}
resource "aws\_vpc\_security\_group\_ingress\_rule" "allow\_tls\_ipv4" {
security\_group\_id = aws\_security\_group.allow\_tls.id
cidr\_ipv4 = aws\_vpc.main.cidr\_block
from\_port = 443
ip\_protocol = "tcp"
to\_port = 443
}
resource "aws\_vpc\_security\_group\_ingress\_rule" "allow\_tls\_ipv6" {
security\_group\_id = aws\_security\_group.allow\_tls.id
cidr\_ipv6 = aws\_vpc.main.ipv6\_cidr\_block
from\_port = 443
ip\_protocol = "tcp"
to\_port = 443
}
resource "aws\_vpc\_security\_group\_egress\_rule" "allow\_all\_traffic\_ipv4" {
security\_group\_id = aws\_security\_group.allow\_tls.id
cidr\_ipv4 = "0.0.0.0/0"
ip\_protocol = "-1" # semantically equivalent to all ports
}
resource "aws\_vpc\_security\_group\_egress\_rule" "allow\_all\_traffic\_ipv6" {
security\_group\_id = aws\_security\_group.allow\_tls.id
cidr\_ipv6 = "::/0"
ip\_protocol = "-1" # semantically equivalent to all ports
}
```
~> \*\*NOTE on Egress rules:\*\* By default, AWS creates an `ALLOW ALL` egress rule when creating a new Security Group inside of a VPC. When creating a new Security Group inside a VPC, \*\*Terraform will remove this default rule\*\*, and require you specifically re-create it if you desire that rule. We feel this leads to fewer surprises in terms of controlling your egress rules. If you desire this rule to be in place, you can use this `egress` block:
```terraform
resource "aws\_security\_group" "example" {
# ... other configuration ...
egress {
from\_port = 0
to\_port = 0
protocol = "-1"
cidr\_blocks = ["0.0.0.0/0"]
ipv6\_cidr\_blocks = ["::/0"]
}
}
```
### Usage With Prefix List IDs
Prefix Lists are either managed by AWS internally, or created by the customer using a
[Prefix List resource](ec2\_managed\_prefix\_list.html). Prefix Lists provided by
AWS are associated with a prefix list name, or service name, that is linked to a specific region.
Prefix list IDs are exported on VPC Endpoints, so you can use this format:
```terraform
resource "aws\_security\_group" "example" {
# ... other configuration ...
egress {
from\_port = 0
to\_port = 0
protocol = "-1"
prefix\_list\_ids = [aws\_vpc\_endpoint.my\_endpoint.prefix\_list\_id]
}
}
resource "aws\_vpc\_endpoint" "my\_endpoint" {
# ... other configuration ...
}
```
You can also find a specific Prefix List using the `aws\_prefix\_list` data source.
### Removing All Ingress and Egress Rules
The `ingress` and `egress` arguments are processed in [attributes-as-blocks](https://developer.hashicorp.com/terraform/language/attr-as-blocks) mode. Due to this, removing these arguments from the configuration will \*\*not\*\* cause Terraform to destroy the managed rules. To subsequently remove all managed ingress and egress rules:
```terraform
resource "aws\_security\_group" "example" {
name = "sg"
vpc\_id = aws\_vpc.example.id
ingress = []
egress = []
}
```
### Recreating a Security Group
A simple security group `name` change "forces new" the security group--Terraform destroys the security group and creates a new one. (Likewise, `description`, `name\_prefix`, or `vpc\_id` [cannot be changed](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/working-with-security-groups.html#creating-security-group).) Attempting to recreate the security group leads to a variety of complications depending on how it is used.
Security groups are generally associated with other resources--\*\*more than 100\*\* AWS Provider resources reference security groups. Referencing a resource from another resource creates a one-way dependency. For example, if you create an EC2 `aws\_instance` that has a `vpc\_security\_group\_ids` argument that refers to an `aws\_security\_group` resource, the `aws\_security\_group` is a dependent of the `aws\_instance`. Because of this, Terraform will create the security group first so that it can then be associated with the EC2 instance.
However, the dependency relationship actually goes both directions causing the \_Security Group Deletion Problem\_. AWS does not allow you to delete the security group associated with another resource (\_e.g.\_, the `aws\_instance`).
Terraform does [not model bi-directional dependencies](https://developer.hashicorp.com/terraform/internals/graph) like this, but, even if it did, simply knowing the dependency situation would not be enough to solve it. For example, some resources must always have an associated security group while others don't need to. In addition, when the `aws\_security\_group` resource attempts to recreate, it receives a dependent object error, which does not provide information on whether the dependent object is a security group rule or, for example, an associated EC2 instance. Within Terraform, the associated resource (\_e.g.\_, `aws\_instance`) does not receive an error when the `aws\_security\_group` is trying to recreate even though that is where changes to the associated resource would need to take place (\_e.g.\_, removing the security group association).
Despite these sticky problems, below are some ways to improve your experience when you find it necessary to recreate a security group.
#### `create\_before\_destroy`
(This example is one approach to [recreating security groups](#recreating-a-security-group). For more information on the challenges and the \_Security Group Deletion Problem\_, see [the section above](#recreating-a-security-group).)
Normally, Terraform first deletes the existing security group resource and then creates a new one. When a security group is associated with a resource, the delete won't succeed. You can invert the default behavior using the [`create\_before\_destroy` meta argument](https://www.terraform.io/language/meta-arguments/lifecycle#create\_before\_destroy):
```terraform
resource "aws\_security\_group" "example" {
name = "changeable-name"
# ... other configuration ...
lifecycle {
create\_before\_destroy = true
}
}
```
#### `replace\_triggered\_by`
(This example is one approach to [recreating security groups](#recreating-a-security-group). For more information on the challenges and the \_Security Group Deletion Problem\_, see [the section above](#recreating-a-security-group).)
To replace a resource when a security group changes, use the [`replace\_triggered\_by` meta argument](https://www.terraform.io/language/meta-arguments/lifecycle#replace\_triggered\_by). Note that in this example, the `aws\_instance` will be destroyed and created again when the `aws\_security\_group` changes.
```terraform
resource "aws\_security\_group" "example" {
name = "sg"
# ... other configuration ...
}
resource "aws\_instance" "example" {
instance\_type = "t3.small"
# ... other configuration ...
vpc\_security\_group\_ids = [aws\_security\_group.test.id]
lifecycle {
# Reference the security group as a whole or individual attributes like `name`
replace\_triggered\_by = [aws\_security\_group.example]
}
}
```
#### Shorter timeout
(This example is one approach to [recreating security groups](#recreating-a-security-group). For more information on the challenges and the \_Security Group Deletion Problem\_, see [the section above](#recreating-a-security-group).)
If destroying a security group takes a long time, it may be because Terraform cannot distinguish between a dependent object (\_e.g.\_, a security group rule or EC2 instance) that is \_in the process of being deleted\_ and one that is not. In other words, it may be waiting for a train that isn't scheduled to arrive. To fail faster, shorten the `delete` [timeout](https://developer.hashicorp.com/terraform/language/resources/syntax#operation-timeouts) from the default timeout:
```terraform
resource "aws\_security\_group" "example" {
name = "izizavle"
# ... other configuration ...
timeouts {
delete = "2m"
}
}
```
#### Provisioners
(This example is one approach to [recreating security groups](#recreating-a-security-group). For more information on the challenges and the \_Security Group Deletion Problem\_, see [the section above](#recreating-a-security-group).)
\*\*DISCLAIMER:\*\* We \*\*\_HIGHLY\_\*\* recommend using one of the above approaches and \_NOT\_ using local provisioners. Provisioners, like the one shown below, should be considered a \*\*last resort\*\* since they are \_not readable\_, \_require skills outside standard Terraform configuration\_, are \_error prone\_ and \_difficult to maintain\_, are not compatible with cloud environments and upgrade tools, require AWS CLI installation, and are subject to AWS CLI and Terraform changes outside the AWS Provider.
```terraform
data "aws\_security\_group" "default" {
name = "default"
# ... other configuration ...
}
resource "aws\_security\_group" "example" {
name = "sg"
# ... other configuration ...
# The downstream resource must have at least one SG attached, therefore we
# attach the default SG of the VPC temporarily and remove it later on
provisioner "local-exec" {
when = destroy
command = < \*\*Note\*\* Although `cidr\_blocks`, `ipv6\_cidr\_blocks`, `prefix\_list\_ids`, and `security\_groups` are all marked as optional, you \_must\_ provide one of them in order to configure the source of the traffic.
\* `cidr\_blocks` - (Optional) List of CIDR blocks.
\* `description` - (Optional) Description of this ingress rule.
\* `ipv6\_cidr\_blocks` - (Optional) List of IPv6 CIDR blocks.
\* `prefix\_list\_ids` - (Optional) List of Prefix List IDs.
\* `security\_groups` - (Optional) List of security groups. A group name can be used relative to the default VPC. Otherwise, group ID.
\* `self` - (Optional) Whether the security group itself will be added as a source to this ingress rule.
### egress
This argument is processed in [attribute-as-blocks mode](https://www.terraform.io/docs/configuration/attr-as-blocks.html).
The following arguments are required:
\* `from\_port` - (Required) Start port (or ICMP type number if protocol is `icmp`)
\* `to\_port` - (Required) End range port (or ICMP code if protocol is `icmp`).
The following arguments are optional:
~> \*\*Note\*\* Although `cidr\_blocks`, `ipv6\_cidr\_blocks`, `prefix\_list\_ids`, and `security\_groups` are all marked as optional, you \_must\_ provide one of them in order to configure the destination of the traffic.
\* `cidr\_blocks` - (Optional) List of CIDR blocks.
\* `description` - (Optional) Description of this egress rule.
\* `ipv6\_cidr\_blocks` - (Optional) List of IPv6 CIDR blocks.
\* `prefix\_list\_ids` - (Optional) List of Prefix List IDs.
\* `protocol` - (Required) Protocol. If you select a protocol of `-1` (semantically equivalent to `all`, which is not a valid value here), you must specify a `from\_port` and `to\_port` equal to 0. The supported values are defined in the `IpProtocol` argument in the [IpPermission](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API\_IpPermission.html) API reference. This argument is normalized to a lowercase value to match the AWS API requirement when using Terraform 0.12.x and above. Please make sure that the value of the protocol is specified as lowercase when used with older version of Terraform to avoid issues during upgrade.
\* `security\_groups` - (Optional) List of security groups. A group name can be used relative to the default VPC. Otherwise, group ID.
\* `self` - (Optional) Whether the security group itself will be added as a source to this egress rule.
## Attribute Reference
This resource exports the following attributes in addition to the arguments above:
\* `arn` - ARN of the security group.
\* `id` - ID of the security group.
\* `owner\_id` - Owner ID.
\* `tags\_all` - A map of tags assigned to the resource, including those inherited from the provider [`default\_tags` configuration block](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#default\_tags-configuration-block).
## Timeouts
[Configuration options](https://developer.hashicorp.com/terraform/language/resources/syntax#operation-timeouts):
- `create` - (Default `10m`)
- `delete` - (Default `15m`)
## Import
In Terraform v1.12.0 and later, the [`import` block](https://developer.hashicorp.com/terraform/language/import) can be used with the `identity` attribute. For example:
```terraform
import {
to = aws\_security\_group.example
identity = {
id = "sg-903004f8"
}
}
resource "aws\_security\_group" "example" {
### Configuration omitted for brevity ###
}
```
### Identity Schema
#### Required
\* `id` (String) ID of the security group.
#### Optional
\* `account\_id` (String) AWS Account where this resource is managed.
\* `region` (String) Region where this resource is managed.
In Terraform v1.5.0 and later, use an [`import` block](https://developer.hashicorp.com/terraform/language/import) to import Security Groups using the security group `id`. For example:
```terraform
import {
to = aws\_security\_group.example
id = "sg-903004f8"
}
```
Using `terraform import`, import Security Groups using the security group `id`. For example:
```console
% terraform import aws\_security\_group.example sg-903004f8
```