AWS Key Management Service - AWS Key Management Service 

AWS Key Management Service - AWS Key Management Service
{
"@context" : "https://schema.org",
"@type" : "BreadcrumbList",
"itemListElement" : [
{
"@type" : "ListItem",
"position" : 1,
"name" : "AWS",
"item" : "https://aws.amazon.com"
},
{
"@type" : "ListItem",
"position" : 2,
"name" : "AWS KMS",
"item" : "https://docs.aws.amazon.com/kms/index.html"
},
{
"@type" : "ListItem",
"position" : 3,
"name" : "Developer Guide",
"item" : "https://docs.aws.amazon.com/kms/latest/developerguide"
},
{
"@type" : "ListItem",
"position" : 4,
"name" : "AWS Key Management Service",
"item" : "https://docs.aws.amazon.com/kms/latest/developerguide/overview.html"
}
]
}

[Documentation](/index.html)[AWS KMS](/kms/index.html)[Developer Guide](overview.html)

[Why use AWS KMS?](#service-kms-why)[AWS KMS in AWS Regions](#kms_regions)[AWS KMS pricing](#pricing)[AWS KMS service level agreement](#kms_service_levels)

# AWS Key Management Service

AWS Key Management Service (AWS KMS) is an AWS managed service that makes it easy for you to create and
control the keys used to encrypt and sign your data. The AWS KMS keys that you
create in AWS KMS are protected by [FIPS 140-3 Security Level 3
validated hardware security modules (HSM)](https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/4884). They never leave AWS KMS unencrypted. To use
or manage your KMS keys, you interact with AWS KMS.

## Why use AWS KMS?

When you encrypt data, you need to protect your encryption key. If you encrypt your key,
you need to protect its encryption key. Eventually, you must protect the highest level
encryption key (known as a *root key*) in the hierarchy that
protects your data. That's where AWS KMS comes in.

AWS KMS protects your root keys. KMS keys are created, managed, used, and deleted
entirely within AWS KMS. They never leave the service unencrypted. To use or manage your
KMS keys, you call AWS KMS.

Additionally, you can create and manage [key
policies](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html) in AWS KMS, ensuring that only trusted users have access to
KMS keys.

## AWS KMS in AWS Regions

The AWS Regions in which AWS KMS is supported are listed in [AWS Key Management Service Endpoints and Quotas](https://docs.aws.amazon.com/general/latest/gr/kms.html). If an
AWS KMS feature is not supported in an AWS Region that AWS KMS supports, the regional difference
is described in the topic about the feature.

## AWS KMS pricing

As with other AWS products, using AWS KMS does not require contracts or minimum purchases.
For more information about AWS KMS pricing, see [AWS Key Management Service
Pricing](https://aws.amazon.com/kms/pricing/).

## AWS KMS service level agreement

AWS Key Management Service is backed by a [service level
agreement](https://aws.amazon.com/kms/sla/) that defines our service availability policy.

**Javascript is disabled or is unavailable in your browser.**

To use the Amazon Web Services Documentation, Javascript must be enabled. Please refer to your browser's Help pages for instructions.

[Document Conventions](/general/latest/gr/docconventions.html)

Accessing AWS Key Management Service

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.