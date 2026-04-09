---
subcategory: "KMS (Key Management)"
layout: "aws"
page\_title: "AWS: aws\_kms\_key"
description: |-
Manages a single-Region or multi-Region primary KMS key.
---
# Resource: aws\_kms\_key
Manages a single-Region or multi-Region primary KMS key.
~> \*\*NOTE on KMS Key Policy:\*\* KMS Key Policy can be configured in either the standalone resource [`aws\_kms\_key\_policy`](kms\_key\_policy.html)
or with the parameter `policy` in this resource.
Configuring with both will cause inconsistencies and may overwrite configuration.
## Example Usage
### Symmetric Encryption KMS Key
```terraform
data "aws\_caller\_identity" "current" {}
resource "aws\_kms\_key" "example" {
description = "An example symmetric encryption KMS key"
enable\_key\_rotation = true
deletion\_window\_in\_days = 20
policy = jsonencode({
Version = "2012-10-17"
Id = "key-default-1"
Statement = [
{
Sid = "Enable IAM User Permissions"
Effect = "Allow"
Principal = {
AWS = "arn:aws:iam::${data.aws\_caller\_identity.current.account\_id}:root"
},
Action = "kms:\*"
Resource = "\*"
},
{
Sid = "Allow administration of the key"
Effect = "Allow"
Principal = {
AWS = "arn:aws:iam::${data.aws\_caller\_identity.current.account\_id}:user/Alice"
},
Action = [
"kms:ReplicateKey",
"kms:Create\*",
"kms:Describe\*",
"kms:Enable\*",
"kms:List\*",
"kms:Put\*",
"kms:Update\*",
"kms:Revoke\*",
"kms:Disable\*",
"kms:Get\*",
"kms:Delete\*",
"kms:ScheduleKeyDeletion",
"kms:CancelKeyDeletion"
],
Resource = "\*"
},
{
Sid = "Allow use of the key"
Effect = "Allow"
Principal = {
AWS = "arn:aws:iam::${data.aws\_caller\_identity.current.account\_id}:user/Bob"
},
Action = [
"kms:DescribeKey",
"kms:Encrypt",
"kms:Decrypt",
"kms:ReEncrypt\*",
"kms:GenerateDataKey",
"kms:GenerateDataKeyWithoutPlaintext"
],
Resource = "\*"
}
]
})
}
```
### Symmetric Encryption KMS Key With Standalone Policy Resource
```terraform
data "aws\_caller\_identity" "current" {}
resource "aws\_kms\_key" "example" {
description = "An example symmetric encryption KMS key"
enable\_key\_rotation = true
deletion\_window\_in\_days = 20
}
resource "aws\_kms\_key\_policy" "example" {
key\_id = aws\_kms\_key.example.id
policy = jsonencode({
Version = "2012-10-17"
Id = "key-default-1"
Statement = [
{
Sid = "Enable IAM User Permissions"
Effect = "Allow"
Principal = {
AWS = "arn:aws:iam::${data.aws\_caller\_identity.current.account\_id}:root"
},
Action = "kms:\*"
Resource = "\*"
}
]
})
}
```
### Asymmetric KMS Key
```terraform
data "aws\_caller\_identity" "current" {}
resource "aws\_kms\_key" "example" {
description = "RSA-3072 asymmetric KMS key for signing and verification"
customer\_master\_key\_spec = "RSA\_3072"
key\_usage = "SIGN\_VERIFY"
enable\_key\_rotation = false
policy = jsonencode({
Version = "2012-10-17"
Id = "key-default-1"
Statement = [
{
Sid = "Enable IAM User Permissions"
Effect = "Allow"
Principal = {
AWS = "arn:aws:iam::${data.aws\_caller\_identity.current.account\_id}:root"
},
Action = "kms:\*"
Resource = "\*"
},
{
Sid = "Allow administration of the key"
Effect = "Allow"
Principal = {
AWS = "arn:aws:iam::${data.aws\_caller\_identity.current.account\_id}:role/Admin"
},
Action = [
"kms:Create\*",
"kms:Describe\*",
"kms:Enable\*",
"kms:List\*",
"kms:Put\*",
"kms:Update\*",
"kms:Revoke\*",
"kms:Disable\*",
"kms:Get\*",
"kms:Delete\*",
"kms:ScheduleKeyDeletion",
"kms:CancelKeyDeletion"
],
Resource = "\*"
},
{
Sid = "Allow use of the key"
Effect = "Allow"
Principal = {
AWS = "arn:aws:iam::${data.aws\_caller\_identity.current.account\_id}:role/Developer"
},
Action = [
"kms:Sign",
"kms:Verify",
"kms:DescribeKey"
],
Resource = "\*"
}
]
})
}
```
### HMAC KMS key
```terraform
data "aws\_caller\_identity" "current" {}
resource "aws\_kms\_key" "example" {
description = "HMAC\_384 key for tokens"
customer\_master\_key\_spec = "HMAC\_384"
key\_usage = "GENERATE\_VERIFY\_MAC"
enable\_key\_rotation = false
policy = jsonencode({
Version = "2012-10-17"
Id = "key-default-1"
Statement = [
{
Sid = "Enable IAM User Permissions"
Effect = "Allow"
Principal = {
AWS = "arn:aws:iam::${data.aws\_caller\_identity.current.account\_id}:root"
},
Action = "kms:\*"
Resource = "\*"
},
{
Sid = "Allow administration of the key"
Effect = "Allow"
Principal = {
AWS = "arn:aws:iam::${data.aws\_caller\_identity.current.account\_id}:role/Admin"
},
Action = [
"kms:Create\*",
"kms:Describe\*",
"kms:Enable\*",
"kms:List\*",
"kms:Put\*",
"kms:Update\*",
"kms:Revoke\*",
"kms:Disable\*",
"kms:Get\*",
"kms:Delete\*",
"kms:ScheduleKeyDeletion",
"kms:CancelKeyDeletion"
],
Resource = "\*"
},
{
Sid = "Allow use of the key"
Effect = "Allow"
Principal = {
AWS = "arn:aws:iam::${data.aws\_caller\_identity.current.account\_id}:role/Developer"
},
Action = [
"kms:GenerateMac",
"kms:VerifyMac",
"kms:DescribeKey"
],
Resource = "\*"
}
]
})
}
```
### Multi-Region Primary Key
```terraform
data "aws\_caller\_identity" "current" {}
resource "aws\_kms\_key" "example" {
description = "An example multi-Region primary key"
multi\_region = true
enable\_key\_rotation = true
deletion\_window\_in\_days = 10
policy = jsonencode({
Version = "2012-10-17"
Id = "key-default-1"
Statement = [
{
Sid = "Enable IAM User Permissions"
Effect = "Allow"
Principal = {
AWS = "arn:aws:iam::${data.aws\_caller\_identity.current.account\_id}:root"
},
Action = "kms:\*"
Resource = "\*"
},
{
Sid = "Allow administration of the key"
Effect = "Allow"
Principal = {
AWS = "arn:aws:iam::${data.aws\_caller\_identity.current.account\_id}:user/Alice"
},
Action = [
"kms:ReplicateKey",
"kms:Create\*",
"kms:Describe\*",
"kms:Enable\*",
"kms:List\*",
"kms:Put\*",
"kms:Update\*",
"kms:Revoke\*",
"kms:Disable\*",
"kms:Get\*",
"kms:Delete\*",
"kms:ScheduleKeyDeletion",
"kms:CancelKeyDeletion"
],
Resource = "\*"
},
{
Sid = "Allow use of the key"
Effect = "Allow"
Principal = {
AWS = "arn:aws:iam::${data.aws\_caller\_identity.current.account\_id}:user/Bob"
},
Action = [
"kms:DescribeKey",
"kms:Encrypt",
"kms:Decrypt",
"kms:ReEncrypt\*",
"kms:GenerateDataKey",
"kms:GenerateDataKeyWithoutPlaintext"
],
Resource = "\*"
}
]
})
}
```
## Argument Reference
This resource supports the following arguments:
\* `region` - (Optional) Region where this resource will be [managed](https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints). Defaults to the Region set in the [provider configuration](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference).
\* `description` - (Optional) The description of the key as viewed in AWS console.
\* `key\_usage` - (Optional) Specifies the intended use of the key. Valid values: `ENCRYPT\_DECRYPT`, `SIGN\_VERIFY`, or `GENERATE\_VERIFY\_MAC`.
Defaults to `ENCRYPT\_DECRYPT`.
\* `custom\_key\_store\_id` - (Optional) ID of the KMS [Custom Key Store](https://docs.aws.amazon.com/kms/latest/developerguide/create-cmk-keystore.html) where the key will be stored instead of KMS (eg CloudHSM).
\* `customer\_master\_key\_spec` - (Optional) Specifies whether the key contains a symmetric key or an asymmetric key pair and the encryption algorithms or signing algorithms that the key supports.
Valid values: `SYMMETRIC\_DEFAULT`, `RSA\_2048`, `RSA\_3072`, `RSA\_4096`, `HMAC\_224`, `HMAC\_256`, `HMAC\_384`, `HMAC\_512`, `ECC\_NIST\_P256`, `ECC\_NIST\_P384`, `ECC\_NIST\_P521`, `ECC\_SECG\_P256K1`, `ML\_DSA\_44`, `ML\_DSA\_65`, `ML\_DSA\_87`, `SM2` (China Regions only), or `ECC\_NIST\_EDWARDS25519`. Defaults to `SYMMETRIC\_DEFAULT`. For help with choosing a key spec, see the [AWS KMS Developer Guide](https://docs.aws.amazon.com/kms/latest/developerguide/symm-asymm-choose.html).
\* `policy` - (Optional) A valid policy JSON document. Although this is a key policy, not an IAM policy, an [`aws\_iam\_policy\_document`](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam\_policy\_document), in the form that designates a principal, can be used. For more information about building policy documents with Terraform, see the [AWS IAM Policy Document Guide](https://learn.hashicorp.com/terraform/aws/iam-policy).
~> \*\*NOTE:\*\* Note: All KMS keys must have a key policy. If a key policy is not specified, AWS gives the KMS key a [default key policy](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default) that gives all principals in the owning account unlimited access to all KMS operations for the key. This default key policy effectively delegates all access control to IAM policies and KMS grants.
\* `bypass\_policy\_lockout\_safety\_check` - (Optional) A flag to indicate whether to bypass the key policy lockout safety check.
Setting this value to true increases the risk that the KMS key becomes unmanageable. Do not set this value to true indiscriminately.
For more information, refer to the scenario in the [Default Key Policy](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default-allow-root-enable-iam) section in the \_AWS Key Management Service Developer Guide\_.
The default value is `false`.
\* `deletion\_window\_in\_days` - (Optional) The waiting period, specified in number of days. After the waiting period ends, AWS KMS deletes the KMS key.
If you specify a value, it must be between `7` and `30`, inclusive. If you do not specify a value, it defaults to `30`.
If the KMS key is a multi-Region primary key with replicas, the waiting period begins when the last of its replica keys is deleted. Otherwise, the waiting period begins immediately.
\* `is\_enabled` - (Optional) Specifies whether the key is enabled. Defaults to `true`.
\* `enable\_key\_rotation` - (Optional, required to be enabled if `rotation\_period\_in\_days` is specified) Specifies whether [key rotation](http://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html) is enabled. Defaults to `false`.
\* `rotation\_period\_in\_days` - (Optional) Custom period of time between each rotation date. Must be a number between 90 and 2560 (inclusive).
\* `multi\_region` - (Optional) Indicates whether the KMS key is a multi-Region (`true`) or regional (`false`) key. Defaults to `false`.
\* `tags` - (Optional) A map of tags to assign to the object. If configured with a provider [`default\_tags` configuration block](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#default\_tags-configuration-block) present, tags with matching keys will overwrite those defined at the provider-level.
\* `xks\_key\_id` - (Optional) Identifies the external key that serves as key material for the KMS key in an external key store.
## Attribute Reference
This resource exports the following attributes in addition to the arguments above:
\* `arn` - The Amazon Resource Name (ARN) of the key.
\* `key\_id` - The globally unique identifier for the key.
\* `tags\_all` - A map of tags assigned to the resource, including those inherited from the provider [`default\_tags` configuration block](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#default\_tags-configuration-block).
## Timeouts
~> \*\*Note:\*\* There are a variety of default timeouts set internally. If you set a shorter custom timeout than one of the defaults, the custom timeout will not be respected as the longer of the custom or internal default will be used.
[Configuration options](https://developer.hashicorp.com/terraform/language/resources/syntax#operation-timeouts):
\* `create` - (Default `2m`)
## Import
In Terraform v1.12.0 and later, the [`import` block](https://developer.hashicorp.com/terraform/language/import) can be used with the `identity` attribute. For example:
```terraform
import {
to = aws\_kms\_key.example
identity = {
id = "1234abcd-12ab-34cd-56ef-1234567890ab"
}
}
resource "aws\_kms\_key" "example" {
### Configuration omitted for brevity ###
}
```
### Identity Schema
#### Required
\* `id` - (String) ID of the KMS key.
#### Optional
\* `account\_id` (String) AWS Account where this resource is managed.
\* `region` (String) Region where this resource is managed.
In Terraform v1.5.0 and later, use an [`import` block](https://developer.hashicorp.com/terraform/language/import) to import KMS Keys using the `id`. For example:
```terraform
import {
to = aws\_kms\_key.a
id = "1234abcd-12ab-34cd-56ef-1234567890ab"
}
```
Using `terraform import`, import KMS Keys using the `id`. For example:
```console
% terraform import aws\_kms\_key.a 1234abcd-12ab-34cd-56ef-1234567890ab
```