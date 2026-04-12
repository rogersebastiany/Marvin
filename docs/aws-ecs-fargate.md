# AWS ECS and Fargate


---

## 1. Security in Amazon Elastic Container Service

Security in Amazon Elastic Container Service - Amazon Elastic Container Service

# Security in Amazon Elastic Container Service

Cloud security at AWS is the highest priority. As an AWS customer, you benefit from a
data center and network architecture that is built to meet the requirements of the most
security-sensitive organizations.

Security is a shared responsibility between AWS and you. The [shared responsibility model](https://aws.amazon.com/compliance/shared-responsibility-model/)
describes this as security *of* the cloud and security
*in* the cloud:

* **Security of the cloud** – AWS is
  responsible for protecting the infrastructure that runs AWS services in the AWS
  Cloud. AWS also provides you with services that you can use securely. Third-party
  auditors regularly test and verify the effectiveness of our security as part of the
  [AWS compliance
  programs](https://aws.amazon.com/compliance/programs/). To learn about the compliance programs that apply to
  Amazon Elastic Container Service, see [AWS
  Services in Scope by Compliance Program](https://aws.amazon.com/compliance/services-in-scope/).
* **Security in the cloud** – Your responsibility
  is determined by the AWS service that you use. You are also responsible for other
  factors including the sensitivity of your data, your company’s requirements, and
  applicable laws and regulations.

This documentation helps you understand how to apply the shared responsibility model when
using Amazon ECS. The following topics show you how to configure Amazon ECS to meet your security and
compliance objectives. You also learn how to use other AWS services that help you to
monitor and secure your Amazon ECS resources.

###### Topics

* [Identity and Access Management for Amazon Elastic Container Service](./security-iam.html)
* [Logging and Monitoring in Amazon Elastic Container Service](./ecs-logging-monitoring.html)
* [Compliance validation for Amazon Elastic Container Service](./ecs-compliance.html)
* [AWS Fargate Federal Information Processing Standard (FIPS-140)](./ecs-fips-compliance.html)
* [Infrastructure Security in Amazon Elastic Container Service](./infrastructure-security.html)
* [AWS shared responsibility model for Amazon ECS](./security-shared-model.html)
* [Shared responsibility model for Amazon ECS Managed Instances](./security-shared-model-managed-instances.html)
* [Network security best practices for Amazon ECS](./security-network.html)
* [Amazon ECS task and container security best practices](./security-tasks-containers.html)

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.

---

## 2. What is Amazon Elastic Container Service?

What is Amazon Elastic Container Service? - Amazon Elastic Container Service

# What is Amazon Elastic Container Service?

###### Tip

Join our upcoming container workshop series to learn best
practices for Amazon ECS and AWS Fargate. [Click
here](https://aws-experience.com/amer/smb/events/series/Get-Hands-On-With-ECS?trk=45cf05ef-a935-47d7-9cce-c8183367acc8%26sc_channel%3Del) to sign up.

Amazon Elastic Container Service (Amazon ECS) is a fully managed container orchestration service that helps you easily
deploy, manage, and scale containerized applications. As a fully managed service, Amazon ECS
comes with AWS configuration and operational best practices built-in. It's integrated with
both AWS tools, such as Amazon Elastic Container Registry, and third-party tools, such as Docker. This integration
makes it easier for teams to focus on building the applications, not the environment. You
can run and scale your container workloads across AWS Regions in the cloud, and
on-premises, without the complexity of managing a control plane.

## Terminology and components

There are three layers in Amazon ECS:

* Capacity - The infrastructure where your containers run
* Controller - Deploy and manage your applications that run on the
  containers
* Provisioning - The tools that you can use to interface with the scheduler to
  deploy and manage your applications and containers

The following diagram shows the Amazon ECS layers.

The capacity is the infrastructure where your containers run. The following is an
overview of the capacity options:

* Amazon ECS Managed Instances is a compute option for Amazon ECS that
  enables you to run containerized workloads on a range of Amazon EC2 instance
  types while offloading infrastructure management to AWS. With
  Amazon ECS Managed Instances, you can access specific compute capabilities such as
  GPU acceleration, specific CPU architectures, high network performance,
  and specialized instances types, while AWS handles provisioning,
  patching, scaling, and maintenance of the underlying
  infrastructure.
* Amazon EC2 instances in the AWS cloud

  You choose the instance type, the number of instances, and manage the
  capacity.
* Serverless in the AWS cloud

  Fargate is a serverless, pay-as-you-go compute engine. With
  Fargate you don't need to manage servers, handle capacity planning, or
  isolate container workloads for security.
* On-premises virtual machines (VM) or servers

  Amazon ECS Anywhere provides support for registering an external instance such as
  an on-premises server or virtual machine (VM), to your Amazon ECS cluster.

The Amazon ECS scheduler is the software that manages your applications.

## Features

Amazon ECS provides the following high-level features:

**Task definition**
:   The blueprint for the application.

**Cluster**
:   The infrastructure your application runs on.

**Task**
:   An application such as a batch job that performs work, and then
    stops.

**Service**
:   A long running stateless application.

**Account Setting**
:   Allows access to features.

**Cluster Auto Scaling**
:   Amazon ECS manages the scaling of Amazon EC2 instances that are registered to your
    cluster.

**Service Auto Scaling**
:   Amazon ECS increases or decreases the desired number of tasks in your service
    automatically.

## Provisioning

There are multiple options for provisioning Amazon ECS:

* **AWS Management Console** — Provides a web interface
  that you can use to access your Amazon ECS resources.
* **AWS Command Line Interface (AWS CLI)** — Provides commands
  for a broad set of AWS services, including Amazon ECS. It's supported on Windows,
  Mac, and Linux. For more information, see [AWS Command Line Interface](https://aws.amazon.com/cli/).
* **AWS SDKs** — Provides
  language-specific APIs and takes care of many of the connection details. These
  include calculating signatures, handling request retries, and error handling.
  For more information, see [AWS SDKs](https://aws.amazon.com/developer/tools/#SDKs).
* **AWS CDK** — Provides an open-source
  software development framework that you can use to model and provision your
  cloud application resources using familiar programming languages. The AWS CDK
  provisions your resources in a safe, repeatable manner through
  AWS CloudFormation.

## Pricing

Amazon ECS pricing depends on the capacity option you choose for your containers.

* [Amazon ECS pricing](https://aws.amazon.com/ecs/pricing) –
  Pricing information for Amazon ECS.
* [AWS Fargate pricing](https://aws.amazon.com/fargate/pricing)
  – Pricing information for Fargate.

## Related services

###### Services to use with Amazon ECS

You can use other AWS services to help you deploy yours tasks and services on
Amazon ECS.

[Amazon EC2 Auto Scaling](https://docs.aws.amazon.com/autoscaling/)
:   Helps ensure you have the correct number of Amazon EC2 instances available to
    handle the load for your application.

[Amazon CloudWatch](https://docs.aws.amazon.com/cloudwatch/)
:   Monitor your services and tasks.

[Amazon Elastic Container Registry](https://docs.aws.amazon.com/ecr/)
:   Store and manage container images.

[Elastic Load Balancing](https://docs.aws.amazon.com/elasticloadbalancing/)
:   Automatically distribute incoming service traffic.

[Amazon GuardDuty](https://docs.aws.amazon.com/guardduty/)
:   Detect potentially unauthorized or malicious use of your container
    instances and workloads.

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.

---

## 3. Architect for AWS Fargate for Amazon ECS

Architect for AWS Fargate for Amazon ECS - Amazon Elastic Container Service

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

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.

---

## 4. Amazon ECS services

Amazon ECS services - Amazon Elastic Container Service

# Amazon ECS services

You can use an Amazon ECS service to run and maintain a specified number of instances of a task
definition simultaneously in an Amazon ECS cluster. If one of your tasks fails or stops, the
Amazon ECS service scheduler launches another instance of your task definition to replace it.
This helps maintain your desired number of tasks in the service.

You can also optionally run your service behind a load balancer. The load balancer
distributes traffic across the tasks that are associated with the service.

We recommend that you use the service scheduler for long running stateless services
and applications. The service scheduler ensures that the scheduling strategy that you
specify is followed and reschedules tasks when a task fails. For example, if the
underlying infrastructure fails, the service scheduler reschedules a task. You can use
task placement strategies and constraints to customize how the scheduler places and
terminates tasks. If a task in a service stops, the scheduler launches a new task to
replace it. This process continues until your service reaches your desired number of
tasks based on the scheduling strategy that the service uses.

The service scheduler also replaces tasks determined to be unhealthy after a container health check or a load balancer target group health check fails. This replacement depends on the `maximumPercent` and `desiredCount` service definition parameters.
If a task is marked unhealthy, the service scheduler will first start a replacement task. Then, the following happens.

* If the replacement task has a health status of `HEALTHY`, the service scheduler stops the unhealthy task
* If the replacement task has a health status of `UNHEALTHY`, the scheduler will stop either the unhealthy replacement task or the existing unhealthy task to get the total task count to equal `desiredCount`.

If the `maximumPercent` parameter limits the scheduler from starting a replacement task first, the scheduler will stop an unhealthy task one at a time at random to free up capacity, and then start a replacement task.
The start and stop process continues until all unhealthy tasks are replaced with healthy tasks. Once all unhealthy tasks have been replaced and only healthy tasks are running, if the total task count exceeds the `desiredCount`, healthy tasks are stopped at random until the total task count equals `desiredCount`. For more information about `maximumPercent` and `desiredCount`, see [Service definition parameters](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service_definition_parameters.html).

The service scheduler includes logic that throttles how often tasks are restarted if
tasks repeatedly fail to start. If a task is stopped without having entered a
`RUNNING` state, the service scheduler starts to slow down the launch
attempts and sends out a service event message. This behavior prevents unnecessary
resources from being used for failed tasks before you can resolve the issue. After the
service is updated, the service scheduler resumes normal scheduling behavior. For more
information, see [Amazon ECS service throttle logic](./service-throttle-logic.html) and [Viewing Amazon ECS service event messages](./service-event-messages.html).

## Infrastructure compute option

There are two compute options that distribute your tasks.

* A capacity provider strategy causes Amazon ECS to distribute
  your tasks in one or across multiple capacity providers.

  If you want to run your workloads on Amazon ECS Managed Instances, you must use the Capacity provider strategy option.

  For the **capacity provider strategy**, the console selects a
  compute option by default. The following describes the order that the console uses
  to select a default:

  + If your cluster has a default capacity provider strategy defined, it is
    selected.
  + If your cluster doesn't have a default capacity provider strategy defined
    but you have the Fargate capacity providers added to the
    cluster, a custom capacity provider strategy that uses the
    `FARGATE` capacity provider is selected.
  + If your cluster doesn't have a default capacity provider strategy defined
    but you have one or more Auto Scaling group capacity providers added to the cluster, the
    **Use custom (Advanced)** option is selected and you
    need to manually define the strategy.
  + If your cluster doesn't have a default capacity provider strategy defined
    and no capacity providers added to the cluster, the Fargate
    launch type is selected.
* A launch type causes Amazon ECS to launch our tasks directly
  on either Fargate or on the EC2 instances registered to your clusters.

  If you want to run your workloads on Amazon ECS Managed Instances, you must use the Capacity provider strategy option.

  By default the service starts in the subnets in your cluster VPC.

## Service auto scaling

Service auto scaling is the ability to increase or
decrease the desired number of tasks in your Amazon ECS service automatically. Amazon ECS leverages
the Application Auto Scaling service to provide this functionality.

For more information, see [Automatically scale your Amazon ECS service](./service-auto-scaling.html).

## Service load balancing

Amazon ECS services hosted on AWS Fargate support the Application Load Balancers, Network Load Balancers, and Gateway Load Balancers. Use the
following table to learn about what type of load balancer to use.

| Load Balancer type | Use in these cases |
| --- | --- |
| Application Load Balancer | Route HTTP/HTTPS (or layer 7) traffic. Application Load Balancers offer several features that make them attractive for use with Amazon ECS services:  * Each service can serve traffic from multiple load   balancers and expose multiple load balanced ports by   specifying multiple target groups. * They are supported by tasks hosted on both   Fargate and EC2   instances. * Application Load Balancers allow containers to use dynamic host port mapping   (so that multiple tasks from the same service are allowed   per container instance). * Application Load Balancers support path-based routing and priority rules (so   that multiple services can use the same listener port on a   single Application Load Balancer). |
| Network Load Balancer | Route TCP or UDP (or layer 4) traffic. |
| Gateway Load Balancer | Route TCP or UDP (or layer 4) traffic. Use virtual appliances, such as firewalls, intrusion detection and prevention systems, and deep packet inspection systems. |

For more information, see [Use load balancing to distribute Amazon ECS service traffic](./service-load-balancing.html).

## Interconecting services

If you need an application to connect to other applications that run as Amazon ECS services, Amazon ECS provides the following ways to do this without a load balancer:

* Service Connect - Allows for service-to-service communications with automatic
  discovery using short names and standard ports.
* Service discovery - Service discovery uses Route 53 to
  create a namespace for your service, which allows it to be discoverable through
  DNS.
* Amazon VPC Lattice - VPC Lattice is a fully managed application networking service to
  connect, secure, and monitor your services across multiple accounts and VPCs.
  There is a cost associated with it.

For more information, see [Interconnect Amazon ECS services](./interconnecting-services.html).

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.

---

## 5. Amazon ECS task definitions

Amazon ECS task definitions - Amazon Elastic Container Service

# Amazon ECS task definitions

A *task definition* is a blueprint for your application. It is a text
file in JSON format that describes the parameters and one or more containers that form your
application.

The following are some of the parameters that you can specify in a task definition:

* The capacity to use, which determines the infrastructure that your tasks are
  hosted on
* The Docker image to use with each container in your task
* How much CPU and memory to use with each task or each container within a
  task
* The memory and CPU requirements
* The operating system of the container that the task runs on
* The Docker networking mode to use for the containers in your task
* The logging configuration to use for your tasks
* Whether the task continues to run if the container finishes or fails
* The command that the container runs when it's started
* Any data volumes that are used with the containers in the task
* The IAM role that your tasks use

For a complete list of task definition parameters, see [Amazon ECS task definition parameters for Fargate](./task_definition_parameters.html).

After you create a task definition, you can run the task definition as a task or a
service.

* A *task* is the instantiation of a task definition within a
  cluster. After you create a task definition for your application within Amazon ECS, you
  can specify the number of tasks to run on your cluster.
* An Amazon ECS *service* runs and maintains your
  desired number of tasks simultaneously in an Amazon ECS cluster. How it works is that, if
  any of your tasks fail or stop for any reason, the Amazon ECS service scheduler launches
  another instance based on your task definition. It does this to replace it and
  thereby maintain your desired number of tasks in the service.

###### Topics

* [Amazon ECS task definition states](./task-definition-state.html)
* [Architect your application for Amazon ECS](./application_architecture.html)
* [Creating an Amazon ECS task definition using the console](./create-task-definition.html)
* [Using Amazon Q Developer to provide task definition recommendations in the Amazon ECS console](./using-amazon-q.html)
* [Updating an Amazon ECS task definition using the console](./update-task-definition-console-v2.html)
* [Deregistering an Amazon ECS task definition revision using the console](./deregister-task-definition-v2.html)
* [Deleting an Amazon ECS task definition revision using the console](./delete-task-definition-v2.html)
* [Amazon ECS task definition use cases](./use-cases.html)
* [Amazon ECS task definition parameters for Amazon ECS Managed Instances](./task_definition_parameters-managed-instances.html)
* [Amazon ECS task definition parameters for Fargate](./task_definition_parameters.html)
* [Amazon ECS task definition parameters for Amazon EC2](./task_definition_parameters_ec2.html)
* [Amazon ECS task definition template](./task-definition-template.html)
* [Example Amazon ECS task definitions](./example_task_definitions.html)

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.

---

## Bibliography

1. [Security in Amazon Elastic Container Service](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/security.html)
2. [What is Amazon Elastic Container Service?](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html)
3. [Architect for AWS Fargate for Amazon ECS](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/AWS_Fargate.html)
4. [Amazon ECS services](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs_services.html)
5. [Amazon ECS task definitions](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definitions.html)