---
subcategory: "ECR (Elastic Container Registry)"
layout: "aws"
page\_title: "AWS: aws\_ecr\_repository"
description: |-
Provides an Elastic Container Registry Repository.
---
# Resource: aws\_ecr\_repository
Provides an Elastic Container Registry Repository.
## Example Usage
```terraform
resource "aws\_ecr\_repository" "foo" {
name = "bar"
image\_tag\_mutability = "MUTABLE"
image\_scanning\_configuration {
scan\_on\_push = true
}
}
```
### With Image Tag Mutability Exclusion
```terraform
resource "aws\_ecr\_repository" "example" {
name = "example-repo"
image\_tag\_mutability = "IMMUTABLE\_WITH\_EXCLUSION"
image\_tag\_mutability\_exclusion\_filter {
filter = "latest\*"
filter\_type = "WILDCARD"
}
image\_tag\_mutability\_exclusion\_filter {
filter = "dev-\*"
filter\_type = "WILDCARD"
}
}
```
## Argument Reference
This resource supports the following arguments:
\* `region` - (Optional) Region where this resource will be [managed](https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints). Defaults to the Region set in the [provider configuration](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference).
\* `name` - (Required) Name of the repository.
\* `encryption\_configuration` - (Optional) Encryption configuration for the repository. See [below for schema](#encryption\_configuration).
\* `force\_delete` - (Optional) If `true`, will delete the repository even if it contains images.
Defaults to `false`.
\* `image\_tag\_mutability` - (Optional) The tag mutability setting for the repository. Must be one of: `MUTABLE`, `IMMUTABLE`, `IMMUTABLE\_WITH\_EXCLUSION`, or `MUTABLE\_WITH\_EXCLUSION`. Defaults to `MUTABLE`.
\* `image\_tag\_mutability\_exclusion\_filter` - (Optional) Configuration block that defines filters to specify which image tags can override the default tag mutability setting. Only applicable when `image\_tag\_mutability` is set to `IMMUTABLE\_WITH\_EXCLUSION` or `MUTABLE\_WITH\_EXCLUSION`. See [below for schema](#image\_tag\_mutability\_exclusion\_filter).
\* `image\_scanning\_configuration` - (Optional) Configuration block that defines image scanning configuration for the repository. By default, image scanning must be manually triggered. See the [ECR User Guide](https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-scanning.html) for more information about image scanning.
\* `scan\_on\_push` - (Required) Indicates whether images are scanned after being pushed to the repository (true) or not scanned (false).
\* `tags` - (Optional) A map of tags to assign to the resource. If configured with a provider [`default\_tags` configuration block](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#default\_tags-configuration-block) present, tags with matching keys will overwrite those defined at the provider-level.
### encryption\_configuration
\* `encryption\_type` - (Optional) The encryption type to use for the repository. Valid values are `AES256` or `KMS`. Defaults to `AES256`.
\* `kms\_key` - (Optional) The ARN of the KMS key to use when `encryption\_type` is `KMS`. If not specified, uses the default AWS managed key for ECR.
### image\_tag\_mutability\_exclusion\_filter
\* `filter` - (Required) The filter pattern to use for excluding image tags from the mutability setting. Must contain only letters, numbers, and special characters (.\_\*-). Each filter can be up to 128 characters long and can contain a maximum of 2 wildcards (\*).
\* `filter\_type` - (Required) The type of filter to use. Must be `WILDCARD`.
## Attribute Reference
This resource exports the following attributes in addition to the arguments above:
\* `arn` - Full ARN of the repository.
\* `registry\_id` - The registry ID where the repository was created.
\* `repository\_url` - The URL of the repository (in the form `aws\_account\_id.dkr.ecr.region.amazonaws.com/repositoryName`).
\* `tags\_all` - A map of tags assigned to the resource, including those inherited from the provider [`default\_tags` configuration block](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#default\_tags-configuration-block).
## Timeouts
[Configuration options](https://developer.hashicorp.com/terraform/language/resources/syntax#operation-timeouts):
- `delete` - (Default `20m`)
## Import
In Terraform v1.12.0 and later, the [`import` block](https://developer.hashicorp.com/terraform/language/import) can be used with the `identity` attribute. For example:
```terraform
import {
to = aws\_ecr\_repository.service
identity = {
name = "test-service"
}
}
resource "aws\_ecr\_repository" "service" {
### Configuration omitted for brevity ###
}
```
### Identity Schema
#### Required
\* `name` - (String) Name of the ECR repository.
#### Optional
\* `account\_id` (String) AWS Account where this resource is managed.
\* `region` (String) Region where this resource is managed.
In Terraform v1.5.0 and later, use an [`import` block](https://developer.hashicorp.com/terraform/language/import) to import ECR Repositories using the `name`. For example:
```terraform
import {
to = aws\_ecr\_repository.service
id = "test-service"
}
```
Using `terraform import`, import ECR Repositories using the `name`. For example:
```console
% terraform import aws\_ecr\_repository.service test-service
```