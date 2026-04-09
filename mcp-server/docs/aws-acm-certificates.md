What is AWS Certificate Manager? - AWS Certificate Manager 

What is AWS Certificate Manager? - AWS Certificate Manager
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
"name" : "AWS Certificate Manager (ACM)",
"item" : "https://docs.aws.amazon.com/acm/index.html"
},
{
"@type" : "ListItem",
"position" : 3,
"name" : "User Guide",
"item" : "https://docs.aws.amazon.com/acm/latest/userguide"
},
{
"@type" : "ListItem",
"position" : 4,
"name" : "What is AWS Certificate Manager?",
"item" : "https://docs.aws.amazon.com/acm/latest/userguide/acm-overview.html"
}
]
}

[Documentation](/index.html)[AWS Certificate Manager (ACM)](/acm/index.html)[User Guide](acm-overview.html)

[Supported Regions](#acm-regions)[Pricing](#acm-billing)

# What is AWS Certificate Manager?

AWS Certificate Manager (ACM) handles the complexity of creating, storing, and renewing public and
private SSL/TLS X.509 certificates and keys that protect your AWS websites and
applications. You can provide certificates for your [integrated
AWS services](./acm-services.html) either by issuing them directly with ACM or by [importing](./import-certificate.html) third-party certificates into the ACM
management system. ACM certificates can secure singular domain names, multiple specific
domain names, wildcard domains, or combinations of these. ACM wildcard certificates can
protect an unlimited number of subdomains. You can also [export](./export-private.html) ACM certificates signed by AWS Private CA for use anywhere in your internal
PKI.

###### Note

ACM is not intended for use with a stand-alone web server. If you want to set up a
stand-alone secure server on an Amazon EC2 instance, the following tutorial has instructions:
[Configure SSL/TLS on Amazon Linux 2023](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/SSL-on-amazon-linux-2023.html).

###### Topics

* [Supported Regions](#acm-regions)
* [Pricing for AWS Certificate Manager](#acm-billing)
* [AWS Certificate Manager concepts](./acm-concepts.html)
* [What is the right AWS certificate service for my needs?](./service-options.html)

## Supported Regions

ACM supports IPv4 and IPv6 on public endpoints. Visit [AWS Regions and Endpoints](https://docs.aws.amazon.com/general/latest/gr/rande.html#acm_region) in the
*AWS General Reference* or the [AWS Region Table](https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/) to see the regional availability for ACM.

Certificates in ACM are regional resources. To use a certificate with Elastic Load Balancing for the
same fully qualified domain name (FQDN) or set of FQDNs in more than one AWS region,
you must request or import a certificate for each region. For certificates provided by
ACM, this means you must revalidate each domain name in the certificate for each
region. You cannot copy a certificate between regions.

To use an ACM certificate with Amazon CloudFront, you must request or import the certificate
in the US East (N. Virginia) region. ACM certificates in this region that are associated
with a CloudFront distribution are distributed to all the geographic locations configured for
that distribution.

## Pricing for AWS Certificate Manager

You are not subject to an additional charge for SSL/TLS certificates that you manage
with AWS Certificate Manager. You pay only for the AWS resources that you create to run your website
or application. For the latest ACM pricing information, see the [AWS Certificate Manager Service Pricing](https://aws.amazon.com/certificate-manager/pricing/)
page on the AWS website.

**Javascript is disabled or is unavailable in your browser.**

To use the Amazon Web Services Documentation, Javascript must be enabled. Please refer to your browser's Help pages for instructions.

[Document Conventions](/general/latest/gr/docconventions.html)

Concepts

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.