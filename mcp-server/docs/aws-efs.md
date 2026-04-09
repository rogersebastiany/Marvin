What is Amazon Elastic File System? - Amazon Elastic File System 

What is Amazon Elastic File System? - Amazon Elastic File System
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
"name" : "Amazon Elastic File System (EFS)",
"item" : "https://docs.aws.amazon.com/efs/index.html"
},
{
"@type" : "ListItem",
"position" : 3,
"name" : "User Guide",
"item" : "https://docs.aws.amazon.com/efs/latest/ug"
},
{
"@type" : "ListItem",
"position" : 4,
"name" : "What is Amazon Elastic File System?",
"item" : "https://docs.aws.amazon.com/efs/latest/ug/whatisefs.html"
}
]
}

[Documentation](/index.html)[Amazon Elastic File System (EFS)](/efs/index.html)[User Guide](whatisefs.html)

[Are you a first-time user of Amazon EFS?](#welcome-first-time-user)

# What is Amazon Elastic File System?

Amazon Elastic File System (Amazon EFS) provides serverless, fully elastic file storage so that you can share file
data without provisioning or managing storage capacity and performance. Amazon EFS is built to scale
on demand to petabytes without disrupting applications, growing and shrinking automatically as
you add and remove files. Because Amazon EFS has a simple web services interface, you can create and
configure file systems quickly and easily. The service manages all the file storage
infrastructure for you, meaning that you can avoid the complexity of deploying, patching, and
maintaining complex file system configurations.

Amazon EFS supports the Network File System version 4 (NFSv4.1 and NFSv4.0) protocol, so the
applications and tools that you use today work seamlessly with Amazon EFS. Amazon EFS is accessible across
most types of Amazon Web Services compute instances, including Amazon EC2, Amazon ECS, Amazon EKS, AWS Lambda,
and AWS Fargate.

The service is designed to be highly scalable, highly available, and highly durable. Amazon EFS
offers the following file system types to meet your availability and durability needs:

* *Regional* (Recommended) – Regional file systems (recommended) store data redundantly across multiple geographically separated Availability Zones within the same AWS Region.
  Storing data across multiple Availability Zones provides continuous availability to the data, even when one or more Availability Zones in an AWS Region are unavailable.
* *One Zone* – One Zone file systems store data within a single Availability Zone. Storing data in a single Availability Zone provides continuous availability to the data.
  In the unlikely case of the loss or damage to all or part of the Availability Zone, however, data that is stored in these types of file systems
  might be lost.

For more information about file system types, see [EFS file system types](./features.html#file-system-type).

Amazon EFS provides the throughput, IOPS, and low latency needed for a broad range of workloads.
EFS file systems can grow to petabyte scale, drive high levels of throughput, and
allow massively parallel access from compute instances to your data. For most workloads, we
recommend using the default modes, which are the General Purpose performance mode and the
Elastic throughput modes.

* *General Purpose* – The General Purpose performance mode is ideal for
  latency-sensitive applications, like web-serving environments, content-management systems,
  home directories, and general file serving.
* *Elastic* – The Elastic
  throughput mode is designed to automatically scale throughput performance up or down to
  meet the needs of your workload activity.

For more information about EFS performance and throughput modes, see [Amazon EFS performance specifications](./performance.html).

Amazon EFS provides file-system-access semantics, such as strong data consistency and file
locking. For more information, see [Data consistency in Amazon EFS](./features.html#consistency).
Amazon EFS also supports controlling access to your file systems through Portable Operating System
Interface (POSIX) permissions. For more information, see [Securing your data in Amazon EFS](./security-considerations.html).

Amazon EFS supports authentication, authorization, and encryption capabilities to help you meet
your security and compliance requirements. Amazon EFS supports two forms of encryption for file
systems: encryption in transit and encryption at rest. You can enable encryption at rest when
creating an EFS file system. If you do, all of your data and metadata is encrypted.
You can enable encryption in transit when you mount the file system. NFS client access to Amazon EFS
is controlled by both AWS Identity and Access Management (IAM) policies and network security policies, such as security
groups. For more information, see [Data encryption in Amazon EFS](./encryption.html), [Identity and access management for Amazon EFS](./security-iam.html), and [Controlling network access to EFS file systems for NFS clients](./NFS-access-control-efs.html).

###### Note

Using Amazon EFS with Microsoft Windows–based Amazon EC2 instances is not supported.

## Are you a first-time user of Amazon EFS?

If you are a first-time user of Amazon EFS, we recommend that you read the following sections
in order:

1. For an Amazon EFS product and pricing overview, see [Amazon EFS](https://aws.amazon.com/efs/).
2. For an Amazon EFS technical overview, see [How Amazon EFS works](./how-it-works.html).
3. Try the [Getting started](./getting-started.html) exercise.

If you want to learn more about Amazon EFS, the following topics discuss the service in greater
detail:

* [Creating and managing EFS resources](./creating-using.html)
* [Managing EFS file systems](./managing.html)
* [Amazon EFS API](./api-reference.html)

**Javascript is disabled or is unavailable in your browser.**

To use the Amazon Web Services Documentation, Javascript must be enabled. Please refer to your browser's Help pages for instructions.

[Document Conventions](/general/latest/gr/docconventions.html)

How it works

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.