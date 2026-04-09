---
subcategory: "S3 (Simple Storage)"
layout: "aws"
page\_title: "AWS: aws\_s3\_bucket"
description: |-
Provides a S3 bucket resource.
---
# Resource: aws\_s3\_bucket
Provides a S3 bucket resource.
-> This resource provides functionality for managing S3 general purpose buckets in an AWS Partition. To manage Amazon S3 Express directory buckets, use the [`aws\_directory\_bucket`](/docs/providers/aws/r/s3\_directory\_bucket.html) resource. To manage [S3 on Outposts](https://docs.aws.amazon.com/AmazonS3/latest/dev/S3onOutposts.html), use the [`aws\_s3control\_bucket`](/docs/providers/aws/r/s3control\_bucket.html) resource.
-> Object Lock can be enabled by using the `object\_lock\_enable` attribute or by using the [`aws\_s3\_bucket\_object\_lock\_configuration`](/docs/providers/aws/r/s3\_bucket\_object\_lock\_configuration.html) resource. Please note, that by using the resource, Object Lock can be enabled/disabled without destroying and recreating the bucket.
-> To support ABAC (Attribute Based Access Control) in general purpose buckets, this resource will now attempt to send tags in the create request and use the S3 Control tagging APIs [`TagResource`](https://docs.aws.amazon.com/AmazonS3/latest/API/API\_control\_TagResource.html), [`UntagResource`](https://docs.aws.amazon.com/AmazonS3/latest/API/API\_control\_UntagResource.html), and [`ListTagsForResource`](https://docs.aws.amazon.com/AmazonS3/latest/API/API\_control\_ListTagsForResource.html) for read and update operations. The calling principal must have the corresponding `s3:TagResource`, `s3:UntagResource`, and `s3:ListTagsForResource` [IAM permissions](https://docs.aws.amazon.com/service-authorization/latest/reference/list\_amazons3.html#amazons3-actions-as-permissions). If the principal lacks the appropriate permissions, the provider will fall back to tagging after creation and using the S3 tagging APIs [`PutBucketTagging`](https://docs.aws.amazon.com/AmazonS3/latest/API/API\_PutBucketTagging.html), [`DeleteBucketTagging`](https://docs.aws.amazon.com/AmazonS3/latest/API/API\_DeleteBucketTagging.html), and [`GetBucketTagging`](https://docs.aws.amazon.com/AmazonS3/latest/API/API\_GetBucketTagging.html) instead. With ABAC enabled, tag modifications may fail with the fall back behavior. See the [AWS documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/buckets-tagging-enable-abac.html) for additional details on enabling ABAC in general purpose buckets.
## Example Usage
### Private Bucket With Tags
```terraform
resource "aws\_s3\_bucket" "example" {
bucket = "my-tf-test-bucket"
tags = {
Name = "My bucket"
Environment = "Dev"
}
}
```
### Bucket In Account-Regional Namespace
```terraform
data "aws\_caller\_identity" "current" {}
data "aws\_region" "current" {}
resource "aws\_s3\_bucket" "example" {
bucket = format("my-tf-test-bucket-%s-%s-an", data.aws\_caller\_identity.current.account\_id, data.aws\_region.current.name)
bucket\_namespace = "account-regional"
}
```
## Argument Reference
This resource supports the following arguments:
\* `region` - (Optional) Region where this resource will be [managed](https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints). Defaults to the Region set in the [provider configuration](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference).
\* `bucket` - (Optional, Forces new resource) Name of the bucket. If omitted, Terraform will assign a random, unique name. Must be lowercase and less than or equal to 63 characters in length. A full list of bucket naming rules [may be found here](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html). The name must not be in the format `[bucket\_name]--[azid]--x-s3`. Use the [`aws\_s3\_directory\_bucket`](s3\_directory\_bucket.html) resource to manage S3 Express buckets.
\* `bucket\_namespace` - (Optional, Forces new resource) Namespace for the bucket. Determines bucket naming scope. Valid values: `account-regional`, `global`. Defaults to `global` (AWS).
\* `bucket\_prefix` - (Optional, Forces new resource) Creates a unique bucket name beginning with the specified prefix. Conflicts with `bucket`. Must be lowercase and less than or equal to 37 characters in length. A full list of bucket naming rules [may be found here](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html).
\* `force\_destroy` - (Optional, Default:`false`) Boolean that indicates all objects (including any [locked objects](https://docs.aws.amazon.com/AmazonS3/latest/dev/object-lock-overview.html)) should be deleted from the bucket \*when the bucket is destroyed\* so that the bucket can be destroyed without error. These objects are \*not\* recoverable. This only deletes objects when the bucket is destroyed, \*not\* when setting this parameter to `true`. Once this parameter is set to `true`, there must be a successful `terraform apply` run before a destroy is required to update this value in the resource state. Without a successful `terraform apply` after this parameter is set, this flag will have no effect. If setting this field in the same operation that would require replacing the bucket or destroying the bucket, this flag will not work. Additionally when importing a bucket, a successful `terraform apply` is required to set this value in state before it will take effect on a destroy operation.
\* `object\_lock\_enabled` - (Optional, Forces new resource) Indicates whether this bucket has an Object Lock configuration enabled. Valid values are `true` or `false`. This argument is not supported in all regions or partitions.
\* `tags` - (Optional) Map of tags to assign to the bucket. If configured with a provider [`default\_tags` configuration block](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#default\_tags-configuration-block) present, tags with matching keys will overwrite those defined at the provider-level.
The following arguments are deprecated, and will be removed in a future major version:
\* `acceleration\_status` - (Optional, \*\*Deprecated\*\*) Sets the accelerate configuration of an existing bucket. Can be `Enabled` or `Suspended`. Cannot be used in `cn-north-1` or `us-gov-west-1`. Terraform will only perform drift detection if a configuration value is provided.
Use the resource [`aws\_s3\_bucket\_accelerate\_configuration`](s3\_bucket\_accelerate\_configuration.html) instead.
\* `acl` - (Optional, \*\*Deprecated\*\*) The [canned ACL](https://docs.aws.amazon.com/AmazonS3/latest/dev/acl-overview.html#canned-acl) to apply. Valid values are `private`, `public-read`, `public-read-write`, `aws-exec-read`, `authenticated-read`, and `log-delivery-write`. Defaults to `private`. Conflicts with `grant`. Terraform will only perform drift detection if a configuration value is provided. Use the resource [`aws\_s3\_bucket\_acl`](s3\_bucket\_acl.html.markdown) instead.
\* `grant` - (Optional, \*\*Deprecated\*\*) An [ACL policy grant](https://docs.aws.amazon.com/AmazonS3/latest/dev/acl-overview.html#sample-acl). See [Grant](#grant) below for details. Conflicts with `acl`. Terraform will only perform drift detection if a configuration value is provided. Use the resource [`aws\_s3\_bucket\_acl`](s3\_bucket\_acl.html.markdown) instead.
\* `cors\_rule` - (Optional, \*\*Deprecated\*\*) Rule of [Cross-Origin Resource Sharing](https://docs.aws.amazon.com/AmazonS3/latest/dev/cors.html). See [CORS rule](#cors-rule) below for details. Terraform will only perform drift detection if a configuration value is provided. Use the resource [`aws\_s3\_bucket\_cors\_configuration`](s3\_bucket\_cors\_configuration.html.markdown) instead.
\* `lifecycle\_rule` - (Optional, \*\*Deprecated\*\*) Configuration of [object lifecycle management](http://docs.aws.amazon.com/AmazonS3/latest/dev/object-lifecycle-mgmt.html). See [Lifecycle Rule](#lifecycle-rule) below for details. Terraform will only perform drift detection if a configuration value is provided.
Use the resource [`aws\_s3\_bucket\_lifecycle\_configuration`](s3\_bucket\_lifecycle\_configuration.html) instead.
\* `logging` - (Optional, \*\*Deprecated\*\*) Configuration of [S3 bucket logging](https://docs.aws.amazon.com/AmazonS3/latest/UG/ManagingBucketLogging.html) parameters. See [Logging](#logging) below for details. Terraform will only perform drift detection if a configuration value is provided.
Use the resource [`aws\_s3\_bucket\_logging`](s3\_bucket\_logging.html.markdown) instead.
\* `object\_lock\_configuration` - (Optional, \*\*Deprecated\*\*) Configuration of [S3 object locking](https://docs.aws.amazon.com/AmazonS3/latest/dev/object-lock.html). See [Object Lock Configuration](#object-lock-configuration) below for details.
Terraform wil only perform drift detection if a configuration value is provided.
Use the `object\_lock\_enabled` parameter and the resource [`aws\_s3\_bucket\_object\_lock\_configuration`](s3\_bucket\_object\_lock\_configuration.html.markdown) instead.
\* `policy` - (Optional, \*\*Deprecated\*\*) Valid [bucket policy](https://docs.aws.amazon.com/AmazonS3/latest/dev/example-bucket-policies.html) JSON document. Note that if the policy document is not specific enough (but still valid), Terraform may view the policy as constantly changing in a `terraform plan`. In this case, please make sure you use the verbose/specific version of the policy. For more information about building AWS IAM policy documents with Terraform, see the [AWS IAM Policy Document Guide](https://learn.hashicorp.com/terraform/aws/iam-policy).
Terraform will only perform drift detection if a configuration value is provided.
Use the resource [`aws\_s3\_bucket\_policy`](s3\_bucket\_policy.html) instead.
\* `replication\_configuration` - (Optional, \*\*Deprecated\*\*) Configuration of [replication configuration](http://docs.aws.amazon.com/AmazonS3/latest/dev/crr.html). See [Replication Configuration](#replication-configuration) below for details. Terraform will only perform drift detection if a configuration value is provided.
Use the resource [`aws\_s3\_bucket\_replication\_configuration`](s3\_bucket\_replication\_configuration.html) instead.
\* `request\_payer` - (Optional, \*\*Deprecated\*\*) Specifies who should bear the cost of Amazon S3 data transfer.
Can be either `BucketOwner` or `Requester`. By default, the owner of the S3 bucket would incur the costs of any data transfer.
See [Requester Pays Buckets](http://docs.aws.amazon.com/AmazonS3/latest/dev/RequesterPaysBuckets.html) developer guide for more information.
Terraform will only perform drift detection if a configuration value is provided.
Use the resource [`aws\_s3\_bucket\_request\_payment\_configuration`](s3\_bucket\_request\_payment\_configuration.html) instead.
\* `server\_side\_encryption\_configuration` - (Optional, \*\*Deprecated\*\*) Configuration of [server-side encryption configuration](http://docs.aws.amazon.com/AmazonS3/latest/dev/bucket-encryption.html). See [Server Side Encryption Configuration](#server-side-encryption-configuration) below for details.
Terraform will only perform drift detection if a configuration value is provided.
Use the resource [`aws\_s3\_bucket\_server\_side\_encryption\_configuration`](s3\_bucket\_server\_side\_encryption\_configuration.html) instead.
\* `versioning` - (Optional, \*\*Deprecated\*\*) Configuration of the [S3 bucket versioning state](https://docs.aws.amazon.com/AmazonS3/latest/dev/Versioning.html). See [Versioning](#versioning) below for details. Terraform will only perform drift detection if a configuration value is provided. Use the resource [`aws\_s3\_bucket\_versioning`](s3\_bucket\_versioning.html.markdown) instead.
\* `website` - (Optional, \*\*Deprecated\*\*) Configuration of the [S3 bucket website](https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteHosting.html). See [Website](#website) below for details. Terraform will only perform drift detection if a configuration value is provided.
Use the resource [`aws\_s3\_bucket\_website\_configuration`](s3\_bucket\_website\_configuration.html.markdown) instead.
### CORS Rule
~> \*\*NOTE:\*\* Currently, changes to the `cors\_rule` configuration of \*existing\* resources cannot be automatically detected by Terraform. To manage changes of CORS rules to an S3 bucket, use the `aws\_s3\_bucket\_cors\_configuration` resource instead. If you use `cors\_rule` on an `aws\_s3\_bucket`, Terraform will assume management over the full set of CORS rules for the S3 bucket, treating additional CORS rules as drift. For this reason, `cors\_rule` cannot be mixed with the external `aws\_s3\_bucket\_cors\_configuration` resource for a given S3 bucket.
The `cors\_rule` configuration block supports the following arguments:
\* `allowed\_headers` - (Optional) List of headers allowed.
\* `allowed\_methods` - (Required) One or more HTTP methods that you allow the origin to execute. Can be `GET`, `PUT`, `POST`, `DELETE` or `HEAD`.
\* `allowed\_origins` - (Required) One or more origins you want customers to be able to access the bucket from.
\* `expose\_headers` - (Optional) One or more headers in the response that you want customers to be able to access from their applications (for example, from a JavaScript `XMLHttpRequest` object).
\* `max\_age\_seconds` - (Optional) Specifies time in seconds that browser can cache the response for a preflight request.
### Grant
~> \*\*NOTE:\*\* Currently, changes to the `grant` configuration of \*existing\* resources cannot be automatically detected by Terraform. To manage changes of ACL grants to an S3 bucket, use the `aws\_s3\_bucket\_acl` resource instead. If you use `grant` on an `aws\_s3\_bucket`, Terraform will assume management over the full set of ACL grants for the S3 bucket, treating additional ACL grants as drift. For this reason, `grant` cannot be mixed with the external `aws\_s3\_bucket\_acl` resource for a given S3 bucket.
The `grant` configuration block supports the following arguments:
\* `id` - (Optional) Canonical user id to grant for. Used only when `type` is `CanonicalUser`.
\* `type` - (Required) Type of grantee to apply for. Valid values are `CanonicalUser` and `Group`. `AmazonCustomerByEmail` is not supported.
\* `permissions` - (Required) List of permissions to apply for grantee. Valid values are `READ`, `WRITE`, `READ\_ACP`, `WRITE\_ACP`, `FULL\_CONTROL`.
\* `uri` - (Optional) Uri address to grant for. Used only when `type` is `Group`.
### Lifecycle Rule
~> \*\*NOTE:\*\* Currently, changes to the `lifecycle\_rule` configuration of \*existing\* resources cannot be automatically detected by Terraform. To manage changes of Lifecycle rules to an S3 bucket, use the `aws\_s3\_bucket\_lifecycle\_configuration` resource instead. If you use `lifecycle\_rule` on an `aws\_s3\_bucket`, Terraform will assume management over the full set of Lifecycle rules for the S3 bucket, treating additional Lifecycle rules as drift. For this reason, `lifecycle\_rule` cannot be mixed with the external `aws\_s3\_bucket\_lifecycle\_configuration` resource for a given S3 bucket.
~> \*\*NOTE:\*\* At least one of `abort\_incomplete\_multipart\_upload\_days`, `expiration`, `transition`, `noncurrent\_version\_expiration`, `noncurrent\_version\_transition` must be specified.
The `lifecycle\_rule` configuration block supports the following arguments:
\* `id` - (Optional) Unique identifier for the rule. Must be less than or equal to 255 characters in length.
\* `prefix` - (Optional) Object key prefix identifying one or more objects to which the rule applies.
\* `tags` - (Optional) Specifies object tags key and value.
\* `enabled` - (Required) Specifies lifecycle rule status.
\* `abort\_incomplete\_multipart\_upload\_days` (Optional) Specifies the number of days after initiating a multipart upload when the multipart upload must be completed.
\* `expiration` - (Optional) Specifies a period in the object's expire. See [Expiration](#expiration) below for details.
\* `transition` - (Optional) Specifies a period in the object's transitions. See [Transition](#transition) below for details.
\* `noncurrent\_version\_expiration` - (Optional) Specifies when noncurrent object versions expire. See [Noncurrent Version Expiration](#noncurrent-version-expiration) below for details.
\* `noncurrent\_version\_transition` - (Optional) Specifies when noncurrent object versions transitions. See [Noncurrent Version Transition](#noncurrent-version-transition) below for details.
### Expiration
The `expiration` configuration block supports the following arguments:
\* `date` - (Optional) Specifies the date after which you want the corresponding action to take effect.
\* `days` - (Optional) Specifies the number of days after object creation when the specific rule action takes effect.
\* `expired\_object\_delete\_marker` - (Optional) On a versioned bucket (versioning-enabled or versioning-suspended bucket), you can add this element in the lifecycle configuration to direct Amazon S3 to delete expired object delete markers. This cannot be specified with Days or Date in a Lifecycle Expiration Policy.
### Transition
The `transition` configuration block supports the following arguments:
\* `date` - (Optional) Specifies the date after which you want the corresponding action to take effect.
\* `days` - (Optional) Specifies the number of days after object creation when the specific rule action takes effect.
\* `storage\_class` - (Required) Specifies the Amazon S3 [storage class](https://docs.aws.amazon.com/AmazonS3/latest/API/API\_Transition.html#AmazonS3-Type-Transition-StorageClass) to which you want the object to transition.
### Noncurrent Version Expiration
The `noncurrent\_version\_expiration` configuration block supports the following arguments:
\* `days` - (Required) Specifies the number of days noncurrent object versions expire.
### Noncurrent Version Transition
The `noncurrent\_version\_transition` configuration supports the following arguments:
\* `days` - (Required) Specifies the number of days noncurrent object versions transition.
\* `storage\_class` - (Required) Specifies the Amazon S3 [storage class](https://docs.aws.amazon.com/AmazonS3/latest/API/API\_Transition.html#AmazonS3-Type-Transition-StorageClass) to which you want the object to transition.
### Logging
~> \*\*NOTE:\*\* Currently, changes to the `logging` configuration of \*existing\* resources cannot be automatically detected by Terraform. To manage changes of logging parameters to an S3 bucket, use the `aws\_s3\_bucket\_logging` resource instead. If you use `logging` on an `aws\_s3\_bucket`, Terraform will assume management over the full set of logging parameters for the S3 bucket, treating additional logging parameters as drift. For this reason, `logging` cannot be mixed with the external `aws\_s3\_bucket\_logging` resource for a given S3 bucket.
The `logging` configuration block supports the following arguments:
\* `target\_bucket` - (Required) Name of the bucket that will receive the log objects.
\* `target\_prefix` - (Optional) To specify a key prefix for log objects.
### Object Lock Configuration
~> \*\*NOTE:\*\* You can only \*\*enable\*\* S3 Object Lock for \*\*new\*\* buckets. If you need to \*\*enable\*\* S3 Object Lock for an \*\*existing\*\* bucket, please contact AWS Support.
When you create a bucket with S3 Object Lock enabled, Amazon S3 automatically enables versioning for the bucket.
Once you create a bucket with S3 Object Lock enabled, you can't disable Object Lock or suspend versioning for the bucket.
~> \*\*NOTE:\*\* Currently, changes to the `object\_lock\_configuration` configuration of \*existing\* resources cannot be automatically detected by Terraform. To manage changes of Object Lock settings to an S3 bucket, use the `aws\_s3\_bucket\_object\_lock\_configuration` resource instead. If you use `object\_lock\_configuration` on an `aws\_s3\_bucket`, Terraform will assume management over the full set of Object Lock configuration parameters for the S3 bucket, treating additional Object Lock configuration parameters as drift. For this reason, `object\_lock\_configuration` cannot be mixed with the external `aws\_s3\_bucket\_object\_lock\_configuration` resource for a given S3 bucket.
The `object\_lock\_configuration` configuration block supports the following arguments:
\* `object\_lock\_enabled` - (Optional, \*\*Deprecated\*\*) Indicates whether this bucket has an Object Lock configuration enabled. Valid value is `Enabled`. Use the top-level argument `object\_lock\_enabled` instead.
\* `rule` - (Optional) Object Lock rule in place for this bucket ([documented below](#rule)).
#### Rule
The `rule` configuration block supports the following argument:
\* `default\_retention` - (Required) Default retention period that you want to apply to new objects placed in this bucket ([documented below](#default-retention)).
#### Default Retention
The `default\_retention` configuration block supports the following arguments:
~> \*\*NOTE:\*\* Either `days` or `years` must be specified, but not both.
\* `mode` - (Required) Default Object Lock retention mode you want to apply to new objects placed in this bucket. Valid values are `GOVERNANCE` and `COMPLIANCE`.
\* `days` - (Optional) Number of days that you want to specify for the default retention period.
\* `years` - (Optional) Number of years that you want to specify for the default retention period.
### Replication Configuration
~> \*\*NOTE:\*\* Currently, changes to the `replication\_configuration` configuration of \*existing\* resources cannot be automatically detected by Terraform. To manage replication configuration changes to an S3 bucket, use the `aws\_s3\_bucket\_replication\_configuration` resource instead. If you use `replication\_configuration` on an `aws\_s3\_bucket`, Terraform will assume management over the full replication configuration for the S3 bucket, treating additional replication configuration rules as drift. For this reason, `replication\_configuration` cannot be mixed with the external `aws\_s3\_bucket\_replication\_configuration` resource for a given S3 bucket.
The `replication\_configuration` configuration block supports the following arguments:
\* `role` - (Required) ARN of the IAM role for Amazon S3 to assume when replicating the objects.
\* `rules` - (Required) Specifies the rules managing the replication ([documented below](#rules)).
#### Rules
The `rules` configuration block supports the following arguments:
~> \*\*NOTE:\*\* Amazon S3's latest version of the replication configuration is V2, which includes the `filter` attribute for replication rules.
With the `filter` attribute, you can specify object filters based on the object key prefix, tags, or both to scope the objects that the rule applies to.
Replication configuration V1 supports filtering based on only the `prefix` attribute. For backwards compatibility, Amazon S3 continues to support the V1 configuration.
\* `delete\_marker\_replication\_status` - (Optional) Whether delete markers are replicated. The only valid value is `Enabled`. To disable, omit this argument. This argument is only valid with V2 replication configurations (i.e., when `filter` is used).
\* `destination` - (Required) Specifies the destination for the rule ([documented below](#destination)).
\* `filter` - (Optional, Conflicts with `prefix`) Filter that identifies subset of objects to which the replication rule applies ([documented below](#filter)).
\* `id` - (Optional) Unique identifier for the rule. Must be less than or equal to 255 characters in length.
\* `prefix` - (Optional, Conflicts with `filter`) Object keyname prefix identifying one or more objects to which the rule applies. Must be less than or equal to 1024 characters in length.
\* `priority` - (Optional) Priority associated with the rule. Priority should only be set if `filter` is configured. If not provided, defaults to `0`. Priority must be unique between multiple rules.
\* `source\_selection\_criteria` - (Optional) Specifies special object selection criteria ([documented below](#source-selection-criteria)).
\* `status` - (Required) Status of the rule. Either `Enabled` or `Disabled`. The rule is ignored if status is not Enabled.
#### Filter
The `filter` configuration block supports the following arguments:
\* `prefix` - (Optional) Object keyname prefix that identifies subset of objects to which the rule applies. Must be less than or equal to 1024 characters in length.
\* `tags` - (Optional) A map of tags that identifies subset of objects to which the rule applies.
The rule applies only to objects having all the tags in its tagset.
#### Destination
~> \*\*NOTE:\*\* Replication to multiple destination buckets requires that `priority` is specified in the `rules` object. If the corresponding rule requires no filter, an empty configuration block `filter {}` must be specified.
The `destination` configuration block supports the following arguments:
\* `bucket` - (Required) ARN of the S3 bucket where you want Amazon S3 to store replicas of the object identified by the rule.
\* `storage\_class` - (Optional) The [storage class](https://docs.aws.amazon.com/AmazonS3/latest/API/API\_Destination.html#AmazonS3-Type-Destination-StorageClass) used to store the object. By default, Amazon S3 uses the storage class of the source object to create the object replica.
\* `replica\_kms\_key\_id` - (Optional) Destination KMS encryption key ARN for SSE-KMS replication. Must be used in conjunction with
`sse\_kms\_encrypted\_objects` source selection criteria.
\* `access\_control\_translation` - (Optional) Specifies the overrides to use for object owners on replication ([documented below](#access\_control\_translation-block)). Must be used in conjunction with `account\_id` owner override configuration.
\* `account\_id` - (Optional) Account ID to use for overriding the object owner on replication. Must be used in conjunction with `access\_control\_translation` override configuration.
\* `replication\_time` - (Optional) Enables S3 Replication Time Control (S3 RTC) ([documented below](#replication-time)).
\* `metrics` - (Optional) Enables replication metrics (required for S3 RTC) ([documented below](#metrics)).
#### `access\_control\_translation` Block
The `access\_control\_translation` configuration block supports the following arguments:
\* `owner` - (Required) Specifies the replica ownership. For default and valid values, see [PUT bucket replication](https://docs.aws.amazon.com/AmazonS3/latest/API/API\_PutBucketReplication.html) in the Amazon S3 API Reference. The only valid value is `Destination`.
#### Replication Time
The `replication\_time` configuration block supports the following arguments:
\* `status` - (Optional) Status of RTC. Either `Enabled` or `Disabled`.
\* `minutes` - (Optional) Threshold within which objects are to be replicated. The only valid value is `15`.
#### Metrics
The `metrics` configuration block supports the following arguments:
\* `status` - (Optional) Status of replication metrics. Either `Enabled` or `Disabled`.
\* `minutes` - (Optional) Threshold within which objects are to be replicated. The only valid value is `15`.
#### Source Selection Criteria
The `source\_selection\_criteria` configuration block supports the following argument:
\* `sse\_kms\_encrypted\_objects` - (Optional) Match SSE-KMS encrypted objects ([documented below](#sse-kms-encrypted-objects)). If specified, `replica\_kms\_key\_id`
in `destination` must be specified as well.
#### SSE KMS Encrypted Objects
The `sse\_kms\_encrypted\_objects` configuration block supports the following argument:
\* `enabled` - (Required) Boolean which indicates if this criteria is enabled.
### Server Side Encryption Configuration
~> \*\*NOTE:\*\* Currently, changes to the `server\_side\_encryption\_configuration` configuration of \*existing\* resources cannot be automatically detected by Terraform. To manage changes in encryption of an S3 bucket, use the `aws\_s3\_bucket\_server\_side\_encryption\_configuration` resource instead. If you use `server\_side\_encryption\_configuration` on an `aws\_s3\_bucket`, Terraform will assume management over the encryption configuration for the S3 bucket, treating additional encryption changes as drift. For this reason, `server\_side\_encryption\_configuration` cannot be mixed with the external `aws\_s3\_bucket\_server\_side\_encryption\_configuration` resource for a given S3 bucket.
~> \*\*NOTE:\*\* [Starting in April 2026](https://docs.aws.amazon.com/AmazonS3/latest/userguide/default-s3-c-encryption-setting-faq.html), Amazon S3 will automatically block server-side encryption with customer-provided keys (SSE-C) for all new buckets. The `blocked\_encryption\_types` argument is not available in this deprecated configuration block. Use the [`aws\_s3\_bucket\_server\_side\_encryption\_configuration`](/docs/providers/aws/r/s3\_bucket\_server\_side\_encryption\_configuration.html) resource to manage this behavior for specific buckets.
The `server\_side\_encryption\_configuration` configuration block supports the following argument:
\* `rule` - (Required) Single object for server-side encryption by default configuration. (documented below)
The `rule` configuration block supports the following arguments:
\* `apply\_server\_side\_encryption\_by\_default` - (Required) Single object for setting server-side encryption by default. (documented below)
\* `bucket\_key\_enabled` - (Optional) Whether or not to use [Amazon S3 Bucket Keys](https://docs.aws.amazon.com/AmazonS3/latest/dev/bucket-key.html) for SSE-KMS.
The `apply\_server\_side\_encryption\_by\_default` configuration block supports the following arguments:
\* `sse\_algorithm` - (Required) Server-side encryption algorithm to use. Valid values are `AES256` and `aws:kms`
\* `kms\_master\_key\_id` - (Optional) AWS KMS master key ID used for the SSE-KMS encryption. This can only be used when you set the value of `sse\_algorithm` as `aws:kms`. The default `aws/s3` AWS KMS master key is used if this element is absent while the `sse\_algorithm` is `aws:kms`.
### Versioning
~> \*\*NOTE:\*\* Currently, changes to the `versioning` configuration of \*existing\* resources cannot be automatically detected by Terraform. To manage changes of versioning state to an S3 bucket, use the `aws\_s3\_bucket\_versioning` resource instead. If you use `versioning` on an `aws\_s3\_bucket`, Terraform will assume management over the versioning state of the S3 bucket, treating additional versioning state changes as drift. For this reason, `versioning` cannot be mixed with the external `aws\_s3\_bucket\_versioning` resource for a given S3 bucket.
The `versioning` configuration block supports the following arguments:
\* `enabled` - (Optional) Enable versioning. Once you version-enable a bucket, it can never return to an unversioned state. You can, however, suspend versioning on that bucket.
\* `mfa\_delete` - (Optional) Enable MFA delete for either `Change the versioning state of your bucket` or `Permanently delete an object version`. Default is `false`. This cannot be used to toggle this setting but is available to allow managed buckets to reflect the state in AWS
### Website
~> \*\*NOTE:\*\* Currently, changes to the `website` configuration of \*existing\* resources cannot be automatically detected by Terraform. To manage changes to the website configuration of an S3 bucket, use the `aws\_s3\_bucket\_website\_configuration` resource instead. If you use `website` on an `aws\_s3\_bucket`, Terraform will assume management over the configuration of the website of the S3 bucket, treating additional website configuration changes as drift. For this reason, `website` cannot be mixed with the external `aws\_s3\_bucket\_website\_configuration` resource for a given S3 bucket.
The `website` configuration block supports the following arguments:
\* `index\_document` - (Required, unless using `redirect\_all\_requests\_to`) Amazon S3 returns this index document when requests are made to the root domain or any of the subfolders.
\* `error\_document` - (Optional) Absolute path to the document to return in case of a 4XX error.
\* `redirect\_all\_requests\_to` - (Optional) Hostname to redirect all website requests for this bucket to. Hostname can optionally be prefixed with a protocol (`http://` or `https://`) to use when redirecting requests. The default is the protocol that is used in the original request.
\* `routing\_rules` - (Optional) JSON array containing [routing rules](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-websiteconfiguration-routingrules.html)
describing redirect behavior and when redirects are applied.
## Attribute Reference
This resource exports the following attributes in addition to the arguments above:
\* `id` - Name of the bucket.
\* `arn` - ARN of the bucket. Will be of format `arn:aws:s3:::bucketname`.
\* `bucket\_domain\_name` - Bucket domain name. Will be of format `bucketname.s3.amazonaws.com`.
\* `bucket\_region` - AWS region this bucket resides in.
\* `bucket\_regional\_domain\_name` - The bucket region-specific domain name. The bucket domain name including the region name. Please refer to the [S3 endpoints reference](https://docs.aws.amazon.com/general/latest/gr/s3.html#s3\_region) for format. Note: AWS CloudFront allows specifying an S3 region-specific endpoint when creating an S3 origin. This will prevent redirect issues from CloudFront to the S3 Origin URL. For more information, see the [Virtual Hosted-Style Requests for Other Regions](https://docs.aws.amazon.com/AmazonS3/latest/userguide/VirtualHosting.html#deprecated-global-endpoint) section in the AWS S3 User Guide.
\* `hosted\_zone\_id` - [Route 53 Hosted Zone ID](https://docs.aws.amazon.com/general/latest/gr/rande.html#s3\_website\_region\_endpoints) for this bucket's region.
\* `tags\_all` - Map of tags assigned to the resource, including those inherited from the provider [`default\_tags` configuration block](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#default\_tags-configuration-block).
\* `website\_endpoint` - (\*\*Deprecated\*\*) Website endpoint, if the bucket is configured with a website. If not, this will be an empty string. Use the resource [`aws\_s3\_bucket\_website\_configuration`](s3\_bucket\_website\_configuration.html.markdown) instead.
\* `website\_domain` - (\*\*Deprecated\*\*) Domain of the website endpoint, if the bucket is configured with a website. If not, this will be an empty string. This is used to create Route 53 alias records. Use the resource [`aws\_s3\_bucket\_website\_configuration`](s3\_bucket\_website\_configuration.html.markdown) instead.
## Timeouts
[Configuration options](https://developer.hashicorp.com/terraform/language/resources/syntax#operation-timeouts):
- `create` - (Default `20m`)
- `read` - (Default `20m`)
- `update` - (Default `20m`)
- `delete` - (Default `60m`)
## Import
In Terraform v1.12.0 and later, the [`import` block](https://developer.hashicorp.com/terraform/language/import) can be used with the `identity` attribute. For example:
```terraform
import {
to = aws\_s3\_bucket.example
identity = {
bucket = "bucket-name"
}
}
resource "aws\_s3\_bucket" "example" {
### Configuration omitted for brevity ###
}
```
### Identity Schema
#### Required
\* `bucket` (String) Name of the S3 bucket.
#### Optional
\* `account\_id` (String) AWS Account where this resource is managed.
\* `region` (String) Region where this resource is managed.
In Terraform v1.5.0 and later, use an [`import` block](https://developer.hashicorp.com/terraform/language/import) to import S3 bucket using the `bucket`. For example:
```terraform
import {
to = aws\_s3\_bucket.example
id = "bucket-name"
}
```
Using `terraform import`, import S3 bucket using the `bucket`. For example:
```console
% terraform import aws\_s3\_bucket.example bucket-name
```