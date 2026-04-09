Welcome to the AWS Security Token Service API Reference - AWS Security Token Service 

Welcome to the AWS Security Token Service API Reference - AWS Security Token Service
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
"name" : "AWS Security Token Service",
"item" : "https://docs.aws.amazon.com/iam/index.html"
},
{
"@type" : "ListItem",
"position" : 3,
"name" : "API Reference",
"item" : "https://docs.aws.amazon.com/STS/latest/APIReference"
},
{
"@type" : "ListItem",
"position" : 4,
"name" : "Welcome to the AWS Security Token Service API Reference",
"item" : "https://docs.aws.amazon.com/STS/latest/APIReference/welcome.html"
}
]
}

[Documentation](/index.html)[AWS Security Token Service](/iam/index.html)[API Reference](welcome.html)

[Endpoints](#sts-endpoints)[Recording API requests](#logging-api-calls-cloudtrail)

# Welcome to the AWS Security Token Service API Reference

AWS provides AWS Security Token Service (AWS STS) as a web service that enables you to request temporary,
limited-privilege credentials for users. This guide describes the AWS STS API. For more
information, see [Temporary Security Credentials](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp.html)
in the *IAM User Guide*.

###### Note

As an alternative to using the API, you can use one of the AWS SDKs, which consist of
libraries and sample code for various programming languages and platforms such as Java,
Ruby, .NET, iOS, Android, and others. The SDKs provide a convenient way to create
programmatic access to AWS STS. For example, the SDKs can cryptographically sign requests,
manage errors, and retry requests automatically. For information about the AWS SDKs, see
[Tools to Build on AWS](https://aws.amazon.com/tools/).

For information about setting up signatures and authorization through the API, see [Signing AWS
API Requests](https://docs.aws.amazon.com/general/latest/gr/signing_aws_api_requests.html) in the *Amazon Web Services General Reference*. For general information
about the Query API, see [Making Query Requests](https://docs.aws.amazon.com/IAM/latest/UserGuide/IAM_UsingQueryAPI.html) in the
*IAM User Guide*. For information about using security tokens with
other AWS products, see [AWS Services
That Work with IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-services-that-work-with-iam.html) in the *IAM User Guide*.

## Endpoints

The AWS Security Token Service (AWS STS) is available as a global service endpoint at
`https://sts.amazonaws.com` and as Regional service endpoints. In Regions
that are [enabled by default](https://docs.aws.amazon.com/accounts/latest/reference/manage-acct-regions.html),
requests to the AWS STS global endpoint are automatically served in the same Region where the
request originates. In opt-in Regions, requests to the AWS STS global endpoint are served by
a single AWS Region, US East (N. Virginia). For more information, see [AWS STS Regions and
endpoints](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_region-endpoints.html) in the *IAM User Guide*.

AWS recommends using Regional AWS STS endpoints instead of the global endpoint to reduce
latency, built-in redundancy, and increase session token validity. For more information,
see [Managing AWS STS in an
AWS Region](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_enable-regions.html) in the *IAM User Guide*.

Most AWS Regions enable operations in all AWS services by default. These Regions
automatically activate for use with AWS STS. Some Regions, such as Asia Pacific (Hong Kong), must
be manually enabled. To learn more about enabling and disabling AWS Regions, see [Managing
AWS Regions](https://docs.aws.amazon.com/general/latest/gr/rande-manage.html) in the *Amazon Web Services General Reference*. When you enable these
AWS Regions, they are automatically activated for use with AWS STS. You cannot activate the
AWS STS endpoint for a disabled Region. Tokens that are valid in all AWS Regions include
more characters than tokens that are valid in Regions enabled by default. Changing this
setting might affect existing systems where you temporarily store tokens. For more
information, see [Managing Global Endpoint Session Tokens](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_enable-regions.html#sts-regions-manage-tokens) in the
*IAM User Guide*.

After you activate a Region for use with AWS STS, you can direct AWS STS API calls to that
Region. AWS STS recommends you provide both the Region and endpoint when you send calls to a
Regional endpoint. You can provide the Region alone for manually enabled Regions, such as
Asia Pacific (Hong Kong). In this case, you direct the calls to the AWS STS Regional endpoint.
However, if you provide the Region alone for Regions enabled by default, AWS STS directs the
calls to the global endpoint of `https://sts.amazonaws.com`.

To view the list of AWS STS endpoints and if they are active by default, see [Writing Code to Use AWS STS Regions](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_enable-regions.html#id_credentials_temp_enable-regions_writing_code) in the
*IAM User Guide*.

## Recording API requests

AWS STS supports AWS CloudTrail, a service that records AWS calls for your AWS account and
delivers log files to an Amazon S3 bucket. By using information collected by CloudTrail, you can
determine the requests successfully sent to AWS STS, as well as who sent the request, and
when it was sent. For more information about CloudTrail, including how to enable it and find your
log files, see [Logging IAM and AWS STS API calls
with AWS CloudTrail](https://docs.aws.amazon.com/IAM/latest/UserGuide/cloudtrail-integration.html) in the *IAM User Guide* and the
[AWS CloudTrail User Guide](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/).

**Javascript is disabled or is unavailable in your browser.**

To use the Amazon Web Services Documentation, Javascript must be enabled. Please refer to your browser's Help pages for instructions.

[Document Conventions](/general/latest/gr/docconventions.html)

Actions

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.