---
subcategory: "WAF"
layout: "aws"
page\_title: "AWS: aws\_wafv2\_web\_acl"
description: |-
Creates a WAFv2 Web ACL resource.
---
# Resource: aws\_wafv2\_web\_acl
Creates a WAFv2 Web ACL resource.
~> \*\*Note:\*\* Inline `rule` blocks in this resource have several known limitations. Consider using [`aws\_wafv2\_web\_acl\_rule`](/docs/providers/aws/r/wafv2\_web\_acl\_rule.html) to manage rules as separate resources instead. Limitations include: \*\*Deletion ordering errors:\*\* When removing a rule that references an IP set or rule group, AWS requires the rule to be detached before the referenced resource is deleted. Terraform's dependency graph cannot model this correctly for inline rules, resulting in `WAFAssociatedItemException` errors. \*\*Spurious diffs:\*\* AWS returns rules in an unpredictable order, which can cause Terraform to detect changes even when the configuration has not changed. \*\*Coupled updates:\*\* Modifying one inline rule may cause all rules to be recreated, which can be disruptive.
!> \*\*Warning:\*\* If you use the `aws\_wafv2\_web\_acl\_rule` or `aws\_wafv2\_web\_acl\_rule\_group\_association` resources with this Web ACL, you must add `lifecycle { ignore\_changes = [rule] }` to this resource to prevent configuration drift. Those resources manage the Web ACL's rules outside of this resource's direct management.
## Example Usage
This resource is based on `aws\_wafv2\_rule\_group`, check the documentation of the `aws\_wafv2\_rule\_group` resource to see examples of the various available statements.
### Managed Rule
```terraform
resource "aws\_wafv2\_web\_acl" "example" {
name = "managed-rule-example"
description = "Example of a managed rule."
scope = "REGIONAL"
default\_action {
allow {}
}
rule {
name = "rule-1"
priority = 1
override\_action {
count {}
}
statement {
managed\_rule\_group\_statement {
name = "AWSManagedRulesCommonRuleSet"
vendor\_name = "AWS"
rule\_action\_override {
action\_to\_use {
count {}
}
name = "SizeRestrictions\_QUERYSTRING"
}
rule\_action\_override {
action\_to\_use {
count {}
}
name = "NoUserAgent\_HEADER"
}
scope\_down\_statement {
geo\_match\_statement {
country\_codes = ["US", "NL"]
}
}
}
}
visibility\_config {
cloudwatch\_metrics\_enabled = false
metric\_name = "friendly-rule-metric-name"
sampled\_requests\_enabled = false
}
}
tags = {
Tag1 = "Value1"
Tag2 = "Value2"
}
token\_domains = ["mywebsite.com", "myotherwebsite.com"]
visibility\_config {
cloudwatch\_metrics\_enabled = false
metric\_name = "friendly-metric-name"
sampled\_requests\_enabled = false
}
}
```
### Account Creation Fraud Prevention
```terraform
resource "aws\_wafv2\_web\_acl" "acfp-example" {
name = "managed-acfp-example"
description = "Example of a managed ACFP rule."
scope = "CLOUDFRONT"
default\_action {
allow {}
}
rule {
name = "acfp-rule-1"
priority = 1
override\_action {
count {}
}
statement {
managed\_rule\_group\_statement {
name = "AWSManagedRulesACFPRuleSet"
vendor\_name = "AWS"
managed\_rule\_group\_configs {
aws\_managed\_rules\_acfp\_rule\_set {
creation\_path = "/signin"
registration\_page\_path = "/register"
request\_inspection {
email\_field {
identifier = "/email"
}
password\_field {
identifier = "/password"
}
payload\_type = "JSON"
username\_field {
identifier = "/username"
}
}
response\_inspection {
status\_code {
failure\_codes = ["403"]
success\_codes = ["200"]
}
}
}
}
}
}
visibility\_config {
cloudwatch\_metrics\_enabled = false
metric\_name = "friendly-rule-metric-name"
sampled\_requests\_enabled = false
}
}
visibility\_config {
cloudwatch\_metrics\_enabled = false
metric\_name = "friendly-metric-name"
sampled\_requests\_enabled = false
}
}
```
### Account Takeover Protection
```terraform
resource "aws\_wafv2\_web\_acl" "atp-example" {
name = "managed-atp-example"
description = "Example of a managed ATP rule."
scope = "CLOUDFRONT"
default\_action {
allow {}
}
rule {
name = "atp-rule-1"
priority = 1
override\_action {
count {}
}
statement {
managed\_rule\_group\_statement {
name = "AWSManagedRulesATPRuleSet"
vendor\_name = "AWS"
managed\_rule\_group\_configs {
aws\_managed\_rules\_atp\_rule\_set {
login\_path = "/api/1/signin"
request\_inspection {
password\_field {
identifier = "/password"
}
payload\_type = "JSON"
username\_field {
identifier = "/email"
}
}
response\_inspection {
status\_code {
failure\_codes = ["403"]
success\_codes = ["200"]
}
}
}
}
}
}
visibility\_config {
cloudwatch\_metrics\_enabled = false
metric\_name = "friendly-rule-metric-name"
sampled\_requests\_enabled = false
}
}
visibility\_config {
cloudwatch\_metrics\_enabled = false
metric\_name = "friendly-metric-name"
sampled\_requests\_enabled = false
}
}
```
### Rate Based
Rate-limit US and NL-based clients to 10,000 requests for every 5 minutes.
```terraform
resource "aws\_wafv2\_web\_acl" "example" {
name = "rate-based-example"
description = "Example of a Cloudfront rate based statement."
scope = "CLOUDFRONT"
default\_action {
allow {}
}
rule {
name = "rule-1"
priority = 1
action {
block {}
}
statement {
rate\_based\_statement {
limit = 10000
aggregate\_key\_type = "IP"
scope\_down\_statement {
geo\_match\_statement {
country\_codes = ["US", "NL"]
}
}
}
}
visibility\_config {
cloudwatch\_metrics\_enabled = false
metric\_name = "friendly-rule-metric-name"
sampled\_requests\_enabled = false
}
}
tags = {
Tag1 = "Value1"
Tag2 = "Value2"
}
visibility\_config {
cloudwatch\_metrics\_enabled = false
metric\_name = "friendly-metric-name"
sampled\_requests\_enabled = false
}
}
```
### Rule Group Reference
```terraform
resource "aws\_wafv2\_rule\_group" "example" {
capacity = 10
name = "example-rule-group"
scope = "REGIONAL"
rule {
name = "rule-1"
priority = 1
action {
count {}
}
statement {
geo\_match\_statement {
country\_codes = ["NL"]
}
}
visibility\_config {
cloudwatch\_metrics\_enabled = false
metric\_name = "friendly-rule-metric-name"
sampled\_requests\_enabled = false
}
}
rule {
name = "rule-to-exclude-a"
priority = 10
action {
allow {}
}
statement {
geo\_match\_statement {
country\_codes = ["US"]
}
}
visibility\_config {
cloudwatch\_metrics\_enabled = false
metric\_name = "friendly-rule-metric-name"
sampled\_requests\_enabled = false
}
}
rule {
name = "rule-to-exclude-b"
priority = 15
action {
allow {}
}
statement {
geo\_match\_statement {
country\_codes = ["GB"]
}
}
visibility\_config {
cloudwatch\_metrics\_enabled = false
metric\_name = "friendly-rule-metric-name"
sampled\_requests\_enabled = false
}
}
visibility\_config {
cloudwatch\_metrics\_enabled = false
metric\_name = "friendly-metric-name"
sampled\_requests\_enabled = false
}
}
resource "aws\_wafv2\_web\_acl" "test" {
name = "rule-group-example"
scope = "REGIONAL"
default\_action {
block {}
}
rule {
name = "rule-1"
priority = 1
override\_action {
count {}
}
statement {
rule\_group\_reference\_statement {
arn = aws\_wafv2\_rule\_group.example.arn
rule\_action\_override {
action\_to\_use {
count {}
}
name = "rule-to-exclude-b"
}
rule\_action\_override {
action\_to\_use {
count {}
}
name = "rule-to-exclude-a"
}
}
}
visibility\_config {
cloudwatch\_metrics\_enabled = false
metric\_name = "friendly-rule-metric-name"
sampled\_requests\_enabled = false
}
}
tags = {
Tag1 = "Value1"
Tag2 = "Value2"
}
visibility\_config {
cloudwatch\_metrics\_enabled = false
metric\_name = "friendly-metric-name"
sampled\_requests\_enabled = false
}
}
```
### Large Request Body Inspections for Regional Resources
```terraform
resource "aws\_wafv2\_web\_acl" "example" {
name = "large-request-body-example"
scope = "REGIONAL"
default\_action {
allow {}
}
association\_config {
request\_body {
api\_gateway {
default\_size\_inspection\_limit = "KB\_64"
}
app\_runner\_service {
default\_size\_inspection\_limit = "KB\_64"
}
cognito\_user\_pool {
default\_size\_inspection\_limit = "KB\_64"
}
verified\_access\_instance {
default\_size\_inspection\_limit = "KB\_64"
}
}
}
visibility\_config {
cloudwatch\_metrics\_enabled = false
metric\_name = "friendly-metric-name"
sampled\_requests\_enabled = false
}
}
```
## Argument Reference
This resource supports the following arguments:
\* `association\_config` - (Optional) Specifies custom configurations for the associations between the web ACL and protected resources. See [`association\_config`](#association\_config-block) below for details.
\* `captcha\_config` - (Optional) Specifies how AWS WAF should handle CAPTCHA evaluations on the ACL level (used by [AWS Bot Control](https://docs.aws.amazon.com/waf/latest/developerguide/aws-managed-rule-groups-bot.html)). See [`captcha\_config`](#captcha\_config-block) below for details.
\* `challenge\_config` - (Optional) Specifies how AWS WAF should handle Challenge evaluations on the ACL level (used by [AWS Bot Control](https://docs.aws.amazon.com/waf/latest/developerguide/aws-managed-rule-groups-bot.html)). See [`challenge\_config`](#challenge\_config-block) below for details.
\* `custom\_response\_body` - (Optional) Defines custom response bodies that can be referenced by `custom\_response` actions. See [`custom\_response\_body`](#custom\_response\_body-block) below for details.
\* `data\_protection\_config` - (Optional) Specifies data protection to apply to the web request data for the web ACL. This is a web ACL level data protection option. See [`data\_protection\_config`](#data\_protection\_config-block) below for details.
\* `default\_action` - (Required) Action to perform if none of the `rules` contained in the WebACL match. See [`default\_action`](#default\_action-block) below for details.
\* `description` - (Optional) Friendly description of the WebACL.
\* `name` - (Optional, Forces new resource) Friendly name of the WebACL. If omitted, Terraform will assign a random, unique name. Conflicts with `name\_prefix`.
\* `name\_prefix` - (Optional) Creates a unique name beginning with the specified prefix. Conflicts with `name`.
\* `region` - (Optional) Region where this resource will be [managed](https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints). Defaults to the Region set in the [provider configuration](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference).
\* `rule\_json` (Optional) Raw JSON string to allow more than three nested statements. Conflicts with `rule` attribute. This is for advanced use cases where more than 3 levels of nested statements are required. \*\*There is no drift detection at this time\*\*. If you use this attribute instead of `rule`, you will be foregoing drift detection. Additionally, importing an existing web ACL into a configuration with `rule\_json` set will result in a one time in-place update as the remote rule configuration is initially written to the `rule` attribute. See the AWS [documentation](https://docs.aws.amazon.com/waf/latest/APIReference/API\_CreateWebACL.html) for the JSON structure.
\* `rule` - (Optional) \*\*`rule` blocks in this resource have several known limitations.\*\* Consider using [`aws\_wafv2\_web\_acl\_rule`](/docs/providers/aws/r/wafv2\_web\_acl\_rule.html) to manage rules as separate resources instead. Rule blocks used to identify the web requests that you want to `allow`, `block`, or `count`. See [`rule`](#rule-block) below for details.
\* `scope` - (Required, Forces new resource) Specifies whether this is for an AWS CloudFront distribution or for a regional application. Valid values are `CLOUDFRONT` or `REGIONAL`. To work with CloudFront, you must also specify the region `us-east-1` (N. Virginia) on the AWS provider.
\* `tags` - (Optional) Map of key-value pairs to associate with the resource. If configured with a provider [`default\_tags` configuration block](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#default\_tags-configuration-block) present, tags with matching keys will overwrite those defined at the provider-level.
\* `token\_domains` - (Optional) Specifies the domains that AWS WAF should accept in a web request token. This enables the use of tokens across multiple protected websites. When AWS WAF provides a token, it uses the domain of the AWS resource that the web ACL is protecting. If you don't specify a list of token domains, AWS WAF accepts tokens only for the domain of the protected resource. With a token domain list, AWS WAF accepts the resource's host domain plus all domains in the token domain list, including their prefixed subdomains.
\* `visibility\_config` - (Required) Defines and enables Amazon CloudWatch metrics and web request sample collection. See [`visibility\_config`](#visibility\_config-block) below for details.
### `association\_config` Block
The `association\_config` block supports the following arguments:
\* `request\_body` - (Optional) Customizes the request body that your protected resource forward to AWS WAF for inspection. See [`request\_body`](#request\_body-block) below for details.
### `custom\_response\_body` Block
Each `custom\_response\_body` block supports the following arguments:
\* `key` - (Required) Unique key identifying the custom response body. This is referenced by the `custom\_response\_body\_key` argument in the [`custom\_response`](#custom\_response-block) block.
\* `content` - (Required) Payload of the custom response.
\* `content\_type` - (Required) Type of content in the payload that you are defining in the `content` argument. Valid values are `TEXT\_PLAIN`, `TEXT\_HTML`, or `APPLICATION\_JSON`.
### `data\_protection\_config` Block
The `data\_protection\_config` block supports the following arguments:
\* `data\_protection` - (Required) A block for data protection configurations for specific web request field types. See [`data\_protection`](#data\_protection-block) block for details.
### `data\_protection` Block
Each `data\_protection` block supports the following arguments:
\* `action` - (Required) Specifies how to protect the field. Valid values are `SUBSTITUTION` or `HASH`.
\* `field` - (Required) Specifies the field type and optional keys to apply the protection behavior to. See [`field`](#field-block) block below for details.
\* `exclude\_rate\_based\_details` - (Optional) Boolean to specify whether to also exclude any rate-based rule details from the data protection you have enabled for a given field.
\* `exclude\_rule\_match\_details` - (Optional) Boolean to specify whether to also exclude any rule match details from the data protection you have enabled for a given field. AWS WAF logs these details for non-terminating matching rules and for the terminating matching rule.
### `field` Block
The `field` block supports the following arguments:
\* `field\_type` - (Required) Specifies the web request component type to protect. Valid Values are `SINGLE\_HEADER`, `SINGLE\_COOKIE`, `SINGLE\_QUERY\_ARGUMENT`, `QUERY\_STRING`, `BODY`.
\* `field\_keys` - (Optional) Array of strings to specify the keys to protect for the specified field type. If you don't specify any key, then all keys for the field type are protected.
### `default\_action` Block
The `default\_action` block supports the following arguments:
~> \*\*Note\*\* One of `allow` or `block` is required when specifying a `default\_action`
\* `allow` - (Optional) Specifies that AWS WAF should allow requests by default. See [`allow`](#allow-block) below for details.
\* `block` - (Optional) Specifies that AWS WAF should block requests by default. See [`block`](#block-block) below for details.
### `rule` Block
~> \*\*Note:\*\* `rule` blocks in this resource have several known limitations. Consider using [`aws\_wafv2\_web\_acl\_rule`](/docs/providers/aws/r/wafv2\_web\_acl\_rule.html) to manage rules as separate resources instead.
One of `action` or `override\_action` is required when specifying a rule.
Each `rule` supports the following arguments:
\* `action` - (Optional) Action that AWS WAF should take on a web request when it matches the rule's statement. This is used only for rules whose \*\*statements do not reference a rule group\*\*. See [`action`](#action-block) for details.
\* `captcha\_config` - (Optional) Specifies how AWS WAF should handle CAPTCHA evaluations. See [`captcha\_config`](#captcha\_config-block) below for details.
\* `challenge\_config` - (Optional) Specifies how AWS WAF should handle Challenge evaluations on the rule level. See [`challenge\_config`](#challenge\_config-block) below for details.
\* `name` - (Required) Friendly name of the rule. Note that the provider assumes that rules with names matching this pattern, `^ShieldMitigationRuleGroup\_\_\_.\*`, are AWS-added for [automatic application layer DDoS mitigation activities](https://docs.aws.amazon.com/waf/latest/developerguide/ddos-automatic-app-layer-response-rg.html). Such rules will be ignored by the provider unless you explicitly include them in your configuration (for example, by using the AWS CLI to discover their properties and creating matching configuration). However, since these rules are owned and managed by AWS, you may get permission errors.
\* `override\_action` - (Optional) Override action to apply to the rules in a rule group. Used only for rule \*\*statements that reference a rule group\*\*, like `rule\_group\_reference\_statement` and `managed\_rule\_group\_statement`. See [`override\_action`](#override\_action-block) below for details.
\* `priority` - (Required) If you define more than one Rule in a WebACL, AWS WAF evaluates each request against the `rules` in order based on the value of `priority`. AWS WAF processes rules with lower priority first.
\* `rule\_label` - (Optional) Labels to apply to web requests that match the rule match statement. See [`rule\_label`](#rule\_label-block) below for details.
\* `statement` - (Required) The AWS WAF processing statement for the rule, for example `byte\_match\_statement` or `geo\_match\_statement`. See [`statement`](#statement-block) below for details.
\* `visibility\_config` - (Required) Defines and enables Amazon CloudWatch metrics and web request sample collection. See [`visibility\_config`](#visibility\_config-block) below for details.
### `action` Block
The `action` block supports the following arguments:
~> \*\*Note\*\* One of `allow`, `block`, or `count`, is required when specifying an `action`.
\* `allow` - (Optional) Instructs AWS WAF to allow the web request. See [`allow`](#allow-block) below for details.
\* `block` - (Optional) Instructs AWS WAF to block the web request. See [`block`](#block-block) below for details.
\* `captcha` - (Optional) Instructs AWS WAF to run a Captcha check against the web request. See [`captcha`](#captcha-block) below for details.
\* `challenge` - (Optional) Instructs AWS WAF to run a check against the request to verify that the request is coming from a legitimate client session. See [`challenge`](#challenge-block) below for details.
\* `count` - (Optional) Instructs AWS WAF to count the web request and allow it. See [`count`](#count-block) below for details.
### `override\_action` Block
The `override\_action` block supports the following arguments:
~> \*\*Note\*\* One of `count` or `none`, expressed as an empty configuration block `{}`, is required when specifying an `override\_action`
\* `count` - (Optional) Override the rule action setting to count (i.e., only count matches). Configured as an empty block `{}`.
\* `none` - (Optional) Don't override the rule action setting. Configured as an empty block `{}`.
### `allow` Block
The `allow` block supports the following arguments:
\* `custom\_request\_handling` - (Optional) Defines custom handling for the web request. See [`custom\_request\_handling`](#custom\_request\_handling-block) below for details.
### `block` Block
The `block` block supports the following arguments:
\* `custom\_response` - (Optional) Defines a custom response for the web request. See [`custom\_response`](#custom\_response-block) below for details.
### `captcha` Block
The `captcha` block supports the following arguments:
\* `custom\_request\_handling` - (Optional) Defines custom handling for the web request. See [`custom\_request\_handling`](#custom\_request\_handling-block) below for details.
### `challenge` Block
The `challenge` block supports the following arguments:
\* `custom\_request\_handling` - (Optional) Defines custom handling for the web request. See [`custom\_request\_handling`](#custom\_request\_handling-block) below for details.
### `count` Block
The `count` block supports the following arguments:
\* `custom\_request\_handling` - (Optional) Defines custom handling for the web request. See [`custom\_request\_handling`](#custom\_request\_handling-block) below for details.
### `custom\_request\_handling` Block
The `custom\_request\_handling` block supports the following arguments:
\* `insert\_header` - (Required) The `insert\_header` blocks used to define HTTP headers added to the request. See [`insert\_header`](#insert\_header-block) below for details.
### `insert\_header` Block
Each `insert\_header` block supports the following arguments. Duplicate header names are not allowed:
\* `name` - Name of the custom header. For custom request header insertion, when AWS WAF inserts the header into the request, it prefixes this name `x-amzn-waf-`, to avoid confusion with the headers that are already in the request. For example, for the header name `sample`, AWS WAF inserts the header `x-amzn-waf-sample`.
\* `value` - Value of the custom header.
### `custom\_response` Block
The `custom\_response` block supports the following arguments:
\* `custom\_response\_body\_key` - (Optional) References the response body that you want AWS WAF to return to the web request client. This must reference a `key` defined in a `custom\_response\_body` block of this resource.
\* `response\_code` - (Required) The HTTP status code to return to the client.
\* `response\_header` - (Optional) The `response\_header` blocks used to define the HTTP response headers added to the response. See [`response\_header`](#response\_header-block) below for details.
### `response\_header` Block
Each `response\_header` block supports the following arguments. Duplicate header names are not allowed:
\* `name` - Name of the custom header. For custom request header insertion, when AWS WAF inserts the header into the request, it prefixes this name `x-amzn-waf-`, to avoid confusion with the headers that are already in the request. For example, for the header name `sample`, AWS WAF inserts the header `x-amzn-waf-sample`.
\* `value` - Value of the custom header.
### `rule\_label` Block
Each block supports the following arguments:
\* `name` - Label string.
### `statement` Block
The processing guidance for a Rule, used by AWS WAF to determine whether a web request matches the rule. See the [documentation](https://docs.aws.amazon.com/waf/latest/developerguide/waf-rule-statements-list.html) for more information.
-> \*\*Note\*\* Although the `statement` block is recursive, currently only 3 levels are supported.
The `statement` block supports the following arguments:
\* `and\_statement` - (Optional) Logical rule statement used to combine other rule statements with AND logic. See [`and\_statement`](#and\_statement-block) below for details.
\* `asn\_match\_statement` - (Optional) Rule statement that inspects web traffic based on the Autonomous System Number (ASN) associated with the request's IP address. See [`asn\_match\_statement`](#asn\_match\_statement-block) below for details.
\* `byte\_match\_statement` - (Optional) Rule statement that defines a string match search for AWS WAF to apply to web requests. See [`byte\_match\_statement`](#byte\_match\_statement-block) below for details.
\* `geo\_match\_statement` - (Optional) Rule statement used to identify web requests based on country of origin. See [`geo\_match\_statement`](#geo\_match\_statement-block) below for details.
\* `ip\_set\_reference\_statement` - (Optional) Rule statement used to detect web requests coming from particular IP addresses or address ranges. See [`ip\_set\_reference\_statement`](#ip\_set\_reference\_statement-block) below for details.
\* `label\_match\_statement` - (Optional) Rule statement that defines a string match search against labels that have been added to the web request by rules that have already run in the web ACL. See [`label\_match\_statement`](#label\_match\_statement-block) below for details.
\* `managed\_rule\_group\_statement` - (Optional) Rule statement used to run the rules that are defined in a managed rule group. This statement can not be nested. See [`managed\_rule\_group\_statement`](#managed\_rule\_group\_statement-block) below for details.
\* `not\_statement` - (Optional) Logical rule statement used to negate the results of another rule statement. See [`not\_statement`](#not\_statement-block) below for details.
\* `or\_statement` - (Optional) Logical rule statement used to combine other rule statements with OR logic. See [`or\_statement`](#or\_statement-block) below for details.
\* `rate\_based\_statement` - (Optional) Rate-based rule tracks the rate of requests for each originating `IP address`, and triggers the rule action when the rate exceeds a limit that you specify on the number of requests in any specified time span. This statement can not be nested. See [`rate\_based\_statement`](#rate\_based\_statement-block) below for details.
\* `regex\_match\_statement` - (Optional) Rule statement used to search web request components for a match against a single regular expression. See [`regex\_match\_statement`](#regex\_match\_statement-block) below for details.
\* `regex\_pattern\_set\_reference\_statement` - (Optional) Rule statement used to search web request components for matches with regular expressions. See [`regex\_pattern\_set\_reference\_statement`](#regex\_pattern\_set\_reference\_statement-block) below for details.
\* `rule\_group\_reference\_statement` - (Optional) Rule statement used to run the rules that are defined in an WAFv2 Rule Group. See [`rule\_group\_reference\_statement`](#rule\_group\_reference\_statement-block) below for details.
\* `size\_constraint\_statement` - (Optional) Rule statement that compares a number of bytes against the size of a request component, using a comparison operator, such as greater than (>) or less than (<). See [`size\_constraint\_statement`](#size\_constraint\_statement-block) below for more details.
\* `sqli\_match\_statement` - (Optional) An SQL injection match condition identifies the part of web requests, such as the URI or the query string, that you want AWS WAF to inspect. See [`sqli\_match\_statement`](#sqli\_match\_statement-block) below for details.
\* `xss\_match\_statement` - (Optional) Rule statement that defines a cross-site scripting (XSS) match search for AWS WAF to apply to web requests. See [`xss\_match\_statement`](#xss\_match\_statement-block) below for details.
### `and\_statement` Block
A logical rule statement used to combine other rule statements with `AND` logic. You provide more than one `statement` within the `and\_statement`.
The `and\_statement` block supports the following arguments:
\* `statement` - (Required) Statements to combine with `AND` logic. You can use any statements that can be nested. See [`statement`](#statement-block) above for details.
### `asn\_match\_statement` Block
A rule statement that inspects web traffic based on the Autonomous System Number (ASN) associated with the request's IP address.
The `asn\_match\_statement` block supports the following arguments:
\* `asn\_list` - (Required) List of Autonomous System Numbers (ASNs).
\* `forwarded\_ip\_config` - (Optional) Configuration for inspecting IP addresses in an HTTP header that you specify, instead of using the IP address that's reported by the web request origin. See [`forwarded\_ip\_config`](#forwarded\_ip\_config-block) below for more details.
### `byte\_match\_statement` Block
The byte match statement provides the bytes to search for, the location in requests that you want AWS WAF to search, and other settings. The bytes to search for are typically a string that corresponds with ASCII characters.
The `byte\_match\_statement` block supports the following arguments:
\* `field\_to\_match` - (Optional) Part of a web request that you want AWS WAF to inspect. See [`field\_to\_match`](#field\_to\_match-block) below for details.
\* `positional\_constraint` - (Required) Area within the portion of a web request that you want AWS WAF to search for `search\_string`. Valid values include the following: `EXACTLY`, `STARTS\_WITH`, `ENDS\_WITH`, `CONTAINS`, `CONTAINS\_WORD`. See the AWS [documentation](https://docs.aws.amazon.com/waf/latest/APIReference/API\_ByteMatchStatement.html) for more information.
\* `search\_string` - (Required) String value that you want AWS WAF to search for. AWS WAF searches only in the part of web requests that you designate for inspection in `field\_to\_match`. The maximum length of the value is 50 bytes.
\* `text\_transformation` - (Required) Text transformations eliminate some of the unusual formatting that attackers use in web requests in an effort to bypass detection. At least one transformation is required. See [`text\_transformation`](#text\_transformation-block) below for details.
### `geo\_match\_statement` Block
The `geo\_match\_statement` block supports the following arguments:
\* `country\_codes` - (Required) Array of two-character country codes, for example, [ "US", "CN" ], from the alpha-2 country ISO codes of the `ISO 3166` international standard. See the [documentation](https://docs.aws.amazon.com/waf/latest/APIReference/API\_GeoMatchStatement.html) for valid values.
\* `forwarded\_ip\_config` - (Optional) Configuration for inspecting IP addresses in an HTTP header that you specify, instead of using the IP address that's reported by the web request origin. See [`forwarded\_ip\_config`](#forwarded\_ip\_config-block) below for details.
### `ip\_set\_reference\_statement` Block
A rule statement used to detect web requests coming from particular IP addresses or address ranges. To use this, create an `aws\_wafv2\_ip\_set` that specifies the addresses you want to detect, then use the `ARN` of that set in this statement.
The `ip\_set\_reference\_statement` block supports the following arguments:
\* `arn` - (Required) The Amazon Resource Name (ARN) of the IP Set that this statement references.
\* `ip\_set\_forwarded\_ip\_config` - (Optional) Configuration for inspecting IP addresses in an HTTP header that you specify, instead of using the IP address that's reported by the web request origin. See [`ip\_set\_forwarded\_ip\_config`](#ip\_set\_forwarded\_ip\_config-block) below for more details.
### `label\_match\_statement` Block
The `label\_match\_statement` block supports the following arguments:
\* `scope` - (Required) Specify whether you want to match using the label name or just the namespace. Valid values are `LABEL` or `NAMESPACE`.
\* `key` - (Required) String to match against.
### `managed\_rule\_group\_statement` Block
A rule statement used to run the rules that are defined in a managed rule group.
You can't nest a `managed\_rule\_group\_statement`, for example for use inside a `not\_statement` or `or\_statement`. It can only be referenced as a `top-level` statement within a `rule`.
The `managed\_rule\_group\_statement` block supports the following arguments:
\* `name` - (Required) Name of the managed rule group.
\* `rule\_action\_override` - (Optional) Action settings to use in the place of the rule actions that are configured inside the rule group. You specify one override for each rule whose action you want to change. See [`rule\_action\_override`](#rule\_action\_override-block) below for details.
\* `managed\_rule\_group\_configs`- (Optional) Additional information that's used by a managed rule group. Only one rule attribute is allowed in each config. See [`managed\_rule\_group\_configs`](#managed\_rule\_group\_configs-block) for more details
\* `scope\_down\_statement` - Narrows the scope of the statement to matching web requests. This can be any nestable statement, and you can nest statements at any level below this scope-down statement. See [`statement`](#statement-block) above for details.
\* `vendor\_name` - (Required) Name of the managed rule group vendor.
\* `version` - (Optional) Version of the managed rule group. You can set `Version\_1.0` or `Version\_1.1` etc. If you want to use the default version, do not set anything.
### `not\_statement` Block
A logical rule statement used to negate the results of another rule statement. You provide one `statement` within the `not\_statement`.
The `not\_statement` block supports the following arguments:
\* `statement` - (Required) Statement to negate. You can use any statement that can be nested. See [`statement`](#statement-block) above for details.
### `or\_statement` Block
A logical rule statement used to combine other rule statements with `OR` logic. You provide more than one `statement` within the `or\_statement`.
The `or\_statement` block supports the following arguments:
\* `statement` - (Required) Statements to combine with `OR` logic. You can use any statements that can be nested. See [`statement`](#statement-block) above for details.
### `rate\_based\_statement` Block
A rate-based rule tracks the rate of requests for each originating IP address, and triggers the rule action when the rate exceeds a limit that you specify on the number of requests in any 5-minute time span. You can use this to put a temporary block on requests from an IP address that is sending excessive requests. See the [documentation](https://docs.aws.amazon.com/waf/latest/APIReference/API\_RateBasedStatement.html) for more information.
You can't nest a `rate\_based\_statement`, for example for use inside a `not\_statement` or `or\_statement`. It can only be referenced as a `top-level` statement within a `rule`.
The `rate\_based\_statement` block supports the following arguments:
\* `aggregate\_key\_type` - (Optional) Setting that indicates how to aggregate the request counts. Valid values include: `CONSTANT`, `CUSTOM\_KEYS`, `FORWARDED\_IP`, or `IP`. Default: `IP`.
\* `custom\_key` - (Optional) Aggregate the request counts using one or more web request components as the aggregate keys. See [`custom\_key`](#custom\_key-block) below for details.
\* `evaluation\_window\_sec` - (Optional) The amount of time, in seconds, that AWS WAF should include in its request counts, looking back from the current time. Valid values are `60`, `120`, `300`, and `600`. Defaults to `300` (5 minutes).
\*\*NOTE:\*\* This setting doesn't determine how often AWS WAF checks the rate, but how far back it looks each time it checks. AWS WAF checks the rate about every 10 seconds.
\* `forwarded\_ip\_config` - (Optional) Configuration for inspecting IP addresses in an HTTP header that you specify, instead of using the IP address that's reported by the web request origin. If `aggregate\_key\_type` is set to `FORWARDED\_IP`, this block is required. See [`forwarded\_ip\_config`](#forwarded\_ip\_config-block) below for details.
\* `limit` - (Required) Limit on requests during the specified evaluation window for a single aggregation instance.
\* `scope\_down\_statement` - (Optional) Optional nested statement that narrows the scope of the rate-based statement to matching web requests. This can be any nestable statement, and you can nest statements at any level below this scope-down statement. See [`statement`](#statement-block) above for details. If `aggregate\_key\_type` is set to `CONSTANT`, this block is required.
### `regex\_match\_statement` Block
A rule statement used to search web request components for a match against a single regular expression.
The `regex\_match\_statement` block supports the following arguments:
\* `regex\_string` - (Required) String representing the regular expression. Minimum of `1` and maximum of `512` characters.
\* `field\_to\_match` - (Required) The part of a web request that you want AWS WAF to inspect. See [`field\_to\_match`](#field\_to\_match-block) below for details.
\* `text\_transformation` - (Required) Text transformations eliminate some of the unusual formatting that attackers use in web requests in an effort to bypass detection. At least one transformation is required. See [`text\_transformation`](#text\_transformation-block) below for details.
### `regex\_pattern\_set\_reference\_statement` Block
A rule statement used to search web request components for matches with regular expressions. To use this, create a `aws\_wafv2\_regex\_pattern\_set` that specifies the expressions that you want to detect, then use the `ARN` of that set in this statement. A web request matches the pattern set rule statement if the request component matches any of the patterns in the set.
The `regex\_pattern\_set\_reference\_statement` block supports the following arguments:
\* `arn` - (Required) The Amazon Resource Name (ARN) of the Regex Pattern Set that this statement references.
\* `field\_to\_match` - (Optional) Part of a web request that you want AWS WAF to inspect. See [`field\_to\_match`](#field\_to\_match-block) below for details.
\* `text\_transformation` - (Required) Text transformations eliminate some of the unusual formatting that attackers use in web requests in an effort to bypass detection. At least one transformation is required. See [`text\_transformation`](#text\_transformation-block) below for details.
### `rule\_group\_reference\_statement` Block
A rule statement used to run the rules that are defined in an WAFv2 Rule Group or `aws\_wafv2\_rule\_group` resource.
You can't nest a `rule\_group\_reference\_statement`, for example for use inside a `not\_statement` or `or\_statement`. It can only be referenced as a `top-level` statement within a `rule`.
The `rule\_group\_reference\_statement` block supports the following arguments:
\* `arn` - (Required) The Amazon Resource Name (ARN) of the `aws\_wafv2\_rule\_group` resource.
\* `rule\_action\_override` - (Optional) Action settings to use in the place of the rule actions that are configured inside the rule group. You specify one override for each rule whose action you want to change. See [`rule\_action\_override`](#rule\_action\_override-block) below for details.
### `size\_constraint\_statement` Block
A rule statement that uses a comparison operator to compare a number of bytes against the size of a request component. AWS WAFv2 inspects up to the first 8192 bytes (8 KB) of a request body, and when inspecting the request URI Path, the slash `/` in
the URI counts as one character.
The `size\_constraint\_statement` block supports the following arguments:
\* `comparison\_operator` - (Required) Operator to use to compare the request part to the size setting. Valid values include: `EQ`, `NE`, `LE`, `LT`, `GE`, or `GT`.
\* `field\_to\_match` - (Optional) Part of a web request that you want AWS WAF to inspect. See [`field\_to\_match`](#field\_to\_match-block) below for details.
\* `size` - (Required) Size, in bytes, to compare to the request part, after any transformations. Valid values are integers between 0 and 21474836480, inclusive.
\* `text\_transformation` - (Required) Text transformations eliminate some of the unusual formatting that attackers use in web requests in an effort to bypass detection. At least one transformation is required. See [`text\_transformation`](#text\_transformation-block) below for details.
### `sqli\_match\_statement` Block
An SQL injection match condition identifies the part of web requests, such as the URI or the query string, that you want AWS WAF to inspect. Later in the process, when you create a web ACL, you specify whether to allow or block requests that appear to contain malicious SQL code.
The `sqli\_match\_statement` block supports the following arguments:
\* `field\_to\_match` - (Optional) Part of a web request that you want AWS WAF to inspect. See [`field\_to\_match`](#field\_to\_match-block) below for details.
\* `sensitivity\_level` - (Optional) Sensitivity that you want AWS WAF to use to inspect for SQL injection attacks. Valid values include: `LOW`, `HIGH`.
\* `text\_transformation` - (Required) Text transformations eliminate some of the unusual formatting that attackers use in web requests in an effort to bypass detection. At least one transformation is required. See [`text\_transformation`](#text\_transformation-block) below for details.
### `xss\_match\_statement` Block
The XSS match statement provides the location in requests that you want AWS WAF to search and text transformations to use on the search area before AWS WAF searches for character sequences that are likely to be malicious strings.
The `xss\_match\_statement` block supports the following arguments:
\* `field\_to\_match` - (Optional) Part of a web request that you want AWS WAF to inspect. See [`field\_to\_match`](#field\_to\_match-block) below for details.
\* `text\_transformation` - (Required) Text transformations eliminate some of the unusual formatting that attackers use in web requests in an effort to bypass detection. At least one transformation is required. See [`text\_transformation`](#text\_transformation-block) below for details.
### `rule\_action\_override` Block
The `rule\_action\_override` block supports the following arguments:
\* `action\_to\_use` - (Required) Override action to use, in place of the configured action of the rule in the rule group. See [`action`](#action-block) for details.
\* `name` - (Required) Name of the rule to override. See the [documentation](https://docs.aws.amazon.com/waf/latest/developerguide/aws-managed-rule-groups-list.html) for a list of names in the appropriate rule group in use.
### `managed\_rule\_group\_configs` Block
The `managed\_rule\_group\_configs` block support the following arguments:
\* `aws\_managed\_rules\_bot\_control\_rule\_set` - (Optional) Additional configuration for using the Bot Control managed rule group. Use this to specify the inspection level that you want to use. See [`aws\_managed\_rules\_bot\_control\_rule\_set`](#aws\_managed\_rules\_bot\_control\_rule\_set-block) for more details
\* `aws\_managed\_rules\_acfp\_rule\_set` - (Optional) Additional configuration for using the Account Creation Fraud Prevention managed rule group. Use this to specify information such as the registration page of your application and the type of content to accept or reject from the client.
\* `aws\_managed\_rules\_anti\_ddos\_rule\_set` - (Optional) Configuration for using the anti-DDoS managed rule group. See [`aws\_managed\_rules\_anti\_ddos\_rule\_set`](#aws\_managed\_rules\_anti\_ddos\_rule\_set-block) for more details.
\* `aws\_managed\_rules\_atp\_rule\_set` - (Optional) Additional configuration for using the Account Takeover Protection managed rule group. Use this to specify information such as the sign-in page of your application and the type of content to accept or reject from the client.
\* `login\_path` - (Optional, \*\*Deprecated\*\*) The path of the login endpoint for your application.
\* `password\_field` - (Optional, \*\*Deprecated\*\*) Details about your login page password field. See [`password\_field`](#password\_field-block) for more details.
\* `payload\_type`- (Optional, \*\*Deprecated\*\*) The payload type for your login endpoint, either JSON or form encoded.
\* `username\_field` - (Optional, \*\*Deprecated\*\*) Details about your login page username field. See [`username\_field`](#username\_field-block) for more details.
### `aws\_managed\_rules\_bot\_control\_rule\_set` Block
\* `enable\_machine\_learning` - (Optional) Applies only to the targeted inspection level. Determines whether to use machine learning (ML) to analyze your web traffic for bot-related activity. Defaults to `true`.
\* `inspection\_level` - (Optional) The inspection level to use for the Bot Control rule group.
### `aws\_managed\_rules\_acfp\_rule\_set` Block
\* `creation\_path` - (Required) The path of the account creation endpoint for your application. This is the page on your website that accepts the completed registration form for a new user. This page must accept POST requests.
\* `enable\_regex\_in\_path` - (Optional) Whether or not to allow the use of regular expressions in the login page path.
\* `registration\_page\_path` - (Required) The path of the account registration endpoint for your application. This is the page on your website that presents the registration form to new users. This page must accept GET text/html requests.
\* `request\_inspection` - (Optional) The criteria for inspecting login requests, used by the ATP rule group to validate credentials usage. See [`request\_inspection`](#request\_inspection-block-acfp) for more details.
\* `response\_inspection` - (Optional) The criteria for inspecting responses to login requests, used by the ATP rule group to track login failure rates. Note that Response Inspection is available only on web ACLs that protect CloudFront distributions. See [`response\_inspection`](#response\_inspection-block) for more details.
### `request\_inspection` Block (ACFP)
\* `addressFields` (Optional) The names of the fields in the request payload that contain your customer's primary physical address. See [`addressFields`](#address\_fields-block) for more details.
\* `emailField` (Optional) The name of the field in the request payload that contains your customer's email. See [`emailField`](#email\_field-block) for more details.
\* `passwordField` (Optional) Details about your login page password field. See [`passwordField`](#password\_field-block) for more details.
\* `payloadType` (Required) The payload type for your login endpoint, either JSON or form encoded.
\* `phoneNumberFields` (Optional) The names of the fields in the request payload that contain your customer's primary phone number. See [`phoneNumberFields`](#phone\_number\_fields-block) for more details.
\* `usernameField` (Optional) Details about your login page username field. See [`usernameField`](#username\_field-block) for more details.
### `aws\_managed\_rules\_anti\_ddos\_rule\_set` Block
\* `client\_side\_action\_config` - (Required) Configuration for the request handling that's applied by the managed rule group rules `ChallengeAllDuringEvent` and `ChallengeDDoSRequests` during a distributed denial of service (DDoS) attack. See [`client\_side\_action\_config`](#client\_side\_action\_config-block) for more details.
\* `sensitivity\_to\_block` - (Optional) Sensitivity that the rule group rule DDoSRequests uses when matching against the DDoS suspicion labeling on a request. Valid values are `LOW` (Default), `MEDIUM`, and `HIGH`.
### `client\_side\_action\_config` Block
\* `challenge` - (Required) Configuration for the use of the `AWSManagedRulesAntiDDoSRuleSet` rules `ChallengeAllDuringEvent` and `ChallengeDDoSRequests`.
\* `exempt\_uri\_regular\_expression` - (Optional) Block for the list of the regular expressions to match against the web request URI, used to identify requests that can't handle a silent browser challenge.
\* `regex\_string` - (Optional) Regular expression string.
\* `sensitivity` - (Optional) Sensitivity that the rule group rule ChallengeDDoSRequests uses when matching against the DDoS suspicion labeling on a request. Valid values are `LOW`, `MEDIUM` and `HIGH` (Default).
\* `usage\_of\_action` - (Required) Configuration whether to use the `AWSManagedRulesAntiDDoSRuleSet` rules `ChallengeAllDuringEvent` and `ChallengeDDoSRequests` in the rule group evaluation. Valid values are `ENABLED` and `DISABLED`.
### `aws\_managed\_rules\_atp\_rule\_set` Block
\* `enable\_regex\_in\_path` - (Optional) Whether or not to allow the use of regular expressions in the login page path.
\* `login\_path` - (Required) The path of the login endpoint for your application.
\* `request\_inspection` - (Optional) The criteria for inspecting login requests, used by the ATP rule group to validate credentials usage. See [`request\_inspection`](#request\_inspection-block) for more details.
\* `response\_inspection` - (Optional) The criteria for inspecting responses to login requests, used by the ATP rule group to track login failure rates. Note that Response Inspection is available only on web ACLs that protect CloudFront distributions. See [`response\_inspection`](#response\_inspection-block) for more details.
### `request\_inspection` Block
\* `password\_field` (Optional) Details about your login page password field. See [`password\_field`](#password\_field-block) for more details.
\* `payload\_type` (Required) The payload type for your login endpoint, either JSON or form encoded.
\* `username\_field` (Optional) Details about your login page username field. See [`username\_field`](#username\_field-block) for more details.
### `address\_fields` Block
\* `identifiers` - (Required) The names of the address fields.
### `email\_field` Block
\* `identifier` - (Required) The name of the field in the request payload that contains your customer's email.
### `password\_field` Block
\* `identifier` - (Required) The name of the password field.
### `phone\_number\_fields` Block
\* `identifiers` - (Required) The names of the phone number fields.
### `username\_field` Block
\* `identifier` - (Required) The name of the username field.
### `response\_inspection` Block
\* `body\_contains` (Optional) Configures inspection of the response body. See [`body\_contains`](#body\_contains-block) for more details.
\* `header` (Optional) Configures inspection of the response header.See [`header`](#header-block) for more details.
\* `json` (Optional) Configures inspection of the response JSON. See [`json`](#json-block) for more details.
\* `status\_code` (Optional) Configures inspection of the response status code.See [`status\_code`](#status\_code-block) for more details.
### `body\_contains` Block
\* `success\_strings` (Required) Strings in the body of the response that indicate a successful login attempt.
\* `failure\_strings` (Required) Strings in the body of the response that indicate a failed login attempt.
### `header` Block
\* `name` (Required) The name of the header to match against. The name must be an exact match, including case.
\* `success\_values` (Required) Values in the response header with the specified name that indicate a successful login attempt.
\* `failure\_values` (Required) Values in the response header with the specified name that indicate a failed login attempt.
### `json` Block
\* `identifier` (Required) The identifier for the value to match against in the JSON.
\* `success\_strings` (Required) Strings in the body of the response that indicate a successful login attempt.
\* `failure\_strings` (Required) Strings in the body of the response that indicate a failed login attempt.
### `status\_code` Block
\* `success\_codes` (Required) Status codes in the response that indicate a successful login attempt.
\* `failure\_codes` (Required) Status codes in the response that indicate a failed login attempt.
### `field\_to\_match` Block
The part of a web request that you want AWS WAF to inspect. Include the single `field\_to\_match` type that you want to inspect, with additional specifications as needed, according to the type. You specify a single request component in `field\_to\_match` for each rule statement that requires it. To inspect more than one component of a web request, create a separate rule statement for each component. See the [documentation](https://docs.aws.amazon.com/waf/latest/developerguide/waf-rule-statement-fields.html#waf-rule-statement-request-component) for more details.
The `field\_to\_match` block supports the following arguments:
~> \*\*Note\*\* Only one of `all\_query\_arguments`, `body`, `cookies`, `header\_order`, `headers`, `ja3\_fingerprint`, `json\_body`, `method`, `query\_string`, `single\_header`, `single\_query\_argument`, `uri\_fragment` or `uri\_path` can be specified. An empty configuration block `{}` should be used when specifying `all\_query\_arguments`, `method`, or `query\_string` attributes.
\* `all\_query\_arguments` - (Optional) Inspect all query arguments.
\* `body` - (Optional) Inspect the request body, which immediately follows the request headers. See [`body`](#body-block) below for details.
\* `cookies` - (Optional) Inspect the cookies in the web request. See [`cookies`](#cookies-block) below for details.
\* `header\_order` - (Optional) Inspect a string containing the list of the request's header names, ordered as they appear in the web request that AWS WAF receives for inspection. See [`header\_order`](#header\_order-block) below for details.
\* `headers` - (Optional) Inspect the request headers. See [`headers`](#headers-block) below for details.
\* `ja3\_fingerprint` - (Optional) Inspect the JA3 fingerprint. See [`ja3\_fingerprint`](#ja3\_fingerprint-block) below for details.
\* `ja4\_fingerprint` - (Optional) Inspect the JA3 fingerprint. See [`ja4\_fingerprint`](#ja3\_fingerprint-block) below for details.
\* `json\_body` - (Optional) Inspect the request body as JSON. See [`json\_body`](#json\_body-block) for details.
\* `method` - (Optional) Inspect the HTTP method. The method indicates the type of operation that the request is asking the origin to perform.
\* `query\_string` - (Optional) Inspect the query string. This is the part of a URL that appears after a `?` character, if any.
\* `single\_header` - (Optional) Inspect a single header. See [`single\_header`](#single\_header-block) below for details.
\* `single\_query\_argument` - (Optional) Inspect a single query argument. See [`single\_query\_argument`](#single\_query\_argument-block) below for details.
\* `uri\_fragment` - (Optional) Inspect the part of a URL that follows the "#" symbol, providing additional information about the resource. See [`uri\_fragment`](#uri\_fragment-block) below for details.
\* `uri\_path` - (Optional) Inspect the request URI path. This is the part of a web request that identifies a resource, for example, `/images/daily-ad.jpg`.
### `forwarded\_ip\_config` Block
The configuration for inspecting IP addresses in an HTTP header that you specify, instead of using the IP address that's reported by the web request origin. Commonly, this is the X-Forwarded-For (XFF) header, but you can specify any header name. If the specified header isn't present in the request, AWS WAFv2 doesn't apply the rule to the web request at all. AWS WAFv2 only evaluates the first IP address found in the specified HTTP header.
The `forwarded\_ip\_config` block supports the following arguments:
\* `fallback\_behavior` - (Required) - Match status to assign to the web request if the request doesn't have a valid IP address in the specified position. Valid values include: `MATCH` or `NO\_MATCH`.
\* `header\_name` - (Required) - Name of the HTTP header to use for the IP address.
### `ip\_set\_forwarded\_ip\_config` Block
The configuration for inspecting IP addresses in an HTTP header that you specify, instead of using the IP address that's reported by the web request origin. Commonly, this is the X-Forwarded-For (XFF) header, but you can specify any header name.
The `ip\_set\_forwarded\_ip\_config` block supports the following arguments:
\* `fallback\_behavior` - (Required) - Match status to assign to the web request if the request doesn't have a valid IP address in the specified position. Valid values include: `MATCH` or `NO\_MATCH`.
\* `header\_name` - (Required) - Name of the HTTP header to use for the IP address.
\* `position` - (Required) - Position in the header to search for the IP address. Valid values include: `FIRST`, `LAST`, or `ANY`. If `ANY` is specified and the header contains more than 10 IP addresses, AWS WAFv2 inspects the last 10.
### `header\_order` Block
Inspect a string containing the list of the request's header names, ordered as they appear in the web request that AWS WAF receives for inspection. AWS WAF generates the string and then uses that as the field to match component in its inspection. AWS WAF separates the header names in the string using colons and no added spaces, for example `host:user-agent:accept:authorization:referer`.
The `header\_order` block supports the following arguments:
\* `oversize\_handling` - (Required) Oversize handling tells AWS WAF what to do with a web request when the request component that the rule inspects is over the limits. Valid values include the following: `CONTINUE`, `MATCH`, `NO\_MATCH`. See the AWS [documentation](https://docs.aws.amazon.com/waf/latest/developerguide/waf-rule-statement-oversize-handling.html) for more information.
### `headers` Block
Inspect the request headers.
The `headers` block supports the following arguments:
\* `match\_pattern` - (Required) The filter to use to identify the subset of headers to inspect in a web request. The `match\_pattern` block supports only one of the following arguments:
\* `all` - An empty configuration block that is used for inspecting all headers.
\* `included\_headers` - An array of strings that will be used for inspecting headers that have a key that matches one of the provided values.
\* `excluded\_headers` - An array of strings that will be used for inspecting headers that do not have a key that matches one of the provided values.
\* `match\_scope` - (Required) The parts of the headers to inspect with the rule inspection criteria. If you specify `All`, AWS WAF inspects both keys and values. Valid values include the following: `ALL`, `Key`, `Value`.
\* `oversize\_handling` - (Required) Oversize handling tells AWS WAF what to do with a web request when the request component that the rule inspects is over the limits. Valid values include the following: `CONTINUE`, `MATCH`, `NO\_MATCH`. See the AWS [documentation](https://docs.aws.amazon.com/waf/latest/developerguide/waf-rule-statement-oversize-handling.html) for more information.
### `ja3\_fingerprint` Block
The `ja3\_fingerprint` block supports the following arguments:
\* `fallback\_behavior` - (Required) The match status to assign to the web request if the request doesn't have a JA3 fingerprint. Valid values include: `MATCH` or `NO\_MATCH`.
### `ja4\_fingerprint` Block
The `ja4\_fingerprint` block supports the following arguments:
\* `fallback\_behavior` - (Required) The match status to assign to the web request if the request doesn't have a JA4 fingerprint. Valid values include: `MATCH` or `NO\_MATCH`.
### `json\_body` Block
The `json\_body` block supports the following arguments:
\* `invalid\_fallback\_behavior` - (Optional) What to do when JSON parsing fails. Defaults to evaluating up to the first parsing failure. Valid values are `EVALUATE\_AS\_STRING`, `MATCH` and `NO\_MATCH`.
\* `match\_pattern` - (Required) The patterns to look for in the JSON body. You must specify exactly one setting: either `all` or `included\_paths`. See [JsonMatchPattern](https://docs.aws.amazon.com/waf/latest/APIReference/API\_JsonMatchPattern.html) for details.
\* `match\_scope` - (Required) The parts of the JSON to match against using the `match\_pattern`. Valid values are `ALL`, `KEY` and `VALUE`.
\* `oversize\_handling` - (Optional) What to do if the body is larger than can be inspected. Valid values are `CONTINUE` (default), `MATCH` and `NO\_MATCH`.
### `single\_header` Block
Inspect a single header. Provide the name of the header to inspect, for example, `User-Agent` or `Referer` (provided as lowercase strings).
The `single\_header` block supports the following arguments:
\* `name` - (Required) Name of the query header to inspect. This setting must be provided as lower case characters.
### `single\_query\_argument` Block
Inspect a single query argument. Provide the name of the query argument to inspect, such as `UserName` or `SalesRegion` (provided as lowercase strings).
The `single\_query\_argument` block supports the following arguments:
\* `name` - (Required) Name of the query header to inspect. This setting must be provided as lower case characters.
### `uri\_fragment` Block
Inspect the part of a URL that follows the "#" symbol, providing additional information about the resource.
The `uri\_fragment` block supports the following arguments:
\* `fallback\_behavior` - (Optional) What AWS WAF should do if it fails to completely parse the JSON body. Valid values are `MATCH` (default) and `NO\_MATCH`.
### `body` Block
The `body` block supports the following arguments:
\* `oversize\_handling` - (Optional) What WAF should do if the body is larger than WAF can inspect. WAF does not support inspecting the entire contents of the body of a web request when the body exceeds 8 KB (8192 bytes). Only the first 8 KB of the request body are forwarded to WAF by the underlying host service. Valid values: `CONTINUE`, `MATCH`, `NO\_MATCH`.
### `cookies` Block
Inspect the cookies in the web request. You can specify the parts of the cookies to inspect and you can narrow the set of cookies to inspect by including or excluding specific keys. This is used to indicate the web request component to inspect, in the [FieldToMatch](https://docs.aws.amazon.com/waf/latest/APIReference/API\_FieldToMatch.html) specification.
The `cookies` block supports the following arguments:
\* `match\_pattern` - (Required) The filter to use to identify the subset of cookies to inspect in a web request. You must specify exactly one setting: either `all`, `included\_cookies` or `excluded\_cookies`. More details: [CookieMatchPattern](https://docs.aws.amazon.com/waf/latest/APIReference/API\_CookieMatchPattern.html)
\* `match\_scope` - (Required) The parts of the cookies to inspect with the rule inspection criteria. If you specify All, AWS WAF inspects both keys and values. Valid values: `ALL`, `KEY`, `VALUE`
\* `oversize\_handling` - (Required) What AWS WAF should do if the cookies of the request are larger than AWS WAF can inspect. AWS WAF does not support inspecting the entire contents of request cookies when they exceed 8 KB (8192 bytes) or 200 total cookies. The underlying host service forwards a maximum of 200 cookies and at most 8 KB of cookie contents to AWS WAF. Valid values: `CONTINUE`, `MATCH`, `NO\_MATCH`.
### `text\_transformation` Block
The `text\_transformation` block supports the following arguments:
\* `priority` - (Required) Relative processing order for multiple transformations that are defined for a rule statement. AWS WAF processes all transformations, from lowest priority to highest, before inspecting the transformed content.
\* `type` - (Required) Transformation to apply, please refer to the Text Transformation [documentation](https://docs.aws.amazon.com/waf/latest/APIReference/API\_TextTransformation.html) for more details.
### `visibility\_config` Block
The `visibility\_config` block supports the following arguments:
\* `cloudwatch\_metrics\_enabled` - (Required) Whether the associated resource sends metrics to CloudWatch. For the list of available metrics, see [AWS WAF Metrics](https://docs.aws.amazon.com/waf/latest/developerguide/monitoring-cloudwatch.html#waf-metrics).
\* `metric\_name` - (Required) A friendly name of the CloudWatch metric. The name can contain only alphanumeric characters (A-Z, a-z, 0-9) hyphen(-) and underscore (\\_), with length from one to 128 characters. It can't contain whitespace or metric names reserved for AWS WAF, for example `All` and `Default\_Action`.
\* `sampled\_requests\_enabled` - (Required) Whether AWS WAF should store a sampling of the web requests that match the rules. You can view the sampled requests through the AWS WAF console.
### `captcha\_config` Block
The `captcha\_config` block supports the following arguments:
\* `immunity\_time\_property` - (Optional) Defines custom immunity time. See [`immunity\_time\_property`](#immunity\_time\_property-block) below for details.
### `challenge\_config` Block
The `challenge\_config` block supports the following arguments:
\* `immunity\_time\_property` - (Optional) Defines custom immunity time. See [`immunity\_time\_property`](#immunity\_time\_property-block) below for details.
### `immunity\_time\_property` Block
The `immunity\_time\_property` block supports the following arguments:
\* `immunity\_time` - (Optional) The amount of time, in seconds, that a CAPTCHA or challenge timestamp is considered valid by AWS WAF. The default setting is 300.
### `request\_body` Block
The `request\_body` block supports the following arguments:
\* `api\_gateway` - (Optional) Customizes the request body that your protected Amazon API Gateway REST APIs forward to AWS WAF for inspection. Applicable only when `scope` is set to `CLOUDFRONT`. See [`api\_gateway`](#api\_gateway-block) below for details.
\* `app\_runner\_service` - (Optional) Customizes the request body that your protected Amazon App Runner services forward to AWS WAF for inspection. Applicable only when `scope` is set to `REGIONAL`. See [`app\_runner\_service`](#app\_runner\_service-block) below for details.
\* `cloudfront` - (Optional) Customizes the request body that your protected Amazon CloudFront distributions forward to AWS WAF for inspection. Applicable only when `scope` is set to `REGIONAL`. See [`cloudfront`](#cloudfront-block) below for details.
\* `cognito\_user\_pool` - (Optional) Customizes the request body that your protected Amazon Cognito user pools forward to AWS WAF for inspection. Applicable only when `scope` is set to `REGIONAL`. See [`cognito\_user\_pool`](#cognito\_user\_pool-block) below for details.
\* `verified\_access\_instance` - (Optional) Customizes the request body that your protected AWS Verfied Access instances forward to AWS WAF for inspection. Applicable only when `scope` is set to `REGIONAL`. See [`verified\_access\_instance`](#verified\_access\_instance-block) below for details.
### `api\_gateway` Block
The `api\_gateway` block supports the following arguments:
\* `default\_size\_inspection\_limit` - (Required) Specifies the maximum size of the web request body component that an associated Amazon API Gateway REST APIs should send to AWS WAF for inspection. This applies to statements in the web ACL that inspect the body or JSON body. Valid values are `KB\_16`, `KB\_32`, `KB\_48` and `KB\_64`.
### `app\_runner\_service` Block
The `app\_runner\_service` block supports the following arguments:
\* `default\_size\_inspection\_limit` - (Required) Specifies the maximum size of the web request body component that an associated Amazon App Runner services should send to AWS WAF for inspection. This applies to statements in the web ACL that inspect the body or JSON body. Valid values are `KB\_16`, `KB\_32`, `KB\_48` and `KB\_64`.
### `cloudfront` Block
The `cloudfront` block supports the following arguments:
\* `default\_size\_inspection\_limit` - (Required) Specifies the maximum size of the web request body component that an associated Amazon CloudFront distribution should send to AWS WAF for inspection. This applies to statements in the web ACL that inspect the body or JSON body. Valid values are `KB\_16`, `KB\_32`, `KB\_48` and `KB\_64`.
### `cognito\_user\_pool` Block
The `cognito\_user\_pool` block supports the following arguments:
\* `default\_size\_inspection\_limit` - (Required) Specifies the maximum size of the web request body component that an associated Amazon Cognito user pools should send to AWS WAF for inspection. This applies to statements in the web ACL that inspect the body or JSON body. Valid values are `KB\_16`, `KB\_32`, `KB\_48` and `KB\_64`.
### `verified\_access\_instance` Block
The `verified\_access\_instance` block supports the following arguments:
\* `default\_size\_inspection\_limit` - (Required) Specifies the maximum size of the web request body component that an associated AWS Verified Access instances should send to AWS WAF for inspection. This applies to statements in the web ACL that inspect the body or JSON body. Valid values are `KB\_16`, `KB\_32`, `KB\_48` and `KB\_64`.
### `custom\_key` Block
Aggregate the request counts using one or more web request components as the aggregate keys. With this option, you must specify the aggregate keys in the `custom\_keys` block. To aggregate on only the IP address or only the forwarded IP address, don't use custom keys. Instead, set the `aggregate\_key\_type` to `IP` or `FORWARDED\_IP`.
The `custom\_key` block supports the following arguments:
\* `asn` - (Optional) Use an Autonomous System Number (ASN) derived from the request's originating or forwarded IP address as an aggregate key. See [RateLimit `asn`](#ratelimit-asn-block) below for details.
\* `cookie` - (Optional) Use the value of a cookie in the request as an aggregate key. See [RateLimit `cookie`](#ratelimit-cookie-block) below for details.
\* `forwarded\_ip` - (Optional) Use the first IP address in an HTTP header as an aggregate key. See [`forwarded\_ip`](#ratelimit-forwarded\_ip-block) below for details.
\* `http\_method` - (Optional) Use the request's HTTP method as an aggregate key. See [RateLimit `http\_method`](#ratelimit-http\_method-block) below for details.
\* `header` - (Optional) Use the value of a header in the request as an aggregate key. See [RateLimit `header`](#ratelimit-header-block) below for details.
\* `ip` - (Optional) Use the request's originating IP address as an aggregate key. See [`RateLimit ip`](#ratelimit-ip-block) below for details.
\* `ja3\_fingerprint` - (Optional) Use the JA3 fingerprint in the request as an aggregate key. See [`RateLimit ip`](#ratelimit-ja3\_fingerprint-block) below for details.
\* `ja4\_fingerprint` - (Optional) Use the JA3 fingerprint in the request as an aggregate key. See [`RateLimit ip`](#ratelimit-ja4\_fingerprint-block) below for details.
\* `label\_namespace` - (Optional) Use the specified label namespace as an aggregate key. See [RateLimit `label\_namespace`](#ratelimit-label\_namespace-block) below for details.
\* `query\_argument` - (Optional) Use the specified query argument as an aggregate key. See [RateLimit `query\_argument`](#ratelimit-query\_argument-block) below for details.
\* `query\_string` - (Optional) Use the request's query string as an aggregate key. See [RateLimit `query\_string`](#ratelimit-query\_string-block) below for details.
\* `uri\_path` - (Optional) Use the request's URI path as an aggregate key. See [RateLimit `uri\_path`](#ratelimit-uri\_path-block) below for details.
### RateLimit `asn` Block
Use an Autonomous System Number (ASN) derived from the request's originating or forwarded IP address as an aggregate key. Each distinct ASN contributes to the aggregation instance.
The `asn` block is configured as an empty block `{}`.
### RateLimit `cookie` Block
Use the value of a cookie in the request as an aggregate key. Each distinct value in the cookie contributes to the aggregation instance. If you use a single cookie as your custom key, then each value fully defines an aggregation instance.
The `cookie` block supports the following arguments:
\* `name`: The name of the cookie to use.
\* `text\_transformation`: Text transformations eliminate some of the unusual formatting that attackers use in web requests in an effort to bypass detection. They are used in rate-based rule statements, to transform request components before using them as custom aggregation keys. Atleast one transformation is required. See [`text\_transformation`](#text\_transformation-block) above for details.
### RateLimit `forwarded\_ip` Block
Use the first IP address in an HTTP header as an aggregate key. Each distinct forwarded IP address contributes to the aggregation instance. When you specify an IP or forwarded IP in the custom key settings, you must also specify at least one other key to use. You can aggregate on only the forwarded IP address by specifying `FORWARDED\_IP` in your rate-based statement's `aggregate\_key\_type`. With this option, you must specify the header to use in the rate-based rule's [`forwarded\_ip\_config`](#forwarded\_ip\_config-block) block.
The `forwarded\_ip` block is configured as an empty block `{}`.
### RateLimit `http\_method` Block
Use the request's HTTP method as an aggregate key. Each distinct HTTP method contributes to the aggregation instance. If you use just the HTTP method as your custom key, then each method fully defines an aggregation instance.
The `http\_method` block is configured as an empty block `{}`.
### RateLimit `header` Block
Use the value of a header in the request as an aggregate key. Each distinct value in the header contributes to the aggregation instance. If you use a single header as your custom key, then each value fully defines an aggregation instance.
The `header` block supports the following arguments:
\* `name`: The name of the header to use.
\* `text\_transformation`: Text transformations eliminate some of the unusual formatting that attackers use in web requests in an effort to bypass detection. They are used in rate-based rule statements, to transform request components before using them as custom aggregation keys. Atleast one transformation is required. See [`text\_transformation`](#text\_transformation-block) above for details.
### RateLimit `ip` Block
Use the request's originating IP address as an aggregate key. Each distinct IP address contributes to the aggregation instance. When you specify an IP or forwarded IP in the custom key settings, you must also specify at least one other key to use. You can aggregate on only the IP address by specifying `IP` in your rate-based statement's `aggregate\_key\_type`.
The `ip` block is configured as an empty block `{}`.
### RateLimit `ja3\_fingerprint` Block
Use the JA3 fingerprint in the request as an aggregate key. Each distinct JA3 fingerprint contributes to the aggregation instance. You can use this key type once.
The `ja3\_fingerprint` block supports the following arguments:
\* `fallback\_behavior` - (Required) - Match status to assign to the web request if there is insufficient TSL Client Hello information to compute the JA3 fingerprint. Valid values include: `MATCH` or `NO\_MATCH`.
### RateLimit `ja4\_fingerprint` Block
Use the JA3 fingerprint in the request as an aggregate key. Each distinct JA3 fingerprint contributes to the aggregation instance. You can use this key type once.
The `ja4\_fingerprint` block supports the following arguments:
\* `fallback\_behavior` - (Required) - Match status to assign to the web request if there is insufficient TSL Client Hello information to compute the JA4 fingerprint. Valid values include: `MATCH` or `NO\_MATCH`.
### RateLimit `label\_namespace` Block
Use the specified label namespace as an aggregate key. Each distinct fully qualified label name that has the specified label namespace contributes to the aggregation instance. If you use just one label namespace as your custom key, then each label name fully defines an aggregation instance. This uses only labels that have been added to the request by rules that are evaluated before this rate-based rule in the web ACL. For information about label namespaces and names, see Label syntax and naming requirements (https://docs.aws.amazon.com/waf/latest/developerguide/waf-rule-label-requirements.html) in the WAF Developer Guide.
The `label\_namespace` block supports the following arguments:
\* `namespace`: The namespace to use for aggregation
### RateLimit `query\_argument` Block
Use the specified query argument as an aggregate key. Each distinct value for the named query argument contributes to the aggregation instance. If you use a single query argument as your custom key, then each value fully defines an aggregation instance.
The `query\_argument` block supports the following arguments:
\* `name`: The name of the query argument to use.
\* `text\_transformation`: Text transformations eliminate some of the unusual formatting that attackers use in web requests in an effort to bypass detection. They are used in rate-based rule statements, to transform request components before using them as custom aggregation keys. Atleast one transformation is required. See [`text\_transformation`](#text\_transformation-block) above for details.
### RateLimit `query\_string` Block
Use the request's query string as an aggregate key. Each distinct string contributes to the aggregation instance. If you use just the query string as your custom key, then each string fully defines an aggregation instance.
The `query\_string` block supports the following arguments:
\* `text\_transformation`: Text transformations eliminate some of the unusual formatting that attackers use in web requests in an effort to bypass detection. They are used in rate-based rule statements, to transform request components before using them as custom aggregation keys. Atleast one transformation is required. See [`text\_transformation`](#text\_transformation-block) above for details.
### RateLimit `uri\_path` Block
Use the request's URI path as an aggregate key. Each distinct URI path contributes to the aggregation instance. If you use just the URI path as your custom key, then each URI path fully defines an aggregation instance.
The `uri\_path` block supports the following arguments:
\* `text\_transformation`: Text transformations eliminate some of the unusual formatting that attackers use in web requests in an effort to bypass detection. They are used in rate-based rule statements, to transform request components before using them as custom aggregation keys. Atleast one transformation is required. See [`text\_transformation`](#text\_transformation-block) above for details.
## Attribute Reference
This resource exports the following attributes in addition to the arguments above:
\* `application\_integration\_url` - The URL to use in SDK integrations with managed rule groups.
\* `arn` - The ARN of the WAF WebACL.
\* `capacity` - Web ACL capacity units (WCUs) currently being used by this web ACL.
\* `id` - The ID of the WAF WebACL.
\* `tags\_all` - Map of tags assigned to the resource, including those inherited from the provider [`default\_tags` configuration block](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#default\_tags-configuration-block).
## Import
In Terraform v1.5.0 and later, use an [`import` block](https://developer.hashicorp.com/terraform/language/import) to import WAFv2 Web ACLs using `ID/Name/Scope`. For example:
```terraform
import {
to = aws\_wafv2\_web\_acl.example
id = "a1b2c3d4-d5f6-7777-8888-9999aaaabbbbcccc/example/REGIONAL"
}
```
Using `terraform import`, import WAFv2 Web ACLs using `ID/Name/Scope`. For example:
```console
% terraform import aws\_wafv2\_web\_acl.example a1b2c3d4-d5f6-7777-8888-9999aaaabbbbcccc/example/REGIONAL
```