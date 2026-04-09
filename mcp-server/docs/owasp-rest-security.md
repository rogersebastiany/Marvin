REST Security - OWASP Cheat Sheet Series

:root{--md-text-font:"Roboto";--md-code-font:"Roboto Mono"}
\_\_md\_scope=new URL("..",location),\_\_md\_hash=e=>[...e].reduce(((e,\_)=>(e<<5)-e+\_.charCodeAt(0)),0),\_\_md\_get=(e,\_=localStorage,t=\_\_md\_scope)=>JSON.parse(\_.getItem(t.pathname+"."+e)),\_\_md\_set=(e,\_,t=localStorage,a=\_\_md\_scope)=>{try{t.setItem(a.pathname+"."+e,JSON.stringify(\_))}catch(e){}}

[Skip to content](#rest-security-cheat-sheet)

OWASP Cheat Sheet Series

REST Security

var palette=\_\_md\_get("\_\_palette");if(palette&&palette.color){if("(prefers-color-scheme)"===palette.color.media){var media=matchMedia("(prefers-color-scheme: light)"),input=document.querySelector(media.matches?"[data-md-color-media='(prefers-color-scheme: light)']":"[data-md-color-media='(prefers-color-scheme: dark)']");palette.color.media=input.getAttribute("data-md-color-media"),palette.color.scheme=input.getAttribute("data-md-color-scheme"),palette.color.primary=input.getAttribute("data-md-color-primary"),palette.color.accent=input.getAttribute("data-md-color-accent")}for(var[key,value]of Object.entries(palette.color))document.body.setAttribute("data-md-color-"+key,value)}

Initializing search

[OWASP/CheatSheetSeries](https://github.com/OWASP/CheatSheetSeries "Go to repository")

OWASP Cheat Sheet Series

[OWASP/CheatSheetSeries](https://github.com/OWASP/CheatSheetSeries "Go to repository")

* [Introduction](../index.html)
* [Index Alphabetical](../Glossary.html)
* [Index ASVS](../IndexASVS.html)
* [Index MASVS](../IndexMASVS.html)
* [Index Proactive Controls](../IndexProactiveControls.html)
* [Index Top 10](../IndexTopTen.html)
* Cheatsheets

  Cheatsheets
  + [AI Agent Security](AI_Agent_Security_Cheat_Sheet.html)
  + [AJAX Security](AJAX_Security_Cheat_Sheet.html)
  + [Abuse Case](Abuse_Case_Cheat_Sheet.html)
  + [Access Control](Access_Control_Cheat_Sheet.html)
  + [Attack Surface Analysis](Attack_Surface_Analysis_Cheat_Sheet.html)
  + [Authentication](Authentication_Cheat_Sheet.html)
  + [Authorization](Authorization_Cheat_Sheet.html)
  + [Authorization Testing Automation](Authorization_Testing_Automation_Cheat_Sheet.html)
  + [Automotive Security](Automotive_Security_Cheat_Sheet.html)
  + [Bean Validation](Bean_Validation_Cheat_Sheet.html)
  + [Browser Extension Vulnerabilities](Browser_Extension_Vulnerabilities_Cheat_Sheet.html)
  + [C-Based Toolchain Hardening](C-Based_Toolchain_Hardening_Cheat_Sheet.html)
  + [CI CD Security](CI_CD_Security_Cheat_Sheet.html)
  + [Choosing and Using Security Questions](Choosing_and_Using_Security_Questions_Cheat_Sheet.html)
  + [Clickjacking Defense](Clickjacking_Defense_Cheat_Sheet.html)
  + [Content Security Policy](Content_Security_Policy_Cheat_Sheet.html)
  + [Cookie Theft Mitigation](Cookie_Theft_Mitigation_Cheat_Sheet.html)
  + [Credential Stuffing Prevention](Credential_Stuffing_Prevention_Cheat_Sheet.html)
  + [Cross-Site Request Forgery Prevention](Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)
  + [Cross Site Scripting Prevention](Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
  + [Cryptographic Storage](Cryptographic_Storage_Cheat_Sheet.html)
  + [DOM Clobbering Prevention](DOM_Clobbering_Prevention_Cheat_Sheet.html)
  + [DOM based XSS Prevention](DOM_based_XSS_Prevention_Cheat_Sheet.html)
  + [Database Security](Database_Security_Cheat_Sheet.html)
  + [Denial of Service](Denial_of_Service_Cheat_Sheet.html)
  + [Dependency Graph SBOM](Dependency_Graph_SBOM_Cheat_Sheet.html)
  + [Deserialization](Deserialization_Cheat_Sheet.html)
  + [Django REST Framework](Django_REST_Framework_Cheat_Sheet.html)
  + [Django Security](Django_Security_Cheat_Sheet.html)
  + [Docker Security](Docker_Security_Cheat_Sheet.html)
  + [DotNet Security](DotNet_Security_Cheat_Sheet.html)
  + [Drone Security](Drone_Security_Cheat_Sheet.html)
  + [Email Validation and Verification](Email_Validation_and_Verification_Cheat_Sheet.html)
  + [Error Handling](Error_Handling_Cheat_Sheet.html)
  + [File Upload](File_Upload_Cheat_Sheet.html)
  + [Forgot Password](Forgot_Password_Cheat_Sheet.html)
  + [GraphQL](GraphQL_Cheat_Sheet.html)
  + [HTML5 Security](HTML5_Security_Cheat_Sheet.html)
  + [HTTP Headers](HTTP_Headers_Cheat_Sheet.html)
  + [HTTP Strict Transport Security](HTTP_Strict_Transport_Security_Cheat_Sheet.html)
  + [Infrastructure as Code Security](Infrastructure_as_Code_Security_Cheat_Sheet.html)
  + [Injection Prevention](Injection_Prevention_Cheat_Sheet.html)
  + [Injection Prevention in Java](Injection_Prevention_in_Java_Cheat_Sheet.html)
  + [Input Validation](Input_Validation_Cheat_Sheet.html)
  + [Insecure Direct Object Reference Prevention](Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html)
  + [JAAS](JAAS_Cheat_Sheet.html)
  + [JSON Web Token for Java](JSON_Web_Token_for_Java_Cheat_Sheet.html)
  + [Java Security](Java_Security_Cheat_Sheet.html)
  + [Key Management](Key_Management_Cheat_Sheet.html)
  + [Kubernetes Security](Kubernetes_Security_Cheat_Sheet.html)
  + [LDAP Injection Prevention](LDAP_Injection_Prevention_Cheat_Sheet.html)
  + [LLM Prompt Injection Prevention](LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
  + [Laravel](Laravel_Cheat_Sheet.html)
  + [Legacy Application Management](Legacy_Application_Management_Cheat_Sheet.html)
  + [Logging](Logging_Cheat_Sheet.html)
  + [Logging Vocabulary](Logging_Vocabulary_Cheat_Sheet.html)
  + [MCP Security](MCP_Security_Cheat_Sheet.html)
  + [Mass Assignment](Mass_Assignment_Cheat_Sheet.html)
  + [Microservices Security](Microservices_Security_Cheat_Sheet.html)
  + [Microservices based Security Arch Doc](Microservices_based_Security_Arch_Doc_Cheat_Sheet.html)
  + [Mobile Application Security](Mobile_Application_Security_Cheat_Sheet.html)
  + [Multi Tenant Security](Multi_Tenant_Security_Cheat_Sheet.html)
  + [Multifactor Authentication](Multifactor_Authentication_Cheat_Sheet.html)
  + [NPM Security](NPM_Security_Cheat_Sheet.html)
  + [Network Segmentation](Network_Segmentation_Cheat_Sheet.html)
  + [NoSQL Security](NoSQL_Security_Cheat_Sheet.html)
  + [NodeJS Docker](NodeJS_Docker_Cheat_Sheet.html)
  + [Nodejs Security](Nodejs_Security_Cheat_Sheet.html)
  + [OAuth2](OAuth2_Cheat_Sheet.html)
  + [OS Command Injection Defense](OS_Command_Injection_Defense_Cheat_Sheet.html)
  + [PHP Configuration](PHP_Configuration_Cheat_Sheet.html)
  + [Password Storage](Password_Storage_Cheat_Sheet.html)
  + [Pinning](Pinning_Cheat_Sheet.html)
  + [Prototype Pollution Prevention](Prototype_Pollution_Prevention_Cheat_Sheet.html)
  + [Query Parameterization](Query_Parameterization_Cheat_Sheet.html)
  + [REST Assessment](REST_Assessment_Cheat_Sheet.html)
  + REST Security

    [REST Security](REST_Security_Cheat_Sheet.html)

    Table of contents
    - [Introduction](#introduction)
    - [HTTPS](#https)
    - [Access Control](#access-control)
    - [JWT](#jwt)
    - [API Keys](#api-keys)
    - [Restrict HTTP methods](#restrict-http-methods)
    - [Preventing Out-of-Order API Execution](#preventing-out-of-order-api-execution)

      * [Problem](#problem)
      * [Example](#example)
      * [Prevention Guidance](#prevention-guidance)
      * [Testing Checklist](#testing-checklist)
    - [Input validation](#input-validation)
    - [Validate content types](#validate-content-types)

      * [Validate request content types](#validate-request-content-types)
      * [Send safe response content types](#send-safe-response-content-types)
    - [Management endpoints](#management-endpoints)
    - [Error handling](#error-handling)
    - [Audit logs](#audit-logs)
    - [Security Headers](#security-headers)
    - [CORS](#cors)
    - [Sensitive information in HTTP requests](#sensitive-information-in-http-requests)
    - [HTTP Return Code](#http-return-code)
  + [Ruby on Rails](Ruby_on_Rails_Cheat_Sheet.html)
  + [SAML Security](SAML_Security_Cheat_Sheet.html)
  + [SQL Injection Prevention](SQL_Injection_Prevention_Cheat_Sheet.html)
  + [Secrets Management](Secrets_Management_Cheat_Sheet.html)
  + [Secure AI Model Ops](Secure_AI_Model_Ops_Cheat_Sheet.html)
  + [Secure Cloud Architecture](Secure_Cloud_Architecture_Cheat_Sheet.html)
  + [Secure Code Review](Secure_Code_Review_Cheat_Sheet.html)
  + [Secure Product Design](Secure_Product_Design_Cheat_Sheet.html)
  + [Securing Cascading Style Sheets](Securing_Cascading_Style_Sheets_Cheat_Sheet.html)
  + [Security Terminology](Security_Terminology_Cheat_Sheet.html)
  + [Server Side Request Forgery Prevention](Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html)
  + [Serverless FaaS Security](Serverless_FaaS_Security_Cheat_Sheet.html)
  + [Session Management](Session_Management_Cheat_Sheet.html)
  + [Software Supply Chain Security](Software_Supply_Chain_Security_Cheat_Sheet.html)
  + [Subdomain Takeover Prevention](Subdomain_Takeover_Prevention_Cheat_Sheet.html)
  + [Symfony](Symfony_Cheat_Sheet.html)
  + [TLS Cipher String](TLS_Cipher_String_Cheat_Sheet.html)
  + [Third Party Javascript Management](Third_Party_Javascript_Management_Cheat_Sheet.html)
  + [Third Party Payment Gateway Integration](Third_Party_Payment_Gateway_Integration_Cheat_Sheet.html)
  + [Threat Modeling](Threat_Modeling_Cheat_Sheet.html)
  + [Transaction Authorization](Transaction_Authorization_Cheat_Sheet.html)
  + [Transport Layer Protection](Transport_Layer_Protection_Cheat_Sheet.html)
  + [Transport Layer Security](Transport_Layer_Security_Cheat_Sheet.html)
  + [Unvalidated Redirects and Forwards](Unvalidated_Redirects_and_Forwards_Cheat_Sheet.html)
  + [User Privacy Protection](User_Privacy_Protection_Cheat_Sheet.html)
  + [Virtual Patching](Virtual_Patching_Cheat_Sheet.html)
  + [Vulnerability Disclosure](Vulnerability_Disclosure_Cheat_Sheet.html)
  + [Vulnerable Dependency Management](Vulnerable_Dependency_Management_Cheat_Sheet.html)
  + [WebSocket Security](WebSocket_Security_Cheat_Sheet.html)
  + [Web Service Security](Web_Service_Security_Cheat_Sheet.html)
  + [XML External Entity Prevention](XML_External_Entity_Prevention_Cheat_Sheet.html)
  + [XML Security](XML_Security_Cheat_Sheet.html)
  + [XSS Filter Evasion](XSS_Filter_Evasion_Cheat_Sheet.html)
  + [XS Leaks](XS_Leaks_Cheat_Sheet.html)
  + [Zero Trust Architecture](Zero_Trust_Architecture_Cheat_Sheet.html)
  + [gRPC Security](gRPC_Security_Cheat_Sheet.html)

Table of contents

* [Introduction](#introduction)
* [HTTPS](#https)
* [Access Control](#access-control)
* [JWT](#jwt)
* [API Keys](#api-keys)
* [Restrict HTTP methods](#restrict-http-methods)
* [Preventing Out-of-Order API Execution](#preventing-out-of-order-api-execution)

  + [Problem](#problem)
  + [Example](#example)
  + [Prevention Guidance](#prevention-guidance)
  + [Testing Checklist](#testing-checklist)
* [Input validation](#input-validation)
* [Validate content types](#validate-content-types)

  + [Validate request content types](#validate-request-content-types)
  + [Send safe response content types](#send-safe-response-content-types)
* [Management endpoints](#management-endpoints)
* [Error handling](#error-handling)
* [Audit logs](#audit-logs)
* [Security Headers](#security-headers)
* [CORS](#cors)
* [Sensitive information in HTTP requests](#sensitive-information-in-http-requests)
* [HTTP Return Code](#http-return-code)

# REST Security Cheat Sheet[¶](#rest-security-cheat-sheet "Permanent link")

## Introduction[¶](#introduction "Permanent link")

[REST](https://en.wikipedia.org/wiki/REST) (or **RE**presentational **S**tate **T**ransfer) is an architectural style first described in [Roy Fielding](https://en.wikipedia.org/wiki/Roy_Fielding)'s Ph.D. dissertation on [Architectural Styles and the Design of Network-based Software Architectures](https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm).

It evolved as Fielding wrote the HTTP/1.1 and URI specs and has been proven to be well-suited for developing distributed hypermedia applications. While REST is more widely applicable, it is most commonly used within the context of communicating with services via HTTP.

The key abstraction of information in REST is a resource. A REST API resource is identified by a URI, usually a HTTP URL. REST components use connectors to perform actions on a resource by using a representation to capture the current or intended state of the resource and transferring that representation.

The primary connector types are client and server, secondary connectors include cache, resolver and tunnel.

REST APIs are stateless. Stateful APIs do not adhere to the REST architectural style. State in the REST acronym refers to the state of the resource which the API accesses, not the state of a session within which the API is called. While there may be good reasons for building a stateful API, it is important to realize that managing sessions is complex and difficult to do securely.

Stateful services are out of scope of this Cheat Sheet: *Passing state from client to backend, while making the service technically stateless, is an anti-pattern that should also be avoided as it is prone to replay and impersonation attacks.*

In order to implement flows with REST APIs, resources are typically created, read, updated and deleted. For example, an ecommerce site may offer methods to create an empty shopping cart, to add items to the cart and to check out the cart. Each of these REST calls is stateless and the endpoint should check whether the caller is authorized to perform the requested operation.

Another key feature of REST applications is the use of standard HTTP verbs and error codes in the pursuit or removing unnecessary variation among different services.

Another key feature of REST applications is the use of [HATEOAS or Hypermedia As The Engine of Application State](https://en.wikipedia.org/wiki/HATEOAS). This provides REST applications a self-documenting nature making it easier for developers to interact with a REST service without prior knowledge.

## HTTPS[¶](#https "Permanent link")

Secure REST services must only provide HTTPS endpoints. This protects authentication credentials in transit, for example passwords, API keys or JSON Web Tokens. It also allows clients to authenticate the service and guarantees integrity of the transmitted data.

See the [Transport Layer Security Cheat Sheet](Transport_Layer_Security_Cheat_Sheet.html) for additional information.

Consider the use of mutually authenticated client-side certificates to provide additional protection for highly privileged web services.

## Access Control[¶](#access-control "Permanent link")

Non-public REST services must perform access control at each API endpoint. Web services in monolithic applications implement this by means of user authentication, authorization logic and session management. This has several drawbacks for modern architectures which compose multiple microservices following the RESTful style.

* in order to minimize latency and reduce coupling between services, the access control decision should be taken locally by REST endpoints
* user authentication should be centralised in a Identity Provider (IdP), which issues access tokens

## JWT[¶](#jwt "Permanent link")

There seems to be a convergence towards using [JSON Web Tokens](https://tools.ietf.org/html/rfc7519) (JWT) as the format for security tokens. JWTs are JSON data structures containing a set of claims that can be used for access control decisions. A cryptographic signature or message authentication code (MAC) can be used to protect the integrity of the JWT.

* Ensure JWTs are integrity protected by either a signature or a MAC. Do not allow the unsecured JWTs: `{"alg":"none"}`.
  + See [here](https://tools.ietf.org/html/rfc7519#section-6.1)
* In general, signatures should be preferred over MACs for integrity protection of JWTs.

If MACs are used for integrity protection, every service that is able to validate JWTs can also create new JWTs using the same key. This means that all services using the same key have to mutually trust each other. Another consequence of this is that a compromise of any service also compromises all other services sharing the same key. See [here](https://tools.ietf.org/html/rfc7515#section-10.5) for additional information.

The relying party or token consumer validates a JWT by verifying its integrity and claims contained.

* A relying party must verify the integrity of the JWT based on its own configuration or hard-coded logic. It must not rely on the information of the JWT header to select the verification algorithm. See [here](https://www.chosenplaintext.ca/2015/03/31/jwt-algorithm-confusion.html) and [here](https://www.youtube.com/watch?v=bW5pS4e_MX8>)

Some claims have been standardized and should be present in JWT used for access controls. At least the following of the standard claims should be verified:

* `iss` or issuer - is this a trusted issuer? Is it the expected owner of the signing key?
* `aud` or audience - is the relying party in the target audience for this JWT?
* `exp` or expiration time - is the current time before the end of the validity period of this token?
* `nbf` or not before time - is the current time after the start of the validity period of this token?

As JWTs contain details of the authenticated entity (user etc.) a disconnect can occur between the JWT and the current state of the users session, for example, if the session is terminated earlier than the expiration time due to an explicit logout or an idle timeout. When an explicit session termination event occurs, a digest or hash of any associated JWTs should be submitted to a denylist on the API which will invalidate that JWT for any requests until the expiration of the token. See the [JSON\_Web\_Token\_for\_Java\_Cheat\_Sheet](JSON_Web_Token_for_Java_Cheat_Sheet.html#token-explicit-revocation-by-the-user) for further details.

## API Keys[¶](#api-keys "Permanent link")

Public REST services without access control run the risk of being farmed leading to excessive bills for bandwidth or compute cycles. API keys can be used to mitigate this risk. They are also often used by organisation to monetize APIs; instead of blocking high-frequency calls, clients are given access in accordance to a purchased access plan.

API keys can reduce the impact of denial-of-service attacks. However, when they are issued to third-party clients, they are relatively easy to compromise.

* Require API keys for every request to the protected endpoint.
* Return `429 Too Many Requests` HTTP response code if requests are coming in too quickly.
* Revoke the API key if the client violates the usage agreement.
* Do not rely exclusively on API keys to protect sensitive, critical or high-value resources.

## Restrict HTTP methods[¶](#restrict-http-methods "Permanent link")

* Apply an allowlist of permitted HTTP Methods e.g. `GET`, `POST`, `PUT`.
* Reject all requests not matching the allowlist with HTTP response code `405 Method not allowed`.
* Make sure the caller is authorised to use the incoming HTTP method on the resource collection, action, and record

In Java EE in particular, this can be difficult to implement properly. See [Bypassing Web Authentication and Authorization with HTTP Verb Tampering](../assets/REST_Security_Cheat_Sheet_Bypassing_VBAAC_with_HTTP_Verb_Tampering.pdf) for an explanation of this common misconfiguration.

## Preventing Out-of-Order API Execution[¶](#preventing-out-of-order-api-execution "Permanent link")

Modern REST APIs often implement business workflows through a sequence of endpoints (for example, create → validate → approve → finalize). If the backend does not explicitly validate workflow state transitions, attackers may invoke endpoints out of sequence to bypass intended controls.

### Problem[¶](#problem "Permanent link")

Out-of-order API execution occurs when an attacker:

* Skips required workflow steps by directly calling later-stage endpoints
* Replays or reuses tokens across workflow boundaries
* Exploits assumptions that the frontend enforces correct sequencing

Because each endpoint may be individually authenticated and authorized, traditional access control checks often fail to detect these issues.

### Example[¶](#example "Permanent link")

A checkout workflow expects the following sequence:

```
POST /checkout/create
POST /checkout/pay
POST /checkout/confirm
```

If the backend does not validate workflow state transitions, an attacker could directly invoke:

```
POST /checkout/confirm
```

without completing payment.

### Prevention Guidance[¶](#prevention-guidance "Permanent link")

* Enforce workflow state validation on the server side for every request
* Model workflows explicitly using finite states or state machines
* Bind tokens or identifiers to specific workflow stages
* Avoid relying on frontend logic to enforce sequencing
* Reject invalid or out-of-order transitions with clear error responses

### Testing Checklist[¶](#testing-checklist "Permanent link")

* Can endpoints be invoked out of sequence?
* Does each endpoint validate the current workflow state?
* Are tokens reusable across workflow steps?
* Are invalid state transitions consistently rejected?

## Input validation[¶](#input-validation "Permanent link")

* Do not trust input parameters/objects.
* Validate input: length / range / format and type.
* Achieve an implicit input validation by using strong types like numbers, booleans, dates, times or fixed data ranges in API parameters.
* Constrain string inputs with regexps.
* Reject unexpected/illegal content.
* Make use of validation/sanitation libraries or frameworks in your specific language.
* Define an appropriate request size limit and reject requests exceeding the limit with HTTP response status 413 Request Entity Too Large.
* Consider logging input validation failures. Assume that someone who is performing hundreds of failed input validations per second is up to no good.
* Have a look at input validation cheat sheet for comprehensive explanation.
* Use a secure parser for parsing the incoming messages. If you are using XML, make sure to use a parser that is not vulnerable to [XXE](https://owasp.org/www-community/vulnerabilities/XML_External_Entity_%28XXE%29_Processing) and similar attacks.

## Validate content types[¶](#validate-content-types "Permanent link")

A REST request or response body should match the intended content type in the header. Otherwise this could cause misinterpretation at the consumer/producer side and lead to code injection/execution.

* Document all supported content types in your API.

### Validate request content types[¶](#validate-request-content-types "Permanent link")

* Reject requests containing unexpected or missing content type headers with HTTP response status `406 Unacceptable` or `415 Unsupported Media Type`. For requests with `Content-Length: 0` however, a `Content-type` header is optional.
* For XML content types ensure appropriate XML parser hardening, see the [XXE cheat sheet](XML_External_Entity_Prevention_Cheat_Sheet.html).
* Avoid accidentally exposing unintended content types by explicitly defining content types e.g. [Jersey](https://jersey.github.io/) (Java) `@consumes("application/json"); @produces("application/json")`. This avoids [XXE-attack](https://owasp.org/www-community/vulnerabilities/XML_External_Entity_%28XXE%29_Processing) vectors for example.

### Send safe response content types[¶](#send-safe-response-content-types "Permanent link")

It is common for REST services to allow multiple response types (e.g. `application/xml` or `application/json`, and the client specifies the preferred order of response types by the Accept header in the request.

* **Do NOT** simply copy the `Accept` header to the `Content-type` header of the response.
* Reject the request (ideally with a `406 Not Acceptable` response) if the `Accept` header does not specifically contain one of the allowable types.

Services including script code (e.g. JavaScript) in their responses must be especially careful to defend against header injection attack.

* Ensure sending intended content type headers in your response matching your body content e.g. `application/json` and not `application/javascript`.

## Management endpoints[¶](#management-endpoints "Permanent link")

* Avoid exposing management endpoints via Internet.
* If management endpoints must be accessible via the Internet, make sure that users must use a strong authentication mechanism, e.g. multi-factor.
* Expose management endpoints via different HTTP ports or hosts preferably on a different NIC and restricted subnet.
* Restrict access to these endpoints by firewall rules or use of access control lists.

## Error handling[¶](#error-handling "Permanent link")

* Respond with generic error messages - avoid revealing details of the failure unnecessarily.
* Do not pass technical details (e.g. call stacks or other internal hints) to the client.

## Audit logs[¶](#audit-logs "Permanent link")

* Write audit logs before and after security related events.
* Consider logging token validation errors in order to detect attacks.
* Take care of log injection attacks by sanitizing log data beforehand.

## Security Headers[¶](#security-headers "Permanent link")

There are a number of [security related headers](https://owasp.org/www-project-secure-headers/) that can be returned in the HTTP responses to instruct browsers to act in specific ways. However, some of these headers are intended to be used with HTML responses, and as such may provide little or no security benefits on an API that does not return HTML. Note that if the API is only consumed by non-browser clients (e.g. mobile apps, server-to-server calls, command-line tools), most of these headers will have no effect since they are directives for browsers.

The following headers should be included in all API responses that may be consumed by browser clients:

| Header | Rationale |
| --- | --- |
| `Cache-Control: no-store` | Header used to direct caching done by browsers. Providing `no-store` indicates that any caches of any kind (private or shared) should not store the response that contains the header. A browser must make a new request everytime the API is called to fetch the latest response. This header with a `no-store` value prevents sensitive information from being cached or stored. |
| `Content-Security-Policy: frame-ancestors 'none'` | Header used to specify whether a response can be framed in a `<frame>`, `<iframe>`, `<embed>` or `<object>` element. For an API response, there is no requirement to be framed in any of those elements. Providing `frame-ancestors 'none'` prevents any domain from framing the response returned by the API call. This header protects against [drag-and-drop](https://www.w3.org/Security/wiki/Clickjacking_Threats#Drag_and_drop_attacks) style clickjacking attacks. |
| `Content-Type` | Header to specify the content type of a response. This must be specified as per the type of content returned by an API call. If not specified or if specified incorrectly, a browser might attempt to guess the content type of the response. This can return in MIME sniffing attacks. One common content type value is `application/json` if the API response is JSON. |
| `Strict-Transport-Security` | Header to instruct a browser that the domain should only be accessed using HTTPS, and that any future attempts to access it using HTTP should automatically be converted to HTTPS. This header ensures that API calls are made over HTTPS and protects against spoofed certificates. |
| `X-Content-Type-Options: nosniff` | Header to instruct a browser to always use the MIME type that is declared in the `Content-Type` header rather than trying to determine the MIME type based on the file's content. This header with a `nosniff` value prevents browsers from performing MIME sniffing, and inappropriately interpreting responses as HTML. |
| `X-Frame-Options: DENY` | Legacy header superseded by `Content-Security-Policy: frame-ancestors 'none'` (see above). Still recommended for compatibility with older browsers that do not support CSP Level 2. Providing `DENY` prevents any domain from framing the response. |

The headers below are only intended to provide additional security when responses are rendered as HTML. As such, if the API will **never** return HTML in responses, then these headers may not be necessary. However, if there is any uncertainty about the function of the headers, or the types of information that the API returns (or may return in future), then it is recommended to include them as part of a defence-in-depth approach.

| Header | Example | Rationale |
| --- | --- | --- |
| Content-Security-Policy | `Content-Security-Policy: default-src 'none'` | The majority of CSP functionality only affects pages rendered as HTML. |
| Permissions-Policy | `Permissions-Policy: accelerometer=(), ambient-light-sensor=(), autoplay=(), battery=(), camera=(), cross-origin-isolated=(), display-capture=(), document-domain=(), encrypted-media=(), execution-while-not-rendered=(), execution-while-out-of-viewport=(), fullscreen=(), geolocation=(), gyroscope=(), keyboard-map=(), magnetometer=(), microphone=(), midi=(), navigation-override=(), payment=(), picture-in-picture=(), publickey-credentials-get=(), screen-wake-lock=(), sync-xhr=(), usb=(), web-share=(), xr-spatial-tracking=()` | This header used to be named Feature-Policy. When browsers heed this header, it is used to control browser features via directives. The example disables features with an empty allowlist for a number of permitted [directive names](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Permissions-Policy#directives). When you apply this header, verify that the directives are up-to-date and fit your needs. Please have a look at this [article](https://developer.chrome.com/en/docs/privacy-sandbox/permissions-policy) for a detailed explanation on how to control browser features. |
| Referrer-Policy | `Referrer-Policy: no-referrer` | Non-HTML responses should not trigger additional requests. |

## CORS[¶](#cors "Permanent link")

Cross-Origin Resource Sharing (CORS) is a W3C standard to flexibly specify what cross-domain requests are permitted. By delivering appropriate CORS Headers your REST API signals to the browser which domains, AKA origins, are allowed to make JavaScript calls to the REST service.

* Disable CORS headers if cross-domain calls are not supported/expected.
* Be as specific as possible and as general as necessary when setting the origins of cross-domain calls.

## Sensitive information in HTTP requests[¶](#sensitive-information-in-http-requests "Permanent link")

RESTful web services should be careful to prevent leaking credentials. Passwords, security tokens, and API keys should not appear in the URL, as this can be captured in web server logs, which makes them intrinsically valuable.

* In `POST`/`PUT` requests sensitive data should be transferred in the request body or request headers.
* In `GET` requests sensitive data should be transferred in an HTTP Header.

**OK:**

`https://example.com/resourceCollection/[ID]/action`

`https://twitter.com/vanderaj/lists`

**NOT OK:**

`https://example.com/controller/123/action?apiKey=a53f435643de32` because the apiKey is in the URL.

## HTTP Return Code[¶](#http-return-code "Permanent link")

HTTP defines [status code](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes). When designing REST API, don't just use `200` for success or `404` for error. Always use the semantically appropriate status code for the response.

Here is a non-exhaustive selection of security related REST API **status codes**. Use it to ensure you return the correct code.

| Code | Message | Description |
| --- | --- | --- |
| 200 | OK | Response to a successful REST API action. The HTTP method can be GET, POST, PUT, PATCH or DELETE. |
| 201 | Created | The request has been fulfilled and resource created. A URI for the created resource is returned in the Location header. |
| 202 | Accepted | The request has been accepted for processing, but processing is not yet complete. |
| 301 | Moved Permanently | Permanent redirection. |
| 304 | Not Modified | Caching related response that returned when the client has the same copy of the resource as the server. |
| 307 | Temporary Redirect | Temporary redirection of resource. |
| 400 | Bad Request | The request is malformed, such as message body format error. |
| 401 | Unauthorized | Wrong or no authentication ID/password provided. |
| 403 | Forbidden | It's used when the authentication succeeded but authenticated user doesn't have permission to the request resource. |
| 404 | Not Found | When a non-existent resource is requested. |
| 405 | Method Not Acceptable | The error for an unexpected HTTP method. For example, the REST API is expecting HTTP GET, but HTTP PUT is used. |
| 406 | Unacceptable | The client presented a content type in the Accept header which is not supported by the server API. |
| 413 | Payload too large | Use it to signal that the request size exceeded the given limit e.g. regarding file uploads. |
| 415 | Unsupported Media Type | The requested content type is not supported by the REST service. |
| 429 | Too Many Requests | The error is used when there may be DOS attack detected or the request is rejected due to rate limiting. |
| 500 | Internal Server Error | An unexpected condition prevented the server from fulfilling the request. Be aware that the response should not reveal internal information that helps an attacker, e.g. detailed error messages or stack traces. |
| 501 | Not Implemented | The REST service does not implement the requested operation yet. |
| 503 | Service Unavailable | The REST service is temporarily unable to process the request. Used to inform the client it should retry at a later time. |

Additional information about HTTP return code usage in REST API can be found [here](https://www.restapitutorial.com/httpstatuscodes.html) and [here](https://restfulapi.net/http-status-codes).

var target=document.getElementById(location.hash.slice(1));target&&target.name&&(target.checked=target.name.startsWith("\_\_tabbed\_"))

©Copyright document.write(new Date().getFullYear()) - Cheat Sheets Series Team - This work is licensed under [Creative Commons Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/).

Made with
[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)

{"base": "..", "features": ["navigation.sections", "navigation.expand"], "search": "../assets/javascripts/workers/search.6ce7567c.min.js", "translations": {"clipboard.copied": "Copied to clipboard", "clipboard.copy": "Copy to clipboard", "search.result.more.one": "1 more on this page", "search.result.more.other": "# more on this page", "search.result.none": "No matching documents", "search.result.one": "1 matching document", "search.result.other": "# matching documents", "search.result.placeholder": "Type to start searching", "search.result.term.missing": "Missing", "select.version": "Select version"}}