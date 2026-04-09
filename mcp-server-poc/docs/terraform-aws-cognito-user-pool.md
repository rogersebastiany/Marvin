---
subcategory: "Cognito IDP (Identity Provider)"
layout: "aws"
page\_title: "AWS: aws\_cognito\_user\_pool"
description: |-
Provides a Cognito User Pool resource.
---
# Resource: aws\_cognito\_user\_pool
Provides a Cognito User Pool resource.
## Example Usage
### Basic configuration
```terraform
resource "aws\_cognito\_user\_pool" "pool" {
name = "mypool"
}
```
### Enabling SMS and Software Token Multi-Factor Authentication
```terraform
resource "aws\_cognito\_user\_pool" "example" {
# ... other configuration ...
mfa\_configuration = "ON"
sms\_authentication\_message = "Your code is {####}"
sms\_configuration {
external\_id = "example"
sns\_caller\_arn = aws\_iam\_role.example.arn
sns\_region = "us-east-1"
}
software\_token\_mfa\_configuration {
enabled = true
}
}
```
### Using Account Recovery Setting
```terraform
resource "aws\_cognito\_user\_pool" "test" {
name = "mypool"
account\_recovery\_setting {
recovery\_mechanism {
name = "verified\_email"
priority = 1
}
recovery\_mechanism {
name = "verified\_phone\_number"
priority = 2
}
}
}
```
## Argument Reference
This resource supports the following arguments:
\* `region` - (Optional) Region where this resource will be [managed](https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints). Defaults to the Region set in the [provider configuration](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference).
\* `name` - (Required) Name of the user pool.
\* `account\_recovery\_setting` - (Optional) Configuration block to define which verified available method a user can use to recover their forgotten password. [Detailed below](#account\_recovery\_setting).
\* `admin\_create\_user\_config` - (Optional) Configuration block for creating a new user profile. [Detailed below](#admin\_create\_user\_config).
\* `alias\_attributes` - (Optional) Attributes supported as an alias for this user pool. Valid values: `phone\_number`, `email`, or `preferred\_username`. Conflicts with `username\_attributes`.
\* `auto\_verified\_attributes` - (Optional) Attributes to be auto-verified. Valid values: `email`, `phone\_number`.
\* `deletion\_protection` - (Optional) When active, DeletionProtection prevents accidental deletion of your user pool. Before you can delete a user pool that you have protected against deletion, you must deactivate this feature. Valid values are `ACTIVE` and `INACTIVE`, Default value is `INACTIVE`.
\* `device\_configuration` - (Optional) Configuration block for the user pool's device tracking. [Detailed below](#device\_configuration).
\* `email\_configuration` - (Optional) Configuration block for configuring email. [Detailed below](#email\_configuration).
\* `email\_mfa\_configuration` - (Optional) Configuration block for configuring email Multi-Factor Authentication (MFA); requires at least 2 `account\_recovery\_setting` entries; requires an `email\_configuration` configuration block. Effective only when `mfa\_configuration` is `ON` or `OPTIONAL`. [Detailed below](#email\_mfa\_configuration).
\* `email\_verification\_message` - (Optional) String representing the email verification message. Conflicts with `verification\_message\_template` configuration block `email\_message` argument.
\* `email\_verification\_subject` - (Optional) String representing the email verification subject. Conflicts with `verification\_message\_template` configuration block `email\_subject` argument.
\* `lambda\_config` - (Optional) Configuration block for the AWS Lambda triggers associated with the user pool. [Detailed below](#lambda\_config).
\* `mfa\_configuration` - (Optional) Multi-Factor Authentication (MFA) configuration for the User Pool. Defaults of `OFF`. Valid values are `OFF` (MFA Tokens are not required), `ON` (MFA is required for all users to sign in; requires at least one of `email\_mfa\_configuration`, `sms\_configuration` or `software\_token\_mfa\_configuration` to be configured), or `OPTIONAL` (MFA Will be required only for individual users who have MFA Enabled; requires at least one of `email\_mfa\_configuration`, `sms\_configuration` or `software\_token\_mfa\_configuration` to be configured).
\* `password\_policy` - (Optional) Configuration block for information about the user pool password policy. [Detailed below](#password\_policy).
\* `schema` - (Optional) Configuration block for the schema attributes of a user pool. [Detailed below](#schema). Schema attributes from the [standard attribute set](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html#cognito-user-pools-standard-attributes) only need to be specified if they are different from the default configuration. Attributes can be added, but not modified or removed. Maximum of 50 attributes.
\* `sign\_in\_policy` - (Optional) Configuration block for information about the user pool sign in policy. [Detailed below](#sign\_in\_policy).
\* `sms\_authentication\_message` - (Optional) String representing the SMS authentication message. The Message must contain the `{####}` placeholder, which will be replaced with the code.
\* `sms\_configuration` - (Optional) Configuration block for Short Message Service (SMS) settings. [Detailed below](#sms\_configuration). These settings apply to SMS user verification and SMS Multi-Factor Authentication (MFA). SMS MFA is activated only when `mfa\_configuration` is set to `ON` or `OPTIONAL` along with this block. Due to Cognito API restrictions, the SMS configuration cannot be removed without recreating the Cognito User Pool. For user data safety, this resource will ignore the removal of this configuration by disabling drift detection. To force resource recreation after this configuration has been applied, see the [`taint` command](https://www.terraform.io/docs/commands/taint.html).
\* `sms\_verification\_message` - (Optional) String representing the SMS verification message. Conflicts with `verification\_message\_template` configuration block `sms\_message` argument.
\* `software\_token\_mfa\_configuration` - (Optional) Configuration block for software token Mult-Factor Authentication (MFA) settings. Effective only when `mfa\_configuration` is `ON` or `OPTIONAL`. [Detailed below](#software\_token\_mfa\_configuration).
\* `tags` - (Optional) Map of tags to assign to the User Pool. If configured with a provider [`default\_tags` configuration block](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#default\_tags-configuration-block) present, tags with matching keys will overwrite those defined at the provider-level.
\* `user\_attribute\_update\_settings` - (Optional) Configuration block for user attribute update settings. [Detailed below](#user\_attribute\_update\_settings).
\* `user\_pool\_add\_ons` - (Optional) Configuration block for user pool add-ons to enable user pool advanced security mode features. [Detailed below](#user\_pool\_add\_ons).
\* `user\_pool\_tier` - (Optional) The user pool [feature plan](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-sign-in-feature-plans.html), or tier. Valid values: `LITE`, `ESSENTIALS`, `PLUS`.
\* `username\_attributes` - (Optional) Whether email addresses or phone numbers can be specified as usernames when a user signs up. Conflicts with `alias\_attributes`.
\* `username\_configuration` - (Optional) Configuration block for username configuration. [Detailed below](#username\_configuration).
\* `verification\_message\_template` - (Optional) Configuration block for verification message templates. [Detailed below](#verification\_message\_template).
\* `web\_authn\_configuration` - (Optional) Configuration block for web authn configuration. [Detailed below](#web\_authn\_configuration).
### account\_recovery\_setting
\* `recovery\_mechanism` - (Optional) List of Account Recovery Options of the following structure:
\* `name` - (Required) Recovery method for a user. Can be of the following: `verified\_email`, `verified\_phone\_number`, and `admin\_only`.
\* `priority` - (Required) Positive integer specifying priority of a method with 1 being the highest priority.
### admin\_create\_user\_config
\* `allow\_admin\_create\_user\_only` - (Optional) Set to True if only the administrator is allowed to create user profiles. Set to False if users can sign themselves up via an app.
\* `invite\_message\_template` - (Optional) Invite message template structure. [Detailed below](#invite\_message\_template).
#### invite\_message\_template
\* `email\_message` - (Optional) Message template for email messages. Must contain `{username}` and `{####}` placeholders, for username and temporary password, respectively.
\* `email\_subject` - (Optional) Subject line for email messages.
\* `sms\_message` - (Optional) Message template for SMS messages. Must contain `{username}` and `{####}` placeholders, for username and temporary password, respectively.
### device\_configuration
\* `challenge\_required\_on\_new\_device` - (Optional) Whether a challenge is required on a new device. Only applicable to a new device.
\* `device\_only\_remembered\_on\_user\_prompt` - (Optional) Whether a device is only remembered on user prompt. `false` equates to "Always" remember, `true` is "User Opt In," and not using a `device\_configuration` block is "No."
### email\_configuration
\* `configuration\_set` - (Optional) Email configuration set name from SES.
\* `email\_sending\_account` - (Optional) Email delivery method to use. `COGNITO\_DEFAULT` for the default email functionality built into Cognito or `DEVELOPER` to use your Amazon SES configuration. Required to be `DEVELOPER` if `from\_email\_address` is set.
\* `from\_email\_address` - (Optional) Sender’s email address or sender’s display name with their email address (e.g., `john@example.com`, `John Smith ` or `\"John Smith Ph.D.\" `). Escaped double quotes are required around display names that contain certain characters as specified in [RFC 5322](https://tools.ietf.org/html/rfc5322).
\* `reply\_to\_email\_address` - (Optional) REPLY-TO email address.
\* `source\_arn` - (Optional) ARN of the SES verified email identity to use. Required if `email\_sending\_account` is set to `DEVELOPER`.
### email\_mfa\_configuration
\* `message` - (Optional) The template for the email messages that your user pool sends to users with codes for MFA and sign-in with email OTPs. The message must contain the {####} placeholder. In the message, Amazon Cognito replaces this placeholder with the code. If you don't provide this parameter, Amazon Cognito sends messages in the default format.
\* `subject` - (Optional) The subject of the email messages that your user pool sends to users with codes for MFA and email OTP sign-in.
### lambda\_config
\* `create\_auth\_challenge` - (Optional) ARN of the lambda creating an authentication challenge.
\* `custom\_message` - (Optional) Custom Message AWS Lambda trigger.
\* `define\_auth\_challenge` - (Optional) Defines the authentication challenge.
\* `post\_authentication` - (Optional) Post-authentication AWS Lambda trigger.
\* `post\_confirmation` - (Optional) Post-confirmation AWS Lambda trigger.
\* `pre\_authentication` - (Optional) Pre-authentication AWS Lambda trigger.
\* `pre\_sign\_up` - (Optional) Pre-registration AWS Lambda trigger.
\* `pre\_token\_generation` - (Optional) Allow to customize identity token claims before token generation. Set this parameter for legacy purposes; for new instances of pre token generation triggers, set the lambda\_arn of `pre\_token\_generation\_config`.
\* `pre\_token\_generation\_config` - (Optional) Allow to customize access tokens. See [pre\_token\_configuration\_type](#pre\_token\_configuration\_type)
\* `user\_migration` - (Optional) User migration Lambda config type.
\* `verify\_auth\_challenge\_response` - (Optional) Verifies the authentication challenge response.
\* `kms\_key\_id` - (Optional) The Amazon Resource Name of Key Management Service Customer master keys. Amazon Cognito uses the key to encrypt codes and temporary passwords sent to CustomEmailSender and CustomSMSSender.
\* `custom\_email\_sender` - (Optional) A custom email sender AWS Lambda trigger. See [custom\_email\_sender](#custom\_email\_sender) Below.
\* `custom\_sms\_sender` - (Optional) A custom SMS sender AWS Lambda trigger. See [custom\_sms\_sender](#custom\_sms\_sender) Below.
#### custom\_email\_sender
\* `lambda\_arn` - (Required) The Lambda Amazon Resource Name of the Lambda function that Amazon Cognito triggers to send email notifications to users.
\* `lambda\_version` - (Required) The Lambda version represents the signature of the "request" attribute in the "event" information Amazon Cognito passes to your custom email Lambda function. The only supported value is `V1\_0`.
#### custom\_sms\_sender
\* `lambda\_arn` - (Required) The Lambda Amazon Resource Name of the Lambda function that Amazon Cognito triggers to send SMS notifications to users.
\* `lambda\_version` - (Required) The Lambda version represents the signature of the "request" attribute in the "event" information Amazon Cognito passes to your custom SMS Lambda function. The only supported value is `V1\_0`.
#### pre\_token\_configuration\_type
\* `lambda\_arn` - (Required) The Lambda Amazon Resource Name of the Lambda function that Amazon Cognito triggers to customize access tokens. If you also set an ARN in `pre\_token\_generation`, its value must be identical to this one.
\* `lambda\_version` - (Required) The Lambda version represents the signature of the "version" attribute in the "event" information Amazon Cognito passes to your pre Token Generation Lambda function. The supported values are `V1\_0`, `V2\_0`, `V3\_0`.
### password\_policy
\* `minimum\_length` - (Optional) Minimum length of the password policy that you have set.
\* `password\_history\_size` - (Optional) Number of previous passwords that you want Amazon Cognito to restrict each user from reusing. Users can't set a password that matches any of number of previous passwords specified by this argument. A value of 0 means that password history is not enforced. Valid values are between 0 and 24.
\*\*Note:\*\* This argument requires advanced security features to be active in the user pool.
\* `require\_lowercase` - (Optional) Whether you have required users to use at least one lowercase letter in their password.
\* `require\_numbers` - (Optional) Whether you have required users to use at least one number in their password.
\* `require\_symbols` - (Optional) Whether you have required users to use at least one symbol in their password.
\* `require\_uppercase` - (Optional) Whether you have required users to use at least one uppercase letter in their password.
\* `temporary\_password\_validity\_days` - (Optional) In the password policy you have set, refers to the number of days a temporary password is valid. If the user does not sign-in during this time, their password will need to be reset by an administrator.
### sign\_in\_policy
\* `allowed\_first\_auth\_factors` (Optional) The sign in methods your user pool supports as the first factor. This is a list of strings, allowed values are `PASSWORD`, `EMAIL\_OTP`, `SMS\_OTP`, and `WEB\_AUTHN`.
### web\_authn\_configuration
\* `relying\_party\_id` - (Optional) The authentication domain that passkeys providers use as a relying party.
\* `user\_verification` - (Optional) If your user pool should require a passkey. Must be one of `required` or `preferred`.
### schema
~> \*\*NOTE:\*\* When defining an `attribute\_data\_type` of `String` or `Number`, the respective attribute constraints configuration block (e.g `string\_attribute\_constraints` or `number\_attribute\_constraints`) is \*\*required\*\* to prevent recreation of the Terraform resource. This requirement is true for both standard (e.g., name, email) and custom schema attributes.
\* `attribute\_data\_type` - (Required) Attribute data type. Must be one of `Boolean`, `Number`, `String`, `DateTime`.
\* `developer\_only\_attribute` - (Optional) Whether the attribute type is developer only.
\* `mutable` - (Optional) Whether the attribute can be changed once it has been created.
\* `name` - (Required) Name of the attribute.
\* `number\_attribute\_constraints` - (Required when `attribute\_data\_type` is `Number`) Configuration block for the constraints for an attribute of the number type. [Detailed below](#number\_attribute\_constraints).
\* `required` - (Optional) Whether a user pool attribute is required. If the attribute is required and the user does not provide a value, registration or sign-in will fail.
\* `string\_attribute\_constraints` - (Required when `attribute\_data\_type` is `String`) Constraints for an attribute of the string type. [Detailed below](#string\_attribute\_constraints).
#### schema: Defaults for Standard Attributes
The [standard attributes](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html#cognito-user-pools-standard-attributes) have the following defaults. Note that attributes which match the default values are not stored in Terraform state when importing.
```terraform
resource "aws\_cognito\_user\_pool" "example" {
# ... other configuration ...
schema {
name = ""
attribute\_data\_type = ""
developer\_only\_attribute = false
mutable = true # false for "sub"
required = false # true for "sub"
string\_attribute\_constraints { # if it is a string
min\_length = 0 # 10 for "birthdate"
max\_length = 2048 # 10 for "birthdate"
}
}
}
```
#### number\_attribute\_constraints
\* `max\_value` - (Optional) Maximum value of an attribute that is of the number data type.
\* `min\_value` - (Optional) Minimum value of an attribute that is of the number data type.
#### string\_attribute\_constraints
\* `max\_length` - (Optional) Maximum length of an attribute value of the string type.
\* `min\_length` - (Optional) Minimum length of an attribute value of the string type.
### sms\_configuration
\* `external\_id` - (Required) External ID used in IAM role trust relationships. For more information about using external IDs, see [How to Use an External ID When Granting Access to Your AWS Resources to a Third Party](http://docs.aws.amazon.com/IAM/latest/UserGuide/id\_roles\_create\_for-user\_externalid.html).
\* `sns\_caller\_arn` - (Required) ARN of the Amazon SNS caller. This is usually the IAM role that you've given Cognito permission to assume.
\* `sns\_region` - (Optional) The AWS Region to use with Amazon SNS integration. You can choose the same Region as your user pool, or a supported Legacy Amazon SNS alternate Region. Amazon Cognito resources in the Asia Pacific (Seoul) AWS Region must use your Amazon SNS configuration in the Asia Pacific (Tokyo) Region. For more information, see [SMS message settings for Amazon Cognito user pools](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-sms-settings.html).
### software\_token\_mfa\_configuration
The following arguments are required in the `software\_token\_mfa\_configuration` configuration block:
\* `enabled` - (Required) Boolean whether to enable software token Multi-Factor (MFA) tokens, such as Time-based One-Time Password (TOTP). To disable software token MFA When `sms\_configuration` is not present, the `mfa\_configuration` argument must be set to `OFF` and the `software\_token\_mfa\_configuration` configuration block must be fully removed.
### user\_attribute\_update\_settings
\* `attributes\_require\_verification\_before\_update` - (Required) A list of attributes requiring verification before update. If set, the provided value(s) must also be set in `auto\_verified\_attributes`. Valid values: `email`, `phone\_number`.
### user\_pool\_add\_ons
\* `advanced\_security\_additional\_flows` - (Optional) A block to specify the threat protection configuration options for additional authentication types in your user pool, including custom authentication. [Detailed below](#advanced\_security\_additional\_flows).
\* `advanced\_security\_mode` - (Required) Mode for advanced security, must be one of `OFF`, `AUDIT` or `ENFORCED`.
### advanced\_security\_additional\_flows
\* `custom\_auth\_mode` - (Optional) Mode of threat protection operation in custom authentication. Valid values are `AUDIT` or `ENFORCED`. The default value is `AUDIT`.
### username\_configuration
\* `case\_sensitive` - (Optional) Whether username case sensitivity will be applied for all users in the user pool through Cognito APIs.
### verification\_message\_template
\* `default\_email\_option` - (Optional) Default email option. Must be either `CONFIRM\_WITH\_CODE` or `CONFIRM\_WITH\_LINK`. Defaults to `CONFIRM\_WITH\_CODE`.
\* `email\_message` - (Optional) Email message template. Must contain the `{####}` placeholder. Conflicts with `email\_verification\_message` argument.
\* `email\_message\_by\_link` - (Optional) Email message template for sending a confirmation link to the user, it must contain the `{##Click Here##}` placeholder.
\* `email\_subject` - (Optional) Subject line for the email message template. Conflicts with `email\_verification\_subject` argument.
\* `email\_subject\_by\_link` - (Optional) Subject line for the email message template for sending a confirmation link to the user.
\* `sms\_message` - (Optional) SMS message template. Must contain the `{####}` placeholder. Conflicts with `sms\_verification\_message` argument.
## Attribute Reference
This resource exports the following attributes in addition to the arguments above:
\* `arn` - ARN of the user pool.
\* `creation\_date` - Date the user pool was created.
\* `custom\_domain` - A custom domain name that you provide to Amazon Cognito. This parameter applies only if you use a custom domain to host the sign-up and sign-in pages for your application. For example: `auth.example.com`.
\* `domain` - Holds the domain prefix if the user pool has a domain associated with it.
\* `endpoint` - Endpoint name of the user pool. Example format: `cognito-idp.REGION.amazonaws.com/xxxx\_yyyyy`
\* `estimated\_number\_of\_users` - A number estimating the size of the user pool.
\* `id` - ID of the user pool.
\* `last\_modified\_date` - Date the user pool was last modified.
\* `tags\_all` - A map of tags assigned to the resource, including those inherited from the provider [`default\_tags` configuration block](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#default\_tags-configuration-block).
## Import
In Terraform v1.5.0 and later, use an [`import` block](https://developer.hashicorp.com/terraform/language/import) to import Cognito User Pools using the `id`. For example:
```terraform
import {
to = aws\_cognito\_user\_pool.pool
id = "us-west-2\_abc123"
}
```
Using `terraform import`, import Cognito User Pools using the `id`. For example:
```console
% terraform import aws\_cognito\_user\_pool.pool us-west-2\_abc123
```