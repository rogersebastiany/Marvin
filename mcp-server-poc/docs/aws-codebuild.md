What is AWS CodeBuild? - AWS CodeBuild 

What is AWS CodeBuild? - AWS CodeBuild
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
"name" : "AWS CodeBuild",
"item" : "https://docs.aws.amazon.com/codebuild/index.html"
},
{
"@type" : "ListItem",
"position" : 3,
"name" : "User Guide",
"item" : "https://docs.aws.amazon.com/codebuild/latest/userguide"
},
{
"@type" : "ListItem",
"position" : 4,
"name" : "What is AWS CodeBuild?",
"item" : "https://docs.aws.amazon.com/codebuild/latest/userguide/welcome.html"
}
]
}

[Documentation](/index.html)[AWS CodeBuild](/codebuild/index.html)[User Guide](welcome.html)

[How to run CodeBuild](#welcome-quick-look)[Pricing for CodeBuild](#welcome-pricing)[How do I get started with CodeBuild?](#welcome-getting-started)

# What is AWS CodeBuild?

AWS CodeBuild is a fully managed build service in the cloud. CodeBuild compiles your source
code, runs unit tests, and produces artifacts that are ready to deploy. CodeBuild eliminates
the need to provision, manage, and scale your own build servers. It provides prepackaged
build environments for popular programming languages and build tools such as Apache
Maven, Gradle, and more. You can also customize build environments in CodeBuild to use your
own build tools. CodeBuild scales automatically to meet peak build requests.

CodeBuild provides these benefits:

* **Fully managed** – CodeBuild eliminates the
  need to set up, patch, update, and manage your own build servers.
* **On demand** – CodeBuild scales on demand to
  meet your build needs. You pay only for the number of build minutes you
  consume.
* **Out of the box** – CodeBuild provides
  preconfigured build environments for the most popular programming languages. All
  you need to do is point to your build script to start your first build.

For more information, see [AWS CodeBuild](https://aws.amazon.com/codebuild/).

## How to run CodeBuild

You can use the AWS CodeBuild or AWS CodePipeline console to run CodeBuild. You can also automate the
running of CodeBuild by using the AWS Command Line Interface (AWS CLI) or the AWS SDKs.

As the following diagram shows, you can add CodeBuild as a build or test action to the
build or test stage of a pipeline in AWS CodePipeline. AWS CodePipeline is a continuous delivery
service that you can use to model, visualize, and automate the steps required to release
your code. This includes building your code. A *pipeline* is a
workflow construct that describes how code changes go through a release process.

To use CodePipeline to create a pipeline and then add a CodeBuild build or test action, see
[Use CodeBuild with CodePipeline](./how-to-create-pipeline.html). For more information about CodePipeline, see the [AWS CodePipeline User Guide](https://docs.aws.amazon.com/codepipeline/latest/userguide/).

The CodeBuild console also provides a way to quickly search for your resources, such as
repositories, build projects, deployment applications, and pipelines. Choose
**Go to resource** or press the `/` key, and then enter
the name of the resource. Any matches appear in the list. Searches are case insensitive.
You only see resources that you have permissions to view. For more information, see
[Viewing resources in the console](./console-resources.html).

## Pricing for CodeBuild

For information, see [CodeBuild pricing](https://aws.amazon.com/codebuild/pricing).

## How do I get started with CodeBuild?

We recommend that you complete the following steps:

1. **Learn** more about CodeBuild by reading the
   information in [Concepts](./concepts.html).
2. **Experiment** with CodeBuild in an example scenario
   by following the instructions in [Getting started using the
   console](./getting-started-overview.html#getting-started).
3. **Use** CodeBuild in your own scenarios by following
   the instructions in [Plan a build](./planning.html).

**Javascript is disabled or is unavailable in your browser.**

To use the Amazon Web Services Documentation, Javascript must be enabled. Please refer to your browser's Help pages for instructions.

[Document Conventions](/general/latest/gr/docconventions.html)

Concepts

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.