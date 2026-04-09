---
subcategory: "ECS (Elastic Container)"
layout: "aws"
page\_title: "AWS: aws\_ecs\_task\_definition"
description: |-
Manages a revision of an ECS task definition.
---
# Resource: aws\_ecs\_task\_definition
Manages a revision of an ECS task definition to be used in `aws\_ecs\_service`.
## Example Usage
### Basic Example
```terraform
resource "aws\_ecs\_task\_definition" "service" {
family = "service"
container\_definitions = jsonencode([
{
name = "first"
image = "service-first"
cpu = 10
memory = 512
essential = true
portMappings = [
{
containerPort = 80
hostPort = 80
}
]
},
{
name = "second"
image = "service-second"
cpu = 10
memory = 256
essential = true
portMappings = [
{
containerPort = 443
hostPort = 443
}
]
}
])
volume {
name = "service-storage"
host\_path = "/ecs/service-storage"
}
placement\_constraints {
type = "memberOf"
expression = "attribute:ecs.availability-zone in [us-west-2a, us-west-2b]"
}
}
```
### With AppMesh Proxy
```terraform
resource "aws\_ecs\_task\_definition" "service" {
family = "service"
container\_definitions = file("task-definitions/service.json")
proxy\_configuration {
type = "APPMESH"
container\_name = "applicationContainerName"
properties = {
AppPorts = "8080"
EgressIgnoredIPs = "169.254.170.2,169.254.169.254"
IgnoredUID = "1337"
ProxyEgressPort = 15001
ProxyIngressPort = 15000
}
}
}
```
### Example Using `docker\_volume\_configuration`
```terraform
resource "aws\_ecs\_task\_definition" "service" {
family = "service"
container\_definitions = file("task-definitions/service.json")
volume {
name = "service-storage"
docker\_volume\_configuration {
scope = "shared"
autoprovision = true
driver = "local"
driver\_opts = {
"type" = "nfs"
"device" = "${aws\_efs\_file\_system.fs.dns\_name}:/"
"o" = "addr=${aws\_efs\_file\_system.fs.dns\_name},rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport"
}
}
}
}
```
### Example Using `efs\_volume\_configuration`
```terraform
resource "aws\_ecs\_task\_definition" "service" {
family = "service"
container\_definitions = file("task-definitions/service.json")
volume {
name = "service-storage"
efs\_volume\_configuration {
file\_system\_id = aws\_efs\_file\_system.fs.id
root\_directory = "/opt/data"
transit\_encryption = "ENABLED"
transit\_encryption\_port = 2999
authorization\_config {
access\_point\_id = aws\_efs\_access\_point.test.id
iam = "ENABLED"
}
}
}
}
```
### Example Using `fsx\_windows\_file\_server\_volume\_configuration`
```terraform
resource "aws\_ecs\_task\_definition" "service" {
family = "service"
container\_definitions = file("task-definitions/service.json")
volume {
name = "service-storage"
fsx\_windows\_file\_server\_volume\_configuration {
file\_system\_id = aws\_fsx\_windows\_file\_system.test.id
root\_directory = "\\data"
authorization\_config {
credentials\_parameter = aws\_secretsmanager\_secret\_version.test.arn
domain = aws\_directory\_service\_directory.test.name
}
}
}
}
resource "aws\_secretsmanager\_secret\_version" "test" {
secret\_id = aws\_secretsmanager\_secret.test.id
secret\_string = jsonencode({ username : "admin", password : aws\_directory\_service\_directory.test.password })
}
```
### Example Using `container\_definitions`
```terraform
resource "aws\_ecs\_task\_definition" "test" {
family = "test"
container\_definitions = < \*\*NOTE:\*\* Proper escaping is required for JSON field values containing quotes (`"`) such as `environment` values. If directly setting the JSON, they should be escaped as `\"` in the JSON, e.g., `"value": "I \"love\" escaped quotes"`. If using a Terraform variable value, they should be escaped as `\\\"` in the variable, e.g., `value = "I \\\"love\\\" escaped quotes"` in the variable and `"value": "${var.myvariable}"` in the JSON.
~> \*\*Note:\*\* Fault injection only works with tasks using the `awsvpc` or `host` network modes. Fault injection isn't available on Windows.
### volume
\* `docker\_volume\_configuration` - (Optional) Configuration block to configure a [docker volume](#docker\_volume\_configuration). Detailed below.
\* `efs\_volume\_configuration` - (Optional) Configuration block for an [EFS volume](#efs\_volume\_configuration). Detailed below.
\* `fsx\_windows\_file\_server\_volume\_configuration` - (Optional) Configuration block for an [FSX Windows File Server volume](#fsx\_windows\_file\_server\_volume\_configuration). Detailed below.
\* `host\_path` - (Optional) Path on the host container instance that is presented to the container. If not set, ECS will create a nonpersistent data volume that starts empty and is deleted after the task has finished.
\* `configure\_at\_launch` - (Optional) Whether the volume should be configured at launch time. This is used to create Amazon EBS volumes for standalone tasks or tasks created as part of a service. Each task definition revision may only have one volume configured at launch in the volume configuration.
\* `name` - (Required) Name of the volume. This name is referenced in the `sourceVolume`
parameter of container definition in the `mountPoints` section.
### docker\_volume\_configuration
For more information, see [Specifying a Docker volume in your Task Definition Developer Guide](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/docker-volumes.html#specify-volume-config)
\* `autoprovision` - (Optional) If this value is `true`, the Docker volume is created if it does not already exist. \*Note\*: This field is only used if the scope is `shared`.
\* `driver\_opts` - (Optional) Map of Docker driver specific options.
\* `driver` - (Optional) Docker volume driver to use. The driver value must match the driver name provided by Docker because it is used for task placement.
\* `labels` - (Optional) Map of custom metadata to add to your Docker volume.
\* `scope` - (Optional) Scope for the Docker volume, which determines its lifecycle, either `task` or `shared`. Docker volumes that are scoped to a `task` are automatically provisioned when the task starts and destroyed when the task stops. Docker volumes that are scoped as `shared` persist after the task stops.
### efs\_volume\_configuration
For more information, see [Specifying an EFS volume in your Task Definition Developer Guide](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/efs-volumes.html#specify-efs-config)
\* `file\_system\_id` - (Required) ID of the EFS File System.
\* `root\_directory` - (Optional) Directory within the Amazon EFS file system to mount as the root directory inside the host. If this parameter is omitted, the root of the Amazon EFS volume will be used. Specifying / will have the same effect as omitting this parameter. This argument is ignored when using `authorization\_config`.
\* `transit\_encryption` - (Optional) Whether or not to enable encryption for Amazon EFS data in transit between the Amazon ECS host and the Amazon EFS server. Transit encryption must be enabled if Amazon EFS IAM authorization is used. Valid values: `ENABLED`, `DISABLED`. If this parameter is omitted, the default value of `DISABLED` is used.
\* `transit\_encryption\_port` - (Optional) Port to use for transit encryption. If you do not specify a transit encryption port, it will use the port selection strategy that the Amazon EFS mount helper uses.
\* `authorization\_config` - (Optional) Configuration block for [authorization](#authorization\_config) for the Amazon EFS file system. Detailed below.
### runtime\_platform
\* `operating\_system\_family` - (Optional) If the `requires\_compatibilities` is `FARGATE` this field is required; must be set to a valid option from the [operating system family in the runtime platform](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task\_definition\_parameters.html#runtime-platform) setting
\* `cpu\_architecture` - (Optional) Must be set to either `X86\_64` or `ARM64`; see [cpu architecture](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task\_definition\_parameters.html#runtime-platform)
#### authorization\_config
\* `access\_point\_id` - (Optional) Access point ID to use. If an access point is specified, the root directory value will be relative to the directory set for the access point. If specified, transit encryption must be enabled in the EFSVolumeConfiguration.
\* `iam` - (Optional) Whether or not to use the Amazon ECS task IAM role defined in a task definition when mounting the Amazon EFS file system. If enabled, transit encryption must be enabled in the EFSVolumeConfiguration. Valid values: `ENABLED`, `DISABLED`. If this parameter is omitted, the default value of `DISABLED` is used.
### fsx\_windows\_file\_server\_volume\_configuration
For more information, see [Specifying an FSX Windows File Server volume in your Task Definition Developer Guide](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/tutorial-wfsx-volumes.html)
\* `file\_system\_id` - (Required) The Amazon FSx for Windows File Server file system ID to use.
\* `root\_directory` - (Required) The directory within the Amazon FSx for Windows File Server file system to mount as the root directory inside the host.
\* `authorization\_config` - (Required) Configuration block for [authorization](#authorization\_config) for the Amazon FSx for Windows File Server file system detailed below.
#### authorization\_config
\* `credentials\_parameter` - (Required) The authorization credential option to use. The authorization credential options can be provided using either the Amazon Resource Name (ARN) of an AWS Secrets Manager secret or AWS Systems Manager Parameter Store parameter. The ARNs refer to the stored credentials.
\* `domain` - (Required) A fully qualified domain name hosted by an AWS Directory Service Managed Microsoft AD (Active Directory) or self-hosted AD on Amazon EC2.
### placement\_constraints
\* `expression` - (Optional) Cluster Query Language expression to apply to the constraint. For more information, see [Cluster Query Language in the Amazon EC2 Container Service Developer Guide](http://docs.aws.amazon.com/AmazonECS/latest/developerguide/cluster-query-language.html).
\* `type` - (Required) Type of constraint. Use `memberOf` to restrict selection to a group of valid candidates. Note that `distinctInstance` is not supported in task definitions.
### proxy\_configuration
\* `container\_name` - (Required) Name of the container that will serve as the App Mesh proxy.
\* `properties` - (Required) Set of network configuration parameters to provide the Container Network Interface (CNI) plugin, specified a key-value mapping.
\* `type` - (Optional) Proxy type. The default value is `APPMESH`. The only supported value is `APPMESH`.
### ephemeral\_storage
\* `size\_in\_gib` - (Required) The total amount, in GiB, of ephemeral storage to set for the task. The minimum supported value is `21` GiB and the maximum supported value is `200` GiB.
## Attribute Reference
This resource exports the following attributes in addition to the arguments above:
\* `arn` - Full ARN of the Task Definition (including both `family` and `revision`).
\* `arn\_without\_revision` - ARN of the Task Definition with the trailing `revision` removed. This may be useful for situations where the latest task definition is always desired. If a revision isn't specified, the latest ACTIVE revision is used. See the [AWS documentation](https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API\_StartTask.html#ECS-StartTask-request-taskDefinition) for details.
\* `revision` - Revision of the task in a particular family.
\* `tags\_all` - Map of tags assigned to the resource, including those inherited from the provider [`default\_tags` configuration block](https://registry.terraform.io/providers/hashicorp/aws/latest/docs#default\_tags-configuration-block).
## Import
In Terraform v1.12.0 and later, the [`import` block](https://developer.hashicorp.com/terraform/language/import) can be used with the `identity` attribute. For example:
```terraform
import {
to = aws\_ecs\_task\_definition.example
identity = {
family = "mytaskfamily"
revision = 123
}
}
resource "aws\_ecs\_task\_definition" "example" {
### Configuration omitted for brevity ###
}
```
### Identity Schema
#### Required
\* `family` (String) The unique name for your task definition.
\* `revision` (Integer) The revision of the task in a particular family.
#### Optional
\* `account\_id` (String) AWS Account where this resource is managed.
\* `region` (String) Region where this resource is managed.
In Terraform v1.5.0 and later, use an [`import` block](https://developer.hashicorp.com/terraform/language/import) to import ECS Task Definitions using their ARNs. For example:
```terraform
import {
to = aws\_ecs\_task\_definition.example
id = "arn:aws:ecs:us-east-1:012345678910:task-definition/mytaskfamily:123"
}
```
Using `terraform import`, import ECS Task Definitions using their ARNs. For example:
```console
% terraform import aws\_ecs\_task\_definition.example arn:aws:ecs:us-east-1:012345678910:task-definition/mytaskfamily:123
```