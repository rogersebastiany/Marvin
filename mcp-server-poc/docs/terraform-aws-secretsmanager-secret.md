---
subcategory: "Secrets Manager"
layout: "aws"
page\_title: "AWS: aws\_secretsmanager\_secret"
description: |-
Provides a resource to manage AWS Secrets Manager secret metadata
---
# Resource: aws\_secretsmanager\_secret
Provides a resource to manage AWS Secrets Manager secret metadata. To manage secret rotation, see the [`aws\_secretsmanager\_secret\_rotation` resource](/docs/providers/aws/r/secretsmanager\_secret\_rotation.html). To manage a secret value, see the [`aws\_secretsmanager\_secret\_version` resource](/docs/providers/aws/r/secretsmanager\_secret\_version.html).
## Example Usage
### Basic
```terraform
resource "aws\_secretsmanager\_secret" "example" {
name = "example"
}
```
## Argument Reference
This resource supports the following arguments:
\* `region` - (Optional) Region where this resource will be [managed](https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints). Defaults to the Region set in the [provider configuration](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference).
\* `description` - (Optional) Description of the secret.
\* `kms\_key\_id` - (Optional) ARN or Id of the AWS KMS key to be used to encrypt the secret values in the versions stored in this secret. If you need to reference a CMK in a different account, you can use only the key ARN. If you don't specify this value, then Secrets Manager defaults to using the AWS account's default KMS key (the one named `aws/secretsmanager`). If the default KMS key with that name doesn't yet exist, then AWS Secrets Manager creates it for you automatically the first time.
\* `name\_prefix` - (Optional) Creates a unique name beginning with the specified prefix. Conflicts with `name`.
\* `name` - (Optional) Friendly name of the new secret. The secret name can consist of uppercase letters, lowercase letters, digits, and any of the following characters: `/\_+=.@-` Conflicts with `name\_prefix`.
\* `policy` - (Optional) Valid JSON document representing a [resource policy](https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access\_resource-based-policies.html). For more information about building AWS IAM policy documents with Terraform, see the [AWS IAM Policy Document Guide](https://learn.hashicorp.com/terraform/aws/iam-policy). Removing `policy` from your configuration or setting `policy` to null or an empty string (i.e., `policy = ""`) \_will not\_ delete the policy since it could have been set by `aws\_secretsmanager\_secret\_policy`. To delete the `policy`, set it to `"{}"` (an empty JSON document).
\* `recovery\_window\_in\_days` - (Optional) Number of days that AWS Secrets Manager waits before it can delete the secret. This value can be `0` to force deletion without recovery or range from `7` to `30` days. The default value is `30`.
\* `replica` - (Optional) Configuration block to support secret replication. See details below.
\* `force\_overwrite\_replica\_secret` - (Optional) Accepts boolean value to specify whether to overwrite a secret with the same name in the destination Region.
\* `tags` - (Optional) Key-value map of user-defined tags that are attached to the secret. If configured with a provider [`default\_tags` configuration block](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#default\_tags-configuration-block) present, tags with matching keys will overwrite those defined at the provider-level.
### replica
\* `kms\_key\_id` - (Optional) ARN, Key ID, or Alias of the AWS KMS key within the region secret is replicated to. If one is not specified, then Secrets Manager defaults to using the AWS account's default KMS key (`aws/secretsmanager`) in the region or creates one for use if non-existent.
\* `region` - (Required) Region for replicating the secret.
## Attribute Reference
This resource exports the following attributes in addition to the arguments above:
\* `id` - ARN of the secret.
\* `arn` - ARN of the secret.
\* `replica` - Attributes of a replica are described below.
\* `tags\_all` - Map of tags assigned to the resource, including those inherited from the provider [`default\_tags` configuration block](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#default\_tags-configuration-block).
### replica
\* `last\_accessed\_date` - Date that you last accessed the secret in the Region.
\* `status` - Status can be `InProgress`, `Failed`, or `InSync`.
\* `status\_message` - Message such as `Replication succeeded` or `Secret with this name already exists in this region`.
## Import
In Terraform v1.12.0 and later, the [`import` block](https://developer.hashicorp.com/terraform/language/import) can be used with the `identity` attribute. For example:
```terraform
import {
to = aws\_secretsmanager\_secret.example
identity = {
"arn" = "arn:aws:secretsmanager:us-east-1:123456789012:secret:example-123456"
}
}
resource "aws\_secretsmanager\_secret" "example" {
### Configuration omitted for brevity ###
}
```
### Identity Schema
#### Required
- `arn` (String) Amazon Resource Name (ARN) of the Secrets Manager secret.
In Terraform v1.5.0 and later, use an [`import` block](https://developer.hashicorp.com/terraform/language/import) to import `aws\_secretsmanager\_secret` using the secret Amazon Resource Name (ARN). For example:
```terraform
import {
to = aws\_secretsmanager\_secret.example
id = "arn:aws:secretsmanager:us-east-1:123456789012:secret:example-123456"
}
```
Using `terraform import`, import `aws\_secretsmanager\_secret` using the secret Amazon Resource Name (ARN). For example:
```console
% terraform import aws\_secretsmanager\_secret.example arn:aws:secretsmanager:us-east-1:123456789012:secret:example-123456
```