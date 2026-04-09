---
subcategory: "ECS (Elastic Container)"
layout: "aws"
page\_title: "AWS: aws\_ecs\_service"
description: |-
Provides an ECS service.
---
# Resource: aws\_ecs\_service
-> \*\*Note:\*\* To prevent a race condition during service deletion, make sure to set `depends\_on` to the related `aws\_iam\_role\_policy`; otherwise, the policy may be destroyed too soon and the ECS service will then get stuck in the `DRAINING` state.
Provides an ECS service - effectively a task that is expected to run until an error occurs or a user terminates it (typically a webserver or a database).
See [ECS Services section in AWS developer guide](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs\_services.html).
## Example Usage
```terraform
resource "aws\_ecs\_service" "mongo" {
name = "mongodb"
cluster = aws\_ecs\_cluster.foo.id
task\_definition = aws\_ecs\_task\_definition.mongo.arn
desired\_count = 3
iam\_role = aws\_iam\_role.foo.arn
depends\_on = [aws\_iam\_role\_policy.foo]
ordered\_placement\_strategy {
type = "binpack"
field = "cpu"
}
load\_balancer {
target\_group\_arn = aws\_lb\_target\_group.foo.arn
container\_name = "mongo"
container\_port = 8080
}
placement\_constraints {
type = "memberOf"
expression = "attribute:ecs.availability-zone in [us-west-2a, us-west-2b]"
}
}
```
### Ignoring Changes to Desired Count
You can utilize the generic Terraform resource [lifecycle configuration block](https://www.terraform.io/docs/configuration/meta-arguments/lifecycle.html) with `ignore\_changes` to create an ECS service with an initial count of running instances, then ignore any changes to that count caused externally (e.g., Application Autoscaling).
```terraform
resource "aws\_ecs\_service" "example" {
# ... other configurations ...
# Example: Create service with 2 instances to start
desired\_count = 2
# Optional: Allow external changes without Terraform plan difference
lifecycle {
ignore\_changes = [desired\_count]
}
}
```
### Daemon Scheduling Strategy
```terraform
resource "aws\_ecs\_service" "bar" {
name = "bar"
cluster = aws\_ecs\_cluster.foo.id
task\_definition = aws\_ecs\_task\_definition.bar.arn
scheduling\_strategy = "DAEMON"
}
```
### CloudWatch Deployment Alarms
```terraform
resource "aws\_ecs\_service" "example" {
name = "example"
cluster = aws\_ecs\_cluster.example.id
alarms {
enable = true
rollback = true
alarm\_names = [
aws\_cloudwatch\_metric\_alarm.example.alarm\_name
]
}
}
```
### External Deployment Controller
```terraform
resource "aws\_ecs\_service" "example" {
name = "example"
cluster = aws\_ecs\_cluster.example.id
deployment\_controller {
type = "EXTERNAL"
}
}
```
### Blue/Green Deployment with SIGINT Rollback
```terraform
resource "aws\_ecs\_service" "example" {
name = "example"
cluster = aws\_ecs\_cluster.example.id
# ... other configurations ...
deployment\_configuration {
strategy = "BLUE\_GREEN"
}
sigint\_rollback = true
wait\_for\_steady\_state = true
}
```
### Linear Deployment Strategy
```terraform
resource "aws\_ecs\_service" "example" {
name = "example"
cluster = aws\_ecs\_cluster.example.id
# ... other configurations ...
deployment\_configuration {
strategy = "LINEAR"
bake\_time\_in\_minutes = 10
linear\_configuration {
step\_percent = 25.0
step\_bake\_time\_in\_minutes = 5
}
}
}
```
### Canary Deployment Strategy
```terraform
resource "aws\_ecs\_service" "example" {
name = "example"
cluster = aws\_ecs\_cluster.example.id
# ... other configurations ...
deployment\_configuration {
strategy = "CANARY"
bake\_time\_in\_minutes = 15
canary\_configuration {
canary\_percent = 10.0
canary\_bake\_time\_in\_minutes = 5
}
}
}
```
### Redeploy Service On Every Apply
The key used with `triggers` is arbitrary.
```terraform
resource "aws\_ecs\_service" "example" {
# ... other configurations ...
force\_new\_deployment = true
triggers = {
redeployment = plantimestamp()
}
}
```
### Service Connect with Access Logs
```terraform
resource "aws\_ecs\_service" "example" {
name = "example"
cluster = aws\_ecs\_cluster.example.id
task\_definition = aws\_ecs\_task\_definition.example.arn
desired\_count = 1
service\_connect\_configuration {
enabled = true
namespace = aws\_service\_discovery\_http\_namespace.example.arn
log\_configuration {
log\_driver = "awslogs"
options = {
"awslogs-group" = aws\_cloudwatch\_log\_group.example.name
"awslogs-region" = data.aws\_region.current.name
"awslogs-stream-prefix" = "service-connect"
}
}
access\_log\_configuration {
format = "TEXT"
include\_query\_parameters = "ENABLED"
}
service {
port\_name = "http"
discovery\_name = "example"
client\_alias {
dns\_name = "example"
port = 8080
}
}
}
}
resource "aws\_cloudwatch\_log\_group" "example" {
name = "/ecs/example/service-connect"
}
data "aws\_region" "current" {}
```
## Argument Reference
The following arguments are required:
\* `name` - (Required) Name of the service (up to 255 letters, numbers, hyphens, and underscores)
The following arguments are optional:
\* `alarms` - (Optional) Information about the CloudWatch alarms. [See below](#alarms).
\* `availability\_zone\_rebalancing` - (Optional) ECS automatically redistributes tasks within a service across Availability Zones (AZs) to mitigate the risk of impaired application availability due to underlying infrastructure failures and task lifecycle activities. The valid values are `ENABLED` and `DISABLED`. When creating a new service, if no value is specified, it defaults to `ENABLED` if the service is compatible with AvailabilityZoneRebalancing. When updating an existing service, if no value is specified it defaults to the existing service's AvailabilityZoneRebalancing value. If the service never had an AvailabilityZoneRebalancing value set, Amazon ECS treats this as `DISABLED`.
\* `capacity\_provider\_strategy` - (Optional) Capacity provider strategies to use for the service. Can be one or more. Updating this argument requires `force\_new\_deployment = true`. [See below](#capacity\_provider\_strategy). Conflicts with `launch\_type`.
\* `cluster` - (Optional) ARN of an ECS cluster.
\* `deployment\_circuit\_breaker` - (Optional) Configuration block for deployment circuit breaker. [See below](#deployment\_circuit\_breaker).
\* `deployment\_configuration` - (Optional) Configuration block for deployment settings. [See below](#deployment\_configuration).
\* `deployment\_controller` - (Optional) Configuration block for deployment controller configuration. [See below](#deployment\_controller).
\* `deployment\_maximum\_percent` - (Optional) Upper limit (as a percentage of the service's desiredCount) of the number of running tasks that can be running in a service during a deployment. Not valid when using the `DAEMON` scheduling strategy.
\* `deployment\_minimum\_healthy\_percent` - (Optional) Lower limit (as a percentage of the service's desiredCount) of the number of running tasks that must remain running and healthy in a service during a deployment.
\* `desired\_count` - (Optional) Number of instances of the task definition to place and keep running. Defaults to 0. Do not specify if using the `DAEMON` scheduling strategy.
\* `enable\_ecs\_managed\_tags` - (Optional) Whether to enable Amazon ECS managed tags for the tasks within the service.
\* `enable\_execute\_command` - (Optional) Whether to enable Amazon ECS Exec for the tasks within the service.
\* `force\_delete` - (Optional) Enable to delete a service even if it wasn't scaled down to zero tasks. It's only necessary to use this if the service uses the `REPLICA` scheduling strategy.
\* `force\_new\_deployment` - (Optional) Enable to force a new task deployment of the service. This can be used to update tasks to use a newer Docker image with same image/tag combination (e.g., `myimage:latest`), roll Fargate tasks onto a newer platform version, or immediately deploy `ordered\_placement\_strategy` and `placement\_constraints` updates.
\* `health\_check\_grace\_period\_seconds` - (Optional) Seconds to ignore failing load balancer health checks on newly instantiated tasks to prevent premature shutdown, up to 2147483647. Only valid for services configured to use load balancers.
\* `iam\_role` - (Optional) ARN of the IAM role that allows Amazon ECS to make calls to your load balancer on your behalf. This parameter is required if you are using a load balancer with your service, but only if your task definition does not use the `awsvpc` network mode. If using `awsvpc` network mode, do not specify this role. If your account has already created the Amazon ECS service-linked role, that role is used by default for your service unless you specify a role here.
\* `launch\_type` - (Optional) Launch type on which to run your service. The valid values are `EC2`, `FARGATE`, and `EXTERNAL`. Defaults to `EC2`. Conflicts with `capacity\_provider\_strategy`.
\* `load\_balancer` - (Optional) Configuration block for load balancers. [See below](#load\_balancer).
\* `network\_configuration` - (Optional) Network configuration for the service. This parameter is required for task definitions that use the `awsvpc` network mode to receive their own Elastic Network Interface, and it is not supported for other network modes. [See below](#network\_configuration).
\* `ordered\_placement\_strategy` - (Optional) Service level strategy rules that are taken into consideration during task placement. List from top to bottom in order of precedence. Updates to this configuration will take effect next task deployment unless `force\_new\_deployment` is enabled. The maximum number of `ordered\_placement\_strategy` blocks is `5`. [See below](#ordered\_placement\_strategy).
\* `placement\_constraints` - (Optional) Rules that are taken into consideration during task placement. Updates to this configuration will take effect next task deployment unless `force\_new\_deployment` is enabled. Maximum number of `placement\_constraints` is `10`. [See below](#placement\_constraints).
\* `platform\_version` - (Optional) Platform version on which to run your service. Only applicable for `launch\_type` set to `FARGATE`. Defaults to `LATEST`. More information about Fargate platform versions can be found in the [AWS ECS User Guide](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform\_versions.html).
\* `propagate\_tags` - (Optional) Whether to propagate the tags from the task definition or the service to the tasks. The valid values are `SERVICE` and `TASK\_DEFINITION`.
\* `region` - (Optional) Region where this resource will be [managed](https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints). Defaults to the Region set in the [provider configuration](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference).
\* `scheduling\_strategy` - (Optional) Scheduling strategy to use for the service. The valid values are `REPLICA` and `DAEMON`. Defaults to `REPLICA`. Note that [\*Tasks using the Fargate launch type or the `CODE\_DEPLOY` or `EXTERNAL` deployment controller types don't support the `DAEMON` scheduling strategy\*](https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API\_CreateService.html).
\* `service\_connect\_configuration` - (Optional) ECS Service Connect configuration for this service to discover and connect to services, and be discovered by, and connected from, other services within a namespace. [See below](#service\_connect\_configuration).
\* `service\_registries` - (Optional) Service discovery registries for the service. The maximum number of `service\_registries` blocks is `1`. [See below](#service\_registries).
\* `sigint\_rollback` - (Optional) Whether to enable graceful termination of deployments using SIGINT signals. When enabled, allows customers to safely cancel an in-progress deployment and automatically trigger a rollback to the previous stable state. Defaults to `false`. Only applicable when using `ECS` deployment controller and requires `wait\_for\_steady\_state = true`.
\* `tags` - (Optional) Key-value map of resource tags. If configured with a provider [`default\_tags` configuration block](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#default\_tags-configuration-block) present, tags with matching keys will overwrite those defined at the provider-level.
\* `task\_definition` - (Optional) Family and revision (`family:revision`) or full ARN of the task definition that you want to run in your service. Required unless using the `EXTERNAL` deployment controller. If a revision is not specified, the latest `ACTIVE` revision is used.
\* `triggers` - (Optional) Map of arbitrary keys and values that, when changed, will trigger an in-place update (redeployment). Useful with `plantimestamp()`. See example above.
\* `volume\_configuration` - (Optional) Configuration for a volume specified in the task definition as a volume that is configured at launch time. Currently, the only supported volume type is an Amazon EBS volume. [See below](#volume\_configuration).
\* `vpc\_lattice\_configurations` - (Optional) The VPC Lattice configuration for your service that allows Lattice to connect, secure, and monitor your service across multiple accounts and VPCs. [See below](#vpc\_lattice\_configurations).
\* `wait\_for\_steady\_state` - (Optional) If `true`, Terraform will wait for the service to reach a steady state (like [`aws ecs wait services-stable`](https://docs.aws.amazon.com/cli/latest/reference/ecs/wait/services-stable.html)) before continuing. Default `false`.
### alarms
The `alarms` configuration block supports the following:
\* `alarm\_names` - (Required) One or more CloudWatch alarm names.
\* `enable` - (Required) Whether to use the CloudWatch alarm option in the service deployment process.
\* `rollback` - (Required) Whether to configure Amazon ECS to roll back the service if a service deployment fails. If rollback is used, when a service deployment fails, the service is rolled back to the last deployment that completed successfully.
### volume\_configuration
The `volume\_configuration` configuration block supports the following:
\* `managed\_ebs\_volume` - (Required) Configuration for the Amazon EBS volume that Amazon ECS creates and manages on your behalf. [See below](#managed\_ebs\_volume).
\* `name` - (Required) Name of the volume.
### vpc\_lattice\_configurations
`vpc\_lattice\_configurations` supports the following:
\* `port\_name` - (Required) The name of the port for a target group associated with the VPC Lattice configuration.
\* `role\_arn` - (Required) The ARN of the IAM role to associate with this volume. This is the Amazon ECS infrastructure IAM role that is used to manage your AWS infrastructure.
\* `target\_group\_arn` - (Required) The full ARN of the target group or groups associated with the VPC Lattice configuration.
### managed\_ebs\_volume
The `managed\_ebs\_volume` configuration block supports the following:
\* `encrypted` - (Optional) Whether the volume should be encrypted. Default value is `true`.
\* `file\_system\_type` - (Optional) Linux filesystem type for the volume. For volumes created from a snapshot, same filesystem type must be specified that the volume was using when the snapshot was created. Valid values are `ext3`, `ext4`, `xfs`. Default value is `xfs`.
\* `iops` - (Optional) Number of I/O operations per second (IOPS).
\* `kms\_key\_id` - (Optional) Amazon Resource Name (ARN) identifier of the Amazon Web Services Key Management Service key to use for Amazon EBS encryption.
\* `role\_arn` - (Required) Amazon ECS infrastructure IAM role that is used to manage your Amazon Web Services infrastructure. Recommended using the Amazon ECS-managed `AmazonECSInfrastructureRolePolicyForVolumes` IAM policy with this role.
\* `size\_in\_gb` - (Optional) Size of the volume in GiB. You must specify either a `size\_in\_gb` or a `snapshot\_id`. You can optionally specify a volume size greater than or equal to the snapshot size.
\* `snapshot\_id` - (Optional) Snapshot that Amazon ECS uses to create the volume. You must specify either a `size\_in\_gb` or a `snapshot\_id`.
\* `tag\_specifications` - (Optional) The tags to apply to the volume. [See below](#tag\_specifications).
\* `throughput` - (Optional) Throughput to provision for a volume, in MiB/s, with a maximum of 1,000 MiB/s.
\* `volume\_initialization\_rate` - (Optional) Volume Initialization Rate in MiB/s. You must also specify a `snapshot\_id`.
\* `volume\_type` - (Optional) Volume type.
### capacity\_provider\_strategy
The `capacity\_provider\_strategy` configuration block supports the following:
\* `base` - (Optional) Number of tasks, at a minimum, to run on the specified capacity provider. Only one capacity provider in a capacity provider strategy can have a base defined.
\* `capacity\_provider` - (Required) Short name of the capacity provider.
\* `weight` - (Required) Relative percentage of the total number of launched tasks that should use the specified capacity provider.
### deployment\_configuration
The `deployment\_configuration` configuration block supports the following:
\* `bake\_time\_in\_minutes` - (Optional) Number of minutes to wait after a new deployment is fully provisioned before terminating the old deployment. Valid range: 0-1440 minutes. Used with `BLUE\_GREEN`, `LINEAR`, and `CANARY` strategies.
\* `canary\_configuration` - (Optional) Configuration block for canary deployment strategy. Required when `strategy` is set to `CANARY`. [See below](#canary\_configuration).
\* `lifecycle\_hook` - (Optional) Configuration block for lifecycle hooks that are invoked during deployments. [See below](#lifecycle\_hook).
\* `linear\_configuration` - (Optional) Configuration block for linear deployment strategy. Required when `strategy` is set to `LINEAR`. [See below](#linear\_configuration).
\* `strategy` - (Optional) Type of deployment strategy. Valid values: `ROLLING`, `BLUE\_GREEN`, `LINEAR`, `CANARY`. Default: `ROLLING`.
### lifecycle\_hook
The `lifecycle\_hook` configuration block supports the following:
\* `hook\_details` - (Optional) Custom parameters that Amazon ECS will pass to the hook target invocations (such as a Lambda function).
\* `hook\_target\_arn` - (Required) ARN of the Lambda function to invoke for the lifecycle hook.
\* `lifecycle\_stages` - (Required) Stages during the deployment when the hook should be invoked. Valid values: `RECONCILE\_SERVICE`, `PRE\_SCALE\_UP`, `POST\_SCALE\_UP`, `TEST\_TRAFFIC\_SHIFT`, `POST\_TEST\_TRAFFIC\_SHIFT`, `PRODUCTION\_TRAFFIC\_SHIFT`, `POST\_PRODUCTION\_TRAFFIC\_SHIFT`.
\* `role\_arn` - (Required) ARN of the IAM role that grants the service permission to invoke the Lambda function.
### linear\_configuration
The `linear\_configuration` configuration block supports the following:
\* `step\_bake\_time\_in\_minutes` - (Optional) Number of minutes to wait between each step during a linear deployment. Valid range: 0-1440 minutes.
\* `step\_percent` - (Required) Percentage of traffic to shift in each step during a linear deployment. Valid range: 3.0-100.0.
### canary\_configuration
The `canary\_configuration` configuration block supports the following:
\* `canary\_bake\_time\_in\_minutes` - (Optional) Number of minutes to wait before shifting all traffic to the new deployment. Valid range: 0-1440 minutes.
\* `canary\_percent` - (Required) Percentage of traffic to route to the canary deployment. Valid range: 0.1-100.0.
### deployment\_circuit\_breaker
The `deployment\_circuit\_breaker` configuration block supports the following:
\* `enable` - (Required) Whether to enable the deployment circuit breaker logic for the service.
\* `rollback` - (Required) Whether to enable Amazon ECS to roll back the service if a service deployment fails. If rollback is enabled, when a service deployment fails, the service is rolled back to the last deployment that completed successfully.
### deployment\_controller
The `deployment\_controller` configuration block supports the following:
\* `type` - (Optional) Type of deployment controller. Valid values: `CODE\_DEPLOY`, `ECS`, `EXTERNAL`. Default: `ECS`.
### load\_balancer
`load\_balancer` supports the following:
\* `advanced\_configuration` - (Optional) Configuration block for Blue/Green deployment settings. Required when using `BLUE\_GREEN` deployment strategy. [See below](#advanced\_configuration).
\* `container\_name` - (Required) Name of the container to associate with the load balancer (as it appears in a container definition).
\* `container\_port` - (Required) Port on the container to associate with the load balancer.
\* `elb\_name` - (Required for ELB Classic) Name of the ELB (Classic) to associate with the service.
\* `target\_group\_arn` - (Required for ALB/NLB) ARN of the Load Balancer target group to associate with the service.
-> \*\*Version note:\*\* Multiple `load\_balancer` configuration block support was added in Terraform AWS Provider version 2.22.0. This allows configuration of [ECS service support for multiple target groups](https://aws.amazon.com/about-aws/whats-new/2019/07/amazon-ecs-services-now-support-multiple-load-balancer-target-groups/).
### advanced\_configuration
The `advanced\_configuration` configuration block supports the following:
\* `alternate\_target\_group\_arn` - (Required) ARN of the alternate target group to use for Blue/Green deployments.
\* `production\_listener\_rule` - (Required) ARN of the listener rule that routes production traffic.
\* `role\_arn` - (Required) ARN of the IAM role that allows ECS to manage the target groups.
\* `test\_listener\_rule` - (Optional) ARN of the listener rule that routes test traffic.
### network\_configuration
`network\_configuration` support the following:
\* `assign\_public\_ip` - (Optional) Assign a public IP address to the ENI (Fargate launch type only). Valid values are `true` or `false`. Default `false`.
\* `security\_groups` - (Optional) Security groups associated with the task or service. If you do not specify a security group, the default security group for the VPC is used.
\* `subnets` - (Required) Subnets associated with the task or service.
For more information, see [Task Networking](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-networking.html)
### ordered\_placement\_strategy
`ordered\_placement\_strategy` supports the following:
\* `field` - (Optional) For the `spread` placement strategy, valid values are `instanceId` (or `host`, which has the same effect), or any platform or custom attribute that is applied to a container instance. For the `binpack` type, valid values are `memory` and `cpu`. For the `random` type, this attribute is not needed. For more information, see [Placement Strategy](https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API\_PlacementStrategy.html).
\* `type` - (Required) Type of placement strategy. Must be one of: `binpack`, `random`, or `spread`
-> \*\*Note:\*\* for `spread`, `host` and `instanceId` will be normalized, by AWS, to be `instanceId`. This means the statefile will show `instanceId` but your config will differ if you use `host`.
### placement\_constraints
`placement\_constraints` support the following:
\* `expression` - (Optional) Cluster Query Language expression to apply to the constraint. Does not need to be specified for the `distinctInstance` type. For more information, see [Cluster Query Language in the Amazon EC2 Container Service Developer Guide](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/cluster-query-language.html).
\* `type` - (Required) Type of constraint. The only valid values at this time are `memberOf` and `distinctInstance`.
### service\_registries
`service\_registries` support the following:
\* `container\_name` - (Optional) Container name value, already specified in the task definition, to be used for your service discovery service.
\* `container\_port` - (Optional) Port value, already specified in the task definition, to be used for your service discovery service.
\* `port` - (Optional) Port value used if your Service Discovery service specified an SRV record.
\* `registry\_arn` - (Required) ARN of the Service Registry. The currently supported service registry is Amazon Route 53 Auto Naming Service(`aws\_service\_discovery\_service`). For more information, see [Service](https://docs.aws.amazon.com/Route53/latest/APIReference/API\_autonaming\_Service.html)
### service\_connect\_configuration
`service\_connect\_configuration` supports the following:
\* `access\_log\_configuration` - (Optional) Configuration for Service Connect access logs. [See below](#access\_log\_configuration).
\* `enabled` - (Required) Whether to use Service Connect with this service.
\* `log\_configuration` - (Optional) Log configuration for the container. [See below](#log\_configuration).
\* `namespace` - (Optional) Namespace name or ARN of the [`aws\_service\_discovery\_http\_namespace`](/docs/providers/aws/r/service\_discovery\_http\_namespace.html) for use with Service Connect.
\* `service` - (Optional) List of Service Connect service objects. [See below](#service).
### access\_log\_configuration
`access\_log\_configuration` supports the following:
\* `format` - (Required) The format for Service Connect access log output. Valid values: `TEXT`, `JSON`. See [AWS documentation](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-connect-envoy-access-logs.html) for format details.
\* `include\_query\_parameters` - (Optional) Specifies whether to include query parameters in Service Connect access logs. Valid values: `ENABLED`, `DISABLED`. Default: `DISABLED`. Query parameters may contain sensitive information.
~> \*\*NOTE:\*\* Access logs are delivered to the destination log group specified in the `log\_configuration` block. You must configure `log\_configuration` to enable access logs.
~> \*\*SECURITY WARNING:\*\* When `include\_query\_parameters` is set to `ENABLED`, query parameters (which may contain sensitive data such as request IDs, tokens, or session identifiers) will be included in access logs.
### log\_configuration
`log\_configuration` supports the following:
\* `log\_driver` - (Required) Log driver to use for the container.
\* `options` - (Optional) Configuration options to send to the log driver.
\* `secret\_option` - (Optional) Secrets to pass to the log configuration. [See below](#secret\_option).
### secret\_option
`secret\_option` supports the following:
\* `name` - (Required) Name of the secret.
\* `value\_from` - (Required) Secret to expose to the container. The supported values are either the full ARN of the AWS Secrets Manager secret or the full ARN of the parameter in the SSM Parameter Store.
### service
`service` supports the following:
\* `client\_alias` - (Optional) List of client aliases for this Service Connect service. You use these to assign names that can be used by client applications. For each service block where enabled is true, exactly one `client\_alias` with one `port` should be specified. [See below](#client\_alias).
\* `discovery\_name` - (Optional) Name of the new AWS Cloud Map service that Amazon ECS creates for this Amazon ECS service.
\* `ingress\_port\_override` - (Optional) Port number for the Service Connect proxy to listen on.
\* `port\_name` - (Required) Name of one of the `portMappings` from all the containers in the task definition of this Amazon ECS service.
\* `timeout` - (Optional) Configuration timeouts for Service Connect
\* `tls` - (Optional) Configuration for enabling Transport Layer Security (TLS)
### timeout
`timeout` supports the following:
\* `idle\_timeout\_seconds` - (Optional) Amount of time in seconds a connection will stay active while idle. A value of 0 can be set to disable idleTimeout.
\* `per\_request\_timeout\_seconds` - (Optional) Amount of time in seconds for the upstream to respond with a complete response per request. A value of 0 can be set to disable perRequestTimeout. Can only be set when appProtocol isn't TCP.
### tls
`tls` supports the following:
\* `issuer\_cert\_authority` - (Required) Details of the certificate authority which will issue the certificate.
\* `kms\_key` - (Optional) KMS key used to encrypt the private key in Secrets Manager.
\* `role\_arn` - (Optional) ARN of the IAM Role that's associated with the Service Connect TLS.
### issuer\_cert\_authority
`issuer\_cert\_authority` supports the following:
\* `aws\_pca\_authority\_arn` - (Optional) ARN of the [`aws\_acmpca\_certificate\_authority`](/docs/providers/aws/r/acmpca\_certificate\_authority.html) used to create the TLS Certificates.
### client\_alias
`client\_alias` supports the following:
\* `dns\_name` - (Optional) Name that you use in the applications of client tasks to connect to this service.
\* `port` - (Required) Listening port number for the Service Connect proxy. This port is available inside of all of the tasks within the same namespace.
\* `test\_traffic\_rules` - (Optional) Configuration block for test traffic routing rules. [See below](#test\_traffic\_rules).
### test\_traffic\_rules
The `test\_traffic\_rules` configuration block supports the following:
\* `header` - (Optional) Configuration block for header-based routing rules. [See below](#header).
### header
The `header` configuration block supports the following:
\* `name` - (Required) Name of the HTTP header to match.
\* `value` - (Required) Configuration block for header value matching criteria. [See below](#value).
### value
The `value` configuration block supports the following:
\* `exact` - (Required) Exact string value to match in the header.
### tag\_specifications
`tag\_specifications` supports the following:
\* `resource\_type` - (Required) The type of volume resource. Valid values, `volume`.
\* `propagate\_tags` - (Optional) Determines whether to propagate the tags from the task definition to the Amazon EBS volume.
\* `tags` - (Optional) The tags applied to this Amazon EBS volume. `AmazonECSCreated` and `AmazonECSManaged` are reserved tags that can't be used.
## Attribute Reference
This resource exports the following attributes in addition to the arguments above:
\* `arn` - ARN that identifies the service.
\* `tags\_all` - A map of tags assigned to the resource, including those inherited from the provider [`default\_tags` configuration block](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#default\_tags-configuration-block).
## Timeouts
[Configuration options](https://developer.hashicorp.com/terraform/language/resources/syntax#operation-timeouts):
- `create` - (Default `20m`)
- `update` - (Default `20m`)
- `delete` - (Default `20m`)
## Import
In Terraform v1.12.0 and later, the [`import` block](https://developer.hashicorp.com/terraform/language/import) can be used with the `identity` attribute. For example:
```terraform
import {
to = aws\_ecs\_service.example
identity = {
cluster = "example-cluster"
name = "example-service"
}
}
resource "aws\_ecs\_service" "example" {
### Configuration omitted for brevity ###
}
```
### Identity Schema
#### Required
\* `cluster` (String) The name of the cluster.
\* `name` (String) The name of the service.
#### Optional
\* `account\_id` (String) AWS Account where this resource is managed.
\* `region` (String) Region where this resource is managed.
In Terraform v1.5.0 and later, use an [`import` block](https://developer.hashicorp.com/terraform/language/import) to import ECS services using the `name` together with ecs cluster `name`. For example:
```terraform
import {
to = aws\_ecs\_service.imported
id = "cluster-name/service-name"
}
```
Using `terraform import`, import ECS services using the `name` together with ecs cluster `name`. For example:
```console
% terraform import aws\_ecs\_service.imported cluster-name/service-name
```