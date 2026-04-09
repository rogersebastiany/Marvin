What is IAM? - AWS Identity and Access Management 

What is IAM? - AWS Identity and Access Management
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
"name" : "AWS Identity and Access Management",
"item" : "https://docs.aws.amazon.com/iam/index.html"
},
{
"@type" : "ListItem",
"position" : 3,
"name" : "User Guide",
"item" : "https://docs.aws.amazon.com/IAM/latest/UserGuide"
},
{
"@type" : "ListItem",
"position" : 4,
"name" : "What is IAM?",
"item" : "https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html"
}
]
}

[Documentation](/index.html)[AWS Identity and Access Management](/iam/index.html)[User Guide](introduction.html)

# What is IAM?

AWS Identity and Access Management (IAM) is a web service that helps you securely control access to AWS
resources. With IAM, you can manage permissions that control which AWS resources users can
access. You use IAM to control who is authenticated (signed in) and authorized (has
permissions) to use resources. IAM provides the infrastructure necessary to control
authentication and authorization for your AWS accounts.

**Identities**

When you create an AWS account, you begin with one sign-in identity called the AWS account *root user* that has complete access to all AWS services and resources. We strongly recommend that you don't use the root user for everyday tasks. For tasks that require root user credentials, see [Tasks that require root user credentials](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_root-user.html#root-user-tasks) in the *IAM User Guide*.

Use IAM to set up other identities in addition to your
root user, such as administrators, analysts, and developers, and grant them access to the resources
they need to succeed in their tasks.

**Access management**

After a user is set up in IAM, they use their sign-in credentials to authenticate with
AWS. Authentication is provided by matching the sign-in credentials to a principal (an
IAM user, AWS STS federated principal, IAM role, or application) trusted by the AWS account. Next, a
request is made to grant the principal access to resources. Access is granted in response to an
authorization request if the user has been given permission to the resource. For example, when
you first sign in to the console and are on the console Home page, you aren't accessing a
specific service. When you select a service, the request for authorization is sent to that
service and it looks to see if your identity is on the list of authorized users, what policies
are being enforced to control the level of access granted, and any other policies that might be
in effect. Authorization requests can be made by principals within your AWS account or from
another AWS account that you trust.

Once authorized, the principal can take action or perform operations on resources in your
AWS account. For example, the principal could launch a new Amazon Elastic Compute Cloud instance, modify
IAM group membership, or delete Amazon Simple Storage Service buckets.

###### Tip

AWS Training and Certification provides a 10-minute video introduction to IAM:

[Introduction to
AWS Identity and Access Management](https://www.aws.training/learningobject/video?id=16448).

**Service availability**

IAM, like many other AWS services, is [eventually consistent](https://wikipedia.org/wiki/Eventual_consistency).
IAM achieves high availability by replicating data across multiple servers within
Amazon's data centers around the world. If a request to change some data is successful,
the change is committed and safely stored. However, the change must be replicated across
IAM, which can take some time. Such changes include creating or updating users,
groups, roles, or policies. We recommend that you do not include such IAM changes in the
critical, high-availability code paths of your application. Instead, make IAM changes in
a separate initialization or setup routine that you run less frequently. Also, be sure
to verify that the changes have been propagated before production workflows depend on
them. For more information, see [Changes that I make are not always immediately visible](./troubleshoot.html#troubleshoot_general_eventual-consistency).

**Service cost information**

AWS Identity and Access Management (IAM), AWS IAM Identity Center and AWS Security Token Service (AWS STS) are features of your AWS account offered at no additional charge. You are
charged only when you access other AWS services using your IAM users or AWS STS temporary security credentials.

IAM Access Analyzer external access analysis is offered at no additional charge. However, you will incur charges for unused access analysis and customer policy checks. For a complete list of charges and prices for IAM Access Analyzer, see [IAM Access Analyzer pricing](https://aws.amazon.com/iam/access-analyzer/pricing).

For information about the pricing of other AWS products, see the [Amazon Web Services pricing
page](https://aws.amazon.com/pricing/).

**Integration with other AWS services**

IAM is integrated with many AWS services. For a list of AWS services that work with IAM and the IAM features the services support, see [AWS services that work with IAM](./reference_aws-services-that-work-with-iam.html).

**Javascript is disabled or is unavailable in your browser.**

To use the Amazon Web Services Documentation, Javascript must be enabled. Please refer to your browser's Help pages for instructions.

[Document Conventions](/general/latest/gr/docconventions.html)

Why should I use IAM?

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.