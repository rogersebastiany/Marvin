Core Concepts - Argo CD - Declarative GitOps CD for Kubernetes

:root{--md-text-font-family:"Work Sans";--md-code-font-family:""}

function gtag(){dataLayer.push(arguments)}window.dataLayer=window.dataLayer||[],gtag("js",new Date),gtag("config","G-5Z1VTPDL73"),document.addEventListener("DOMContentLoaded",function(){"undefined"!=typeof location$&&location$.subscribe(function(t){gtag("config","G-5Z1VTPDL73",{page\_path:t.pathname})})})

function \_\_prefix(e){return new URL("..",location).pathname+"."+e}function \_\_get(e,t=localStorage){return JSON.parse(t.getItem(\_\_prefix(e)))}
var palette=\_\_get("\_\_palette");if(null!==palette&&"object"==typeof palette.color)for(var key in palette.color)document.body.setAttribute("data-md-color-"+key,palette.color[key])

[Skip to content](#core-concepts)

Argo CD - Declarative GitOps CD for Kubernetes

Core Concepts

Initializing search

[GitHub](https://github.com/argoproj/argo-cd "Go to repository")

Argo CD - Declarative GitOps CD for Kubernetes

[GitHub](https://github.com/argoproj/argo-cd "Go to repository")

* [Overview](..)
* [Understand The Basics](../understand_the_basics/)
* [Core Concepts](./)
* [Getting Started](../getting_started/)
* Operator Manual

  Operator Manual
  + [Overview](../operator-manual/)
  + [Architectural Overview](../operator-manual/architecture/)
  + [Installation](../operator-manual/installation/)
  + [Feature Maturity](../operator-manual/feature-maturity/)
  + [Argo CD Core](../operator-manual/core/)
  + [Declarative Setup](../operator-manual/declarative-setup/)
  + [Applications in any namespace](../operator-manual/app-any-namespace/)
  + [Ingress Configuration](../operator-manual/ingress/)
  + High Availability

    High Availability
    - [Overview](../operator-manual/high_availability/)
    - [Dynamic Cluster Distribution](../operator-manual/dynamic-cluster-distribution/)
  + User Management

    User Management
    - [Overview](../operator-manual/user-management/)
    - [Auth0](../operator-manual/user-management/auth0/)
    - [Microsoft](../operator-manual/user-management/microsoft/)
    - [Okta](../operator-manual/user-management/okta/)
    - [OneLogin](../operator-manual/user-management/onelogin/)
    - [Keycloak](../operator-manual/user-management/keycloak/)
    - [OpenUnison](../operator-manual/user-management/openunison/)
    - [GitHub Actions](../operator-manual/user-management/github-actions/)
    - [Google](../operator-manual/user-management/google/)
    - [Zitadel](../operator-manual/user-management/zitadel/)
    - [Identity Center (AWS SSO)](../operator-manual/user-management/identity-center/)
    - [RBAC Configuration](../operator-manual/rbac/)
  + Security

    Security
    - [Overview](../operator-manual/security/)
    - [Snyk Scans](../snyk/)
    - [Verification of Argo CD Artifacts](../operator-manual/signed-release-assets/)
  + [TLS configuration](../operator-manual/tls/)
  + [Cluster Management](../operator-manual/cluster-management/)
  + [Cluster Bootstrapping](../operator-manual/cluster-bootstrapping/)
  + [Secret Management](../operator-manual/secret-management/)
  + [Disaster Recovery](../operator-manual/disaster_recovery/)
  + [Reconcile Optimization](../operator-manual/reconcile/)
  + [Git Webhook Configuration](../operator-manual/webhook/)
  + [Resource Health](../operator-manual/health/)
  + [Resource Actions](../operator-manual/resource_actions/)
  + [Custom Tooling](../operator-manual/custom_tools/)
  + [Custom Styles](../operator-manual/custom-styles/)
  + [UI Customization](../operator-manual/ui-customization/)
  + [Metrics](../operator-manual/metrics/)
  + [Web-based Terminal](../operator-manual/web_based_terminal/)
  + [Config Management Plugins](../operator-manual/config-management-plugins/)
  + [Deep Links](../operator-manual/deep_links/)
  + [Git Configuration](../operator-manual/git_configuration/)
  + [Managed By URL Annotation](../operator-manual/managed-by-url/)
  + Notifications

    Notifications
    - [Overview](../operator-manual/notifications/)
    - [Triggers](../operator-manual/notifications/triggers/)
    - [Templates](../operator-manual/notifications/templates/)
    - [Functions](../operator-manual/notifications/functions/)
    - [Triggers and Templates Catalog](../operator-manual/notifications/catalog/)
    - [Monitoring](../operator-manual/notifications/monitoring/)
    - [Subscriptions](../operator-manual/notifications/subscriptions/)
    - [Troubleshooting](../operator-manual/notifications/troubleshooting/)
    - [Troubleshooting commands](../operator-manual/notifications/troubleshooting-commands/)
    - [Troubleshooting errors](../operator-manual/notifications/troubleshooting-errors/)
    - [Examples](../operator-manual/notifications/examples/)
    - Notification Services

      Notification Services
      * [Alertmanager](../operator-manual/notifications/services/alertmanager/)
      * [AWS SQS](../operator-manual/notifications/services/awssqs/)
      * [Email](../operator-manual/notifications/services/email/)
      * [GitHub](../operator-manual/notifications/services/github/)
      * [Google Chat](../operator-manual/notifications/services/googlechat/)
      * [Grafana](../operator-manual/notifications/services/grafana/)
      * [Mattermost](../operator-manual/notifications/services/mattermost/)
      * [NewRelic](../operator-manual/notifications/services/newrelic/)
      * [Opsgenie](../operator-manual/notifications/services/opsgenie/)
      * [Overview](../operator-manual/notifications/services/overview/)
      * [PagerDuty](../operator-manual/notifications/services/pagerduty/)
      * [PagerDuty V2](../operator-manual/notifications/services/pagerduty_v2/)
      * [Pushover](../operator-manual/notifications/services/pushover/)
      * [Rocket.Chat](../operator-manual/notifications/services/rocketchat/)
      * [Slack](../operator-manual/notifications/services/slack/)
      * [Teams Workflows](../operator-manual/notifications/services/teams-workflows/)
      * [Teams (Office 365 Connectors)](../operator-manual/notifications/services/teams/)
      * [Telegram](../operator-manual/notifications/services/telegram/)
      * [Webex Teams](../operator-manual/notifications/services/webex/)
      * [Webhook](../operator-manual/notifications/services/webhook/)
  + [Troubleshooting Tools](../operator-manual/troubleshooting/)
  + ApplicationSet

    ApplicationSet
    - [Introduction](../operator-manual/applicationset/)
    - [Installations](../operator-manual/applicationset/Getting-Started/)
    - [Use Cases](../operator-manual/applicationset/Use-Cases/)
    - [Security](../operator-manual/applicationset/Security/)
    - [How ApplicationSet controller interacts with Argo CD](../operator-manual/applicationset/Argo-CD-Integration/)
    - Generators

      Generators
      * [Generators](../operator-manual/applicationset/Generators/)
      * [List Generator](../operator-manual/applicationset/Generators-List/)
      * [Cluster Generator](../operator-manual/applicationset/Generators-Cluster/)
      * [Git Generator](../operator-manual/applicationset/Generators-Git/)
      * [Matrix Generator](../operator-manual/applicationset/Generators-Matrix/)
      * [Merge Generator](../operator-manual/applicationset/Generators-Merge/)
      * [SCM Provider Generator](../operator-manual/applicationset/Generators-SCM-Provider/)
      * [Cluster Decision Resource Generator](../operator-manual/applicationset/Generators-Cluster-Decision-Resource/)
      * [Pull Request Generator](../operator-manual/applicationset/Generators-Pull-Request/)
      * [Post Selector all generators](../operator-manual/applicationset/Generators-Post-Selector/)
      * [Plugin Generator](../operator-manual/applicationset/Generators-Plugin/)
    - Template fields

      Template fields
      * [Templates](../operator-manual/applicationset/Template/)
      * [Go Template](../operator-manual/applicationset/GoTemplate/)
    - [Controlling Resource Modification](../operator-manual/applicationset/Controlling-Resource-Modification/)
    - [Application Pruning & Resource Deletion](../operator-manual/applicationset/Application-Deletion/)
    - [Progressive Syncs](../operator-manual/applicationset/Progressive-Syncs/)
    - [Git File Generator Globbing](../operator-manual/applicationset/Generators-Git-File-Globbing/)
    - [ApplicationSet Specification Reference](../operator-manual/applicationset/applicationset-specification/)
    - [ApplicationSet in any namespace](../operator-manual/applicationset/Appset-Any-Namespace/)
  + Server Configuration Parameters

    Server Configuration Parameters
    - [argocd-server Command Reference](../operator-manual/server-commands/argocd-server/)
    - [argocd-application-controller Command Reference](../operator-manual/server-commands/argocd-application-controller/)
    - [argocd-repo-server Command Reference](../operator-manual/server-commands/argocd-repo-server/)
    - [argocd-dex Command Reference](../operator-manual/server-commands/argocd-dex/)
    - [Additional configuration method](../operator-manual/server-commands/additional-configuration-method/)
  + Upgrading

    Upgrading
    - [Overview](../operator-manual/upgrading/overview/)
    - [v3.2 to 3.3](../operator-manual/upgrading/3.2-3.3/)
    - [v3.1 to 3.2](../operator-manual/upgrading/3.1-3.2/)
    - [v3.0 to 3.1](../operator-manual/upgrading/3.0-3.1/)
    - [v2.14 to 3.0](../operator-manual/upgrading/2.14-3.0/)
    - [v2.13 to 2.14](../operator-manual/upgrading/2.13-2.14/)
    - [v2.12 to 2.13](../operator-manual/upgrading/2.12-2.13/)
    - [v2.11 to 2.12](../operator-manual/upgrading/2.11-2.12/)
    - [v2.10 to 2.11](../operator-manual/upgrading/2.10-2.11/)
    - [v2.9 to 2.10](../operator-manual/upgrading/2.9-2.10/)
    - [v2.8 to 2.9](../operator-manual/upgrading/2.8-2.9/)
    - [v2.7 to 2.8](../operator-manual/upgrading/2.7-2.8/)
    - [v2.6 to 2.7](../operator-manual/upgrading/2.6-2.7/)
    - [v2.5 to 2.6](../operator-manual/upgrading/2.5-2.6/)
    - [v2.4 to 2.5](../operator-manual/upgrading/2.4-2.5/)
    - [v2.3 to 2.4](../operator-manual/upgrading/2.3-2.4/)
    - [v2.2 to 2.3](../operator-manual/upgrading/2.2-2.3/)
    - [v2.1 to 2.2](../operator-manual/upgrading/2.1-2.2/)
    - [v2.0 to 2.1](../operator-manual/upgrading/2.0-2.1/)
    - [v1.8 to 2.0](../operator-manual/upgrading/1.8-2.0/)
    - [v1.7 to 1.8](../operator-manual/upgrading/1.7-1.8/)
    - [v1.6 to 1.7](../operator-manual/upgrading/1.6-1.7/)
    - [v1.5 to 1.6](../operator-manual/upgrading/1.5-1.6/)
    - [v1.4 to 1.5](../operator-manual/upgrading/1.4-1.5/)
    - [v1.3 to 1.4](../operator-manual/upgrading/1.3-1.4/)
    - [v1.2 to 1.3](../operator-manual/upgrading/1.2-1.3/)
    - [v1.1 to 1.2](../operator-manual/upgrading/1.1-1.2/)
    - [v1.0 to 1.1](../operator-manual/upgrading/1.0-1.1/)
  + [Project Specification Reference](../operator-manual/project-specification/)
* User Guide

  User Guide
  + [Overview](../user-guide/)
  + [Tools](../user-guide/application_sources/)
  + [Kustomize](../user-guide/kustomize/)
  + [Helm](../user-guide/helm/)
  + [OCI](../user-guide/oci/)
  + [Importing Argo CD go packages](../user-guide/import/)
  + [Jsonnet](../user-guide/jsonnet/)
  + [Directory](../user-guide/directory/)
  + [Tool Detection](../user-guide/tool_detection/)
  + [Projects](../user-guide/projects/)
  + [Private Repositories](../user-guide/private-repositories/)
  + [Plugins](../user-guide/plugins/)
  + [Multiple Sources for an Application](../user-guide/multiple_sources/)
  + [GnuPG verification](../user-guide/gpg-verification/)
  + [Automated Sync Policy](../user-guide/auto_sync/)
  + Diffing

    Diffing
    - [Diff Strategies](../user-guide/diff-strategies/)
    - [Diff Customization](../user-guide/diffing/)
  + [Orphaned Resources Monitoring](../user-guide/orphaned-resources/)
  + [Compare Options](../user-guide/compare-options/)
  + [Sync Options](../user-guide/sync-options/)
  + [Parameter Overrides](../user-guide/parameters/)
  + [Environment Variables](../user-guide/environment-variables/)
  + [Build Environment](../user-guide/build-environment/)
  + [Tracking and Deployment Strategies](../user-guide/tracking_strategies/)
  + [Resource Tracking](../user-guide/resource_tracking/)
  + [Resource hooks](../user-guide/resource_hooks/)
  + [Selective Sync](../user-guide/selective_sync/)
  + [Sync Phases and Waves](../user-guide/sync-waves/)
  + [Sync Windows](../user-guide/sync_windows/)
  + [Sync Applications with Kubectl](../user-guide/sync-kubectl/)
  + [Skip Application Reconcile](../user-guide/skip_reconcile/)
  + [Generating Applications with ApplicationSet](../user-guide/application-set/)
  + [Automation from CI Pipelines](../user-guide/ci_automation/)
  + [App Deletion](../user-guide/app_deletion/)
  + [Best Practices](../user-guide/best_practices/)
  + [Status Badge](../user-guide/status-badge/)
  + [External URL Links](../user-guide/external-url/)
  + [Add extra Application info](../user-guide/extra_info/)
  + [Notification subscriptions](../user-guide/subscriptions/)
  + [Annotations and Labels used by Argo CD](../user-guide/annotations-and-labels/)
  + [Command Reference](../user-guide/commands/argocd/)
  + [Application Specification Reference](../user-guide/application-specification/)
* Developer Guide

  Developer Guide
  + [Overview](../developer-guide/)
  + [Development Environment](../developer-guide/development-environment/)
  + [Development Cycle](../developer-guide/development-cycle/)
  + [Submit Your PR](../developer-guide/submit-your-pr/)
  + Architecture

    Architecture
    - [Authentication and Authorization](../developer-guide/architecture/authz-authn/)
    - [Component Architecture](../developer-guide/architecture/components/)
  + [Code Contribution Guide](../developer-guide/code-contributions/)
  + [Toolchain Guide](../developer-guide/toolchain-guide/)
  + [MacOS users](../developer-guide/mac-users/)
  + [Release Process And Cadence](../developer-guide/release-process-and-cadence/)
  + [Running Argo CD locally](../developer-guide/running-locally/)
  + [Debugging a local Argo CD instance](../developer-guide/debugging-locally/)
  + [Debugging a Remote ArgoCD Environment](../developer-guide/debugging-remote-environment/)
  + [API Docs](../developer-guide/api-docs/)
  + [E2E Tests](../developer-guide/test-e2e/)
  + [Managing Dependencies](../developer-guide/dependencies/)
  + [Continuous Integration (CI)](../developer-guide/ci/)
  + [Releasing](../developer-guide/releasing/)
  + [Documentation Site](../developer-guide/docs-site/)
  + [Static Code Analysis](../developer-guide/static-code-analysis/)
  + Extensions

    Extensions
    - [UI Extensions](../developer-guide/extensions/ui-extensions/)
    - [Proxy Extensions](../developer-guide/extensions/proxy-extensions/)
  + [Contribution FAQ](../developer-guide/faq/)
  + [Tilt Development](../developer-guide/tilt/)
  + [Custom resource icons](../developer-guide/custom-resource-icons/)
  + [Maintaining Internal Argo CD Forks](../developer-guide/maintaining-internal-argo-cd-forks/)
* [FAQ](../faq/)
* [Security Considerations](../security_considerations/)
* [Support](../SUPPORT/)
* [Roadmap](../roadmap/)
* [Releases ⧉](https://github.com/argoproj/argo-cd/releases)
* [Blog ⧉](https://blog.argoproj.io/)

# Core Concepts[¶](#core-concepts "Permanent link")

Let's assume you're familiar with core Git, Docker, Kubernetes, Continuous Delivery, and GitOps concepts.
Below are some of the concepts that are specific to Argo CD.

* **Application** A group of Kubernetes resources as defined by a manifest. This is a Custom Resource Definition (CRD).
* **Application source type** Which **Tool** is used to build the application.
* **Target state** The desired state of an application, as represented by files in a Git repository.
* **Live state** The live state of that application. What pods etc are deployed.
* **Sync status** Whether or not the live state matches the target state. Is the deployed application the same as Git says it should be?
* **Sync** The process of making an application move to its target state. E.g. by applying changes to a Kubernetes cluster.
* **Sync operation status** Whether or not a sync succeeded.
* **Refresh** Compare the latest code in Git with the live state. Figure out what is different.
* **Health** The health of the application, is it running correctly? Can it serve requests?
* **Tool** A tool to create manifests from a directory of files. E.g. Kustomize. See **Application Source Type**.
* **Configuration management tool** See **Tool**.
* **Configuration management plugin** A custom tool.

[Previous
Understand The Basics](../understand_the_basics/)
[Next
Getting Started](../getting_started/)

Made with
[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)

{"base": "..", "features": [], "search": "../assets/javascripts/workers/search.b0710199.min.js", "translations": {"clipboard.copied": "Copied to clipboard", "clipboard.copy": "Copy to clipboard", "search.config.lang": "en", "search.config.pipeline": "trimmer, stopWordFilter", "search.config.separator": "[\\s\\-]+", "search.placeholder": "Search", "search.result.more.one": "1 more on this page", "search.result.more.other": "# more on this page", "search.result.none": "No matching documents", "search.result.one": "1 matching document", "search.result.other": "# matching documents", "search.result.placeholder": "Type to start searching", "search.result.term.missing": "Missing", "select.version.title": "Select version"}, "version": null}