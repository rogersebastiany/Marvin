---
subcategory: "ECS (Elastic Container)"
layout: "aws"
page\_title: "AWS: aws\_ecs\_cluster"
description: |-
Provides an ECS cluster.
---
# Resource: aws\_ecs\_cluster
Provides an ECS cluster.
## Example Usage
```terraform
resource "aws\_ecs\_cluster" "foo" {
name = "white-hart"
setting {
name = "containerInsights"
value = "enabled"
}
}
```
### Execute Command Configuration with Override Logging
```terraform
resource "aws\_kms\_key" "example" {
description = "example"
deletion\_window\_in\_days = 7
}
resource "aws\_cloudwatch\_log\_group" "example" {
name = "example"
}
resource "aws\_ecs\_cluster" "test" {
name = "example"
configuration {
execute\_command\_configuration {
kms\_key\_id = aws\_kms\_key.example.arn
logging = "OVERRIDE"
log\_configuration {
cloud\_watch\_encryption\_enabled = true
cloud\_watch\_log\_group\_name = aws\_cloudwatch\_log\_group.example.name
}
}
}
}
```
### Fargate Ephemeral Storage Encryption with Customer-Managed KMS Key
```terraform
data "aws\_caller\_identity" "current" {}
resource "aws\_kms\_key" "example" {
description = "example"
deletion\_window\_in\_days = 7
}
resource "aws\_kms\_key\_policy" "example" {
key\_id = aws\_kms\_key.example.id
policy = jsonencode({
Id = "ECSClusterFargatePolicy"
Statement = [
{
Sid = "Enable IAM User Permissions"
Effect = "Allow"
Principal = {
"AWS" : "\*"
}
Action = "kms:\*"
Resource = "\*"
},
{
Sid = "Allow generate data key access for Fargate tasks."
Effect = "Allow"
Principal = {
Service = "fargate.amazonaws.com"
}
Action = [
"kms:GenerateDataKeyWithoutPlaintext"
]
Condition = {
StringEquals = {
"kms:EncryptionContext:aws:ecs:clusterAccount" = [
data.aws\_caller\_identity.current.account\_id
]
"kms:EncryptionContext:aws:ecs:clusterName" = [
"example"
]
}
}
Resource = "\*"
},
{
Sid = "Allow grant creation permission for Fargate tasks."
Effect = "Allow"
Principal = {
Service = "fargate.amazonaws.com"
}
Action = [
"kms:CreateGrant"
]
Condition = {
StringEquals = {
"kms:EncryptionContext:aws:ecs:clusterAccount" = [
data.aws\_caller\_identity.current.account\_id
]
"kms:EncryptionContext:aws:ecs:clusterName" = [
"example"
]
}
"ForAllValues:StringEquals" = {
"kms:GrantOperations" = [
"Decrypt"
]
}
}
Resource = "\*"
}
]
Version = "2012-10-17"
})
}
resource "aws\_ecs\_cluster" "test" {
name = "example"
configuration {
managed\_storage\_configuration {
fargate\_ephemeral\_storage\_kms\_key\_id = aws\_kms\_key.example.arn
}
}
depends\_on = [
aws\_kms\_key\_policy.example
]
}
```
## Argument Reference
The following arguments are required:
\* `name` - (Required) Name of the cluster (up to 255 letters, numbers, hyphens, and underscores)
The following arguments are optional:
\* `region` - (Optional) Region where this resource will be [managed](https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints). Defaults to the Region set in the [provider configuration](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference).
\* `configuration` - (Optional) Execute command configuration for the cluster. See [`configuration` Block](#configuration-block) for details.
\* `service\_connect\_defaults` - (Optional) Default Service Connect namespace. See [`service\_connect\_defaults` Block](#service\_connect\_defaults-block) for details.
\* `setting` - (Optional) Configuration block(s) with cluster settings. For example, this can be used to enable CloudWatch Container Insights for a cluster. See [`setting` Block](#setting-block) for details.
\* `tags` - (Optional) Key-value map of resource tags. If configured with a provider [`default\_tags` configuration block](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#default\_tags-configuration-block) present, tags with matching keys will overwrite those defined at the provider-level.
### `configuration` Block
The `configuration` configuration block supports the following arguments:
\* `execute\_command\_configuration` - (Optional) Details of the execute command configuration. See [`execute\_command\_configuration` Block](#execute\_command\_configuration-block) for details.
\* `managed\_storage\_configuration` - (Optional) Details of the managed storage configuration. See [`managed\_storage\_configuration` Block](#managed\_storage\_configuration-block) for details.
### `execute\_command\_configuration` Block
The `execute\_command\_configuration` configuration block supports the following arguments:
\* `kms\_key\_id` - (Optional) AWS Key Management Service key ID to encrypt the data between the local client and the container.
\* `log\_configuration` - (Optional) Log configuration for the results of the execute command actions. Required when `logging` is `OVERRIDE`. See [`log\_configuration` Block](#log\_configuration-block) for details.
\* `logging` - (Optional) Log setting to use for redirecting logs for your execute command results. Valid values: `NONE`, `DEFAULT`, `OVERRIDE`.
#### `log\_configuration` Block
The `log\_configuration` configuration block supports the following arguments:
\* `cloud\_watch\_encryption\_enabled` - (Optional) Whether to enable encryption on the CloudWatch logs. If not specified, encryption will be disabled.
\* `cloud\_watch\_log\_group\_name` - (Optional) The name of the CloudWatch log group to send logs to.
\* `s3\_bucket\_name` - (Optional) Name of the S3 bucket to send logs to.
\* `s3\_bucket\_encryption\_enabled` - (Optional) Whether to enable encryption on the logs sent to S3. If not specified, encryption will be disabled.
\* `s3\_key\_prefix` - (Optional) Optional folder in the S3 bucket to place logs in.
### `managed\_storage\_configuration` Block
The `managed\_storage\_configuration` configuration block supports the following arguments:
\* `fargate\_ephemeral\_storage\_kms\_key\_id` - (Optional) AWS Key Management Service key ARN for the Fargate ephemeral storage.
\* `kms\_key\_id` - (Optional) AWS Key Management Service key ARN to encrypt the managed storage.
### `service\_connect\_defaults` Block
The `service\_connect\_defaults` configuration block supports the following arguments:
\* `namespace` - (Required) ARN of the [`aws\_service\_discovery\_http\_namespace`](/docs/providers/aws/r/service\_discovery\_http\_namespace.html) that's used when you create a service and don't specify a Service Connect configuration.
### `setting` Block
The `setting` configuration block supports the following arguments:
\* `name` - (Required) Name of the setting to manage. Valid values: `containerInsights`.
\* `value` - (Required) Value to assign to the setting. Valid values: `enhanced`, `enabled`, `disabled`.
## Attribute Reference
This resource exports the following attributes in addition to the arguments above:
\* `arn` - ARN that identifies the cluster.
\* `tags\_all` - Map of tags assigned to the resource, including those inherited from the provider [`default\_tags` configuration block](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#default\_tags-configuration-block).
## Import
In Terraform v1.5.0 and later, use an [`import` block](https://developer.hashicorp.com/terraform/language/import) to import ECS clusters using the cluster name. For example:
```terraform
import {
to = aws\_ecs\_cluster.stateless
id = "stateless-app"
}
```
Using `terraform import`, import ECS clusters using the cluster name. For example:
```console
% terraform import aws\_ecs\_cluster.stateless stateless-app
```