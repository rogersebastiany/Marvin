Amazon ECS task IAM role - Amazon Elastic Container Service 

Amazon ECS task IAM role - Amazon Elastic Container Service
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
"name" : "Security in Amazon Elastic Container Service",
"item" : "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/security.html"
},
{
"@type" : "ListItem",
"position" : 5,
"name" : "Identity and Access Management for Amazon Elastic Container Service",
"item" : "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/security-iam.html"
},
{
"@type" : "ListItem",
"position" : 6,
"name" : "IAM roles for Amazon ECS",
"item" : "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/security-ecs-iam-role-overview.html"
},
{
"@type" : "ListItem",
"position" : 7,
"name" : "Amazon ECS task IAM role",
"item" : "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/security-ecs-iam-role-overview.html"
}
]
}

[Documentation](/index.html)[Amazon ECS](/ecs/index.html)[Developer Guide](Welcome.html)

[Creating the task IAM role](#create_task_iam_policy_and_role)[Amazon ECR permissions](#ecr-required-iam-permissions)[ECS Exec permissions](#ecs-exec-required-iam-permissions)[Amazon EC2 instances additional configuration](#task-iam-role-considerations)[External instance additional configuration](#enable_task_iam_roles)[Amazon EC2 Windows instance additional configuration](#windows_task_IAM_roles)

# Amazon ECS task IAM role

Your Amazon ECS tasks can have an IAM role associated with them. The permissions granted in the IAM role are vended to containers running in the task. This role allows your application code (running in the container) to use other AWS services. The task role is
required when your application accesses other AWS services, such as Amazon S3.

###### Note

These permissions aren't accessed by the Amazon ECS container and Fargate agents. For the IAM permissions
that Amazon ECS needs to pull container images and run the task, see [Amazon ECS task execution IAM role](./task_execution_IAM_role.html).

The following are the benefits of using task roles:

* **Separation of concerns**: If you're using EC2,
  task IAM roles allow you to specify IAM permissions for your containers
  without requiring these permissions to be specified using EC2 instance profiles (for
  more information, see [Using instance profiles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-ec2_instance-profiles.html) in the *AWS Identity and Access Management User
  Guide*). Therefore, you can deploy your applications independently and
  uniformly on ECS container instances without needing to modify IAM permissions
  associated with EC2 instances.
* **Auditability**: Access and event logging are
  available through CloudTrail to ensure retrospective auditing. Task credentials have a
  context of '`taskArn`' that is attached to the session, so CloudTrail logs show
  which task the role credentials were vended for.
* **Uniform credentials delivery**: ECS delivers IAM
  role credentials to your containers and makes them accessible through a well-defined
  interface irrespective of the compute option associated with your tasks. On ECS
  Fargate, EC2 instance profiles are not available for containers in your tasks.
  Task IAM roles enable you to associate IAM permissions to your containers
  irrespective of the compute option when you use AWS SDK or AWS CLI in your
  containers. For more information about how the AWS SDK accesses these credentials,
  see [Container
  credential provider](https://docs.aws.amazon.com/sdkref/latest/guide/feature-container-credentials.html).

###### Important

Containers are not a security boundary and the use of task IAM roles does not change
this. Each task running on Fargate has its own isolation boundary and does not share
the underlying kernel, CPU resources, memory resources, or elastic network interface
with another task. For EC2 and External Container Instances on ECS, there is no task
isolation (unlike with Fargate) and containers can potentially access credentials for
other tasks on the same container instance. They can also access permissions assigned to
the [ECS container instance
role](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/instance_IAM_role.html).
Follow the recommendations in [Roles recommendations](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/security-iam-roles.html#security-iam-roles-recommendations) to block access to the Amazon EC2 Instance Metadata
Service for containers (For more information, see [Use the
Instance Metadata Service to access instance metadata](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html) in the *Amazon EC2 User Guide*).

Note that when you specify an IAM role for a task, the AWS CLI or other SDKs in
the containers for that task use the AWS credentials provided by the task role
exclusively and they do not inherit any IAM permissions from the Amazon EC2 or
external instance they are running on.

## Creating the task IAM role

When creating an IAM policy for your tasks to use, the policy must include the
permissions that you want the containers in your tasks to assume. You can use an
existing AWS managed policy, or you can create a custom policy from scratch that meets
your specific needs. For more information, see [Creating IAM
policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_create.html) in the *IAM User Guide*.

###### Important

For Amazon ECS tasks (for all launch types), we recommend that you use the IAM policy
and role for your tasks. These credentials allow your task to make AWS API
requests without calling `sts:AssumeRole` to assume the same role that is
already associated with the task. If your task requires that a role assumes itself,
you must create a trust policy that explicitly allows that role to assume itself.
For more information, see  [Updating a role trust policy](https://docs.aws.amazon.com//IAM/latest/UserGuide/id_roles_update-role-trust-policy.html) in the *IAM User Guide*.

After the IAM policy is created, you can create an IAM role which includes that
policy which you reference in your Amazon ECS task definition. You can create the role using
the **Elastic Container Service Task** use case in the IAM console.
Then, you can attach your specific IAM policy to the role that gives the containers in
your task the permissions you desire. The procedures below describe how to do
this.

If you have multiple task definitions or services that require IAM permissions, you
should consider creating a role for each specific task definition or service with the
minimum required permissions for the tasks to operate so that you can minimize the
access that you provide for each task.

For information about the service endpoint for your Region, see [Service
endpoints](https://docs.aws.amazon.com/general/latest/gr/ecs-service.html#ecs_region) in the *Amazon Web Services General Reference Guide*.

The IAM task role must have a trust policy that specifies the
`ecs-tasks.amazonaws.com` service. The `sts:AssumeRole`
permission allows your tasks to assume an IAM role that's different from the one that
the Amazon EC2 instance uses. This way, your task doesn't inherit the role associated with
the Amazon EC2 instance. The following is an example trust policy. Replace the Region
identifier and specify the AWS account number that you use when launching
tasks.

###### Important

When creating your task IAM role, it is recommended that you use the
`aws:SourceAccount` or `aws:SourceArn` condition keys in
the trust relationship policy associated with the role to scope
the permissions further to prevent the confused deputy security issue. Using the
`aws:SourceArn` condition key to specify a specific cluster is not
currently supported, you should use the wildcard to specify all clusters. To learn
more about the confused deputy problem and how to protect your AWS account, see
[The
confused deputy problem](https://docs.aws.amazon.com/IAM/latest/UserGuide/confused-deputy.html) in the
*IAM User Guide*.

JSON
:   :   ```
        {
           "Version":"2012-10-17",
           "Statement":[
              {
                 "Effect":"Allow",
                 "Principal":{
                    "Service":[
                       "ecs-tasks.amazonaws.com"
                    ]
                 },
                 "Action":"sts:AssumeRole",
                 "Condition":{
                    "ArnLike":{
                    "aws:SourceArn":"arn:aws:ecs:us-west-2:111122223333:*"
                    },
                    "StringEquals":{
                       "aws:SourceAccount":"111122223333"
                    }
                 }
              }
           ]
        }
        ```

Use the following procedure to create a policy to retrieve objects from Amazon S3
with an example policy. Replace all `user input` with your own
values.

AWS Management Console
:   ###### To use the JSON policy editor to create a policy

    1. Sign in to the AWS Management Console and open the IAM console at <https://console.aws.amazon.com/iam/>.
    2. In the navigation pane on the left, choose **Policies**.

       If this is your first time choosing **Policies**, the
       **Welcome to Managed Policies** page appears. Choose **Get
       Started**.
    3. At the top of the page, choose **Create policy**.
    4. In the **Policy editor** section, choose the
       **JSON** option.
    5. Enter the following JSON policy document:

       ```
       {
          "Version":"2012-10-17",
          "Statement":[
             {
                "Effect":"Allow",
                "Action":[
                   "s3:GetObject"
                ],
                "Resource":[
                   "arn:aws:s3:::my-task-secrets-bucket/*"
                ]
             }
          ]
       }
       ```
    6. Choose **Next**.

       ###### Note

       You can switch between the **Visual** and **JSON**
       editor options anytime. However, if you make changes or choose **Next**
       in the **Visual** editor, IAM might restructure your policy to
       optimize it for the visual editor. For more information, see [Policy restructuring](https://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_policies.html#troubleshoot_viseditor-restructure)
       in the *IAM User Guide*.
    7. On the **Review and create** page, enter a **Policy
       name** and a **Description** (optional) for the policy that
       you are creating. Review **Permissions defined in this policy** to see
       the permissions that are granted by your policy.
    8. Choose **Create policy** to save your new policy.

AWS CLI
:   Replace all `user input` with your own values.

    1. Create a file called `s3-policy.json` with the
       following content.

       JSON

       JSON
       :   :   ```
               {
                  "Version":"2012-10-17",
                  "Statement":[
                     {
                        "Effect":"Allow",
                        "Action":[
                           "s3:GetObject"
                        ],
                        "Resource":[
                           "arn:aws:s3:::my-task-secrets-bucket/*"
                        ]
                     }
                  ]
               }
               ```
    2. Use the following command to create the IAM policy using the
       JSON policy document file. Replace all `user
       input` with your own values.

       ```
       aws iam create-policy \
             --policy-name taskRolePolicy \
             --policy-document file://s3-policy.json
       ```

Use the following procedure to create the service role.

AWS Management Console
:   ###### To create the service role for Elastic Container Service (IAM console)

    1. Sign in to the AWS Management Console and open the IAM console at <https://console.aws.amazon.com/iam/>.
    2. In the navigation pane of the IAM console, choose **Roles**, and
       then choose **Create role**.
    3. For **Trusted entity type**, choose **AWS service**.
    4. For **Service or use case**, choose **Elastic Container Service**, and then choose the **Elastic Container Service Task** use case.
    5. Choose **Next**.
    6. For **Add permissions**, search for and choose the policy you
       created.
    7. Choose **Next**.
    8. For **Role name**, enter a name for your role. For
       this example, type `AmazonECSTaskS3BucketRole` to name the
       role.
    9. Review the role, and then choose **Create role**.

AWS CLI
:   1. Create a file named `ecs-tasks-trust-policy.json` that
       contains the trust policy to use for the task IAM role. The file
       should contain the following. Replace the Region identifier and
       specify the AWS account number that you use when launching
       tasks.

       JSON

       JSON
       :   :   ```
               {
                  "Version":"2012-10-17",
                  "Statement":[
                     {
                        "Effect":"Allow",
                        "Principal":{
                           "Service":[
                              "ecs-tasks.amazonaws.com"
                           ]
                        },
                        "Action":"sts:AssumeRole",
                        "Condition":{
                           "ArnLike":{
                           "aws:SourceArn":"arn:aws:ecs:us-west-2:111122223333:*"
                           },
                           "StringEquals":{
                              "aws:SourceAccount":"111122223333"
                           }
                        }
                     }
                  ]
               }
               ```
    2. Create an IAM role named `ecsTaskRole` using the
       trust policy created in the previous step.

       ```
       aws iam create-role \
             --role-name ecsTaskRole \
             --assume-role-policy-document file://ecs-tasks-trust-policy.json
       ```
    3. Retrieve the ARN of the IAM policy you created using the
       following command. Replace `taskRolePolicy`
       with the name of the policy you created.

       ```
       aws iam list-policies --scope Local --query 'Policies[?PolicyName==`taskRolePolicy`].Arn'
       ```
    4. Attach the IAM policy you created to the
       `ecsTaskRole` role. Replace the
       `policy-arn` with the ARN of the policy that you
       created.

       ```
       aws iam attach-role-policy \
             --role-name ecsTaskRole \
             --policy-arn arn:aws:iam:111122223333:aws:policy/taskRolePolicy
       ```

After you create the role, add additional permissions to the role for the following
features.

| Feature | Additional permissions |
| --- | --- |
| Use ECS Exec | [ECS Exec permissions](#ecs-exec-required-iam-permissions) |
| Use an image from a private Amazon ECR repository | [Amazon ECR permissions](#ecr-required-iam-permissions) |
| Use EC2 instances (Windows and Linux) | [Amazon EC2 instances additional configuration](#task-iam-role-considerations) |
| Use external instances | [External instance additional configuration](#enable_task_iam_roles) |
| Use Windows EC2 instances | [Amazon EC2 Windows instance additional configuration](#windows_task_IAM_roles) |

## Amazon ECR permissions

The following permissions are required when your application code needs to interact with Amazon ECR repositories directly. Note that for basic implementation where you only need to pull images from Amazon ECR, these permissions are not required at the task IAM role level. Instead, the Amazon ECS task execution role should have these permissions. For more information about the task execution role, see [Amazon ECS task execution IAM role](./task_execution_IAM_role.html).

If your application code running in the container needs to interact with Amazon ECR APIs directly, you should add the
following permissions to a task IAM role and include the task IAM role in your task
definition. For more information, see [Adding and
Removing IAM Policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage-attach-detach.html) in the *IAM User Guide*.

Use the following policy for your task IAM role to add the required Amazon ECR
permissions for container applications that need to interact with Amazon ECR directly:

JSON
:   :   ```
        {
            "Version":"2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "ecr:BatchGetImage",
                        "ecr:GetDownloadUrlForLayer",
                        "ecr:GetAuthorizationToken"
                    ],
                    "Resource": "*"
                }
            ]
        }
        ```

## ECS Exec permissions

The [ECS Exec](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-exec.html) feature requires a task IAM role to grant containers the
permissions needed for communication between the managed SSM agent
(`execute-command` agent) and the SSM service. You should add the
following permissions to a task IAM role and include the task IAM role in your task
definition. For more information, see [Adding and
Removing IAM Policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage-attach-detach.html) in the *IAM User Guide*.

Use the following policy for your task IAM role to add the required SSM
permissions.

JSON
:   :   ```
        {
           "Version":"2012-10-17",
           "Statement": [
               {
               "Effect": "Allow",
               "Action": [
                    "ssmmessages:CreateControlChannel",
                    "ssmmessages:CreateDataChannel",
                    "ssmmessages:OpenControlChannel",
                    "ssmmessages:OpenDataChannel"
               ],
              "Resource": "*"
              }
           ]
        }
        ```

## Amazon EC2 instances additional configuration

We recommend that you limit the permissions in your container instance role to the
minimal list of permissions used in the `AmazonEC2ContainerServiceforEC2Role`
managed IAM policy.

Your Amazon EC2 instances require at least version `1.11.0` of the container
agent to use task role; however, we recommend using the latest container agent version.
For information about checking your agent version and updating to the latest version,
see [Updating the Amazon ECS container agent](./ecs-agent-update.html). If you use an
Amazon ECS-optimized AMI, your instance needs at least `1.11.0-1` of the
`ecs-init` package. If your instances are using the latest
Amazon ECS-optimized AMI, then they contain the required versions of the container agent and
`ecs-init`. For more information, see [Amazon ECS-optimized Linux AMIs](./ecs-optimized_AMI.html).

If you are not using the Amazon ECS-optimized AMI for your container instances, add the
`--net=host` option to your **docker run** command that
starts the agent and the following agent configuration variables for your desired
configuration (for more information, see [Amazon ECS container agent configuration](./ecs-agent-config.html)):

`ECS_ENABLE_TASK_IAM_ROLE=true`
:   Uses IAM roles for tasks for containers with the `bridge` and
    `default` network modes.

`ECS_ENABLE_TASK_IAM_ROLE_NETWORK_HOST=true`
:   Uses IAM roles for tasks for containers with the `host`
    network mode. This variable is only supported on agent versions 1.12.0 and
    later.

For an example run command, see [Manually updating the Amazon ECS container agent (for non-Amazon ECS-Optimized AMIs)](./manually_update_agent.html). You will also need to set the following
networking commands on your container instance so that the containers in your tasks can
retrieve their AWS credentials:

```
sudo sysctl -w net.ipv4.conf.all.route_localnet=1
sudo iptables -t nat -A PREROUTING -p tcp -d 169.254.170.2 --dport 80 -j DNAT --to-destination 127.0.0.1:51679
sudo iptables -t nat -A OUTPUT -d 169.254.170.2 -p tcp -m tcp --dport 80 -j REDIRECT --to-ports 51679
```

You must save these **iptables** rules on your container instance for
them to survive a reboot. You can use the **iptables-save** and
**iptables-restore** commands to save your
**iptables** rules and restore them at boot. For more information,
consult your specific operating system documentation.

To prevent containers run by tasks that use the `awsvpc` network mode from
accessing the credential information supplied to the Amazon EC2 instance profile, while still
allowing the permissions that are provided by the task role, set the
`ECS_AWSVPC_BLOCK_IMDS` agent configuration variable to `true`
in the agent configuration file and restart the agent. For more information, see [Amazon ECS container agent configuration](./ecs-agent-config.html).

To prevent containers run by tasks that use the `bridge` network mode from
accessing the credential information supplied to the Amazon EC2 instance profile, while still
allowing the permissions that are provided by the task role, by running the following
**iptables** command on your Amazon EC2 instances. This command doesn't
affect containers in tasks that use the `host` or `awsvpc` network
modes. For more information, see [Network mode](./task_definition_parameters.html#network_mode).

* ```
  sudo yum install -y iptables-services; sudo iptables --insert DOCKER-USER 1 --in-interface docker+ --destination 169.254.169.254/32 --jump DROP
  ```

  You must save this **iptables** rule on your Amazon EC2 instance for
  it to survive a reboot. When using the Amazon ECS-optimized AMI, you can use the
  following command. For other operating systems, consult the documentation for
  that operating system.

  ```
  sudo iptables-save | sudo tee /etc/sysconfig/iptables && sudo systemctl enable --now iptables
  ```

## External instance additional configuration

Your external instances require at least version `1.11.0` of the container
agent to use task IAM roles; however, we recommend using the latest container agent
version. For information about checking your agent version and updating to the latest
version, see [Updating the Amazon ECS container agent](./ecs-agent-update.html). If you
are using an Amazon ECS-optimized AMI, your instance needs at least `1.11.0-1` of
the `ecs-init` package. If your instances are using the latest
Amazon ECS-optimized AMI, then they contain the required versions of the container agent and
`ecs-init`. For more information, see [Amazon ECS-optimized Linux AMIs](./ecs-optimized_AMI.html).

If you are not using the Amazon ECS-optimized AMI for your container instances, add the
`--net=host` option to your **docker run** command that
starts the agent and the following agent configuration variables for your desired
configuration (for more information, see [Amazon ECS container agent configuration](./ecs-agent-config.html)):

`ECS_ENABLE_TASK_IAM_ROLE=true`
:   Uses IAM roles for tasks for containers with the `bridge` and
    `default` network modes.

`ECS_ENABLE_TASK_IAM_ROLE_NETWORK_HOST=true`
:   Uses IAM roles for tasks for containers with the `host`
    network mode. This variable is only supported on agent versions 1.12.0 and
    later.

For an example run command, see [Manually updating the Amazon ECS container agent (for non-Amazon ECS-Optimized AMIs)](./manually_update_agent.html). You will also need to set the following
networking commands on your container instance so that the containers in your tasks can
retrieve their AWS credentials:

```
sudo sysctl -w net.ipv4.conf.all.route_localnet=1
sudo iptables -t nat -A PREROUTING -p tcp -d 169.254.170.2 --dport 80 -j DNAT --to-destination 127.0.0.1:51679
sudo iptables -t nat -A OUTPUT -d 169.254.170.2 -p tcp -m tcp --dport 80 -j REDIRECT --to-ports 51679
```

You must save these **iptables** rules on your container instance for
them to survive a reboot. You can use the **iptables-save** and
**iptables-restore** commands to save your
**iptables** rules and restore them at boot. For more information,
consult your specific operating system documentation.

## Amazon EC2 Windows instance additional configuration

###### Important

This applies only to Windows containers on EC2 that use task
roles.

The task role with Windows features requires additional configuration on
EC2.

* When you launch your container instances, you must set the
  `-EnableTaskIAMRole` option in the container instances user data
  script. The `EnableTaskIAMRole` turns on the Task IAM roles feature for
  the tasks. For example:

  ```
  <powershell>
  Import-Module ECSTools
  Initialize-ECSAgent -Cluster 'windows' -EnableTaskIAMRole 
  </powershell>
  ```
* You must bootstrap your container with the networking commands that are provided
  in [Amazon ECS container bootstrap script](#windows_task_IAM_roles_bootstrap).
* You must create an IAM role and policy for your tasks. For more information, see
  [Creating the task IAM role](#create_task_iam_policy_and_role).
* The IAM roles for the task credential provider use port 80 on the container
  instance. Therefore, if you configure IAM roles for tasks on your container
  instance, your containers can't use port 80 for the host port in any port mappings.
  To expose your containers on port 80, we recommend configuring a service for them
  that uses load balancing. You can use port 80 on the load balancer. By doing so,
  traffic can be routed to another host port on your container instances. For more
  information, see [Use load balancing to distribute Amazon ECS service traffic](./service-load-balancing.html).
* If your Windows instance is restarted, you must delete the proxy interface and
  initialize the Amazon ECS container agent again to bring the credential proxy back
  up.

### Amazon ECS container bootstrap script

Before containers can access the credential proxy on the container instance to get
credentials, the container must be bootstrapped with the required networking commands.
The following code example script should be run on your containers when they
start.

###### Note

You do not need to run this script when you use `awsvpc` network mode
on Windows.

If you run Windows containers which include Powershell, then use the following
script:

```
# Copyright Amazon.com Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may
# not use this file except in compliance with the License. A copy of the
# License is located at
#
#	http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.
 
$gateway = (Get-NetRoute | Where { $_.DestinationPrefix -eq '0.0.0.0/0' } | Sort-Object RouteMetric | Select NextHop).NextHop
$ifIndex = (Get-NetAdapter -InterfaceDescription "Hyper-V Virtual Ethernet*" | Sort-Object | Select ifIndex).ifIndex
New-NetRoute -DestinationPrefix 169.254.170.2/32 -InterfaceIndex $ifIndex -NextHop $gateway -PolicyStore ActiveStore # credentials API
New-NetRoute -DestinationPrefix 169.254.169.254/32 -InterfaceIndex $ifIndex -NextHop $gateway -PolicyStore ActiveStore # metadata API
```

If you run Windows containers that only have the Command shell, then use the following
script:

```
# Copyright Amazon.com Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may
# not use this file except in compliance with the License. A copy of the
# License is located at
#
#	http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.
 
for /f "tokens=1" %i  in ('netsh interface ipv4 show interfaces ^| findstr /x /r ".*vEthernet.*"') do set interface=%i
for /f "tokens=3" %i  in ('netsh interface ipv4 show addresses %interface% ^| findstr /x /r ".*Default.Gateway.*"') do set gateway=%i
netsh interface ipv4 add route prefix=169.254.170.2/32 interface="%interface%" nexthop="%gateway%" store=active # credentials API
netsh interface ipv4 add route prefix=169.254.169.254/32 interface="%interface%" nexthop="%gateway%" store=active # metadata API
```

**Javascript is disabled or is unavailable in your browser.**

To use the Amazon Web Services Documentation, Javascript must be enabled. Please refer to your browser's Help pages for instructions.

[Document Conventions](/general/latest/gr/docconventions.html)

Task execution IAM role

Container instance IAM role

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.