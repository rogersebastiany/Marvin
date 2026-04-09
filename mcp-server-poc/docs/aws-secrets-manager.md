What is AWS Secrets Manager? - AWS Secrets Manager 

What is AWS Secrets Manager? - AWS Secrets Manager
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
"name" : "AWS Secrets Manager",
"item" : "https://docs.aws.amazon.com/secretsmanager/index.html"
},
{
"@type" : "ListItem",
"position" : 3,
"name" : "User Guide",
"item" : "https://docs.aws.amazon.com/secretsmanager/latest/userguide"
},
{
"@type" : "ListItem",
"position" : 4,
"name" : "What is AWS Secrets Manager?",
"item" : "https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html"
}
]
}

[Documentation](/index.html)[AWS Secrets Manager](/secretsmanager/index.html)[User Guide](intro.html)

[Get started with Secrets Manager](#get-started)[Compliance with standards](#compliance)[Pricing](#asm_pricing)

# What is AWS Secrets Manager?

AWS Secrets Manager helps you manage, retrieve, and rotate database credentials, application credentials, OAuth tokens, API keys, and other secrets throughout their lifecycles. Many AWS services store and use secrets in Secrets Manager.

Secrets Manager helps you improve your security posture, because you no longer need hard-coded credentials in application source code. Storing the credentials in Secrets Manager helps avoid possible compromise by anyone who can inspect your application or the components. You replace hard-coded credentials with a runtime call to the Secrets Manager service to retrieve credentials dynamically when you need them.

With Secrets Manager, you can configure an automatic rotation schedule for your secrets. This enables you to replace long-term secrets with short-term ones, significantly reducing the risk of compromise. Since the credentials are no longer stored with the application, rotating credentials no longer requires updating your applications and deploying changes to application clients.

For other types of secrets you might have in your organization:

* AWS credentials – We recommend [AWS Identity and Access Management](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html).
* Encryption keys – We recommend [AWS Key Management Service](https://docs.aws.amazon.com/kms/latest/developerguide/overview.html).
* SSH keys – We recommend [Amazon EC2 Instance Connect](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Connect-using-EC2-Instance-Connect.html).
* Private keys and certificates – We recommend [AWS Certificate Manager](https://docs.aws.amazon.com/acm/latest/userguide/acm-overview.html).

## Get started with Secrets Manager

If you are new to Secrets Manager, start with one of the following tutorials:

* [Move hardcoded secrets to AWS Secrets Manager](./hardcoded.html)
* [Move hardcoded database credentials to AWS Secrets Manager](./hardcoded-db-creds.html)
* [Set up alternating users rotation for AWS Secrets Manager](./tutorials_rotation-alternating.html)
* [Set up single user rotation for AWS Secrets Manager](./tutorials_rotation-single.html)

Other tasks you can do with secrets:

* [Manage secrets](./managing-secrets.html)
* [Control access to your secrets](./auth-and-access.html)
* [Get secrets](./retrieving-secrets.html)
* [Rotate secrets](./rotating-secrets.html)
* [Monitor secrets](./monitoring.html)
* [Monitor secrets for compliance](./configuring-awsconfig-rules.html)
* [Create secrets in AWS CloudFormation](./cloudformation.html)

## Compliance with standards

AWS Secrets Manager has undergone auditing for the multiple standards and can be part of your
solution when you need to obtain compliance certification. For more information, see [Compliance validation for AWS Secrets Manager](./secretsmanager-compliance.html).

## Pricing

When you use Secrets Manager, you pay only for what you use, with no minimum or setup fees. There is
no charge for secrets that are marked for deletion. For the current complete pricing list, see
[AWS Secrets Manager Pricing](https://aws.amazon.com/secrets-manager/pricing). To monitor
your costs, see [Monitor Secrets Manager costs](./monitor-secretsmanager-costs.html).

You can use the AWS managed key `aws/secretsmanager` that Secrets Manager creates to
encrypt your secrets for free. If you create your own KMS keys to encrypt your secrets,
AWS charges you at the current AWS KMS rate. For more information, see [AWS Key Management Service Pricing](https://aws.amazon.com/kms/pricing).

When you turn on automatic rotation (except [managed
rotation](./rotate-secrets_managed.html)), Secrets Manager uses an AWS Lambda function to rotate the secret, and you are charged
for the rotation function at the current Lambda rate. For more information, see [AWS Lambda Pricing](https://aws.amazon.com//lambda/pricing/).

If you enable AWS CloudTrail on your account, you can obtain logs of the API calls that Secrets Manager
sends out. Secrets Manager logs all events as management events. AWS CloudTrail stores the first copy of all
management events for free. However, you can incur charges for Amazon S3 for log storage and for
Amazon SNS if you enable notification. Also, if you set up additional trails, the additional copies
of management events can incur costs. For more information, see [AWS CloudTrail pricing](https://aws.amazon.com/cloudtrail/pricing).

You can use cost allocation tags in Secrets Manager to track and categorize expenses associated with
specific secrets or projects. For more information, see [Tagging secrets in AWS Secrets Manager](./managing-secrets_tagging.html) in this guide and [Using AWS cost allocation
tags](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html) in the AWS Billing User Guide.

**Javascript is disabled or is unavailable in your browser.**

To use the Amazon Web Services Documentation, Javascript must be enabled. Please refer to your browser's Help pages for instructions.

[Document Conventions](/general/latest/gr/docconventions.html)

Access Secrets Manager

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.