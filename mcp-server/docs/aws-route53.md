What is Amazon Route 53? - Amazon Route 53 

What is Amazon Route 53? - Amazon Route 53
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
"name" : "Amazon Route 53",
"item" : "https://docs.aws.amazon.com/route53/index.html"
},
{
"@type" : "ListItem",
"position" : 3,
"name" : "Developer Guide",
"item" : "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide"
},
{
"@type" : "ListItem",
"position" : 4,
"name" : "What is Amazon Route 53?",
"item" : "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/Welcome.html"
}
]
}

[Documentation](/index.html)[Amazon Route 53](/route53/index.html)[Developer Guide](Welcome.html)

# What is Amazon Route 53?

Amazon Route 53 is a highly available and scalable Domain Name System (DNS) web service. You can use Route 53 to perform three main functions
in any combination: domain registration, DNS routing, and health checking.

If you choose to use Route 53 for all three functions, be sure to follow the order below:

**1. Register domain names**
:   Your website needs a name, such as example.com. Route 53 lets you register a name for your website or web application,
    known as a *domain name*.

    * For an overview, see [How domain registration works](./welcome-domain-registration.html).
    * For a procedure, see [Registering a new domain](./domain-register.html).
    * For a tutorial that takes you through registering a domain and creating a simple website in an Amazon S3 bucket, see
      [Getting started with Amazon Route 53](./getting-started.html).

**2. Route internet traffic to the resources for your domain**
:   When a user opens a web browser and enters your domain name (example.com) or subdomain name (acme.example.com) in the address bar,
    Route 53 helps connect the browser with your website or web application.

    * For an overview, see [How internet traffic is routed to your website or web application](./welcome-dns-service.html).
    * For procedures, see [Configuring Amazon Route 53 as your DNS service](./dns-configuring.html).
    * For a procedure on how to route email to Amazon WorkMail, see [Routing traffic to Amazon WorkMail](./routing-to-workmail.html).

**3. Check the health of your resources**
:   Route 53 sends automated requests over the internet to a resource, such as a web server, to verify that it's reachable, available,
    and functional. You also can choose to receive notifications when a resource becomes unavailable and choose to route internet traffic
    away from unhealthy resources.

    * For an overview, see [How Amazon Route 53 checks the health of your resources](./welcome-health-checks.html).
    * For procedures, see [Creating Amazon Route 53 health checks](./dns-failover.html).

###### Other Route 53 features

In addition to being a Domain Name System (DNS) web service, Route 53 offers the following
features:

**VPC Resolver**
:   Get recursive DNS for your Amazon VPCs in AWS Regions, VPCs in AWS Outposts racks, or any other on-premises networks.
    Create conditional forwarding rules and
    Route 53 endpoints to resolve custom names mastered in Route 53 private hosted zones or in your on-premises DNS servers.

    For more information , see [What is Route 53 VPC Resolver?](./resolver.html).

**Amazon Route 53 Resolver on Outposts**
:   Connect VPC Resolver on Outpost racks with DNS servers in your on-premises data
    centers through Resolver endpoints. This enables resolution of DNS queries between
    the Outposts racks and your other on-premises resources.

    For more information , see [What is Amazon Route 53 on Outposts?](./outpost-resolver.html).

**Resolver DNS Firewall**
:   Protect your recursive DNS queries within the VPC Resolver. Create domain lists and build firewall rules that filter outbound DNS traffic against these rules.

    For more information , see [Using DNS Firewall to filter outbound DNS traffic](./resolver-dns-firewall.html).

**Traffic Flow**
:   Easy-to-use and cost-effective global traffic management: route end users to the best endpoint for your application based on geoproximity, latency, health, and other considerations.

    For more information , see [Using Traffic Flow to route DNS traffic](./traffic-flow.html).

**Amazon Route 53 Profiles**
:   With Route 53 Profiles, you can apply and manage DNS-related Route 53 configurations across many VPCs and in different AWS account.

    For more information , see [What are Amazon Route 53 Profiles?](./profiles.html).

###### Topics

* [How domain registration works](./welcome-domain-registration.html)
* [How internet traffic is routed to your website or web application](./welcome-dns-service.html)
* [How Amazon Route 53 checks the health of your resources](./welcome-health-checks.html)
* [Amazon Route 53 concepts](./route-53-concepts.html)
* [How to get started with Amazon Route 53](./welcome-how-to-get-started.html)
* [Accessing Amazon Route 53](./welcome-accessing-route-53.html)
* [AWS Identity and Access Management](./IAMRoute53.html)
* [Amazon Route 53 pricing and billing](./Route53Pricing.html)
* [Using Route 53 with an AWS SDK](./sdk-general-information-section.html)

**Javascript is disabled or is unavailable in your browser.**

To use the Amazon Web Services Documentation, Javascript must be enabled. Please refer to your browser's Help pages for instructions.

[Document Conventions](/general/latest/gr/docconventions.html)

How domain registration works

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.