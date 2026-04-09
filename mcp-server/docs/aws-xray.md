What is AWS X-Ray? - AWS X-Ray 

What is AWS X-Ray? - AWS X-Ray
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
"name" : "AWS X-Ray",
"item" : "https://docs.aws.amazon.com/xray/index.html"
},
{
"@type" : "ListItem",
"position" : 3,
"name" : "Developer Guide",
"item" : "https://docs.aws.amazon.com/xray/latest/devguide"
},
{
"@type" : "ListItem",
"position" : 4,
"name" : "What is AWS X-Ray?",
"item" : "https://docs.aws.amazon.com/xray/latest/devguide/aws-xray.html"
}
]
}

[Documentation](/index.html)[AWS X-Ray](/xray/index.html)[Developer Guide](aws-xray.html)

# What is AWS X-Ray?

AWS X-Ray is a service that collects data about requests that your application serves, and provides tools that
you can use to view, filter, and gain insights into that data to identify issues and opportunities for optimization.
For any traced request to your application, you can see detailed information not only about the request and
response, but also about calls that your application makes to downstream AWS resources, microservices, databases,
and web APIs.

AWS X-Ray receives traces from your application, in addition to AWS services your application uses that are
already integrated with X-Ray. Instrumenting your application involves sending trace data for incoming and outbound
requests and other events within your application, along with metadata about each request. Many instrumentation
scenarios require only configuration changes. For example, you can instrument all incoming HTTP requests and
downstream calls to AWS services that your Java application makes. There are several SDKs, agents, and tools that
can be used to instrument your application for X-Ray tracing.
See [Instrumenting your application](./xray-instrumenting-your-app.html) for more information.

AWS services that are [integrated with X-Ray](./xray-services.html) can add tracing headers to
incoming requests, send trace data to X-Ray, or run the X-Ray daemon. For example, AWS Lambda can send trace data
about requests to your Lambda functions, and run the X-Ray daemon on workers to make it simpler to use the X-Ray
SDK.

Instead of sending trace data directly to X-Ray, each client SDK sends JSON segment documents to a
daemon process listening for UDP traffic. The [X-Ray daemon](./xray-daemon.html) buffers segments in a queue and uploads them to X-Ray in
batches. The daemon is available for Linux, Windows, and macOS, and is included on AWS Elastic Beanstalk and
AWS Lambda platforms.

X-Ray uses trace data from the AWS resources that power your cloud applications to generate
a detailed *trace map*. The trace map shows the client,
your front-end service, and backend services that your front-end service calls to process
requests and persist data. Use the trace map to identify bottlenecks, latency spikes, and
other issues to solve to improve the performance of your applications.

**Javascript is disabled or is unavailable in your browser.**

To use the Amazon Web Services Documentation, Javascript must be enabled. Please refer to your browser's Help pages for instructions.

[Document Conventions](/general/latest/gr/docconventions.html)

Getting started

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.