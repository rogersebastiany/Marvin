Architect for AWS Fargate for Amazon ECS - Amazon Elastic Container Service 

Architect for AWS Fargate for Amazon ECS - Amazon Elastic Container Service
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
"name" : "Amazon ECS",
"item" : "https://docs.aws.amazon.com/ecs/index.html"
},
{
"@type" : "ListItem",
"position" : 3,
"name" : "Developer Guide",
"item" : "https://docs.aws.amazon.com/AmazonECS/latest/developerguide"
},
{
"@type" : "ListItem",
"position" : 4,
"name" : "Architect for AWS Fargate for Amazon ECS",
"item" : "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/AWS\_Fargate.html"
}
]
}

[Documentation](/index.html)[Amazon ECS](/ecs/index.html)[Developer Guide](Welcome.html)

[Walkthroughs](#fargate-walkthrough)[Capacity providers](#fargate-spot)[Task definitions](#fargate-task-defintion)[Platform versions](#fargate-platform-versions)[Service load balancing](#fargate-tasks-services-load-balancing)[Usage metrics](#fargate-usage-metrics)

# Architect for AWS Fargate for Amazon ECS

AWS Fargate is a technology that you can use with Amazon ECS to run [containers](https://aws.amazon.com/containers/) without having to manage
servers or clusters of Amazon EC2 instances. With AWS Fargate, you no longer have to
provision, configure, or scale clusters of virtual machines to run containers. This removes
the need to choose server types, decide when to scale your clusters, or optimize cluster
packing.

When you run your tasks and services with Fargate, you
package your application in containers, specify the CPU and memory requirements, define
networking and IAM policies, and launch the application. Each Fargate task
has its own isolation boundary and does not share the underlying kernel, CPU resources,
memory resources, or elastic network interface with another task. You configure your task
definitions for Fargate by setting the `requiresCompatibilities`
task definition parameter to `FARGATE`. For more information, see [Capacity](./task_definition_parameters.html#requires_compatibilities).

Fargate offers platform versions for Amazon Linux 2 (platform version 1.3.0),
Bottlerocket operating system (platform version 1.4.0), and Microsoft Windows 2019 Server
Full and Core editions.Unless otherwise specified, the information applies to all
Fargate platforms.

For information about the Regions that support Linux containers on
Fargate, see [Linux containers on AWS Fargate](./AWS_Fargate-Regions.html#linux-regions).

For information about the Regions that support Windows containers on
Fargate, see [Windows containers on AWS Fargate](./AWS_Fargate-Regions.html#windows-regions).

## Walkthroughs

For information about how to get started using the console, see:

* [Learn how to create an Amazon ECS Linux task for Fargate](./getting-started-fargate.html)
* [Learn how to create an Amazon ECS Windows task for Fargate](./Windows_fargate-getting_started.html)

For information about how to get started using the AWS CLI, see:

* [Creating an Amazon ECS Linux task for the Fargate with the AWS CLI](./ECS_AWSCLI_Fargate.html)
* [Creating an Amazon ECS Windows task for the Fargate with the AWS CLI](./ECS_AWSCLI_Fargate_windows.html)

## Capacity providers

The following capacity providers are available:

* Fargate
* Fargate Spot - Run interruption tolerant Amazon ECS tasks at a discounted rate
  compared to the AWS Fargate price. Fargate Spot runs tasks on spare
  compute capacity. When AWS needs the capacity back, your tasks will be
  interrupted with a two-minute warning. For more information, see [Amazon ECS clusters for Fargate](./fargate-capacity-providers.html).

## Task definitions

Fargate tasks don't support all of the Amazon ECS
task definition parameters that are available. Some parameters aren't supported at all,
and others behave differently for Fargate tasks. For more information, see
[Task CPU and memory](./fargate-tasks-services.html#fargate-tasks-size).

## Platform versions

AWS Fargate platform versions are used to refer to a specific runtime environment for
Fargate task infrastructure. It is a combination of the kernel and container
runtime versions. You select a platform version when you run a task or when you create a
service to maintain a number of identical tasks.

New revisions of platform versions are released as the runtime environment evolves, for example, if
there are kernel or operating system updates, new features, bug fixes, or security updates.
A Fargate platform version is updated by making a new platform version revision. Each task
runs on one platform version revision during its
lifecycle. If you want to use the latest platform version revision, then you must start a new
task. A new task that runs on Fargate always runs on the latest revision
of a platform version, ensuring that tasks are always started on secure and patched infrastructure.

If a security issue is found that affects an existing platform version, AWS creates a
new patched revision of the platform version and retires tasks running on the
vulnerable revision. In some cases, you may be notified that your tasks on Fargate
have been scheduled for retirement. For more information, see [Task retirement and maintenance for AWS Fargate on Amazon ECS](./task-maintenance.html).

For more information see [Fargate platform versions for Amazon ECS](./platform-fargate.html).

## Service load balancing

Your Amazon ECS service on AWS Fargate can optionally be configured to use
Elastic Load Balancing to distribute traffic evenly across the tasks in your service.

Amazon ECS services on AWS Fargate support the Application Load Balancer, Network Load Balancer, and Gateway Load Balancer load balancer
types. Application Load Balancers are used to route HTTP/HTTPS (or layer 7) traffic. Network Load Balancers are used to
route TCP or UDP (or layer 4) traffic. For more information, see [Use load balancing to distribute Amazon ECS service traffic](./service-load-balancing.html).

When you create a target group for these services, you must choose `ip` as
the target type, not `instance`. This is because tasks that use the
`awsvpc` network mode are associated with an elastic network interface,
not an Amazon EC2 instance. For more information, see [Use load balancing to distribute Amazon ECS service traffic](./service-load-balancing.html).

Using a Network Load Balancer to route UDP traffic to your Amazon ECS on AWS Fargate tasks is
only supported when using platform version 1.4 or later.

## Usage metrics

You can use CloudWatch usage metrics to provide visibility into your accounts usage of
resources. Use these metrics to visualize your current service usage on CloudWatch graphs and
dashboards.

AWS Fargate usage metrics correspond to AWS service quotas. You can configure
alarms that alert you when your usage approaches a service quota. For more information
about AWS Fargate service quotas, [Amazon ECS endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/ecs-service.html) in the *Amazon Web Services General Reference*..

For more information about AWS Fargate usage metrics, see [AWS Fargate usage metrics](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/monitoring-fargate-usage.html).

**Javascript is disabled or is unavailable in your browser.**

To use the Amazon Web Services Documentation, Javascript must be enabled. Please refer to your browser's Help pages for instructions.

[Document Conventions](/general/latest/gr/docconventions.html)

Daemon auto repair

Security considerations for when to use Fargate

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.