---
subcategory: "IAM (Identity & Access Management)"
layout: "aws"
page\_title: "AWS: aws\_iam\_role"
description: |-
Provides an IAM role.
---
# Resource: aws\_iam\_role
Provides an IAM role.
~> \*\*NOTE:\*\* If policies are attached to the role via the [`aws\_iam\_policy\_attachment` resource](/docs/providers/aws/r/iam\_policy\_attachment.html) and you are modifying the role `name` or `path`, the `force\_detach\_policies` argument must be set to `true` and applied before attempting the operation otherwise you will encounter a `DeleteConflict` error. The [`aws\_iam\_role\_policy\_attachment` resource (recommended)](/docs/providers/aws/r/iam\_role\_policy\_attachment.html) does not have this requirement.
~> \*\*NOTE:\*\* If you use this resource's `managed\_policy\_arns` argument or `inline\_policy` configuration blocks, this resource will take over exclusive management of the role's respective policy types (e.g., both policy types if both arguments are used). These arguments are incompatible with other ways of managing a role's policies, such as [`aws\_iam\_policy\_attachment`](/docs/providers/aws/r/iam\_policy\_attachment.html), [`aws\_iam\_role\_policy\_attachment`](/docs/providers/aws/r/iam\_role\_policy\_attachment.html), and [`aws\_iam\_role\_policy`](/docs/providers/aws/r/iam\_role\_policy.html). If you attempt to manage a role's policies by multiple means, you will get resource cycling and/or errors.
~> \*\*NOTE:\*\* We suggest using [`jsonencode()`](https://developer.hashicorp.com/terraform/language/functions/jsonencode) or [`aws\_iam\_policy\_document`](/docs/providers/aws/d/iam\_policy\_document.html) when assigning a value to `assume\_role\_policy` or `inline\_policy.\*.policy`. They seamlessly translate Terraform language into JSON, enabling you to maintain consistency within your configuration without the need for context switches. Also, you can sidestep potential complications arising from formatting discrepancies, whitespace inconsistencies, and other nuances inherent to JSON.
## Example Usage
### Basic Example
```terraform
resource "aws\_iam\_role" "test\_role" {
name = "test\_role"
# Terraform's "jsonencode" function converts a
# Terraform expression result to valid JSON syntax.
assume\_role\_policy = jsonencode({
Version = "2012-10-17"
Statement = [
{
Action = "sts:AssumeRole"
Effect = "Allow"
Sid = ""
Principal = {
Service = "ec2.amazonaws.com"
}
},
]
})
tags = {
tag-key = "tag-value"
}
}
```
### Example of Using Data Source for Assume Role Policy
```terraform
data "aws\_iam\_policy\_document" "instance\_assume\_role\_policy" {
statement {
actions = ["sts:AssumeRole"]
principals {
type = "Service"
identifiers = ["ec2.amazonaws.com"]
}
}
}
resource "aws\_iam\_role" "instance" {
name = "instance\_role"
path = "/system/"
assume\_role\_policy = data.aws\_iam\_policy\_document.instance\_assume\_role\_policy.json
}
```
### Example of Exclusive Inline Policies
~> The `inline\_policy` argument is deprecated. Use the [`aws\_iam\_role\_policy`](./iam\_role\_policy.html.markdown) resource instead. If Terraform should exclusively manage all inline policy associations (the current behavior of this argument), use the [`aws\_iam\_role\_policies\_exclusive`](./iam\_role\_policies\_exclusive.html.markdown) resource as well.
This example creates an IAM role with two inline IAM policies. If someone adds another inline policy out-of-band, on the next apply, Terraform will remove that policy. If someone deletes these policies out-of-band, Terraform will recreate them.
```terraform
resource "aws\_iam\_role" "example" {
name = "yak\_role"
assume\_role\_policy = data.aws\_iam\_policy\_document.instance\_assume\_role\_policy.json # (not shown)
inline\_policy {
name = "my\_inline\_policy"
policy = jsonencode({
Version = "2012-10-17"
Statement = [
{
Action = ["ec2:Describe\*"]
Effect = "Allow"
Resource = "\*"
},
]
})
}
inline\_policy {
name = "policy-8675309"
policy = data.aws\_iam\_policy\_document.inline\_policy.json
}
}
data "aws\_iam\_policy\_document" "inline\_policy" {
statement {
actions = ["ec2:DescribeAccountAttributes"]
resources = ["\*"]
}
}
```
### Example of Removing Inline Policies
~> The `inline\_policy` argument is deprecated. Use the [`aws\_iam\_role\_policy`](./iam\_role\_policy.html.markdown) resource instead. If Terraform should exclusively manage all inline policy associations (the current behavior of this argument), use the [`aws\_iam\_role\_policies\_exclusive`](./iam\_role\_policies\_exclusive.html.markdown) resource as well.
This example creates an IAM role with what appears to be empty IAM `inline\_policy` argument instead of using `inline\_policy` as a configuration block. The result is that if someone were to add an inline policy out-of-band, on the next apply, Terraform will remove that policy.
```terraform
resource "aws\_iam\_role" "example" {
name = "yak\_role"
assume\_role\_policy = data.aws\_iam\_policy\_document.instance\_assume\_role\_policy.json # (not shown)
inline\_policy {}
}
```
### Example of Exclusive Managed Policies
~> The `managed\_policy\_arns` argument is deprecated. Use the [`aws\_iam\_role\_policy\_attachment`](./iam\_role\_policy\_attachment.html.markdown) resource instead. If Terraform should exclusively manage all managed policy attachments (the current behavior of this argument), use the [`aws\_iam\_role\_policy\_attachments\_exclusive`](./iam\_role\_policy\_attachments\_exclusive.html.markdown) resource as well.
This example creates an IAM role and attaches two managed IAM policies. If someone attaches another managed policy out-of-band, on the next apply, Terraform will detach that policy. If someone detaches these policies out-of-band, Terraform will attach them again.
```terraform
resource "aws\_iam\_role" "example" {
name = "yak\_role"
assume\_role\_policy = data.aws\_iam\_policy\_document.instance\_assume\_role\_policy.json # (not shown)
managed\_policy\_arns = [aws\_iam\_policy.policy\_one.arn, aws\_iam\_policy.policy\_two.arn]
}
resource "aws\_iam\_policy" "policy\_one" {
name = "policy-618033"
policy = jsonencode({
Version = "2012-10-17"
Statement = [
{
Action = ["ec2:Describe\*"]
Effect = "Allow"
Resource = "\*"
},
]
})
}
resource "aws\_iam\_policy" "policy\_two" {
name = "policy-381966"
policy = jsonencode({
Version = "2012-10-17"
Statement = [
{
Action = ["s3:ListAllMyBuckets", "s3:ListBucket", "s3:HeadBucket"]
Effect = "Allow"
Resource = "\*"
},
]
})
}
```
### Example of Removing Managed Policies
~> The `managed\_policy\_arns` argument is deprecated. Use the [`aws\_iam\_role\_policy\_attachment`](./iam\_role\_policy\_attachment.html.markdown) resource instead. If Terraform should exclusively manage all managed policy attachments (the current behavior of this argument), use the [`aws\_iam\_role\_policy\_attachments\_exclusive`](./iam\_role\_policy\_attachments\_exclusive.html.markdown) resource as well.
This example creates an IAM role with an empty `managed\_policy\_arns` argument. If someone attaches a policy out-of-band, on the next apply, Terraform will detach that policy.
```terraform
resource "aws\_iam\_role" "example" {
name = "yak\_role"
assume\_role\_policy = data.aws\_iam\_policy\_document.instance\_assume\_role\_policy.json # (not shown)
managed\_policy\_arns = []
}
```
## Argument Reference
The following arguments are required:
\* `assume\_role\_policy` - (Required) Policy that grants an entity permission to assume the role.
~> \*\*NOTE:\*\* The `assume\_role\_policy` is very similar to but slightly different than a standard IAM policy and cannot use an `aws\_iam\_policy` resource. However, it \_can\_ use an `aws\_iam\_policy\_document` [data source](/docs/providers/aws/d/iam\_policy\_document.html). See the example above of how this works.
The following arguments are optional:
\* `description` - (Optional) Description of the role.
\* `force\_detach\_policies` - (Optional) Whether to force detaching any policies the role has before destroying it. Defaults to `false`.
\* `inline\_policy` - (Optional, \*\*Deprecated\*\*) Configuration block defining an exclusive set of IAM inline policies associated with the IAM role. See below. If no blocks are configured, Terraform will not manage any inline policies in this resource. Configuring one empty block (i.e., `inline\_policy {}`) will cause Terraform to remove \_all\_ inline policies added out of band on `apply`.
\* `managed\_policy\_arns` - (Optional, \*\*Deprecated\*\*) Set of exclusive IAM managed policy ARNs to attach to the IAM role. If this attribute is not configured, Terraform will ignore policy attachments to this resource. When configured, Terraform will align the role's managed policy attachments with this set by attaching or detaching managed policies. Configuring an empty set (i.e., `managed\_policy\_arns = []`) will cause Terraform to remove \_all\_ managed policy attachments.
\* `max\_session\_duration` - (Optional) Maximum session duration (in seconds) that you want to set for the specified role. If you do not specify a value for this setting, the default maximum of one hour is applied. This setting can have a value from 1 hour to 12 hours.
\* `name` - (Optional, Forces new resource) Friendly name of the role. If omitted, Terraform will assign a random, unique name. See [IAM Identifiers](https://docs.aws.amazon.com/IAM/latest/UserGuide/Using\_Identifiers.html) for more information.
\* `name\_prefix` - (Optional, Forces new resource) Creates a unique friendly name beginning with the specified prefix. Conflicts with `name`.
\* `path` - (Optional) Path to the role. See [IAM Identifiers](https://docs.aws.amazon.com/IAM/latest/UserGuide/Using\_Identifiers.html) for more information.
\* `permissions\_boundary` - (Optional) ARN of the policy that is used to set the permissions boundary for the role.
\* `tags` - Key-value mapping of tags for the IAM role. If configured with a provider [`default\_tags` configuration block](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#default\_tags-configuration-block) present, tags with matching keys will overwrite those defined at the provider-level.
### inline\_policy
This configuration block supports the following:
~> \*\*NOTE:\*\* Since one empty block (i.e., `inline\_policy {}`) is valid syntactically to remove out of band policies on `apply`, `name` and `policy` are technically \_optional\_. However, they are both \_required\_ in order to manage actual inline policies. Not including one or the other may not result in Terraform errors but will result in unpredictable and incorrect behavior.
\* `name` - (Required) Name of the role policy.
\* `policy` - (Required) Policy document as a JSON formatted string. For more information about building IAM policy documents with Terraform, see the [AWS IAM Policy Document Guide](https://learn.hashicorp.com/tutorials/terraform/aws-iam-policy).
## Attribute Reference
This resource exports the following attributes in addition to the arguments above:
\* `arn` - Amazon Resource Name (ARN) specifying the role.
\* `create\_date` - Creation date of the IAM role.
\* `id` - Name of the role.
\* `name` - Name of the role.
\* `tags\_all` - A map of tags assigned to the resource, including those inherited from the provider [`default\_tags` configuration block](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#default\_tags-configuration-block).
\* `unique\_id` - Stable and unique string identifying the role.
## Import
In Terraform v1.12.0 and later, the [`import` block](https://developer.hashicorp.com/terraform/language/import) can be used with the `identity` attribute. For example:
```terraform
import {
to = aws\_iam\_role.example
identity = {
name = "developer\_name"
}
}
resource "aws\_iam\_role" "example" {
### Configuration omitted for brevity ###
}
```
### Identity Schema
#### Required
\* `name` (String) Name of the IAM role.
#### Optional
\* `account\_id` (String) AWS Account where this resource is managed.
In Terraform v1.5.0 and later, use an [`import` block](https://developer.hashicorp.com/terraform/language/import) to import IAM Roles using the `name`. For example:
```terraform
import {
to = aws\_iam\_role.example
id = "developer\_name"
}
```
Using `terraform import`, import IAM Roles using the `name`. For example:
```console
% terraform import aws\_iam\_role.example developer\_name
```