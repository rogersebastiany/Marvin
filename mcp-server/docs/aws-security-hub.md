Introduction to AWS Security Hub CSPM - AWS Security Hub 

Introduction to AWS Security Hub CSPM - AWS Security Hub
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
"name" : "AWS Security Hub",
"item" : "https://docs.aws.amazon.com/securityhub/index.html"
},
{
"@type" : "ListItem",
"position" : 3,
"name" : "
User Guide
",
"item" : "https://docs.aws.amazon.com/securityhub/latest/userguide"
},
{
"@type" : "ListItem",
"position" : 4,
"name" : "Introduction to AWS Security Hub CSPM",
"item" : "https://docs.aws.amazon.com/securityhub/latest/userguide/what-is-securityhub.html"
}
]
}

[Documentation](/index.html)[AWS Security Hub](/securityhub/index.html)[User Guide](what-are-securityhub-services.html)

[Benefits of Security Hub CSPM](#securityhub-benefits)[Accessing Security Hub CSPM](#securityhub-get-started)[Related services](#securityhub-related-services)[Security Hub CSPM free trial, usage, and pricing](#securityhub-free-trial)

# Introduction to AWS Security Hub CSPM

AWS Security Hub Cloud Security Posture Management (AWS Security Hub CSPM)
provides you with a comprehensive view of your security state in AWS and helps you assess
your AWS environment against security industry standards and best practices.

AWS Security Hub CSPM
collects security data across AWS accounts, AWS services, and supported third-party
products and helps you analyze your security trends and identify the highest priority
security issues.

To help you manage the security state of your organization, Security Hub CSPM supports multiple security standards. These include
the AWS Foundational Security Best Practices (FSBP) standard developed by AWS, and external compliance frameworks such as
the Center for Internet Security (CIS), the Payment Card Industry Data Security Standard (PCI DSS), and the National Institute of
Standards and Technology (NIST). Each standard includes several security controls, each of which represents a security best practice.
Security Hub CSPM runs checks against security controls and generates control findings to help you assess your compliance against security best practices.

In addition to generating control findings, Security Hub CSPM also receives findings from other AWS services—such as Amazon GuardDuty,
Amazon Inspector, and Amazon Macie— and supported third-party
products. This gives you a single pane of glass into a variety of security-related issues. You can also send Security Hub CSPM findings to other
AWS services and supported third-party products.

Security Hub CSPM offers automation features that help you triage and remediate security issues. For example,
you can use automation rules to automatically update critical findings when a security check fails. You can also leverage the integration with
Amazon EventBridge to trigger automatic responses to specific findings.

###### Topics

* [Benefits of Security Hub CSPM](#securityhub-benefits)
* [Accessing Security Hub CSPM](#securityhub-get-started)
* [Related services](#securityhub-related-services)
* [Security Hub CSPM free trial and pricing](#securityhub-free-trial)
* [Concepts and terminology in Security Hub CSPM](./securityhub-concepts.html)
* [Enabling Security Hub CSPM](./securityhub-settingup.html)
* [Managing administrator and member accounts in Security Hub CSPM](./securityhub-accounts.html)
* [Understanding cross-Region aggregation in Security Hub CSPM](./finding-aggregation.html)
* [Understanding security standards in Security Hub CSPM](./standards-view-manage.html)
* [Understanding security controls in Security Hub CSPM](./controls-view-manage.html)
* [Understanding integrations in Security Hub CSPM](./securityhub-findings-providers.html)
* [Creating and updating findings in Security Hub CSPM](./securityhub-findings.html)
* [Viewing insights in Security Hub CSPM](./securityhub-insights.html)
* [Automatically modifying and acting on findings in Security Hub CSPM](./automations.html)
* [Working with the dashboard in Security Hub CSPM](./dashboard.html)
* [Regional limits for Security Hub CSPM](./securityhub-regions.html)
* [Creating Security Hub CSPM resources with CloudFormation](./creating-resources-with-cloudformation.html)
* [Subscribing to Security Hub CSPM announcements with Amazon SNS](./securityhub-announcements.html)
* [Disabling Security Hub CSPM](./securityhub-disable.html)
* [Security in AWS Security Hub CSPM](./security.html)
* [Logging Security Hub API calls with CloudTrail](./securityhub-ct.html)

## Benefits of Security Hub CSPM

Here are some of the key ways that Security Hub CSPM helps you monitor your compliance and security posture across your AWS environment.

Reduced effort to collect and prioritize findings
:   Security Hub CSPM reduces the effort to collect and prioritize security findings across accounts from
    integrated AWS services and AWS partner products. Security Hub CSPM processes finding data using the AWS Security Finding Format (ASFF),
    a standard finding format. This eliminates the need to manage findings from myriad sources in multiple formats. Security Hub CSPM also
    correlates findings across providers to help you prioritize the most important ones.

Automatic security checks against best practices and standards
:   Security Hub CSPM automatically runs continuous, account-level configuration and security checks based on AWS best practices and industry
    standards. Security Hub CSPM uses the results of these checks to calculate security scores, and identifies specific accounts and resources that require
    attention.

Consolidated view of findings across accounts and providers
:   Security Hub CSPM consolidates your security findings across accounts and provider products and displays results on the Security Hub CSPM console. You can
    also retrieve findings through the Security Hub CSPM API, AWS CLI, or SDKs. With a holistic view of your current security status, you can spot trends, identify potential issues, and take necessary
    remediation steps.

Ability to automate finding updates and remediation
:   You can create automation rules that modify or suppress findings based on your defined criteria. Security Hub CSPM also supports an integration with Amazon EventBridge. To automate the remediation of specific findings, you can define custom actions to take when a
    finding is generated. For example, you can configure custom actions to send findings to a ticketing system or to an automated remediation system.

## Accessing Security Hub CSPM

Security Hub CSPM is available in most AWS Regions. For a list of Regions where Security Hub CSPM is currently
available, see [AWS Security Hub CSPM endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/sechub.html) in the
*AWS General Reference*. For information about managing AWS Regions
for your AWS account, see [Specifying which AWS Regions your account can use](https://docs.aws.amazon.com/accounts/latest/reference/manage-acct-regions.html)
in the *AWS Account Management Reference Guide*.

In each Region, you can access and use Security Hub CSPM in any of the following ways:

**Security Hub CSPM console**
:   The AWS Management Console is a browser-based interface that you can use to create and manage AWS
    resources. As part of that console, the Security Hub CSPM console provides access to your Security Hub CSPM
    account, data, and resources. You can perform Security Hub CSPM tasks by using the Security Hub CSPM
    console—view findings, create automation rules, create an aggregation Region, and more.

**Security Hub CSPM API**
:   The Security Hub CSPM API gives you programmatic access to your Security Hub CSPM
    account, data, and resources. With the API, you can send HTTPS requests directly to Security Hub CSPM.
    For information about the API, see the *[AWS Security Hub API Reference](https://docs.aws.amazon.com/securityhub/1.0/APIReference/)*.

**AWS CLI**
:   With the AWS CLI, you can run commands at your system's command line to
    perform Security Hub CSPM tasks. In some cases, using the command line can be faster and more convenient
    than using the console. The command line is also useful if you want to build scripts
    that perform tasks. For information about installing and using the AWS CLI, see the [AWS Command Line Interface User Guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html).

**AWS SDKs**
:   AWS provides SDKs that consist of libraries and sample code for various programming
    languages and platforms—for example, Java, Go, Python, C++, and .NET. The SDKs provide
    convenient, programmatic access to Security Hub CSPM and other AWS services in your preferred language. They also handle tasks such
    as cryptographically signing requests, managing errors, and retrying requests automatically.
    For information about installing and using the AWS SDKs, see [Tools to Build on AWS](https://aws.amazon.com/developertools/).

###### Important

Security Hub CSPM only detects and consolidates findings that are generated after you enable Security Hub CSPM. It doesn't retroactively detect and consolidate
security findings that were generated before you enabled Security Hub CSPM.

Security Hub CSPM only receives and processes findings in the Region where you enabled Security Hub CSPM in your account.

For full compliance with CIS AWS Foundations Benchmark security checks, you must enable Security Hub CSPM in all supported AWS Regions.

## Related services

To further secure your AWS environment, consider using other
AWS services in combination with Security Hub CSPM. Some AWS services send their findings to Security Hub CSPM, and Security Hub CSPM normalizes the findings
into a standard format. Some AWS services can also receive findings from Security Hub CSPM.

For a list of other AWS services that send or receive Security Hub CSPM findings, see
[AWS service integrations with Security Hub CSPM](./securityhub-internal-providers.html).

Security Hub CSPM uses service-linked rules from AWS Config to run security checks for most controls. Controls refer to specific
AWS services and AWS resources. For a list of Security Hub CSPM controls, see
[Control reference for Security Hub CSPM](./securityhub-controls-reference.html). You must enable
AWS Config and record resources in AWS Config for Security Hub CSPM to generate most control findings. For more information, see
[Considerations before enabling and configuring AWS Config](./securityhub-setup-prereqs.html#securityhub-prereq-config).

## Security Hub CSPM free trial and pricing

When you enable Security Hub CSPM in an AWS account for the first time, that account is automatically enrolled in a 30-day
Security Hub CSPM free trial.

When you use Security Hub CSPM during the free trial, you are charged for usage of other services that Security Hub CSPM interacts with, such as AWS Config items. You are not
charged for AWS Config rules that are activated only by Security Hub CSPM security standards.

You are not charged for using Security Hub CSPM until your free trial ends.

### Viewing usage details

Security Hub CSPM provides usage information, including the number of security checks and findings
processed by your account. The usage details also include the time remaining in the
free trial. This information can help you understand your Security Hub CSPM usage after the free
trial ends. The usage information is also available after the free trial ends.

###### To display usage information (console)

1. Open the AWS Security Hub CSPM console at <https://console.aws.amazon.com/securityhub/>.
2. In the navigation pane, choose **Usage** under **Settings**.

The usage information is only for the current account and current Region. In an
aggregation Region, the usage information doesn't include linked Regions. For more
information about linked Regions, see [Types of data that are aggregated](./finding-aggregation.html#finding-aggregation-overview).

To view cost details for your account, use the [AWS Billing
console](https://console.aws.amazon.com/billing/).

### Pricing details

For more information about how Security Hub CSPM charges for ingested findings and security
checks, see [Security Hub CSPM
pricing](https://aws.amazon.com/security-hub/pricing/).

**Javascript is disabled or is unavailable in your browser.**

To use the Amazon Web Services Documentation, Javascript must be enabled. Please refer to your browser's Help pages for instructions.

[Document Conventions](/general/latest/gr/docconventions.html)

Logging API calls

Concepts

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.