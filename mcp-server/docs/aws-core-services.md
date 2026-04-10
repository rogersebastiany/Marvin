# AWS Core Services


---

## 1. What is IAM?

What is IAM? - AWS Identity and Access Management

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

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.

---

## 2. AWS Key Management Service

AWS Key Management Service - AWS Key Management Service

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

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.

---

## 3. What is Amazon Cognito?

What is Amazon Cognito? - Amazon Cognito

# What is Amazon Cognito?

Amazon Cognito is an identity platform for web and mobile apps. It’s a user directory, an
authentication server, and an authorization service for OAuth 2.0 access tokens and AWS
credentials. With Amazon Cognito, you can authenticate and authorize users from the built-in user
directory, from your enterprise directory, and from consumer identity providers like Google and
Facebook.

###### Topics

* [User pools](#what-is-amazon-cognito-user-pools)
* [Identity pools](#what-is-amazon-cognito-identity-pools)
* [Features of Amazon Cognito](#what-is-amazon-cognito-features)
* [Amazon Cognito user pools and identity pools comparison](#what-is-amazon-cognito-features-comparison)
* [Getting started with Amazon Cognito](#getting-started-overview)
* [Regional availability](#getting-started-regional-availability)
* [Pricing for Amazon Cognito](#pricing-for-amazon-cognito)
* [Common Amazon Cognito terms and concepts](./cognito-terms.html)
* [Getting started with AWS](./cognito-getting-started-account-iam.html)

The two components that follow make up Amazon Cognito. They operate independently or in tandem, based
on your access needs for your users.

## User pools

Create a user pool when you want to authenticate and authorize users to your app or API.
User pools are a user directory with both self-service and administrator-driven user creation,
management, and authentication. Your user pool can be an independent directory and OIDC
identity provider (IdP), and an intermediate service provider (SP) to third-party providers of
workforce and customer identities. You can provide single sign-on (SSO) in your app for your
organization's workforce identities in SAML 2.0 and OIDC IdPs with user pools. You can also
provide SSO in your app for your organization's customer identities in the public OAuth 2.0
identity stores Amazon, Google, Apple and Facebook. For more information about customer
identity and access management (CIAM), see [What is CIAM?](https://aws.amazon.com/what-is/ciam/).

User pools don’t require integration with an identity pool. From a user pool, you can
issue authenticated JSON web tokens (JWTs) directly to an app, a web server, or an API.

## Identity pools

Set up an Amazon Cognito identity pool when you want to authorize authenticated or anonymous users
to access your AWS resources. An identity pool issues AWS credentials for your app to
serve resources to users. You can authenticate users with a trusted identity provider, like a
user pool or a SAML 2.0 service. It can also optionally issue credentials for guest users.
Identity pools use both role-based and attribute-based access control to manage your users’
authorization to access your AWS resources.

Identity pools don’t require integration with a user pool. An identity pool can accept
authenticated claims directly from both workforce and consumer identity providers.

**An Amazon Cognito user pool and identity pool used together**

In the diagram that begins this topic, you use Amazon Cognito to authenticate your user and then
grant them access to an AWS service.

1. Your app user signs in through a user pool and receives OAuth 2.0 tokens.
2. Your app exchanges a user pool token with an identity pool for temporary AWS
   credentials that you can use with AWS APIs and the AWS Command Line Interface (AWS CLI).
3. Your app assigns the credentials session to your user, and delivers authorized access
   to AWS services like Amazon S3 and Amazon DynamoDB.

For more examples that use identity pools and user pools, see [Common Amazon Cognito scenarios](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-scenarios.html).

In Amazon Cognito, the *security of the cloud* obligation of the
[shared
responsibility model](https://aws.amazon.com/compliance/shared-responsibility-model/) is compliant with SOC 1-3, PCI DSS, ISO 27001, and is HIPAA-BAA
eligible. You can design your *security in the cloud* in
Amazon Cognito to be compliant with SOC1-3, ISO 27001, and HIPAA-BAA, but not PCI DSS. For
more information, see [AWS
services in scope](http://aws.amazon.com/compliance/services-in-scope/). See also [Regional data considerations](https://docs.aws.amazon.com/cognito/latest/developerguide/security-cognito-regional-data-considerations.html).

## Features of Amazon Cognito

### User pools

An Amazon Cognito user pool is a user directory. With a user pool, your users can sign in to your
web or mobile app through Amazon Cognito, or federate through a third-party IdP. Federated and local
users have a user profile in your user pool.

Local users are those who signed up or you created directly in your user pool. You can
manage and customize these user profiles in the AWS Management Console, an AWS SDK, or the
AWS Command Line Interface (AWS CLI).

Amazon Cognito user pools accept tokens and assertions from third-party IdPs, and collect the user
attributes into a JWT that it issues to your app. You can standardize your app on one set of
JWTs while Amazon Cognito handles the interactions with IdPs, mapping their claims to a central token
format.

An Amazon Cognito user pool can be a standalone IdP. Amazon Cognito draws from the OpenID Connect (OIDC)
standard to generate JWTs for authentication and authorization. When you sign in local
users, your user pool is authoritative for those users. You have access to the following
features when you authenticate local users.

* Implement your own web front-end that calls the Amazon Cognito user pools API to authenticate,
  authorize, and manage your users.
* Set up multi-factor authentication (MFA) for your users. Amazon Cognito supports time-based
  one-time password (TOTP) and SMS message MFA.
* Secure against access from user accounts that are under malicious control.
* Create your own custom multi-step authentication flows.
* Look up users in another directory and migrate them to Amazon Cognito.

An Amazon Cognito user pool can also fulfill a dual role as a service provider (SP) to your IdPs,
and an IdP to your app. Amazon Cognito user pools can connect to consumer IdPs like Facebook and Google, or
workforce IdPs like Okta and Active Directory Federation Services (ADFS).

With the OAuth 2.0 and OpenID Connect (OIDC) tokens that an Amazon Cognito user pool issues, you
can

* Accept an ID token in your app that authenticates a user, and provides the
  information that you need to set up the user’s profile
* Accept an access token in your API with the OIDC scopes that authorize your users’
  API calls.
* Retrieve AWS credentials from an Amazon Cognito identity pool.

**Features of Amazon Cognito user pools**

| Feature | Description |
| OIDC identity provider | Issue ID tokens to authenticate users |
| Authorization server | Issue access tokens to authorize user access to APIs |
| SAML 2.0 service provider | Transform SAML assertions into ID and access tokens |
| OIDC relying party | Transform OIDC tokens into ID and access tokens |
| Social provider relying party | Transform ID tokens from Apple, Facebook, Amazon, or Google to your own ID and access tokens |
| Authentication frontend service | Sign up, manage, and authenticate users with managed login |
| API support for your own UI | Create, manage and authenticate users through authentication API requests in supported AWS SDKs¹ |
| Multi-factor authentication | Use SMS messages, TOTPs, or your user's device as an additional authentication factor¹ |
| Security monitoring & response | Secure against malicious activity and insecure passwords¹ |
| Customize authentication flows | Build your own authentication mechanism, or add custom steps to existing flows² |
| Groups | Create logical groupings of users, and a hierarchy of IAM role claims when you pass tokens to identity pools |
| Customize tokens | Customize your ID and access tokens with new, modified, and suppressed claims |
| Customize user attributes | Assign values to user attributes and add your own custom attributes |

¹ Feature is unavailable to federated users.

² Feature is unavailable to federated and managed login users.

For more information about user pools, see [Getting started with user pools](./getting-started-user-pools.html) and the [Amazon Cognito user
pools API reference](https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/).

### Identity pools

An identity pool is a collection of unique identifiers, or identities, that you assign
to your users or guests and authorize to receive temporary AWS credentials. When you
present proof of authentication to an identity pool in the form of the trusted claims from a
SAML 2.0, OpenID Connect (OIDC), or OAuth 2.0 social identity provider (IdP), you associate
your user with an identity in the identity pool. The token that your identity pool creates
for the identity can retrieve temporary session credentials from AWS Security Token Service (AWS STS).

To complement authenticated identities, you can also configure an identity pool to
authorize AWS access without IdP authentication. You can offer custom proof of
authentication with [Developer-authenticated identities](./developer-authenticated-identities.html). You can also grant temporary AWS
credentials to guest users, with [unauthenticated
identities](./identity-pools.html#authenticated-and-unauthenticated-identities).

With identity pools, you have two ways to integrate with IAM policies in your
AWS account. You can use these two features together or individually.

###### Role-based access control

When your user passes claims to your identity pool, Amazon Cognito chooses the IAM role that
it requests. To customize the role’s permissions to your needs, you apply IAM policies
to each role. For example, if your user demonstrates that they are in the marketing
department, they receive credentials for a role with policies tailored to marketing
department access needs. Amazon Cognito can request a default role, a role based on rules that
query your user’s claims, or a role based on your user’s group membership in a user pool.
You can also configure the role trust policy so that IAM trusts only your identity pool
to generate temporary sessions.

###### Attributes for access control

Your identity pool reads attributes from your user’s claims, and maps them to
principal tags in your user’s temporary session. You can then configure your IAM
resource-based policies to allow or deny access to resources based on IAM principals
that carry the session tags from your identity pool. For example, if your user
demonstrates that they are in the marketing department, AWS STS tags their session
`Department: marketing`. Your Amazon S3 bucket permits read operations based on an
[aws:PrincipalTag](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html#condition-keys-principaltag) condition that requires a value of
`marketing` for the `Department` tag.

**Features of Amazon Cognito identity pools**

| Feature | Description |
| Amazon Cognito user pool relying party | Exchange an ID token from your user pool for web identity credentials from AWS STS |
| SAML 2.0 service provider | Exchange SAML assertions for web identity credentials from AWS STS |
| OIDC relying party | Exchange OIDC tokens for web identity credentials from AWS STS |
| Social provider relying party | Exchange OAuth tokens from Amazon, Facebook, Google, Apple, and Twitter for web identity credentials from AWS STS |
| Custom relying party | With AWS credentials, exchange claims in any format for web identity credentials from AWS STS |
| Unauthenticated access | Issue limited-access web identity credentials from AWS STS without authentication |
| Role-based access control | Choose an IAM role for your authenticated user based on their claims, and configure your roles to only be assumed in the context of your identity pool |
| Attribute-based access control | Convert claims into principal tags for your AWS STS temporary session, and use IAM policies to filter resource access based on principal tags |

For more information about identity pools, see [Getting started with Amazon Cognito identity pools](./getting-started-with-identity-pools.html) and the [Amazon Cognito identity
pools API reference](https://docs.aws.amazon.com/cognitoidentity/latest/APIReference/).

## Amazon Cognito user pools and identity pools comparison

| Feature | Description | User pools | Identity pools |
| --- | --- | --- | --- |
| OIDC identity provider | Issue OIDC ID tokens to authenticate app users | ✓ |  |
| User directory | Store user profiles for authentication | ✓ |  |
| Authorize API access | Issue access tokens to authorize user access to APIs (including user profile self-service API operations), databases, and other resources that accept OAuth scopes | ✓ |  |
| IAM web identity authorization | Generate tokens that you can exchange with AWS STS for temporary AWS credentials |  | ✓ |
| SAML 2.0 service provider & OIDC identity provider | Issue customized OIDC tokens based on claims from a SAML 2.0 identity provider | ✓ |  |
| OIDC relying party & OIDC identity provider | Issue customized OIDC tokens based on claims from an OIDC identity provider | ✓ |  |
| OAuth 2.0 relying party & OIDC identity provider | Issue customized OIDC tokens based on scopes from OAuth 2.0 social providers like Apple and Google | ✓ |  |
| SAML 2.0 service provider & credentials broker | Issue temporary AWS credentials based on claims from a SAML 2.0 identity provider |  | ✓ |
| OIDC relying party & credentials broker | Issue temporary AWS credentials based on claims from an OIDC identity provider |  | ✓ |
| Social provider relying party & credentials broker | Issue temporary AWS credentials based on JSON web tokens from developer applications with social providers like Apple and Google |  | ✓ |
| Amazon Cognito user pool relying party & credentials broker | Issue temporary AWS credentials based on JSON web tokens from Amazon Cognito user pools |  | ✓ |
| Custom relying party & credentials broker | Issue temporary AWS credentials to arbitrary identities, authorized by developer IAM credentials |  | ✓ |
| Authentication frontend service | Sign up, manage, and authenticate users with managed login | ✓ |  |
| API support for your own authentication UI | Create, manage and authenticate users through API requests in supported AWS SDKs¹ | ✓ |  |
| MFA | Use SMS messages, TOTPs, or your user's device as an additional authentication factor¹ | ✓ |  |
| Security monitoring & response | Protect against malicious activity and insecure passwords¹ | ✓ |  |
| Customize authentication flows | Build your own authentication mechanism, or add custom steps to existing flows¹ | ✓ |  |
| User groups | Create logical groupings of users, and a hierarchy of IAM role claims when you pass tokens to identity pools | ✓ |  |
| Customize tokens | Customize your ID and access tokens with new, modified, and suppressed claims and scopes | ✓ |  |
| AWS WAF web ACLs | Monitor and control requests to your authentication front end with AWS WAF | ✓ |  |
| Customize user attributes | Assign values to user attributes and add your own custom attributes | ✓ |  |
| Unauthenticated access | Issue limited-access web identity credentials from AWS STS without authentication |  | ✓ |
| Role-based access control | Choose an IAM role for your authenticated user based on their claims, and configure your role trust to limit access to web identity users |  | ✓ |
| Attribute-based access control | Transform user claims into principal tags for your AWS STS temporary session, and use IAM policies to filter resource access based on principal tags |  | ✓ |

¹ Feature is not available to federated users.

## Getting started with Amazon Cognito

For example user pool applications, see [Getting started with user pools](./getting-started-user-pools.html).

For an introduction to identity pools, see [Getting started with Amazon Cognito identity pools](./getting-started-with-identity-pools.html).

For links to guided setup experiences with user pools and identity pools, see [Guided setup options for Amazon Cognito](./cognito-guided-setup.html).

To get started with an AWS SDK, see [AWS Developer Tools](https://aws.amazon.com/products/developer-tools). For developer resources
specific to Amazon Cognito, see [Amazon Cognito developer
resources](https://aws.amazon.com/cognito/dev-resources/).

To use Amazon Cognito, you need an AWS account. For more information, see [Getting started with AWS](./cognito-getting-started-account-iam.html).

## Regional availability

Amazon Cognito is available in multiple AWS Regions worldwide. In each Region, Amazon Cognito is
distributed across multiple Availability Zones. These Availability Zones are physically
isolated from each other, but are united by private, low-latency, high-throughput, and highly
redundant network connections. These Availability Zones enable AWS to provide services,
including Amazon Cognito, with very high levels of availability and redundancy, while also minimizing
latency.

To see if Amazon Cognito is currently available in any AWS Region, see [AWS Services by
Region](https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/).

To learn about regional API service endpoints, see [AWS regions and endpoints](https://docs.aws.amazon.com/general/latest/gr/rande.html##cognito_identity_region)
in the *Amazon Web Services General Reference*.

To learn more about the number of Availability Zones that are available in each Region,
see [AWS global
infrastructure](https://aws.amazon.com/about-aws/global-infrastructure/).

## Pricing for Amazon Cognito

For information about Amazon Cognito pricing, see [Amazon Cognito pricing](https://aws.amazon.com/cognito/pricing/).

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.

---

## 4. What is AWS Secrets Manager?

What is AWS Secrets Manager? - AWS Secrets Manager

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

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.

---

## 5. What is Amazon VPC?

What is Amazon VPC? - Amazon Virtual Private Cloud

# What is Amazon VPC?

With Amazon Virtual Private Cloud (Amazon VPC), you can launch AWS resources in a logically isolated virtual
network that you've defined. This virtual network closely resembles a traditional network
that you'd operate in your own data center, with the benefits of using the scalable
infrastructure of AWS.

The following diagram shows an example VPC. The VPC has one subnet in each of the
Availability Zones in the Region, EC2 instances in each subnet, and an internet gateway
to allow communication between the resources in your VPC and the internet.

For more information, see [Amazon Virtual Private Cloud (Amazon VPC)](https://aws.amazon.com/vpc/).

## Features

The following features help you configure a VPC to provide the connectivity
that your applications need:

**Virtual private clouds (VPC)**
:   A [VPC](./configure-your-vpc.html) is a virtual
    network that closely resembles a traditional network that you'd operate
    in your own data center. After you create a VPC, you can add subnets.

**Subnets**
:   A [subnet](./configure-subnets.html) is a range of
    IP addresses in your VPC. A subnet must reside in a single Availability Zone.
    After you add subnets, you can deploy AWS resources in your VPC.

**IP addressing**
:   You can assign [IP addresses](./vpc-ip-addressing.html),
    both IPv4 and IPv6, to your VPCs and subnets. You can also bring your public
    IPv4 addresses and IPv6 GUA addresses to AWS and allocate them to resources in your VPC,
    such as EC2 instances, NAT gateways, and Network Load Balancers.

**Routing**
:   Use [route tables](./VPC_Route_Tables.html) to determine
    where network traffic from your subnet or gateway is directed.

**Gateways and endpoints**
:   A [gateway](./extend-intro.html) connects your VPC to
    another network. For example, use an [internet gateway](./VPC_Internet_Gateway.html)
    to connect your VPC to the internet. Use a [VPC endpoint](https://docs.aws.amazon.com/vpc/latest/privatelink/privatelink-access-aws-services.html) to connect to AWS services privately, without
    the use of an internet gateway or NAT device.

**Peering connections**
:   Use a [VPC peering connection](https://docs.aws.amazon.com/vpc/latest/peering/)
    to route traffic between the resources in two VPCs.

**Traffic Mirroring**
:   [Copy network traffic](https://docs.aws.amazon.com/vpc/latest/mirroring/) from
    network interfaces and send it to security and monitoring appliances for
    deep packet inspection.

**Transit gateways**
:   Use a [transit gateway](./extend-tgw.html), which
    acts as a central hub, to route traffic between your VPCs, VPN connections,
    and Direct Connect connections.

**VPC Flow Logs**
:   A [flow log](./flow-logs.html) captures information
    about the IP traffic going to and from network interfaces in your VPC.

**VPN connections**
:   Connect your VPCs to your on-premises networks using
    [AWS Virtual Private Network (Site-to-Site VPN)](./vpn-connections.html).

## Getting started with Amazon VPC

Your AWS account includes a [default VPC](./default-vpc.html) in each AWS Region.
Your default VPCs are configured such that you can immediately start launching and connecting
to EC2 instances. For more information, see [Plan your VPC](./vpc-getting-started.html).

You can choose to create additional VPCs with the subnets, IP addresses, gateways
and routing that you need. For more information, see [Create a VPC](./create-vpc.html).

## Working with Amazon VPC

You can create and manage your VPCs using any of the following interfaces:

* **AWS Management Console** — Provides a web interface that you can
  use to access your VPCs.
* **AWS Command Line Interface (AWS CLI)** —
  Provides commands for a broad set of AWS services, including Amazon VPC, and is
  supported on Windows, Mac, and Linux. For more information, see [AWS Command Line Interface](https://aws.amazon.com/cli/).
* **AWS SDKs** — Provides language-specific
  APIs and takes care of many of the connection details, such as calculating
  signatures, handling request retries, and error handling. For more information,
  see [AWS SDKs](https://aws.amazon.com/developer/tools/).
* **Query API** — Provides low-level API actions
  that you call using HTTPS requests. Using the Query API is the most direct way to
  access Amazon VPC, but it requires that your application handle low-level details such as
  generating the hash to sign the request, and error handling. For more information,
  see [Amazon VPC actions](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/OperationList-query-vpc.html) in
  the *Amazon EC2 API Reference*.

## Pricing for Amazon VPC

There's no additional charge for using a VPC. There are, however, charges for some VPC
components, such as NAT gateways, IP Address Manager, traffic mirroring, Reachability Analyzer, and
Network Access Analyzer. For more information, see [Amazon VPC Pricing](https://aws.amazon.com/vpc/pricing/).

Nearly all resources that you launch in your virtual private cloud (VPC) provide you
with an IP address for connectivity. The vast majority of resources in your VPC use
private IPv4 addresses. Resources that require direct access to the internet over IPv4,
however, use public IPv4 addresses.

Amazon VPC enables you to launch managed services, such as Elastic Load Balancing, Amazon RDS, and Amazon EMR, without having a VPC set up beforehand. It does this by using the [default
VPC](./default-vpc.html) in your account if you have
one. Any public IPv4 addresses provisioned to your account by the managed
service will be charged. These charges will be associated with Amazon VPC service in
your AWS Cost and Usage Report.

**Pricing for public IPv4 addresses**

A *public IPv4 address* is an IPv4 address that is
routable from the internet. A public IPv4 address is necessary for a resource to be
directly reachable from the internet over IPv4.

If you are an existing or new [AWS Free Tier](https://aws.amazon.com/free/)
customer, you get 750 hours of public IPv4 address usage with the EC2 service at no
charge. If you are not using the EC2 service in the AWS Free Tier, Public IPv4
addresses are charged. For specific pricing information, see the *Public IPv4 address* tab in [Amazon VPC Pricing](https://aws.amazon.com/vpc/pricing/).

Private IPv4 addresses ([RFC
1918](https://datatracker.ietf.org/doc/html/rfc1918)) are not charged. For more information about how public IPv4 addresses
are charged for shared VPCs, see [Billing and
metering for the owner and participants](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-sharing.html#vpc-sharing-permissions).

Public IPv4 addresses have the following types:

* **Elastic IP addresses (EIPs)**: Static, public IPv4 addresses
  provided by Amazon that you can associate with an EC2 instance, elastic network
  interface, or AWS resource.
* **EC2 public IPv4 addresses**: Public IPv4 addresses assigned to
  an EC2 instance by Amazon (if the EC2 instance is launched into a default subnet or
  if the instance is launched into a subnet that’s been configured to automatically
  assign a public IPv4 address).
* **BYOIPv4 addresses**: Public IPv4 addresses in the IPv4 address
  range that you’ve brought to AWS using [Bring your own IP addresses (BYOIP)](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-byoip.html).
* **Service-managed IPv4 addresses**: Public IPv4 addresses
  automatically provisioned on AWS resources and managed by an AWS service. For
  example, public IPv4 addresses on Amazon ECS, Amazon RDS, or Amazon WorkSpaces.

The following list shows the most common AWS services that can use public IPv4
addresses.

* Amazon WorkSpaces Applications
* [AWS Client VPN](https://docs.aws.amazon.com/vpn/latest/clientvpn-admin/what-is.html#what-is-pricing)
* AWS Database Migration Service
* Amazon EC2
* Amazon Elastic Container Service
* Amazon EKS
* Amazon EMR
* Amazon GameLift Servers
* AWS Global Accelerator
* AWS Mainframe Modernization
* Amazon Managed Streaming for Apache Kafka
* Amazon MQ
* Amazon RDS
* Amazon Redshift
* AWS Site-to-Site VPN
* Amazon VPC NAT gateway
* Amazon WorkSpaces
* Elastic Load Balancing

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.

---

## 6. What are AWS WAF, AWS Shield Advanced, AWS Shield network security director and AWS Firewall Manager?

What are AWS WAF, AWS Shield Advanced, AWS Shield network security director and AWS Firewall Manager? - AWS WAF, AWS Firewall Manager, AWS Shield Advanced, and AWS Shield network security director

**Introducing a new console experience for AWS WAF**

You can now use the updated experience to access AWS WAF functionality anywhere in the console.
For more details, see [Working with the console](https://docs.aws.amazon.com/waf/latest/developerguide/working-with-console.html).

# What are AWS WAF, AWS Shield Advanced, AWS Shield network security director and AWS Firewall Manager?

You can use [AWS WAF](./waf-chapter.html), [AWS Shield](./shield-chapter.html), and [AWS Firewall Manager](./fms-chapter.html) together to create a comprehensive
security solution. AWS WAF is a web application firewall that you can use to monitor web requests
that your end users send to your applications and to control access to your content.
Shield Advanced provides protection against distributed denial of service (DDoS) attacks
for AWS resources, at the network and transport layers (layer 3 and 4) and the application layer (layer 7).
AWS Firewall Manager provides management of protections like AWS WAF and Shield Advanced across accounts and resources,
even as new resources are added.

###### Topics

* [What is AWS WAF?](#waf-intro)
* [What is AWS Shield Advanced?](#ddos-intro)
* [What is AWS Shield network security director?](#nsd-intro)
* [What is AWS Firewall Manager?](#fms-intro)

## What is AWS WAF?

AWS WAF is a web application firewall that lets you monitor the HTTP and HTTPS requests that
are forwarded to your protected web application resources. You can protect the following
resource types:

* Amazon CloudFront distribution
* Amazon API Gateway REST API
* Application Load Balancer
* AWS AppSync GraphQL API
* Amazon Cognito user pool
* AWS App Runner service
* AWS Verified Access instance
* AWS Amplify

AWS WAF lets you control access to your content. Based on conditions that you specify,
such as the IP addresses that requests originate from or the values of query strings, your
protected resource responds to requests either with the requested content, with an HTTP 403
status code (Forbidden), or with a custom response.

At the simplest level, AWS WAF lets you choose one of the following behaviors:

* **Allow all requests except the ones that you
  specify** – This is useful when you want Amazon CloudFront, Amazon API Gateway, Application Load Balancer, AWS AppSync, Amazon Cognito, AWS App Runner, or AWS Verified Access to
  serve content for a public website, but you also want to block requests from
  attackers.
* **Block all requests except the ones that you
  specify** – This is useful when you want to serve content for a
  restricted website whose users are readily identifiable by properties in web
  requests, such as the IP addresses that they use to browse to the website.
* **Count requests that match your criteria** – You can
  use the Count action to track your web traffic without modifying how you handle it.
  You can use this for general monitoring and also to test your new web request
  handling rules. When you want to allow or block requests based on new properties in
  the web requests, you can first configure AWS WAF to count the requests that match
  those properties. This lets you confirm your new configuration settings before you
  switch your rules to allow or block matching requests.
* **Run CAPTCHA or challenge checks against requests that match your
  criteria** – You can implement CAPTCHA and silent challenge controls
  against requests to help reduce bot traffic to your protected resources.

Using AWS WAF has several benefits:

* Additional protection against web attacks using criteria that you specify. You
  can define criteria using characteristics of web requests such as the
  following:

  + IP addresses that requests originate from.
  + Country that requests originate from.
  + Values in request headers.
  + Strings that appear in requests, either specific strings or strings that
    match regular expression (regex) patterns.
  + Length of requests.
  + Presence of SQL code that is likely to be malicious (known as *SQL injection*).
  + Presence of a script that is likely to be malicious (known as *cross-site scripting*).
* Rules that can allow, block, or count web requests that meet the specified
  criteria. Alternatively, rules can block or count web requests that not only meet
  the specified criteria, but also exceed a specified number of requests in a minute
  or in five minutes.
* Rules that you can reuse for multiple web applications.
* Managed rule groups from AWS and AWS Marketplace sellers.
* Real-time metrics and sampled web requests.
* Automated administration using the AWS WAF API.

If you want granular control over the protections that you add to your resources, AWS WAF
alone might be the right choice. For more information about AWS WAF, see [AWS WAF](./waf-chapter.html).

## What is AWS Shield Advanced?

You can use AWS WAF web access control lists (web ACLs) to help minimize the effects of a
Distributed Denial of Service (DDoS) attack. For additional protection against DDoS
attacks, AWS also provides AWS Shield Standard and AWS Shield Advanced. AWS Shield Standard is
automatically included at no extra cost beyond what you already pay for AWS WAF and your
other AWS services.

Shield Advanced provides expanded DDoS attack protection for your
Amazon EC2 instances, Elastic Load Balancing load balancers, CloudFront distributions, Route 53 hosted zones, and AWS Global Accelerator standard accelerators.
Shield Advanced incurs additional charges. Shield Advanced options and features include automatic application layer DDoS mitigation, advanced event visibility, and dedicated
support from the Shield Response Team (SRT). If you own high visibility websites or are otherwise
prone to frequent DDoS attacks, consider purchasing the additional protections that
Shield Advanced provides. For additional information, see [AWS Shield Advanced capabilities and options](./ddos-advanced-summary-capabilities.html) and [Deciding whether to subscribe to AWS Shield Advanced and apply additional protections](./ddos-advanced-summary-deciding.html).

## What is AWS Shield network security director?

AWS Shield network security director helps secure your AWS environment by discovering your compute, networking, and network security resources across your account.
network security director evaluates each resource's security configuration by analyzing network topology and security configurations against AWS best practices and threat intelligence.
To help you strengthen your security, network security director rates its findings from low to critical severity and shares specific remediation steps, which you can explore using natural language queries through Amazon Q Developer.

For more information about AWS Shield network security director, see [AWS Shield network security director (preview)](./nsd-chapter.html).

## What is AWS Firewall Manager?

AWS Firewall Manager simplifies your administration and maintenance tasks across multiple accounts
and resources for a variety of protections, including AWS WAF, AWS Shield Advanced, Amazon VPC security groups and network ACLs,
AWS Network Firewall, and Amazon Route 53 Resolver DNS Firewall. With Firewall Manager, you set up your protections just once
and the service automatically applies them across your accounts and resources, even as you add new accounts and resources.

For more information about Firewall Manager, see [AWS Firewall Manager](./fms-chapter.html).

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.

---

## 7. What is Amazon S3?

What is Amazon S3? - Amazon Simple Storage Service

# What is Amazon S3?

Amazon Simple Storage Service (Amazon S3) is an object storage service that offers industry-leading scalability,
data availability, security, and performance. Customers of all sizes and industries can use
Amazon S3 to store and protect any amount of data for a range of use cases, such as data lakes,
websites, mobile applications, backup and restore, archive, enterprise applications, IoT
devices, and big data analytics. Amazon S3 provides management features so that you can optimize,
organize, and configure access to your data to meet your specific business, organizational,
and compliance requirements.

###### Note

For more information about using the Amazon S3 Express One Zone storage class with directory buckets, see [S3 Express One Zone](./directory-bucket-high-performance.html#s3-express-one-zone) and [Working with directory buckets](./directory-buckets-overview.html).

###### Topics

* [Features of Amazon S3](#S3Features)
* [How Amazon S3 works](#CoreConcepts)
* [Amazon S3 data consistency model](#ConsistencyModel)
* [Related services](#RelatedAmazonWebServices)
* [Accessing Amazon S3](#API)
* [Paying for Amazon S3](#PayingforStorage)
* [PCI DSS compliance](#pci-dss-compliance)

## Features of Amazon S3

### Storage classes

Amazon S3 offers a range of storage classes designed for different use cases. For
example, you can store mission-critical production data in S3 Standard or S3 Express One Zone for frequent
access, save costs by storing infrequently accessed data in S3 Standard-IA or
S3 One Zone-IA, and archive data at the lowest costs in S3 Glacier Instant Retrieval,
S3 Glacier Flexible Retrieval, and S3 Glacier Deep Archive.

Amazon S3 Express One Zone is a high-performance, single-zone Amazon S3 storage class that is purpose-built
to deliver consistent, single-digit millisecond data access for your most
latency-sensitive applications. S3 Express One Zone is the lowest latency cloud object
storage class available today, with data access
speeds
up to 10x faster and with request costs
50
percent lower than S3 Standard. S3 Express One Zone is the first S3 storage class where you can select a single Availability Zone with
the option to co-locate your object storage with your compute resources, which provides the highest possible access speed.
Additionally, to further increase access speed and support hundreds of thousands of
requests per second, data is stored in a new bucket type: an
Amazon S3 directory bucket. For more information, see [S3 Express One Zone](./directory-bucket-high-performance.html#s3-express-one-zone) and [Working with directory buckets](./directory-buckets-overview.html).

You can store data with changing or unknown access patterns in
S3 Intelligent-Tiering, which optimizes storage costs by automatically moving your
data between four access tiers when your access patterns change. These four access
tiers include two low-latency access tiers optimized for frequent and infrequent
access, and two opt-in archive access tiers designed for asynchronous access for
rarely accessed data.

For more information, see [Understanding and managing Amazon S3 storage classes](./storage-class-intro.html).

### Storage management

Amazon S3 has storage management features that you can use to manage costs, meet
regulatory requirements, reduce latency, and save multiple distinct copies of your
data for compliance requirements.

* [S3 Lifecycle](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html) – Configure a lifecycle configuration to manage
  your objects and store them cost effectively throughout their lifecycle. You
  can transition objects to other S3 storage classes or expire objects that
  reach the end of their lifetimes.
* [S3 Object Lock](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html) – Prevent Amazon S3 objects from being
  deleted or overwritten for a fixed amount of time or indefinitely. You can
  use Object Lock to help meet regulatory requirements that require *write-once-read-many*
  *(WORM)* storage or to simply add another
  layer of protection against object changes and deletions.
* [S3 Replication](https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication.html)
  – Replicate objects and their respective metadata and object tags to
  one or more destination buckets in the same or different AWS Regions for
  reduced latency, compliance, security, and other use cases.
* [S3 Batch Operations](https://docs.aws.amazon.com/AmazonS3/latest/userguide/batch-ops.html) – Manage billions of objects at scale
  with a single S3 API request or a few clicks in the Amazon S3 console. You can
  use Batch Operations to perform operations such as **Copy**, **Invoke AWS Lambda
  function**, and **Restore** on
  millions or billions of objects.

### Access management and security

Amazon S3 provides features for auditing and managing access to your buckets and
objects. By default, S3 buckets and the objects in them are private. You have access
only to the S3 resources that you create. To grant granular resource permissions
that support your specific use case or to audit the permissions of your Amazon S3
resources, you can use the following features.

* [S3 Block Public Access](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html) – Block public access to S3
  buckets and objects. By default, Block Public Access settings are turned on
  at the bucket level. We recommend that you keep all Block Public Access
  settings enabled unless you know that you need to turn off one or more of
  them for your specific use case. For more information, see [Configuring block public access settings for your S3 buckets](./configuring-block-public-access-bucket.html).
* [AWS Identity and Access Management (IAM)](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-iam.html) – IAM is a web service that helps
  you securely control access to AWS resources, including your Amazon S3
  resources. With IAM, you can centrally manage permissions that control
  which AWS resources users can access. You use IAM to control who is
  authenticated (signed in) and authorized (has permissions) to use
  resources.
* [Bucket
  policies](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-policies.html) – Use IAM-based policy language to configure
  resource-based permissions for your S3 buckets and the objects in
  them.
* [Amazon S3 access points](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-points.html)
  – Configure named network endpoints with dedicated access policies to
  manage data access at scale for shared datasets in Amazon S3.
* [Access control
  lists (ACLs)](https://docs.aws.amazon.com/AmazonS3/latest/userguide/acls.html) – Grant read and write permissions for
  individual buckets and objects to authorized users. As a general rule, we
  recommend using S3 resource-based policies (bucket policies and access point
  policies) or IAM user policies for access control instead of ACLs.
  Policies are a simplified and more flexible access control option. With
  bucket policies and access point policies, you can define rules that apply
  broadly across all requests to your Amazon S3 resources. For more information
  about the specific cases when you'd use ACLs instead of resource-based
  policies or IAM user policies, see [Managing access with ACLs](./acls.html).
* [S3 Object Ownership](https://docs.aws.amazon.com/AmazonS3/latest/userguide/about-object-ownership.html) – Take ownership of every object
  in your bucket, simplifying access management for data stored in Amazon S3.
  S3 Object Ownership is an Amazon S3 bucket-level setting that you can use to
  disable or enable ACLs. By default, ACLs are disabled. With ACLs disabled,
  the bucket owner owns all the objects in the bucket and manages access to
  data exclusively by using access-management policies.
* [IAM Access Analyzer for S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-analyzer.html)
  – Evaluate and monitor your S3 bucket access policies, ensuring that
  the policies provide only the intended access to your S3 resources.

### Data processing

To transform data and trigger workflows to automate a variety of other processing
activities at scale, you can use the following features.

* [S3 Object Lambda](https://docs.aws.amazon.com/AmazonS3/latest/userguide/transforming-objects.html)
  – Add your own code to S3 GET, HEAD, and LIST requests to modify and process data as
  it is returned to an application. Filter rows, dynamically resize images,
  redact confidential data, and much more.
* [Event
  notifications](https://docs.aws.amazon.com/AmazonS3/latest/userguide/EventNotifications.html) – Trigger workflows that use Amazon Simple Notification Service
  (Amazon SNS), Amazon Simple Queue Service (Amazon SQS), and AWS Lambda when a change is made to your S3
  resources.

### Storage logging and monitoring

Amazon S3 provides logging and monitoring tools that you can use to monitor and control
how your Amazon S3 resources are being used. For more information, see [Monitoring
tools](https://docs.aws.amazon.com/AmazonS3/latest/userguide/monitoring-automated-manual.html).

###### Automated monitoring tools

* [Amazon CloudWatch
  metrics for Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/cloudwatch-monitoring.html)  – Track the operational health of your
  S3 resources and configure billing alerts when estimated charges reach a
  user-defined threshold.
* [AWS CloudTrail](https://docs.aws.amazon.com/AmazonS3/latest/userguide/cloudtrail-logging.html)
  – Record actions taken by a user, a role, or an AWS service in
  Amazon S3. CloudTrail logs provide you with detailed API tracking for S3 bucket-level
  and object-level operations.

###### Manual monitoring tools

* [Server access
  logging](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ServerLogs.html) – Get detailed records for the requests that are
  made to a bucket. You can use server access logs for many use cases, such as
  conducting security and access audits, learning about your customer base,
  and understanding your Amazon S3 bill.
* [AWS Trusted
  Advisor](https://docs.aws.amazon.com/awssupport/latest/user/trusted-advisor.html) – Evaluate your account by using AWS best
  practice checks to identify ways to optimize your AWS infrastructure,
  improve security and performance, reduce costs, and monitor service quotas.
  You can then follow the recommendations to optimize your services and
  resources.

### Analytics and insights

Amazon S3 offers features to help you gain visibility into your storage usage, which
empowers you to better understand, analyze, and optimize your storage at
scale.

* [Amazon S3 Storage Lens](https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage_lens.html)
  – Understand, analyze, and optimize your storage. S3 Storage Lens provides
  60+ usage and activity metrics and interactive dashboards to aggregate data
  for your entire organization, specific accounts, AWS Regions, buckets, or
  prefixes.
* [Storage
  Class Analysis](https://docs.aws.amazon.com/AmazonS3/latest/userguide/analytics-storage-class.html) – Analyze storage access patterns to
  decide when it's time to move data to a more cost-effective storage class.
* [S3 Inventory with
  Inventory reports](https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-inventory.html) – Audit and report on objects and their
  corresponding metadata and configure other Amazon S3 features to take action in
  Inventory reports. For example, you can report on the replication and
  encryption status of your objects. For a list of all the metadata available
  for each object in Inventory reports, see [Amazon S3 Inventory list](./storage-inventory.html#storage-inventory-contents).

### Strong consistency

Amazon S3 provides strong read-after-write consistency for PUT and DELETE requests of
objects in your Amazon S3 bucket in all AWS Regions. This behavior applies to both
writes of new objects as well as PUT requests that overwrite existing objects and
DELETE requests. In addition, read operations on Amazon S3 Select, Amazon S3 access control
lists (ACLs), Amazon S3 Object Tags, and object metadata (for example, the HEAD object)
are strongly consistent. For more information, see [Amazon S3 data consistency model](#ConsistencyModel).

## How Amazon S3 works

Amazon S3 is an object storage service that stores data as objects, hierarchical data, or tabular data within buckets. An
*object* is a file and any metadata that describes
the file. A *bucket* is a container for objects.

To store your data in Amazon S3, you first create a bucket and specify a bucket name and
AWS Region. Then, you upload your data to that bucket as objects in Amazon S3. Each object
has a *key* (or *key
name*), which is the unique identifier for the object within the
bucket.

S3 provides features that you can configure to support your specific use case. For
example, you can use S3 Versioning to keep multiple versions of an object in the same
bucket, which allows you to restore objects that are accidentally deleted or
overwritten.

Buckets and the objects in them are private and can be accessed only if you explicitly
grant access permissions. You can use bucket policies, AWS Identity and Access Management (IAM) policies,
access control lists (ACLs), and S3 Access Points to manage access.

###### Topics

* [Buckets](#BasicsBucket)
* [Objects](#BasicsObjects)
* [Keys](#BasicsKeys)
* [S3 Versioning](#Versions)
* [Version ID](#BasicsVersionID)
* [Bucket policy](#BucketPolicies)
* [S3 access points](#BasicsAccessPoints)
* [Access control lists (ACLs)](#S3_ACLs)
* [Regions](#Regions)

### Buckets

Amazon S3 supports four types of buckets—general purpose buckets, directory buckets, table buckets, and vector buckets. Each type of bucket provides a unique set of features for different use cases.

**General purpose buckets** – General purpose buckets are recommended for most use cases and access patterns and are the original S3 bucket type.
A general purpose bucket is a container for objects stored in Amazon S3, and you can store any number of objects in a bucket and across all storage classes (except for
S3 Express One Zone), so you can redundantly store objects across multiple Availability Zones. For more information, see [Creating, configuring, and working with Amazon S3 general purpose buckets](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-buckets-s3.html).

By default, general purpose buckets exist in a global namespace, which means that each bucket name must be unique across all AWS accounts in all the AWS Regions within a partition. A partition is a grouping of Regions. AWS currently has four partitions: `aws` (Standard Regions), `aws-cn` (China Regions), `aws-us-gov` (AWS GovCloud (US)), and `aws-eusc` (European Sovereign Cloud). When you create a general purpose bucket, you can choose to create a bucket in the shared global namespace or you can choose to create a bucket in your account regional namespace. Your account regional namespace is a subdivision of the global namespace that only your account can create buckets in. New general purpose buckets created in your account regional namespace are unique to your account and can never be re-created by another account. For more information on bucket namespaces, see [Namespaces for general purpose buckets](https://docs.aws.amazon.com/AmazonS3/latest/userguide/gpbucketnamespaces.html).

###### Note

By default, all general purpose buckets are private. However, you can grant public access to general purpose buckets.
You can control access to general purpose buckets at the bucket, prefix (folder), or object tag level.
For more information, see [Access control in Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-management.html).

**Directory buckets** – Recommended for low-latency use cases and data-residency use cases. By default, you can create up to 100 directory buckets in your
AWS account, with no limit on the number of objects that you can store in a directory bucket. Directory buckets organize objects into hierarchical directories (prefixes) instead of the flat storage structure
of general purpose buckets. This bucket type has no prefix limits and individual directories can scale horizontally. For more information, see [Working with directory buckets](https://docs.aws.amazon.com/AmazonS3/latest/userguide/directory-buckets-overview.html).

* For low-latency use cases, you can create a directory bucket in a single AWS Availability Zone to store data. Directory buckets in Availability Zones support the
  S3 Express One Zone storage class. With S3 Express One Zone, your data is redundantly stored on multiple devices within a single Availability Zone. The S3 Express One Zone storage class is recommended if your application
  is performance sensitive and benefits from single-digit millisecond `PUT` and `GET` latencies. To learn more about creating directory buckets in Availability Zones, see [High performance workloads](https://docs.aws.amazon.com/AmazonS3/latest/userguide/directory-bucket-high-performance.html).
* For data-residency use cases, you can create a directory bucket in a single AWS Dedicated Local Zone (DLZ) to store data. In Dedicated Local Zones, you can create S3 directory buckets to store data
  in a specific data perimeter, which helps support your data residency and isolation use cases. Directory buckets in Local Zones support the S3 One Zone-Infrequent Access (S3 One Zone-IA; Z-IA) storage class. To learn more about creating
  directory buckets in Local Zones, see [Data residency workloads](https://docs.aws.amazon.com/AmazonS3/latest/userguide/directory-bucket-data-residency.html).

###### Note

Directory buckets have all public access disabled by default. This behavior can't be changed. You can't grant access to objects stored in directory buckets. You can grant access only to your
directory buckets. For more information, see [Authenticating and authorizing requests](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-express-authenticating-authorizing.html).

**Table buckets** – Recommended for storing tabular data, such as daily purchase transactions, streaming sensor data, or ad impressions. Tabular data represents data in columns and rows, like in a database table. Table buckets provide
S3 storage that's optimized for analytics and machine learning workloads, with features designed to continuously improve query performance and reduce storage costs for tables. S3 Tables are purpose-built for
storing tabular data in the Apache Iceberg format. You can query tabular data in S3 Tables with popular query engines, including
Amazon Athena, Amazon Redshift, and Apache Spark. By default, you can create up to 10 table buckets per AWS account per AWS Region
and up to 10,000 tables per table bucket. For more information, see [Working with S3 Tables and table buckets](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables.html).

###### Note

All table buckets and tables are private and can't be made public. These resources can only be accessed by users who are explicitly granted access. To grant access, you can use IAM resource-based policies
for table buckets and tables, and IAM identity-based policies for users and roles. For more information, see [Security for S3 Tables](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-security-overview.html).

**Vector buckets** – S3 vector buckets are a type of Amazon S3 bucket that are purpose-built to store and query vectors. Vector buckets use dedicated API operations to write and query vector data efficiently. With S3 vector buckets, you can store vector embeddings for machine learning models, perform similarity searches, and integrate with services like Amazon Bedrock and Amazon OpenSearch.

S3 vector buckets organize data using vector indexes, which are resources within a bucket that store and organize vector data for efficient similarity search. Each vector index can be configured with specific dimensions, distance metrics (like cosine similarity), and metadata configurations to optimize for your specific use case. For more information, see [Working with S3 Vectors and vector buckets](./s3-vectors.html).

#### Additional information about all bucket types

When you create a bucket, you enter a bucket name and choose the AWS Region
where the bucket will reside. After you create a bucket, you cannot change the name
of the bucket or its Region. Bucket names must follow the following bucket naming rules:

* [General purpose bucket naming rules](./bucketnamingrules.html)
* [Directory bucket naming rules](./directory-bucket-naming-rules.html)
* [Table bucket naming rules](./s3-tables-buckets-naming.html#table-buckets-naming-rules)

Buckets also:

* Organize the Amazon S3 namespace at the highest level. For general purpose buckets, this namespace is `S3`. For directory buckets,
  this namespace is `s3express`. For table buckets, this namespace is `s3tables`.
* Identify the account responsible for storage and data transfer
  charges.
* Serve as the unit of aggregation for usage reporting.

### Objects

Objects are the fundamental entities stored in Amazon S3. Objects consist of object
data and metadata. The metadata is a set of name-value pairs that describe the
object. These pairs include some default metadata, such as the date last modified,
and standard HTTP metadata, such as `Content-Type`. You can also specify
custom metadata at the time that the object is stored.

Every object is contained in a bucket. For example, if the object named
`photos/puppy.jpg` is stored in the
`amzn-s3-demo-bucket` general purpose bucket in the US West (Oregon)
Region, then it is addressable by using the URL
`https://amzn-s3-demo-bucket.s3.us-west-2.amazonaws.com/photos/puppy.jpg`.
For more information, see [Accessing a
Bucket](./access-bucket-intro.html).

An object is uniquely identified within a bucket by a [key (name)](#BasicsKeys) and a [version ID](#BasicsVersionID) (if
S3 Versioning is enabled on the bucket). For more information about objects, see
[Amazon S3 objects overview](./UsingObjects.html).

### Keys

An *object key* (or *key
name*) is the unique identifier for an object within a bucket. Every
object in a bucket has exactly one key. The combination of a bucket, object key, and
optionally, version ID (if S3 Versioning is enabled for the bucket) uniquely identify
each object. So you can think of Amazon S3 as a basic data map between "bucket + key +
version" and the object itself.

Every object in Amazon S3 can be uniquely addressed through the combination of the web service
endpoint, bucket name, key, and optionally, a version. For example, in the URL
`https://amzn-s3-demo-bucket.s3.us-west-2.amazonaws.com/photos/puppy.jpg`,
`amzn-s3-demo-bucket` is the name of the bucket
and `photos/puppy.jpg` is the key.

For more information about object keys, see [Naming Amazon S3 objects](./object-keys.html).

### S3 Versioning

You can use S3 Versioning to keep multiple variants of an object in the same
bucket. With S3 Versioning, you can preserve, retrieve, and restore every version of
every object stored in your buckets. You can easily recover from both unintended
user actions and application failures.

For more information, see [Retaining multiple versions of objects with S3 Versioning](./Versioning.html).

### Version ID

When you enable S3 Versioning in a bucket, Amazon S3 generates a unique version ID for
each object added to the bucket. Objects that already existed in the bucket at the
time that you enable versioning have a version ID of `null`. If you
modify these (or any other) objects with other operations, such as [CopyObject](https://docs.aws.amazon.com/AmazonS3/latest/API/API_CopyObject.html) and [PutObject](https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutObject.html), the new objects
get a unique version ID.

For more information, see [Retaining multiple versions of objects with S3 Versioning](./Versioning.html).

### Bucket policy

A bucket policy is a resource-based AWS Identity and Access Management (IAM) policy that you can use to
grant access permissions to your bucket and the objects in it. Only the bucket owner
can associate a policy with a bucket. The permissions attached to the bucket apply
to all of the objects in the bucket that are owned by the bucket owner. Bucket
policies are limited to 20 KB in size.

Bucket policies use JSON-based access policy language that is standard across
AWS. You can use bucket policies to add or deny permissions for the objects in a
bucket. Bucket policies allow or deny requests based on the elements in the policy,
including the requester, S3 actions, resources, and aspects or conditions of the
request (for example, the IP address used to make the request). For example, you can
create a bucket policy that grants cross-account permissions to upload objects to an
S3 bucket while ensuring that the bucket owner has full control of the uploaded
objects. For more information, see [Examples of Amazon S3 bucket policies](./example-bucket-policies.html).

In your bucket policy, you can use wildcard characters on Amazon Resource Names
(ARNs) and other values to grant permissions to a subset of objects. For example,
you can control access to groups of objects that begin with a common [prefix](https://docs.aws.amazon.com/general/latest/gr/glos-chap.html#keyprefix) or end with a given extension, such as
`.html`.

### S3 access points

Amazon S3 access points are named network endpoints with dedicated access policies that
describe how data can be accessed using that endpoint. Access points are attached to an
underlying data source, such as a general purpose bucket, directory bucket, or a FSx for OpenZFS volume, that you can use to
perform S3 object operations, such as `GetObject` and
`PutObject`. Access points simplify managing data access at scale for
shared datasets in Amazon S3.

Each access point has its own access point policy. You can configure [Block Public Access](./access-control-block-public-access.html) settings
for each access point attached to a bucket. To restrict Amazon S3 data access to a private network, you can
also configure any access point to accept requests only from a virtual private cloud
(VPC).

For more information about access points for general purpose buckets, see [Managing access to shared datasets with access points](./access-points.html). For more information about access points for directory buckets, see [Managing access to shared datasets in directory buckets with access points](./access-points-directory-buckets.html).

### Access control lists (ACLs)

You can use ACLs to grant read and write permissions to authorized users for
individual general purpose buckets and objects. Each general purpose bucket and object has an ACL attached to it as
a subresource. The ACL defines which AWS accounts or groups are granted access and
the type of access. ACLs are an access control mechanism that predates IAM. For
more information about ACLs, see [Access control list (ACL) overview](./acl-overview.html).

S3 Object Ownership is an Amazon S3 bucket-level setting that you can use to both control ownership of the objects that are
uploaded to your bucket and to disable or enable ACLs. By default, Object Ownership is set to the Bucket owner enforced setting,
and all ACLs are disabled. When ACLs are disabled, the bucket owner owns all the objects in the bucket and manages access to them
exclusively by using access-management policies.

A majority of modern use cases in Amazon S3 no longer require the use of ACLs. We recommend that you keep ACLs disabled, except
in circumstances where you need to control access for each object individually. With ACLs disabled, you can use policies
to control access to all objects in your bucket, regardless of who uploaded the objects to your bucket.
For more information, see [Controlling ownership of objects and disabling ACLs for your bucket](./about-object-ownership.html).

### Regions

You can choose the geographical AWS Region where Amazon S3 stores the buckets that
you create. You might choose a Region to optimize latency, minimize costs, or
address regulatory requirements. Objects stored in an AWS Region never leave the
Region unless you explicitly transfer or replicate them to another Region. For example, objects stored in the Europe (Ireland) Region
never leave it.

###### Note

You can access Amazon S3 and its features only in the AWS Regions that are
enabled for your account. For more information about enabling a Region to create
and manage AWS resources, see [Managing AWS Regions](https://docs.aws.amazon.com/general/latest/gr/rande-manage.html) in
the *AWS General Reference*.

For a list of Amazon S3 Regions and endpoints, see [Regions and endpoints](https://docs.aws.amazon.com/general/latest/gr/s3.html) in the
*AWS General Reference*.

## Amazon S3 data consistency model

Amazon S3 provides strong read-after-write consistency for PUT and DELETE requests of
objects in your Amazon S3 bucket in all AWS Regions. This behavior applies to both writes
to new objects as well as PUT requests that overwrite existing objects and DELETE
requests. In addition, read operations on Amazon S3 Select, Amazon S3 access controls lists
(ACLs), Amazon S3 Object Tags, and object metadata (for example, the HEAD object) are
strongly consistent.

Updates to a single key are atomic. For example, if you make a PUT request to an
existing key from one thread and perform a GET request on the same key from a second
thread concurrently, you will get either the old data or the new data, but never partial
or corrupt data.

Amazon S3 achieves high availability by replicating data across multiple servers within
AWS data centers. If a PUT request is successful, your data is safely stored. Any read
(GET or LIST request) that is initiated following the receipt of a successful PUT
response will return the data written by the PUT request. Here are examples of this
behavior:

* A process writes a new object to Amazon S3 and immediately lists keys within its
  bucket. The new object appears in the list.
* A process replaces an existing object and immediately tries to read it. Amazon S3
  returns the new data.
* A process deletes an existing object and immediately tries to read it. Amazon S3
  does not return any data because the object has been deleted.
* A process deletes an existing object and immediately lists keys within its
  bucket. The object does not appear in the listing.

###### Note

* Amazon S3 does not support object locking for concurrent writers. If two PUT
  requests are simultaneously made to the same key, the request with the
  latest timestamp wins. If this is an issue, you must build an object-locking
  mechanism into your application.
* Updates are key-based. There is no way to make atomic updates across keys.
  For example, you cannot make the update of one key dependent on the update
  of another key unless you design this functionality into your
  application.

Bucket configurations have an eventual consistency model. Specifically, this means
that:

* If you delete a bucket and immediately list all buckets, the deleted bucket
  might still appear in the list.
* If you enable versioning on a bucket for the first time, it might take a short
  amount of time for the change to be fully propagated. We recommend that you wait
  for 15 minutes after enabling versioning before issuing write operations (PUT or
  DELETE requests) on objects in the bucket.

### Concurrent applications

This section provides examples of behavior to be expected from Amazon S3 when multiple
clients are writing to the same items.

In this example, both W1 (write 1) and W2 (write 2) finish before the start of R1
(read 1) and R2 (read 2). Because S3 is strongly consistent, R1 and R2 both return
`color = ruby`.

In the next example, W2 does not finish before the start of R1. Therefore, R1
might return `color = ruby` or `color = garnet`. However,
because W1 and W2 finish before the start of R2, R2 returns `color =
garnet`.

In the last example, W2 begins before W1 has received an acknowledgment.
Therefore, these writes are considered concurrent. Amazon S3 internally uses
last-writer-wins semantics to determine which write takes precedence. However, the
order in which Amazon S3 receives the requests and the order in which applications
receive acknowledgments cannot be predicted because of various factors, such as
network latency. For example, W2 might be initiated by an Amazon EC2 instance in the same
Region, while W1 might be initiated by a host that is farther away. The best way to
determine the final value is to perform a read after both writes have been
acknowledged.

## Related services

After you load your data into Amazon S3, you can use it with other AWS services. The
following are the services that you might use most frequently:

* [Amazon Elastic Compute Cloud
  (Amazon EC2)](https://aws.amazon.com/ec2/) – Provides secure and scalable computing
  capacity in the AWS Cloud. Using Amazon EC2 eliminates your need to invest in
  hardware upfront, so you can develop and deploy applications faster. You can
  use Amazon EC2 to launch as many or as few virtual servers as you need, configure
  security and networking, and manage storage.
* [Amazon EMR](https://aws.amazon.com/elasticmapreduce/) – Helps businesses, researchers, data
  analysts, and developers easily and cost-effectively process vast amounts of
  data. Amazon EMR uses a hosted Hadoop framework running on the web-scale
  infrastructure of Amazon EC2 and Amazon S3.
* [AWS Snow
  Family](https://aws.amazon.com/snow/) – Helps customers that need to run
  operations in austere, non-data center environments, and in locations where
  there's a lack of consistent network connectivity. You can use AWS Snow Family
  devices to locally and cost-effectively access the storage and compute power of
  the AWS Cloud in places where an internet connection might not be an option.
* [AWS Transfer Family](https://aws.amazon.com/aws-transfer-family/) – Provides fully managed support for
  file transfers directly into and out of Amazon S3 or Amazon Elastic File System (Amazon EFS) using Secure
  Shell (SSH) File Transfer Protocol (SFTP), File Transfer Protocol over SSL
  (FTPS), and File Transfer Protocol (FTP).

## Accessing Amazon S3

You can work with Amazon S3 in any of the following ways:

### AWS Management Console

The console is a web-based user interface for managing Amazon S3 and AWS resources.
If you've signed up for an AWS account, you can access the Amazon S3 console by signing
into the AWS Management Console and choosing **S3** from the AWS Management Console home
page.

### AWS Command Line Interface

You can use the AWS command line tools to issue commands or build scripts at
your system's command line to perform AWS (including S3) tasks.

The [AWS Command Line Interface (AWS CLI)](https://aws.amazon.com/cli/) provides commands
for a broad set of AWS services. The AWS CLI is supported on Windows, macOS, and
Linux. To get started, see the [*AWS Command Line Interface User Guide*](https://docs.aws.amazon.com/cli/latest/userguide/). For more information about the commands for
Amazon S3, see [s3api](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3api/index.html) and [s3control](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3control/index.html) in the *AWS CLI Command Reference*.

### AWS SDKs

AWS provides SDKs (software development kits) that consist of libraries and sample code
for various programming languages and platforms (Java, Python, Ruby, .NET, iOS,
Android, and so on). The AWS SDKs provide a convenient way to create programmatic
access to S3 and AWS. Amazon S3 is a REST service. You can send requests to Amazon S3 using
the AWS SDK libraries, which wrap the underlying Amazon S3 REST API and simplify your
programming tasks. For example, the SDKs take care of tasks such as calculating
signatures, cryptographically signing requests, managing errors, and retrying
requests automatically. For information about the AWS SDKs, including how to
download and install them, see [Tools for
AWS](https://aws.amazon.com/tools/).

Every interaction with Amazon S3 is either authenticated or anonymous. If you are using
the AWS SDKs, the libraries compute the signature for authentication from the keys
that you provide. For more information about how to make requests to Amazon S3, see [Making requests](https://docs.aws.amazon.com/AmazonS3/latest/API/MakingRequests.html).

### Amazon S3 REST API

The architecture of Amazon S3 is designed to be programming language-neutral, using
AWS-supported interfaces to store and retrieve objects. You can access S3 and
AWS programmatically by using the Amazon S3 REST API. The REST API is an HTTP interface
to Amazon S3. With the REST API, you use standard HTTP requests to create, fetch, and
delete buckets and objects.

To use the REST API, you can use any toolkit that supports HTTP. You can even use
a browser to fetch objects, as long as they are anonymously readable.

The REST API uses standard HTTP headers and status codes, so that standard
browsers and toolkits work as expected. In some areas, we have added functionality
to HTTP (for example, we added headers to support access control). In these cases,
we have done our best to add the new functionality in a way that matches the style
of standard HTTP usage.

If you make direct REST API calls in your application, you must write the code to
compute the signature and add it to the request. For more information about how to
make requests to Amazon S3, see [Making requests](https://docs.aws.amazon.com/AmazonS3/latest/API/MakingRequests.html) in the *Amazon S3 API Reference*.

###### Note

SOAP API support over HTTP is deprecated, but it is still available over
HTTPS. Newer Amazon S3 features are not supported for SOAP. We recommend that you use
either the REST API or the AWS SDKs.

## Paying for Amazon S3

Pricing for Amazon S3 is designed so that you don't have to plan for the storage
requirements of your application. Most storage providers require you to purchase a
predetermined amount of storage and network transfer capacity. In this scenario, if you
exceed that capacity, your service is shut off or you are charged high overage fees. If
you do not exceed that capacity, you pay as though you used it all.

Amazon S3 charges you only for what you actually use, with no hidden fees and no overage
charges. This model gives you a variable-cost service that can grow with your business
while giving you the cost advantages of the AWS infrastructure. For more information,
see [Amazon S3 Pricing](https://aws.amazon.com/s3/pricing/).

When you sign up for AWS, your AWS account is automatically signed up for all
services in AWS, including Amazon S3. However, you are charged only for the services that
you use. If you are a new Amazon S3 customer, you can get started with Amazon S3 for free. For
more information, see [AWS free tier](https://aws.amazon.com/free).

To see your bill, go to the Billing and Cost Management Dashboard in the [AWS Billing and Cost Management console](https://console.aws.amazon.com/billing/). To learn more about AWS account billing, see the [*AWS Billing User Guide*](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/billing-what-is.html). If you have
questions concerning AWS billing and AWS accounts, contact [AWS Support](https://aws.amazon.com/contact-us/).

## PCI DSS compliance

Amazon S3 supports the processing, storage, and transmission
of credit card data by a merchant or service provider, and has been
validated as being compliant with Payment Card Industry (PCI) Data Security Standard (DSS).
For more information about PCI DSS, including how to request a copy of the AWS PCI Compliance Package,
see [PCI DSS Level 1](https://aws.amazon.com/compliance/pci-dss-level-1-faqs/).

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.

---

## Bibliography

1. [What is IAM?](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html)
2. [AWS Key Management Service](https://docs.aws.amazon.com/kms/latest/developerguide/overview.html)
3. [What is Amazon Cognito?](https://docs.aws.amazon.com/cognito/latest/developerguide/what-is-amazon-cognito.html)
4. [What is AWS Secrets Manager?](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html)
5. [What is Amazon VPC?](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html)
6. [What are AWS WAF, AWS Shield Advanced, AWS Shield network security director and AWS Firewall Manager?](https://docs.aws.amazon.com/waf/latest/developerguide/what-is-aws-waf.html)
7. [What is Amazon S3?](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html)