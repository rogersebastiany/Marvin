AWS Shield - AWS WAF, AWS Firewall Manager, AWS Shield Advanced, and AWS Shield network security director 

AWS Shield - AWS WAF, AWS Firewall Manager, AWS Shield Advanced, and AWS Shield network security director
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
"name" : "AWS WAF",
"item" : "https://docs.aws.amazon.com/waf/index.html"
},
{
"@type" : "ListItem",
"position" : 3,
"name" : "Developer Guide",
"item" : "https://docs.aws.amazon.com/waf/latest/developerguide"
},
{
"@type" : "ListItem",
"position" : 4,
"name" : "AWS Shield",
"item" : "https://docs.aws.amazon.com/waf/latest/developerguide/shield-chapter.html"
}
]
}

[Documentation](/index.html)[AWS WAF](/waf/index.html)[Developer Guide](what-is-aws-waf.html)

**Introducing a new console experience for AWS WAF**

You can now use the updated experience to access AWS WAF functionality anywhere in the console.
For more details, see [Working with the console](https://docs.aws.amazon.com/waf/latest/developerguide/working-with-console.html).

# AWS Shield

Protection against Distributed Denial of Service (DDoS) attacks is of primary importance for your internet-facing
applications. When you build your application on AWS, you can make use of protections that
AWS provides at no additional cost. Additionally, you can use the AWS Shield Advanced managed
threat protection service to improve your security posture with additional DDoS detection,
mitigation, and response capabilities.

AWS is committed to providing you with the tools, best practices, and
services to help ensure high availability, security, and resiliency in your defense against bad
actors on the internet. This guide is provided to help IT decision makers and security
engineers understand how to use Shield and Shield Advanced to better protect their applications from DDoS attacks and other external
threats.

When you build your application on AWS,
you receive automatic protection by AWS against common volumetric DDoS attack vectors, like UDP
reflection attacks and TCP SYN floods. You can leverage these protections to ensure the availability
of the applications that you run on AWS by designing and configuring your architecture for DDoS resiliency.

This guide provides recommendations that can help you design, create, and configure your
application architectures for DDoS resiliency. Applications that adhere to the best
practices provided in this guide can benefit from an improved continuity of availability
when they are targeted by larger DDoS attacks and by wider ranges of DDoS attack vectors.
Additionally, this guide shows you how to use Shield Advanced to implement an optimized DDoS
protection posture for your critical applications. These include applications for which
you've guaranteed a certain level of availability to your customers and those that require
operational support from AWS during DDoS events.

Security is a shared responsibility between AWS and you. The [shared
responsibility model](https://aws.amazon.com/compliance/shared-responsibility-model/) describes this as security *of* the cloud and security *in* the cloud:

* **Security of the cloud** – AWS is responsible for protecting the infrastructure that runs AWS services in
  the AWS Cloud. AWS also provides you with services that you can use securely. The effectiveness of our security is regularly tested and verified
  by third-party auditors as part of the [AWS compliance programs](https://aws.amazon.com/compliance/programs/). To learn about
  the compliance programs that apply to Shield Advanced, see [AWS Services in Scope
  by Compliance Program](https://aws.amazon.com/compliance/services-in-scope/).
* **Security in the cloud** – Your responsibility is
  determined by the AWS service that you use. You are also responsible for other factors
  including the sensitivity of your data, your organization’s requirements, and applicable
  laws and regulations.

**Javascript is disabled or is unavailable in your browser.**

To use the Amazon Web Services Documentation, Javascript must be enabled. Please refer to your browser's Help pages for instructions.

[Document Conventions](/general/latest/gr/docconventions.html)

AWS WAF Classic quotas

How Shield and Shield Advanced work

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.