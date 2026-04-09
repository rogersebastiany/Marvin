Overview - Amazon Bedrock 

Overview - Amazon Bedrock
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
"name" : "Amazon Bedrock",
"item" : "https://docs.aws.amazon.com/bedrock/index.html"
},
{
"@type" : "ListItem",
"position" : 3,
"name" : "User Guide",
"item" : "https://docs.aws.amazon.com/bedrock/latest/userguide"
},
{
"@type" : "ListItem",
"position" : 4,
"name" : "Overview",
"item" : "https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html"
}
]
}

[Documentation](/index.html)[Amazon Bedrock](/bedrock/index.html)[User Guide](what-is-bedrock.html)

[Quickstart](#quickstart)[Supported models](#featured-models)[What's new?](#whats-new)[Start Building](#start-building)

# Overview

Amazon Bedrock is a fully managed service that provides secure, enterprise-grade access to [high-performing foundation models](./models.html) from leading AI companies, enabling you to build and scale generative AI applications.

## Quickstart

Read the [Quickstart](./getting-started.html) to write your first API call using Amazon Bedrock in under five minutes.

Responses API
:   ```
    from openai import OpenAI

    client = OpenAI()

    response = client.responses.create(
        model="openai.gpt-oss-120b",
        input="Can you explain the features of Amazon Bedrock?"
        )
    print(response)
    ```

Chat Completions API
:   ```
    from openai import OpenAI

    client = OpenAI()

    response = client.chat.completions.create(
        model="openai.gpt-oss-120b",
        messages=[{"role": "user", "content": "Can you explain the features of Amazon Bedrock?"}]
        )
    print(response)
    ```

Invoke API
:   ```
    import json
    import boto3

    client = boto3.client('bedrock-runtime', region_name='us-east-1')
    response = client.invoke_model(
        modelId='anthropic.claude-opus-4-6-v1',
        body=json.dumps({
                'anthropic_version': 'bedrock-2023-05-31',
                'messages': [{ 'role': 'user', 'content': 'Can you explain the features of Amazon Bedrock?'}],
                'max_tokens': 1024
        })
     )
     print(json.loads(response['body'].read()))
    ```

Converse API
:   ```
    import boto3

    client = boto3.client('bedrock-runtime', region_name='us-east-1')
    response = client.converse(
        modelId='anthropic.claude-opus-4-6-v1',
        messages=[
            {
                'role': 'user',
                'content': [{'text': 'Can you explain the features of Amazon Bedrock?'}]
            }
        ]
    )
    print(response)
    ```

## Supported models

Bedrock supports [100+ foundation models](./models.html) from industry-leading providers, including Amazon, Anthropic, DeepSeek, Moonshot AI, MiniMax, and OpenAI.

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| **Nova 2** | **Claude Opus 4.6** | **Deepseek 3.2** | **Kimi K2.5** | **MiniMax M2.1** | **GPT-OSS-20B** |

## What's new?

* Amazon Bedrock now supports OpenAI-compatible [Projects API](./projects.html) in the Mantle inference engine in Amazon Bedrock.
* **Anthropic's Claude 4.6 now available on Amazon Bedrock**: [Claude Sonnet 4.6](https://aws.amazon.com/about-aws/whats-new/2026/02/claude-sonnet-4.6-available-in-amazon-bedrock/) and [Claude Opus 4.6](https://aws.amazon.com/about-aws/whats-new/2026/2/claude-opus-4.6-available-amazon-bedrock/) are now available on Amazon Bedrock.
* **[Six new open weight models](https://aws.amazon.com/about-aws/whats-new/2026/02/amazon-bedrock-adds-support-six-open-weights-models/)**: Amazon Bedrock now supports six new models spanning frontier reasoning and agentic coding: DeepSeek V3.2, MiniMax M2.1, GLM 4.7, GLM 4.7 Flash, Kimi K2.5, and Qwen3 Coder Next.
* **Server-side tools**: Amazon Bedrock [now supports](https://aws.amazon.com/about-aws/whats-new/2026/01/amazon-bedrock-server-side-custom-tools-responses-api/) server-side tools in the Responses API using OpenAI API-compatible service endpoints. You can also use your AgentCore Gateway tools to integrate with Amazon Bedrock models, enabling server-side tool execution without client-side orchestration.

## Start Building

|  |  |
| --- | --- |
|  | Explore the [APIs supported by Amazon Bedrock](./apis.html) and [Endpoints supported by Amazon Bedrock](./endpoints.html) supported by Amazon Bedrock. |
|  | Build using the [Submit prompts and generate responses with model inference](./inference.html) operations provided by Amazon Bedrock. |
|  | Customize your models to improve performance and quality. [Customize your model to improve its performance for your use case](./custom-models.html) |

**Javascript is disabled or is unavailable in your browser.**

To use the Amazon Web Services Documentation, Javascript must be enabled. Please refer to your browser's Help pages for instructions.

[Document Conventions](/general/latest/gr/docconventions.html)

Quickstart

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.