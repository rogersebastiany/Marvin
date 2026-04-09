What is Amazon API Gateway? - Amazon API Gateway 

What is Amazon API Gateway? - Amazon API Gateway
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
"name" : "Amazon API Gateway",
"item" : "https://docs.aws.amazon.com/apigateway/index.html"
},
{
"@type" : "ListItem",
"position" : 3,
"name" : "Developer Guide",
"item" : "https://docs.aws.amazon.com/apigateway/latest/developerguide"
},
{
"@type" : "ListItem",
"position" : 4,
"name" : "What is Amazon API Gateway?",
"item" : "https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html"
}
]
}

[Documentation](/index.html)[Amazon API Gateway](/apigateway/index.html)[Developer Guide](welcome.html)

[Architecture of API Gateway](#api-gateway-overview-aws-backbone)[Features of API Gateway](#api-gateway-overview-features)[Accessing API Gateway](#introduction-accessing-apigateway)[Part of AWS serverless infrastructure](#api-gateway-overview-a-serverless-pillar)[How to get started with Amazon API Gateway](#welcome-how-to-get-started)

# What is Amazon API Gateway?

Amazon API Gateway is an AWS service for creating, publishing, maintaining, monitoring, and
securing REST, HTTP, and WebSocket APIs at any scale. API developers can create APIs that
access AWS or other web services, as well as data stored in the [AWS Cloud](https://aws.amazon.com/what-is-cloud-computing/). As an API Gateway
API developer, you can create APIs for use in your own client applications. Or you can make
your APIs available to third-party app developers. For more information, see [Who uses API Gateway?](./api-gateway-overview-developer-experience.html#apigateway-who-uses-api-gateway).

API Gateway creates RESTful APIs that:

* Are HTTP-based.
* Enable stateless client-server communication.
* Implement standard HTTP methods such as GET, POST, PUT, PATCH, and DELETE.

For more information about API Gateway REST APIs and HTTP APIs, see [Choose between REST APIs and HTTP APIs](./http-api-vs-rest.html), [API Gateway HTTP APIs](./http-api.html), [Use API Gateway to create REST APIs](./api-gateway-overview-developer-experience.html#api-gateway-overview-rest), and [Develop REST APIs in API Gateway](./rest-api-develop.html).

API Gateway creates WebSocket APIs that:

* Adhere to the [WebSocket](https://datatracker.ietf.org/doc/html/rfc6455)
  protocol, which enables stateful, full-duplex communication between client and
  server.
* Route incoming messages based on message content.

For more information about API Gateway WebSocket APIs, see [Use API Gateway to create WebSocket APIs](./api-gateway-overview-developer-experience.html#api-gateway-overview-websocket) and [Overview of WebSocket APIs in API Gateway](./apigateway-websocket-api-overview.html).

###### Topics

* [Architecture of API Gateway](#api-gateway-overview-aws-backbone)
* [Features of API Gateway](#api-gateway-overview-features)
* [API Gateway use cases](./api-gateway-overview-developer-experience.html)
* [Accessing API Gateway](#introduction-accessing-apigateway)
* [Part of AWS serverless infrastructure](#api-gateway-overview-a-serverless-pillar)
* [How to get started with Amazon API Gateway](#welcome-how-to-get-started)
* [Amazon API Gateway concepts](./api-gateway-basic-concept.html)
* [Choose between REST APIs and HTTP APIs](./http-api-vs-rest.html)
* [Get started with the REST API console](./getting-started-rest-new-console.html)

## Architecture of API Gateway

The following diagram shows API Gateway architecture.

This diagram illustrates how the APIs you build in Amazon API Gateway provide you or your
developer customers with an integrated and consistent developer experience for building
AWS serverless applications. API Gateway handles all the tasks involved in accepting and
processing up to hundreds of thousands of concurrent API calls. These tasks include
traffic management, authorization and access control, monitoring, and API version
management.

API Gateway acts as a "front door" for applications to access data, business logic, or
functionality from your backend services, such as workloads running on Amazon Elastic Compute Cloud
(Amazon EC2), code running on AWS Lambda, any web application, or real-time communication
applications.

## Features of API Gateway

Amazon API Gateway offers features such as the following:

* Support for stateful ([WebSocket](./apigateway-websocket-api.html)) and stateless ([HTTP](./http-api.html) and
  [REST](./apigateway-rest-api.html)) APIs.
* Powerful, flexible [authentication](./apigateway-control-access-to-api.html) mechanisms, such as AWS Identity and Access Management policies, Lambda
  authorizer functions, and Amazon Cognito user pools.
* [Canary release deployments](./canary-release.html) for safely
  rolling out changes.
* [CloudTrail](./cloudtrail.html) logging and monitoring of API usage and
  API changes.
* CloudWatch access logging and execution logging, including the ability to set
  alarms. For more information, see [Monitor REST API execution with Amazon CloudWatch metrics](./monitoring-cloudwatch.html) and
  [Monitor WebSocket API execution with CloudWatch metrics](./apigateway-websocket-api-logging.html).
* Ability to use CloudFormation templates to enable API creation. For more information,
  see [Amazon API Gateway Resource
  Types Reference](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ApiGateway.html) and [Amazon API Gateway V2 Resource
  Types Reference](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ApiGatewayV2.html).
* Support for [custom domain
  names](./how-to-custom-domains.html).
* Integration with [AWS WAF](./apigateway-control-access-aws-waf.html) for protecting your APIs against common web exploits.
* Integration with [AWS X-Ray](./apigateway-xray.html) for
  understanding and triaging performance latencies.

For a complete list of API Gateway feature releases, see [Document history](./history.html).

## Accessing API Gateway

You can access Amazon API Gateway in the following ways:

* **AWS Management Console** – The AWS Management Console provides a web interface for creating
  and managing APIs. After you complete the steps in [Set up to use API Gateway](./setting-up.html), you can access the API Gateway
  console at <https://console.aws.amazon.com/apigateway>.
* **AWS SDKs** – If you're using a
  programming language that AWS provides an SDK for, you can use an SDK to access
  API Gateway. SDKs simplify authentication, integrate easily with your development
  environment, and provide access to API Gateway commands. For more information, see
  [Tools for Amazon Web
  Services](https://aws.amazon.com/developer/tools/).
* **API Gateway V1 and V2 APIs** – If you're using
  a programming language that an SDK isn't available for, see the [Amazon API Gateway Version 1 API Reference](https://docs.aws.amazon.com/apigateway/latest/api/API_Operations.html)
  and [Amazon API Gateway Version 2 API Reference](https://docs.aws.amazon.com/apigatewayv2/latest/api-reference/api-reference.html).
* **AWS Command Line Interface** – For more information, see
  [Getting Set Up with the AWS Command Line Interface](https://docs.aws.amazon.com/cli/latest/userguide/) in the
  *AWS Command Line Interface User Guide*.
* **AWS Tools for Windows PowerShell** – For more information, see
  [Setting Up the AWS Tools for Windows PowerShell](https://docs.aws.amazon.com/powershell/latest/userguide/) in the
  *AWS Tools for PowerShell User Guide*.

## Part of AWS serverless infrastructure

Together with [AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/), API Gateway forms the app-facing
part of the AWS serverless infrastructure. To learn more about getting started with serverless, see the
[Serverless Developer Guide](https://docs.aws.amazon.com/serverless/latest/devguide/welcome.html).

For an app to call publicly available AWS services, you can use Lambda to interact
with required services and expose Lambda functions through API methods in API Gateway.
AWS Lambda runs your code on a highly available computing infrastructure. It performs the
necessary execution and administration of computing resources. To enable serverless
applications, API Gateway supports [streamlined
proxy integrations](./api-gateway-set-up-simple-proxy.html) with AWS Lambda and HTTP endpoints.

## How to get started with Amazon API Gateway

For an introduction to Amazon API Gateway, see the following:

* [Get started with API Gateway](./getting-started.html), which provides a walkthrough for creating an HTTP API.
* [Serverless land](https://serverlessland.com/video?tag=Amazon%20API%20Gateway), which provides instructional videos.
* [Happy Little API
  Shorts](https://www.youtube.com/playlist?list=PLJo-rJlep0EDFw7t0-IBHffVYKcPMDXHY), which is a series of brief instructional videos.

**Javascript is disabled or is unavailable in your browser.**

To use the Amazon Web Services Documentation, Javascript must be enabled. Please refer to your browser's Help pages for instructions.

[Document Conventions](/general/latest/gr/docconventions.html)

API Gateway use cases

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.