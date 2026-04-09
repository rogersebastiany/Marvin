Pass sensitive data to an Amazon ECS container - Amazon Elastic Container Service 

Pass sensitive data to an Amazon ECS container - Amazon Elastic Container Service
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
"name" : "Amazon ECS task definitions",
"item" : "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task\_definitions.html"
},
{
"@type" : "ListItem",
"position" : 5,
"name" : "Amazon ECS task definition use cases",
"item" : "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/use-cases.html"
},
{
"@type" : "ListItem",
"position" : 6,
"name" : "Pass sensitive data to an Amazon ECS container",
"item" : "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/use-cases.html"
}
]
}

[Documentation](/index.html)[Amazon ECS](/ecs/index.html)[Developer Guide](Welcome.html)

[Use AWS Secrets Manager or AWS Systems Manager Parameter Store for storing secret materials](#security-secrets-management-recommendations-storing-secret-materials)[Retrieve data from an encrypted Amazon S3 bucket](#security-secrets-management-recommendations-encrypted-s3-buckets)[Mount the secret to a volume using a sidecar container](#security-secrets-management-recommendations-mount-secret-volumes)

# Pass sensitive data to an Amazon ECS container

You can safely pass sensitive data, such as credentials to a database, into your container.

Secrets, such as API keys and database credentials, are frequently used by applications to
gain access other systems. They often consist of a username and password, a certificate, or
API key. Access to these secrets should be restricted to specific IAM principals that are
using IAM and injected into containers at runtime.

Secrets can be seamlessly injected into containers from AWS Secrets Manager and Amazon EC2 Systems Manager Parameter
Store. These secrets can be referenced in your task as any of the following.

1. They're referenced as environment variables that use the `secrets`
   container definition parameter.
2. They're referenced as `secretOptions` if your logging platform requires
   authentication. For more information, see [logging configuration options](https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_LogConfiguration.html#API_LogConfiguration_Contents).
3. They're referenced as secrets pulled by images that use the
   `repositoryCredentials` container definition parameter if the
   registry where the container is being pulled from requires authentication. Use this
   method when pulling images from Amazon ECR Public Gallery. For more information, see
   [Private registry
   authentication for tasks](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/private-auth.html).

We recommend that you do the following when setting up secrets management.

## Use AWS Secrets Manager or AWS Systems Manager Parameter Store for storing secret materials

You should securely store API keys, database credentials, and other secret
materials in Secrets Manager or as an encrypted parameter in Systems Manager Parameter
Store. These services are similar because they're both managed key-value stores
that use AWS KMS to encrypt sensitive data. Secrets Manager, however, also includes the
ability to automatically rotate secrets, generate random secrets, and share
secrets across accounts. To utilize these features, use
Secrets Manager. Otherwise, use encrypted parameters in Systems Manager Parameter
Store.

###### Important

If your secret changes, you must force a new deployment or launch a new task to retrieve
the latest secret value. For more information, see the following topics:

* Tasks - Stop the task, and then start it. For more information, see [Stopping an Amazon ECS task](./standalone-task-stop.html) and [Running an application as an Amazon ECS task](./standalone-task-create.html).
* Service - Update the service and use the force new deployment option. For more information, see [Updating an Amazon ECS service](./update-service-console-v2.html).

## Retrieve data from an encrypted Amazon S3 bucket

You should store secrets in an encrypted Amazon S3 bucket and use task roles to restrict access
to those secrets. This prevents the values of environment variables from inadvertently leaking
in logs and getting revealed when running `docker inspect`. When you do this,
your application must be written to read the secret from the Amazon S3 bucket. For
instructions, see [Setting default server-side
encryption behavior for Amazon S3 buckets](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-encryption.html).

## Mount the secret to a volume using a sidecar container

Because there's an elevated risk of data leakage with environment variables,
you should run a sidecar container that reads your secrets from AWS Secrets Manager and
write them to a shared volume. This container can run and exit before the
application container by using [Amazon ECS
container ordering](https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_ContainerDependency.html). When you do this, the application container
subsequently mounts the volume where the secret was written. Like the Amazon S3
bucket method, your application must be written to read the secret from the
shared volume. Because the volume is scoped to the task, the volume is
automatically deleted after the task stops. For an example, see the [task-def.json](https://github.com/aws-samples/aws-secret-sidecar-injector/blob/master/ecs-task-def/task-def.json) project.

On Amazon EC2, the volume that the secret is written to can be encrypted with a AWS KMS
customer managed key. On AWS Fargate, volume storage is automatically encrypted using
a service managed key.

**Javascript is disabled or is unavailable in your browser.**

To use the Amazon Web Services Documentation, Javascript must be enabled. Please refer to your browser's Help pages for instructions.

[Document Conventions](/general/latest/gr/docconventions.html)

Specifying a container restart policy in a task definition

Pass an individual environment
variable to a container

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.