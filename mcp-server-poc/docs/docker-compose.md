Quickstart | Docker Docs{"@context":"https://schema.org","@type":"TechArticle","articleSection":"manuals","author":{"@type":"Organization","name":"Docker Inc","url":"https://www.docker.com"},"dateModified":"2026-03-09T16:00:22Z","description":"Follow this hands-on tutorial to learn how to use Docker Compose from defining application dependencies to experimenting with commands.","headline":"Quickstart","inLanguage":"en","isPartOf":{"@id":"https://docs.docker.com/compose/","@type":"WebPage","name":"Docker Compose"},"keywords":["docker","compose","example","docker","compose","tutorial","how","to","use","docker","compose","running","docker","compose","how","to","run","docker","compose","docker","compose","build","image","docker","compose","command","example","run","docker","compose","file","how","to","create","a","docker","compose","file","run","a","docker","compose","file"],"mainEntityOfPage":{"@id":"https://docs.docker.com/compose/gettingstarted/","@type":"WebPage"},"publisher":{"@type":"Organization","logo":{"@type":"ImageObject","url":"https://docs.docker.com/assets/images/docker-logo.png"},"name":"Docker Inc","url":"https://www.docker.com"},"url":"https://docs.docker.com/compose/gettingstarted/"}{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","item":{"@id":"https://docs.docker.com/manuals/","name":"Manuals"},"position":1},{"@type":"ListItem","item":{"@id":"https://docs.docker.com/compose/","name":"Docker Compose"},"position":2},{"@type":"ListItem","item":{"@id":"https://docs.docker.com/compose/gettingstarted/","name":"Quickstart"},"position":3}]}

function OptanonWrapper(){}(function(e,t,n,s,o){e[s]=e[s]||[],e[s].push({"gtm.start":(new Date).getTime(),event:"gtm.js"});var a=t.getElementsByTagName(n)[0],i=t.createElement(n),r=s!="dataLayer"?"&l="+s:"";i.async=!0,i.src="https://www.googletagmanager.com/gtm.js?id="+o+r,a.parentNode.insertBefore(i,a)})(window,document,"script","dataLayer","GTM-WL2QLG5")(function(e,t,n,s,o,i){e.hj=e.hj||function(){(e.hj.q=e.hj.q||[]).push(arguments)},e.\_hjSettings={hjid:3169877,hjsv:6},o=t.getElementsByTagName("head")[0],i=t.createElement("script"),i.async=1,i.src=n+e.\_hjSettings.hjid+s+e.\_hjSettings.hjsv,o.appendChild(i)})(window,document,"https://static.hotjar.com/c/hotjar-",".js?sv=")(()=>{var e=localStorage.getItem("theme-preference"),t=window.matchMedia("(prefers-color-scheme: dark)").matches;document.firstElementChild.className=e==="dark"||e==="light"?e:t?"dark":"light",document.firstElementChild.dataset.themePreference=e||"auto"})()

* [Get started](/get-started/)
* [Guides](/guides/)
* [Manuals](/manuals/)
* [Reference](/reference/)

Gordon

Gordon, your AI assistant for Docker docs

Search

await import('/pagefind/pagefind-component-ui.js');
const { configureInstance, getInstanceManager } = window.PagefindComponents;
configureInstance('default', {
bundlePath: '/pagefind/',
ranking: {
termFrequency: 0.0,
termSimilarity: 2.0,
pageLength: 0.0,
termSaturation: 1.0,
metaWeights: {
title: 10.0,
description: 4.0,
keywords: 6.0
}
}
});
document.body.insertAdjacentHTML('beforeend', `
<pagefind-modal id="search-modal" reset-on-close>
<pagefind-modal-header>
<pagefind-input placeholder="Search documentation…"></pagefind-input>
</pagefind-modal-header>
<pagefind-modal-body>
<p id="search-placeholder" class="text-center text-gray-500 dark:text-gray-400 py-8">
Start typing to search the documentation
</p>
<pagefind-summary></pagefind-summary>
<pagefind-results>
\x3Cscript type="text/pagefind-template">
<li class="py-3 border-b border-gray-200 dark:border-gray-700 last:border-b-0">
\u007b\u007b#if meta.breadcrumbs\u007d\u007d
<p class="text-xs text-gray-500 dark:text-gray-400 mb-1">\u007b\u007b meta.breadcrumbs \u007d\u007d</p>
\u007b\u007b\/if\u007d\u007d
<p class="font-medium">
<a class="text-blue-600 dark:text-blue-400 hover:underline" href="\u007b\u007b meta.url | default(url) | safeUrl \u007d\u007d">
\u007b\u007b meta.title \u007d\u007d
</a>
</p>
\u007b\u007b#if excerpt\u007d\u007d
<p class="text-gray-600 dark:text-gray-400 mt-1 text-sm">\u007b\u007b\u002b excerpt \u002b\u007d\u007d</p>
\u007b\u007b\/if\u007d\u007d
\u007b\u007b#if sub\_results\u007d\u007d
<ul class="mt-3 ml-4 flex flex-wrap gap-2">
\u007b\u007b#each sub\_results as sub\u007d\u007d
\u007b\u007b#if (lt @index 5)\u007d\u007d
<li class="text-sm">
<a class="text-blue-600 dark:text-blue-400 hover:underline" href="\u007b\u007b sub.url | safeUrl \u007d\u007d">
\u007b\u007b sub.title \u007d\u007d
</a>
</li>
\u007b\u007b\/if\u007d\u007d
\u007b\u007b\/each\u007d\u007d
</ul>
\u007b\u007b\/if\u007d\u007d
</li>
\x3C/script>
</pagefind-results>
</pagefind-modal-body>
</pagefind-modal>
`);
const modal = document.getElementById('search-modal');
const placeholder = document.getElementById('search-placeholder');
const instance = getInstanceManager().getInstance('default');
instance.on('search', (term) => {
placeholder.hidden = !!term;
});
instance.on('results', () => {
placeholder.hidden = !!instance.searchTerm;
});
const openModal = () => modal.open?.();
document.getElementById('search-modal-trigger').addEventListener('click', openModal);
document.addEventListener('keydown', (e) => {
if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
e.preventDefault();
openModal();
}
});

window.GORDON\_BASE\_URL="https://ai-backend-service.docker.com"

Start a new chat

### What can I help you with?

I'm Gordon, your AI assistant for Docker and documentation
questions.

Try asking

Get started with Docker

Docker Hardened Images

MCP Toolkit

Create an org

Was this helpful?

Helpful

Not quite

Copy

remaining in this thread.

You've reached the maximum of
 questions per thread. For
better answer quality, start a new thread.

Start a new thread

When enabled, Gordon considers the current page you're viewing
to provide more relevant answers.

[Share feedback](https://github.com/docker/docs/issues/23966)

Answers are generated based on the documentation.

@keyframes robotFloat{0%,100%{transform:translateY(0)rotate(0)}50%{transform:translateY(-15px)rotate(1deg)}}#gordon-chat pre{background:#0d1117;border-radius:.25rem;padding:0;margin:.5rem 0;overflow-x:auto;white-space:pre}#gordon-chat pre code{background:#0d1117;color:#c9d1d9;padding:1rem;display:block;font-family:roboto mono,monospace;font-size:.875rem;line-height:1.5;white-space:pre;overflow-x:auto}#gordon-chat pre code \*{white-space:pre}#gordon-chat .prose code.not-prose{background-color:#e5e7eb;color:#111827;padding:.2em .4em;border-radius:.25rem;font-family:roboto mono,monospace;font-size:.875em}.dark #gordon-chat .prose code.not-prose{background-color:#374151;color:#e5e7eb}

Back

[Manuals](https://docs.docker.com/manuals/)

* [Get started](/get-started/)
* [Guides](/guides/)
* [Reference](/reference/)

* Open source
* [Docker Engine](https://docs.docker.com/engine/)

  + [Install](https://docs.docker.com/engine/install/)

    - [Ubuntu](https://docs.docker.com/engine/install/ubuntu/ "Ubuntu")
    - [Debian](https://docs.docker.com/engine/install/debian/ "Debian")
    - [RHEL](https://docs.docker.com/engine/install/rhel/ "RHEL")
    - [Fedora](https://docs.docker.com/engine/install/fedora/ "Fedora")
    - [Raspberry Pi OS (32-bit / armhf)](https://docs.docker.com/engine/install/raspberry-pi-os/ "Raspberry Pi OS (32-bit / armhf)")
    - [CentOS](https://docs.docker.com/engine/install/centos/ "CentOS")
    - [SLES (s390x)](https://docs.docker.com/engine/install/sles/ "SLES (s390x)")
    - [Binaries](https://docs.docker.com/engine/install/binaries/ "Binaries")
    - [Post-installation steps](https://docs.docker.com/engine/install/linux-postinstall/ "Post-installation steps")
  + [Storage](https://docs.docker.com/engine/storage/)

    - [Volumes](https://docs.docker.com/engine/storage/volumes/ "Volumes")
    - [Bind mounts](https://docs.docker.com/engine/storage/bind-mounts/ "Bind mounts")
    - [tmpfs mounts](https://docs.docker.com/engine/storage/tmpfs/ "tmpfs mounts")
    - [Storage drivers](https://docs.docker.com/engine/storage/drivers/)

      * [Select a storage driver](https://docs.docker.com/engine/storage/drivers/select-storage-driver/ "Select a storage driver")
      * [BTRFS storage driver](https://docs.docker.com/engine/storage/drivers/btrfs-driver/ "BTRFS storage driver")
      * [Device Mapper storage driver (deprecated)](https://docs.docker.com/engine/storage/drivers/device-mapper-driver/ "Device Mapper storage driver (deprecated)")
      * [OverlayFS storage driver](https://docs.docker.com/engine/storage/drivers/overlayfs-driver/ "OverlayFS storage driver")
      * [VFS storage driver](https://docs.docker.com/engine/storage/drivers/vfs-driver/ "VFS storage driver")
      * [windowsfilter storage driver](https://docs.docker.com/engine/storage/drivers/windowsfilter-driver/ "windowsfilter storage driver")
      * [ZFS storage driver](https://docs.docker.com/engine/storage/drivers/zfs-driver/ "ZFS storage driver")
    - [containerd image store](https://docs.docker.com/engine/storage/containerd/ "containerd image store")
  + [Networking](https://docs.docker.com/engine/network/)

    - [Docker with iptables](https://docs.docker.com/engine/network/firewall-iptables/ "Docker with iptables")
    - [Docker with nftables](https://docs.docker.com/engine/network/firewall-nftables/ "Docker with nftables")
    - [Packet filtering and firewalls](https://docs.docker.com/engine/network/packet-filtering-firewalls/ "Packet filtering and firewalls")
    - [Port publishing and mapping](https://docs.docker.com/engine/network/port-publishing/ "Port publishing and mapping")
    - [Network drivers](https://docs.docker.com/engine/network/drivers/)

      * [Bridge network driver](https://docs.docker.com/engine/network/drivers/bridge/ "Bridge network driver")
      * [Host network driver](https://docs.docker.com/engine/network/drivers/host/ "Host network driver")
      * [IPvlan network driver](https://docs.docker.com/engine/network/drivers/ipvlan/ "IPvlan network driver")
      * [Macvlan network driver](https://docs.docker.com/engine/network/drivers/macvlan/ "Macvlan network driver")
      * [None network driver](https://docs.docker.com/engine/network/drivers/none/ "None network driver")
      * [Overlay network driver](https://docs.docker.com/engine/network/drivers/overlay/ "Overlay network driver")
    - [CA certificates](https://docs.docker.com/engine/network/ca-certs/ "CA certificates")
    - [Legacy container links](https://docs.docker.com/engine/network/links/ "Legacy container links")
  + Containers

    - [Start containers automatically](https://docs.docker.com/engine/containers/start-containers-automatically/ "Start containers automatically")
    - [Run multiple processes in a container](https://docs.docker.com/engine/containers/multi-service_container/ "Run multiple processes in a container")
    - [Resource constraints](https://docs.docker.com/engine/containers/resource_constraints/ "Resource constraints")
    - [GPU access](https://docs.docker.com/engine/containers/gpu/ "GPU access")
    - [Runtime metrics](https://docs.docker.com/engine/containers/runmetrics/ "Runtime metrics")
    - [Running containers](https://docs.docker.com/engine/containers/run/ "Running containers")
  + CLI

    - [Completion](https://docs.docker.com/engine/cli/completion/ "Completion")
    - [Proxy configuration](https://docs.docker.com/engine/cli/proxy/ "Proxy configuration")
    - [Filter commands](https://docs.docker.com/engine/cli/filter/ "Filter commands")
    - [Format command and log output](https://docs.docker.com/engine/cli/formatting/ "Format command and log output")
    - [OpenTelemetry for the Docker CLI](https://docs.docker.com/engine/cli/otel/ "OpenTelemetry for the Docker CLI")
  + [Daemon](https://docs.docker.com/engine/daemon/)

    - [Start the daemon](https://docs.docker.com/engine/daemon/start/ "Start the daemon")
    - [Use IPv6 networking](https://docs.docker.com/engine/daemon/ipv6/ "Use IPv6 networking")
    - [Daemon proxy configuration](https://docs.docker.com/engine/daemon/proxy/ "Daemon proxy configuration")
    - [Live restore](https://docs.docker.com/engine/daemon/live-restore/ "Live restore")
    - [Alternative container runtimes](https://docs.docker.com/engine/daemon/alternative-runtimes/ "Alternative container runtimes")
    - [Collect Docker metrics with Prometheus](https://docs.docker.com/engine/daemon/prometheus/ "Collect Docker metrics with Prometheus")
    - [Configure remote access for Docker daemon](https://docs.docker.com/engine/daemon/remote-access/ "Configure remote access for Docker daemon")
    - [Read the daemon logs](https://docs.docker.com/engine/daemon/logs/ "Read the daemon logs")
    - [Troubleshooting the Docker daemon](https://docs.docker.com/engine/daemon/troubleshoot/ "Troubleshooting the Docker daemon")
  + Manage resources

    - [Docker contexts](https://docs.docker.com/engine/manage-resources/contexts/ "Docker contexts")
    - [Docker object labels](https://docs.docker.com/engine/manage-resources/labels/ "Docker object labels")
    - [Prune unused Docker objects](https://docs.docker.com/engine/manage-resources/pruning/ "Prune unused Docker objects")
  + [Logs and metrics](https://docs.docker.com/engine/logging/)

    - [Configure logging drivers](https://docs.docker.com/engine/logging/configure/ "Configure logging drivers")
    - [Customize log driver output](https://docs.docker.com/engine/logging/log_tags/ "Customize log driver output")
    - Logging drivers

      * [Amazon CloudWatch Logs logging driver](https://docs.docker.com/engine/logging/drivers/awslogs/ "Amazon CloudWatch Logs logging driver")
      * [ETW logging driver](https://docs.docker.com/engine/logging/drivers/etwlogs/ "ETW logging driver")
      * [Fluentd logging driver](https://docs.docker.com/engine/logging/drivers/fluentd/ "Fluentd logging driver")
      * [Google Cloud Logging driver](https://docs.docker.com/engine/logging/drivers/gcplogs/ "Google Cloud Logging driver")
      * [Graylog Extended Format logging driver](https://docs.docker.com/engine/logging/drivers/gelf/ "Graylog Extended Format logging driver")
      * [Journald logging driver](https://docs.docker.com/engine/logging/drivers/journald/ "Journald logging driver")
      * [JSON File logging driver](https://docs.docker.com/engine/logging/drivers/json-file/ "JSON File logging driver")
      * [Local file logging driver](https://docs.docker.com/engine/logging/drivers/local/ "Local file logging driver")
      * [Splunk logging driver](https://docs.docker.com/engine/logging/drivers/splunk/ "Splunk logging driver")
      * [Syslog logging driver](https://docs.docker.com/engine/logging/drivers/syslog/ "Syslog logging driver")
    - [Use a logging driver plugin](https://docs.docker.com/engine/logging/plugins/ "Use a logging driver plugin")
    - [Use docker logs with remote logging drivers](https://docs.docker.com/engine/logging/dual-logging/ "Use docker logs with remote logging drivers")
  + [Security](https://docs.docker.com/engine/security/)

    - [Rootless mode](https://docs.docker.com/engine/security/rootless/)

      * [Tips](https://docs.docker.com/engine/security/rootless/tips/ "Tips")
      * [Troubleshooting](https://docs.docker.com/engine/security/rootless/troubleshoot/ "Troubleshooting")
    - [Antivirus software and Docker](https://docs.docker.com/engine/security/antivirus/ "Antivirus software and Docker")
    - [AppArmor security profiles for Docker](https://docs.docker.com/engine/security/apparmor/ "AppArmor security profiles for Docker")
    - [Content trust in Docker](https://docs.docker.com/engine/security/trust/)

      * [Automation with content trust](https://docs.docker.com/engine/security/trust/trust_automation/ "Automation with content trust")
      * [Delegations for content trust](https://docs.docker.com/engine/security/trust/trust_delegation/ "Delegations for content trust")
      * [Deploy Notary Server with Compose](https://docs.docker.com/engine/security/trust/deploying_notary/ "Deploy Notary Server with Compose")
      * [Manage keys for content trust](https://docs.docker.com/engine/security/trust/trust_key_mng/ "Manage keys for content trust")
      * [Play in a content trust sandbox](https://docs.docker.com/engine/security/trust/trust_sandbox/ "Play in a content trust sandbox")
    - [Docker security non-events](https://docs.docker.com/engine/security/non-events/ "Docker security non-events")
    - [Isolate containers with a user namespace](https://docs.docker.com/engine/security/userns-remap/ "Isolate containers with a user namespace")
    - [Protect the Docker daemon socket](https://docs.docker.com/engine/security/protect-access/ "Protect the Docker daemon socket")
    - [Seccomp security profiles for Docker](https://docs.docker.com/engine/security/seccomp/ "Seccomp security profiles for Docker")
    - [Verify repository client with certificates](https://docs.docker.com/engine/security/certificates/ "Verify repository client with certificates")
  + [Swarm mode](https://docs.docker.com/engine/swarm/)

    - [Administer and maintain a swarm of Docker Engines](https://docs.docker.com/engine/swarm/admin_guide/ "Administer and maintain a swarm of Docker Engines")
    - [Deploy a stack to a swarm](https://docs.docker.com/engine/swarm/stack-deploy/ "Deploy a stack to a swarm")
    - [Deploy services to a swarm](https://docs.docker.com/engine/swarm/services/ "Deploy services to a swarm")
    - [Getting started with Swarm mode](https://docs.docker.com/engine/swarm/swarm-tutorial/)

      * [Create a swarm](https://docs.docker.com/engine/swarm/swarm-tutorial/create-swarm/ "Create a swarm")
      * [Add nodes to the swarm](https://docs.docker.com/engine/swarm/swarm-tutorial/add-nodes/ "Add nodes to the swarm")
      * [Deploy a service to the swarm](https://docs.docker.com/engine/swarm/swarm-tutorial/deploy-service/ "Deploy a service to the swarm")
      * [Inspect a service on the swarm](https://docs.docker.com/engine/swarm/swarm-tutorial/inspect-service/ "Inspect a service on the swarm")
      * [Scale the service in the swarm](https://docs.docker.com/engine/swarm/swarm-tutorial/scale-service/ "Scale the service in the swarm")
      * [Delete the service running on the swarm](https://docs.docker.com/engine/swarm/swarm-tutorial/delete-service/ "Delete the service running on the swarm")
      * [Apply rolling updates to a service](https://docs.docker.com/engine/swarm/swarm-tutorial/rolling-update/ "Apply rolling updates to a service")
      * [Drain a node on the swarm](https://docs.docker.com/engine/swarm/swarm-tutorial/drain-node/ "Drain a node on the swarm")
    - How swarm works

      * [How nodes work](https://docs.docker.com/engine/swarm/how-swarm-mode-works/nodes/ "How nodes work")
      * [How services work](https://docs.docker.com/engine/swarm/how-swarm-mode-works/services/ "How services work")
      * [Manage swarm security with public key infrastructure (PKI)](https://docs.docker.com/engine/swarm/how-swarm-mode-works/pki/ "Manage swarm security with public key infrastructure (PKI)")
      * [Swarm task states](https://docs.docker.com/engine/swarm/how-swarm-mode-works/swarm-task-states/ "Swarm task states")
    - [Join nodes to a swarm](https://docs.docker.com/engine/swarm/join-nodes/ "Join nodes to a swarm")
    - [Lock your swarm to protect its encryption key](https://docs.docker.com/engine/swarm/swarm_manager_locking/ "Lock your swarm to protect its encryption key")
    - [Manage nodes in a swarm](https://docs.docker.com/engine/swarm/manage-nodes/ "Manage nodes in a swarm")
    - [Manage sensitive data with Docker secrets](https://docs.docker.com/engine/swarm/secrets/ "Manage sensitive data with Docker secrets")
    - [Manage swarm service networks](https://docs.docker.com/engine/swarm/networking/ "Manage swarm service networks")
    - [Raft consensus in swarm mode](https://docs.docker.com/engine/swarm/raft/ "Raft consensus in swarm mode")
    - [Run Docker Engine in swarm mode](https://docs.docker.com/engine/swarm/swarm-mode/ "Run Docker Engine in swarm mode")
    - [Store configuration data using Docker Configs](https://docs.docker.com/engine/swarm/configs/ "Store configuration data using Docker Configs")
    - [Swarm mode key concepts](https://docs.docker.com/engine/swarm/key-concepts/ "Swarm mode key concepts")
    - [Use Swarm mode routing mesh](https://docs.docker.com/engine/swarm/ingress/ "Use Swarm mode routing mesh")
  + [Deprecated features](https://docs.docker.com/engine/deprecated/ "Deprecated features")
  + [Docker Engine plugins](https://docs.docker.com/engine/extend/)

    - [Access authorization plugin](https://docs.docker.com/engine/extend/plugins_authorization/ "Access authorization plugin")
    - [Docker log driver plugins](https://docs.docker.com/engine/extend/plugins_logging/ "Docker log driver plugins")
    - [Docker network driver plugins](https://docs.docker.com/engine/extend/plugins_network/ "Docker network driver plugins")
    - [Docker Plugin API](https://docs.docker.com/engine/extend/plugin_api/ "Docker Plugin API")
    - [Docker volume plugins](https://docs.docker.com/engine/extend/plugins_volume/ "Docker volume plugins")
    - [Plugin Config Version 1 of Plugin V2](https://docs.docker.com/engine/extend/config/ "Plugin Config Version 1 of Plugin V2")
    - [Use Docker Engine plugins](https://docs.docker.com/engine/extend/legacy_plugins/ "Use Docker Engine plugins")
  + Release notes

    - [Engine v29](https://docs.docker.com/engine/release-notes/29/ "Engine v29")
    - [Engine v28](https://docs.docker.com/engine/release-notes/28/ "Engine v28")
    - [Engine v27](https://docs.docker.com/engine/release-notes/27/ "Engine v27")
    - [Engine v26.1](https://docs.docker.com/engine/release-notes/26.1/ "Engine v26.1")
    - [Engine v26.0](https://docs.docker.com/engine/release-notes/26.0/ "Engine v26.0")
    - [Engine v25.0](https://docs.docker.com/engine/release-notes/25.0/ "Engine v25.0")
    - [Engine v24.0](https://docs.docker.com/engine/release-notes/24.0/ "Engine v24.0")
    - [Engine v23.0](https://docs.docker.com/engine/release-notes/23.0/ "Engine v23.0")
    - [Engine v20.10](https://docs.docker.com/engine/release-notes/20.10/ "Engine v20.10")
    - [Engine v19.03](https://docs.docker.com/engine/release-notes/19.03/ "Engine v19.03")
    - [Engine v18.09](https://docs.docker.com/engine/release-notes/18.09/ "Engine v18.09")
    - [Engine v18.06](https://docs.docker.com/engine/release-notes/18.06/ "Engine v18.06")
    - [Engine v18.05](https://docs.docker.com/engine/release-notes/18.05/ "Engine v18.05")
    - [Engine v18.04](https://docs.docker.com/engine/release-notes/18.04/ "Engine v18.04")
    - [Engine v18.03](https://docs.docker.com/engine/release-notes/18.03/ "Engine v18.03")
    - [Engine v18.02](https://docs.docker.com/engine/release-notes/18.02/ "Engine v18.02")
    - [Engine v18.01](https://docs.docker.com/engine/release-notes/18.01/ "Engine v18.01")
    - [Engine v17.12](https://docs.docker.com/engine/release-notes/17.12/ "Engine v17.12")
    - [Engine v17.11](https://docs.docker.com/engine/release-notes/17.11/ "Engine v17.11")
    - [Engine v17.10](https://docs.docker.com/engine/release-notes/17.10/ "Engine v17.10")
    - [Engine v17.09](https://docs.docker.com/engine/release-notes/17.09/ "Engine v17.09")
    - [Engine v17.07](https://docs.docker.com/engine/release-notes/17.07/ "Engine v17.07")
    - [Engine v17.06](https://docs.docker.com/engine/release-notes/17.06/ "Engine v17.06")
    - [Engine v17.05](https://docs.docker.com/engine/release-notes/17.05/ "Engine v17.05")
    - [Engine v17.04](https://docs.docker.com/engine/release-notes/17.04/ "Engine v17.04")
    - [Engine v17.03](https://docs.docker.com/engine/release-notes/17.03/ "Engine v17.03")
    - [Prior releases](https://docs.docker.com/engine/release-notes/prior-releases/ "Prior releases")
* [Docker Build](https://docs.docker.com/build/)

  + Core concepts

    - [Docker Build Overview](https://docs.docker.com/build/concepts/overview/ "Docker Build Overview")
    - [Dockerfile overview](https://docs.docker.com/build/concepts/dockerfile/ "Dockerfile overview")
    - [Build context](https://docs.docker.com/build/concepts/context/ "Build context")
  + [Build checks](https://docs.docker.com/build/checks/ "Build checks")
  + Building

    - [Multi-stage](https://docs.docker.com/build/building/multi-stage/ "Multi-stage")
    - [Variables](https://docs.docker.com/build/building/variables/ "Variables")
    - [Secrets](https://docs.docker.com/build/building/secrets/ "Secrets")
    - [Multi-platform](https://docs.docker.com/build/building/multi-platform/ "Multi-platform")
    - [Export binaries](https://docs.docker.com/build/building/export/ "Export binaries")
    - [Container Device Interface (CDI)](https://docs.docker.com/build/building/cdi/ "Container Device Interface (CDI)")
    - [Best practices](https://docs.docker.com/build/building/best-practices/ "Best practices")
    - [Base images](https://docs.docker.com/build/building/base-images/ "Base images")
  + [Builders](https://docs.docker.com/build/builders/)

    - [Build drivers](https://docs.docker.com/build/builders/drivers/)

      * [Docker container driver](https://docs.docker.com/build/builders/drivers/docker-container/ "Docker container driver")
      * [Docker driver](https://docs.docker.com/build/builders/drivers/docker/ "Docker driver")
      * [Kubernetes driver](https://docs.docker.com/build/builders/drivers/kubernetes/ "Kubernetes driver")
      * [Remote driver](https://docs.docker.com/build/builders/drivers/remote/ "Remote driver")
    - [Manage builders](https://docs.docker.com/build/builders/manage/ "Manage builders")
  + [Bake](https://docs.docker.com/build/bake/)

    - [Introduction](https://docs.docker.com/build/bake/introduction/ "Introduction")
    - [Targets](https://docs.docker.com/build/bake/targets/ "Targets")
    - [Inheritance](https://docs.docker.com/build/bake/inheritance/ "Inheritance")
    - [Variables](https://docs.docker.com/build/bake/variables/ "Variables")
    - [Expressions](https://docs.docker.com/build/bake/expressions/ "Expressions")
    - [Functions](https://docs.docker.com/build/bake/funcs/ "Functions")
    - [Matrix targets](https://docs.docker.com/build/bake/matrices/ "Matrix targets")
    - [Contexts](https://docs.docker.com/build/bake/contexts/ "Contexts")
    - [Bake file reference](https://docs.docker.com/build/bake/reference/ "Bake file reference")
    - [Bake standard library functions](https://docs.docker.com/build/bake/stdlib/ "Bake standard library functions")
    - [Building with Bake from a Compose file](https://docs.docker.com/build/bake/compose-file/ "Building with Bake from a Compose file")
    - [Overriding configurations](https://docs.docker.com/build/bake/overrides/ "Overriding configurations")
    - [Remote Bake file definition](https://docs.docker.com/build/bake/remote-definition/ "Remote Bake file definition")
  + [Cache](https://docs.docker.com/build/cache/)

    - [Build cache invalidation](https://docs.docker.com/build/cache/invalidation/ "Build cache invalidation")
    - [Build garbage collection](https://docs.docker.com/build/cache/garbage-collection/ "Build garbage collection")
    - [Cache storage backends](https://docs.docker.com/build/cache/backends/)

      * [Amazon S3 cache](https://docs.docker.com/build/cache/backends/s3/ "Amazon S3 cache")
      * [Azure Blob Storage cache](https://docs.docker.com/build/cache/backends/azblob/ "Azure Blob Storage cache")
      * [GitHub Actions cache](https://docs.docker.com/build/cache/backends/gha/ "GitHub Actions cache")
      * [Inline cache](https://docs.docker.com/build/cache/backends/inline/ "Inline cache")
      * [Local cache](https://docs.docker.com/build/cache/backends/local/ "Local cache")
      * [Registry cache](https://docs.docker.com/build/cache/backends/registry/ "Registry cache")
    - [Optimize cache usage in builds](https://docs.docker.com/build/cache/optimize/ "Optimize cache usage in builds")
  + [CI](https://docs.docker.com/build/ci/)

    - [GitHub Actions](https://docs.docker.com/build/ci/github-actions/)

      * [Annotations](https://docs.docker.com/build/ci/github-actions/annotations/ "Annotations")
      * [Attestations](https://docs.docker.com/build/ci/github-actions/attestations/ "Attestations")
      * [Build checks](https://docs.docker.com/build/ci/github-actions/checks/ "Build checks")
      * [Build secrets](https://docs.docker.com/build/ci/github-actions/secrets/ "Build secrets")
      * [Build summary](https://docs.docker.com/build/ci/github-actions/build-summary/ "Build summary")
      * [BuildKit configuration](https://docs.docker.com/build/ci/github-actions/configure-builder/ "BuildKit configuration")
      * [Cache management](https://docs.docker.com/build/ci/github-actions/cache/ "Cache management")
      * [Copy image between registries](https://docs.docker.com/build/ci/github-actions/copy-image-registries/ "Copy image between registries")
      * [Export to Docker](https://docs.docker.com/build/ci/github-actions/export-docker/ "Export to Docker")
      * [GitHub Builder
        New](https://docs.docker.com/build/ci/github-actions/github-builder/)

        + [Architecture](https://docs.docker.com/build/ci/github-actions/github-builder/architecture/ "Architecture")
        + [Build workflow](https://docs.docker.com/build/ci/github-actions/github-builder/build/ "Build workflow")
        + [Bake workflow](https://docs.docker.com/build/ci/github-actions/github-builder/bake/ "Bake workflow")
      * [Local registry](https://docs.docker.com/build/ci/github-actions/local-registry/ "Local registry")
      * [Multi-platform image](https://docs.docker.com/build/ci/github-actions/multi-platform/ "Multi-platform image")
      * [Named contexts](https://docs.docker.com/build/ci/github-actions/named-contexts/ "Named contexts")
      * [Push to multiple registries](https://docs.docker.com/build/ci/github-actions/push-multi-registries/ "Push to multiple registries")
      * [Reproducible builds](https://docs.docker.com/build/ci/github-actions/reproducible-builds/ "Reproducible builds")
      * [Share image between jobs](https://docs.docker.com/build/ci/github-actions/share-image-jobs/ "Share image between jobs")
      * [Tags and labels](https://docs.docker.com/build/ci/github-actions/manage-tags-labels/ "Tags and labels")
      * [Test before push](https://docs.docker.com/build/ci/github-actions/test-before-push/ "Test before push")
      * [Update Docker Hub description](https://docs.docker.com/build/ci/github-actions/update-dockerhub-desc/ "Update Docker Hub description")
  + [Validating builds
    Experimental](https://docs.docker.com/build/policies/)

    - [Introduction](https://docs.docker.com/build/policies/intro/ "Introduction")
    - [Usage](https://docs.docker.com/build/policies/usage/ "Usage")
    - [Image validation](https://docs.docker.com/build/policies/validate-images/ "Image validation")
    - [Git validation](https://docs.docker.com/build/policies/validate-git/ "Git validation")
    - [Templates & examples](https://docs.docker.com/build/policies/examples/ "Templates & examples")
    - [Testing](https://docs.docker.com/build/policies/testing/ "Testing")
    - [Debugging](https://docs.docker.com/build/policies/debugging/ "Debugging")
    - [Input reference](https://docs.docker.com/build/policies/inputs/ "Input reference")
    - [Built-in functions](https://docs.docker.com/build/policies/built-ins/ "Built-in functions")
  + Metadata

    - [Annotations](https://docs.docker.com/build/metadata/annotations/ "Annotations")
    - [Build attestations](https://docs.docker.com/build/metadata/attestations/)

      * [Image attestation storage](https://docs.docker.com/build/metadata/attestations/attestation-storage/ "Image attestation storage")
      * [Provenance attestations](https://docs.docker.com/build/metadata/attestations/slsa-provenance/ "Provenance attestations")
      * [SBOM attestations](https://docs.docker.com/build/metadata/attestations/sbom/ "SBOM attestations")
      * [SLSA definitions](https://docs.docker.com/build/metadata/attestations/slsa-definitions/ "SLSA definitions")
  + [Exporters](https://docs.docker.com/build/exporters/)

    - [Image and registry exporters](https://docs.docker.com/build/exporters/image-registry/ "Image and registry exporters")
    - [Local and tar exporters](https://docs.docker.com/build/exporters/local-tar/ "Local and tar exporters")
    - [OCI and Docker exporters](https://docs.docker.com/build/exporters/oci-docker/ "OCI and Docker exporters")
  + [BuildKit](https://docs.docker.com/build/buildkit/)

    - [buildkitd.toml](https://docs.docker.com/build/buildkit/toml-configuration/ "buildkitd.toml")
    - [Configure BuildKit](https://docs.docker.com/build/buildkit/configure/ "Configure BuildKit")
    - [Custom Dockerfile syntax](https://docs.docker.com/build/buildkit/frontend/ "Custom Dockerfile syntax")
    - [Dockerfile release notes](https://github.com/moby/buildkit/releases "Dockerfile release notes")
  + Debugging

    - [OpenTelemetry support](https://docs.docker.com/build/debug/opentelemetry/ "OpenTelemetry support")
  + [Build release notes](https://github.com/docker/buildx/releases "Build release notes")
* [Docker Compose](https://docs.docker.com/compose/)

  + Introduction to Compose

    - [How Compose works](https://docs.docker.com/compose/intro/compose-application-model/ "How Compose works")
    - [Why use Compose?](https://docs.docker.com/compose/intro/features-uses/ "Why use Compose?")
    - [History and development](https://docs.docker.com/compose/intro/history/ "History and development")
  + [Install](https://docs.docker.com/compose/install/)

    - [Plugin](https://docs.docker.com/compose/install/linux/ "Plugin")
    - [Standalone (Legacy)](https://docs.docker.com/compose/install/standalone/ "Standalone (Legacy)")
    - [Uninstall](https://docs.docker.com/compose/install/uninstall/ "Uninstall")
  + [Quickstart](https://docs.docker.com/compose/gettingstarted/ "Quickstart")
  + How-tos

    - [Specify a project name](https://docs.docker.com/compose/how-tos/project-name/ "Specify a project name")
    - [Use lifecycle hooks](https://docs.docker.com/compose/how-tos/lifecycle/ "Use lifecycle hooks")
    - [Use service profiles](https://docs.docker.com/compose/how-tos/profiles/ "Use service profiles")
    - [Control startup order](https://docs.docker.com/compose/how-tos/startup-order/ "Control startup order")
    - [Use environment variables](https://docs.docker.com/compose/how-tos/environment-variables/)

      * [Set environment variables](https://docs.docker.com/compose/how-tos/environment-variables/set-environment-variables/ "Set environment variables")
      * [Environment variables precedence](https://docs.docker.com/compose/how-tos/environment-variables/envvars-precedence/ "Environment variables precedence")
      * [Pre-defined environment variables](https://docs.docker.com/compose/how-tos/environment-variables/envvars/ "Pre-defined environment variables")
      * [Interpolation](https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/ "Interpolation")
      * [Best practices](https://docs.docker.com/compose/how-tos/environment-variables/best-practices/ "Best practices")
    - [Build dependent images](https://docs.docker.com/compose/how-tos/dependent-images/ "Build dependent images")
    - [Use Compose Watch](https://docs.docker.com/compose/how-tos/file-watch/ "Use Compose Watch")
    - [Secrets in Compose](https://docs.docker.com/compose/how-tos/use-secrets/ "Secrets in Compose")
    - [Networking](https://docs.docker.com/compose/how-tos/networking/ "Networking")
    - [Use multiple Compose files](https://docs.docker.com/compose/how-tos/multiple-compose-files/)

      * [Merge](https://docs.docker.com/compose/how-tos/multiple-compose-files/merge/ "Merge")
      * [Extend](https://docs.docker.com/compose/how-tos/multiple-compose-files/extends/ "Extend")
      * [Include](https://docs.docker.com/compose/how-tos/multiple-compose-files/include/ "Include")
    - [Enable GPU support](https://docs.docker.com/compose/how-tos/gpu-support/ "Enable GPU support")
    - [Use Compose in production](https://docs.docker.com/compose/how-tos/production/ "Use Compose in production")
    - [OCI artifact applications](https://docs.docker.com/compose/how-tos/oci-artifact/ "OCI artifact applications")
    - [Use provider services](https://docs.docker.com/compose/how-tos/provider-services/ "Use provider services")
  + [Compose Bridge](https://docs.docker.com/compose/bridge/)

    - [Usage](https://docs.docker.com/compose/bridge/usage/ "Usage")
    - [Customize](https://docs.docker.com/compose/bridge/customize/ "Customize")
    - [Use Model Runner](https://docs.docker.com/compose/bridge/use-model-runner/ "Use Model Runner")
  + [Compose SDK
    New](https://docs.docker.com/compose/compose-sdk/ "Compose SDK")
  + [Trust model for Compose files](https://docs.docker.com/compose/trust-model/ "Trust model for Compose files")
  + Support and feedback

    - [FAQs](https://docs.docker.com/compose/support-and-feedback/faq/ "FAQs")
    - [Give feedback](https://docs.docker.com/compose/support-and-feedback/feedback/ "Give feedback")
  + [Release notes](https://github.com/docker/compose/releases "Release notes")
* [Testcontainers](https://docs.docker.com/testcontainers/ "Testcontainers")
* [Docker Agent
  Experimental](https://docs.docker.com/ai/docker-agent/)

  + [Model providers](https://docs.docker.com/ai/docker-agent/model-providers/ "Model providers")
  + [Local models](https://docs.docker.com/ai/docker-agent/local-models/ "Local models")
  + [Building a coding agent](https://docs.docker.com/ai/docker-agent/tutorial/ "Building a coding agent")
  + [Best practices](https://docs.docker.com/ai/docker-agent/best-practices/ "Best practices")
  + [Sharing agents](https://docs.docker.com/ai/docker-agent/sharing-agents/ "Sharing agents")
  + [Integrations](https://docs.docker.com/ai/docker-agent/integrations/)

    - [A2A](https://docs.docker.com/ai/docker-agent/integrations/a2a/ "A2A")
    - [ACP](https://docs.docker.com/ai/docker-agent/integrations/acp/ "ACP")
    - [MCP](https://docs.docker.com/ai/docker-agent/integrations/mcp/ "MCP")
  + Reference

    - [Configuration file](https://docs.docker.com/ai/docker-agent/reference/config/ "Configuration file")
    - [Toolsets](https://docs.docker.com/ai/docker-agent/reference/toolsets/ "Toolsets")
    - [CLI](https://docs.docker.com/ai/docker-agent/reference/cli/ "CLI")
    - [Examples](https://docs.docker.com/ai/docker-agent/reference/examples/ "Examples")
  + [RAG](https://docs.docker.com/ai/docker-agent/rag/ "RAG")
  + [Evals](https://docs.docker.com/ai/docker-agent/evals/ "Evals")

* AI
* [Overview](https://docs.docker.com/ai-overview/ "Overview")
* [MCP Catalog and Toolkit
  Beta](https://docs.docker.com/ai/mcp-catalog-and-toolkit/)

  + [Get started](https://docs.docker.com/ai/mcp-catalog-and-toolkit/get-started/ "Get started")
  + [Catalog](https://docs.docker.com/ai/mcp-catalog-and-toolkit/catalog/ "Catalog")
  + [Profiles](https://docs.docker.com/ai/mcp-catalog-and-toolkit/profiles/ "Profiles")
  + [Toolkit UI](https://docs.docker.com/ai/mcp-catalog-and-toolkit/toolkit/ "Toolkit UI")
  + [Use with CLI](https://docs.docker.com/ai/mcp-catalog-and-toolkit/cli/ "Use with CLI")
  + [Dynamic discovery](https://docs.docker.com/ai/mcp-catalog-and-toolkit/dynamic-mcp/ "Dynamic discovery")
  + [Gateway](https://docs.docker.com/ai/mcp-catalog-and-toolkit/mcp-gateway/ "Gateway")
  + [Hub MCP server](https://docs.docker.com/ai/mcp-catalog-and-toolkit/hub-mcp/ "Hub MCP server")
  + [FAQs](https://docs.docker.com/ai/mcp-catalog-and-toolkit/faqs/ "FAQs")
  + [E2B sandboxes](https://docs.docker.com/ai/mcp-catalog-and-toolkit/e2b-sandboxes/ "E2B sandboxes")
* [Docker Sandboxes
  Experimental](https://docs.docker.com/ai/sandboxes/)

  + [Get started](https://docs.docker.com/ai/sandboxes/get-started/ "Get started")
  + [Usage](https://docs.docker.com/ai/sandboxes/usage/ "Usage")
  + [Agents](https://docs.docker.com/ai/sandboxes/agents/)

    - [Claude Code](https://docs.docker.com/ai/sandboxes/agents/claude-code/ "Claude Code")
    - [Codex](https://docs.docker.com/ai/sandboxes/agents/codex/ "Codex")
    - [Copilot](https://docs.docker.com/ai/sandboxes/agents/copilot/ "Copilot")
    - [Gemini](https://docs.docker.com/ai/sandboxes/agents/gemini/ "Gemini")
    - [Kiro](https://docs.docker.com/ai/sandboxes/agents/kiro/ "Kiro")
    - [OpenCode](https://docs.docker.com/ai/sandboxes/agents/opencode/ "OpenCode")
    - [Docker Agent](https://docs.docker.com/ai/sandboxes/agents/docker-agent/ "Docker Agent")
    - [Custom environments](https://docs.docker.com/ai/sandboxes/agents/custom-environments/ "Custom environments")
  + [Architecture](https://docs.docker.com/ai/sandboxes/architecture/ "Architecture")
  + [Security model](https://docs.docker.com/ai/sandboxes/security/)

    - [Isolation layers](https://docs.docker.com/ai/sandboxes/security/isolation/ "Isolation layers")
    - [Defaults](https://docs.docker.com/ai/sandboxes/security/defaults/ "Defaults")
    - [Credentials](https://docs.docker.com/ai/sandboxes/security/credentials/ "Credentials")
    - [Policies](https://docs.docker.com/ai/sandboxes/security/policy/ "Policies")
    - [Workspace trust](https://docs.docker.com/ai/sandboxes/security/workspace/ "Workspace trust")
  + [Troubleshooting](https://docs.docker.com/ai/sandboxes/troubleshooting/ "Troubleshooting")
  + [FAQ](https://docs.docker.com/ai/sandboxes/faq/ "FAQ")
  + [Docker Desktop](https://docs.docker.com/ai/sandboxes/docker-desktop/ "Docker Desktop")
* [Model Runner](https://docs.docker.com/ai/model-runner/)

  + [Get started with DMR](https://docs.docker.com/ai/model-runner/get-started/ "Get started with DMR")
  + [DMR REST API](https://docs.docker.com/ai/model-runner/api-reference/ "DMR REST API")
  + [Configuration options](https://docs.docker.com/ai/model-runner/configuration/ "Configuration options")
  + [DMR examples](https://docs.docker.com/ai/model-runner/examples/ "DMR examples")
  + [IDE and tool integrations](https://docs.docker.com/ai/model-runner/ide-integrations/ "IDE and tool integrations")
  + [Open WebUI integration](https://docs.docker.com/ai/model-runner/openwebui-integration/ "Open WebUI integration")
  + [Inference engines](https://docs.docker.com/ai/model-runner/inference-engines/ "Inference engines")
* [Gordon
  Beta](https://docs.docker.com/ai/gordon/)

  + [Use cases](https://docs.docker.com/ai/gordon/use-cases/ "Use cases")
  + Concepts

    - [Capabilities](https://docs.docker.com/ai/gordon/concepts/capabilities/ "Capabilities")
    - [Data privacy](https://docs.docker.com/ai/gordon/concepts/data-privacy/ "Data privacy")
  + How-to guides

    - [Docker Desktop](https://docs.docker.com/ai/gordon/how-to/docker-desktop/ "Docker Desktop")
    - [CLI](https://docs.docker.com/ai/gordon/how-to/cli/ "CLI")
    - [Permissions](https://docs.docker.com/ai/gordon/how-to/permissions/ "Permissions")
    - [Configure tools](https://docs.docker.com/ai/gordon/how-to/configure-tools/ "Configure tools")
* AI and Docker Compose

  + [Use AI models in Compose](https://docs.docker.com/ai/compose/models-and-compose/ "Use AI models in Compose")

* Products
* [Docker Hardened Images
  New](https://docs.docker.com/dhi/)

  + [Quickstart](https://docs.docker.com/dhi/get-started/ "Quickstart")
  + [Features](https://docs.docker.com/dhi/features/ "Features")
  + [Explore](https://docs.docker.com/dhi/explore/)

    - [Hardened images](https://docs.docker.com/dhi/explore/what/ "Hardened images")
    - [Build process](https://docs.docker.com/dhi/explore/build-process/ "Build process")
    - [Image types](https://docs.docker.com/dhi/explore/available/ "Image types")
    - [Scanner integrations](https://docs.docker.com/dhi/explore/scanner-integrations/ "Scanner integrations")
    - [Image testing](https://docs.docker.com/dhi/explore/test/ "Image testing")
    - [Responsibility overview](https://docs.docker.com/dhi/explore/responsibility/ "Responsibility overview")
    - [Feedback](https://docs.docker.com/dhi/explore/feedback/ "Feedback")
  + [Migration](https://docs.docker.com/dhi/migration/)

    - [Migration checklist](https://docs.docker.com/dhi/migration/checklist/ "Migration checklist")
    - [AI-assisted migration
      Experimental](https://docs.docker.com/dhi/migration/migrate-with-ai/ "AI-assisted migration")
    - [Migrate from Alpine or Debian](https://docs.docker.com/dhi/migration/migrate-from-doi/ "Migrate from Alpine or Debian")
    - [Migrate from Ubuntu](https://docs.docker.com/dhi/migration/migrate-from-ubuntu/ "Migrate from Ubuntu")
    - [Migrate from Wolfi](https://docs.docker.com/dhi/migration/migrate-from-wolfi/ "Migrate from Wolfi")
    - [Migration examples](https://docs.docker.com/dhi/migration/examples/)

      * [Go](https://docs.docker.com/dhi/migration/examples/go/ "Go")
      * [Python](https://docs.docker.com/dhi/migration/examples/python/ "Python")
      * [Node.js](https://docs.docker.com/dhi/migration/examples/node/ "Node.js")
  + [How-tos](https://docs.docker.com/dhi/how-to/)

    - [Search and evaluate](https://docs.docker.com/dhi/how-to/explore/ "Search and evaluate")
    - [Mirror a repository](https://docs.docker.com/dhi/how-to/mirror/ "Mirror a repository")
    - [Customize an image or chart](https://docs.docker.com/dhi/how-to/customize/ "Customize an image or chart")
    - [Create and build an image](https://docs.docker.com/dhi/how-to/build/ "Create and build an image")
    - [Use an image](https://docs.docker.com/dhi/how-to/use/ "Use an image")
    - [Use a Helm chart](https://docs.docker.com/dhi/how-to/helm/ "Use a Helm chart")
    - [Use hardened packages](https://docs.docker.com/dhi/how-to/hardened-packages/ "Use hardened packages")
    - [Manage images and charts](https://docs.docker.com/dhi/how-to/manage/ "Manage images and charts")
    - [Verify an image or chart](https://docs.docker.com/dhi/how-to/verify/ "Verify an image or chart")
    - [Scan an image](https://docs.docker.com/dhi/how-to/scan/ "Scan an image")
    - [Enforce image usage](https://docs.docker.com/dhi/how-to/policies/ "Enforce image usage")
    - [Use the CLI](https://docs.docker.com/dhi/how-to/cli/ "Use the CLI")
    - [Use DHI Select & Enterprise](https://docs.docker.com/dhi/how-to/select-enterprise/ "Use DHI Select & Enterprise")
  + [Core concepts](https://docs.docker.com/dhi/core-concepts/)

    - [Attestations](https://docs.docker.com/dhi/core-concepts/attestations/ "Attestations")
    - [CIS Benchmark](https://docs.docker.com/dhi/core-concepts/cis/ "CIS Benchmark")
    - [Code signing](https://docs.docker.com/dhi/core-concepts/signatures/ "Code signing")
    - [CVEs](https://docs.docker.com/dhi/core-concepts/cves/ "CVEs")
    - [Distroless images](https://docs.docker.com/dhi/core-concepts/distroless/ "Distroless images")
    - [FIPS](https://docs.docker.com/dhi/core-concepts/fips/ "FIPS")
    - [glibc and musl](https://docs.docker.com/dhi/core-concepts/glibc-musl/ "glibc and musl")
    - [Hardening](https://docs.docker.com/dhi/core-concepts/hardening/ "Hardening")
    - [Image digests](https://docs.docker.com/dhi/core-concepts/digests/ "Image digests")
    - [Image provenance](https://docs.docker.com/dhi/core-concepts/provenance/ "Image provenance")
    - [Immutability](https://docs.docker.com/dhi/core-concepts/immutability/ "Immutability")
    - [SBOMs](https://docs.docker.com/dhi/core-concepts/sbom/ "SBOMs")
    - [SLSA](https://docs.docker.com/dhi/core-concepts/slsa/ "SLSA")
    - [Software Supply Chain Security](https://docs.docker.com/dhi/core-concepts/sscs/ "Software Supply Chain Security")
    - [SSDLC](https://docs.docker.com/dhi/core-concepts/ssdlc/ "SSDLC")
    - [STIG](https://docs.docker.com/dhi/core-concepts/stig/ "STIG")
    - [VEX](https://docs.docker.com/dhi/core-concepts/vex/ "VEX")
  + [Troubleshoot](https://docs.docker.com/dhi/troubleshoot/ "Troubleshoot")
  + [Additional resources](https://docs.docker.com/dhi/resources/ "Additional resources")
* [Docker Desktop](https://docs.docker.com/desktop/)

  + Setup

    - Install

      * [Mac](https://docs.docker.com/desktop/setup/install/mac-install/ "Mac")
      * [Mac permission requirements](https://docs.docker.com/desktop/setup/install/mac-permission-requirements/ "Mac permission requirements")
      * [Windows](https://docs.docker.com/desktop/setup/install/windows-install/ "Windows")
      * [Windows permission requirements](https://docs.docker.com/desktop/setup/install/windows-permission-requirements/ "Windows permission requirements")
      * [Linux](https://docs.docker.com/desktop/setup/install/linux/)

        + [Ubuntu](https://docs.docker.com/desktop/setup/install/linux/ubuntu/ "Ubuntu")
        + [Debian](https://docs.docker.com/desktop/setup/install/linux/debian/ "Debian")
        + [Fedora](https://docs.docker.com/desktop/setup/install/linux/fedora/ "Fedora")
        + [Arch](https://docs.docker.com/desktop/setup/install/linux/archlinux/ "Arch")
        + [RHEL](https://docs.docker.com/desktop/setup/install/linux/rhel/ "RHEL")
    - [VM or VDI environments](https://docs.docker.com/desktop/setup/vm-vdi/ "VM or VDI environments")
    - [Sign in](https://docs.docker.com/desktop/setup/sign-in/ "Sign in")
    - [Allowlist](https://docs.docker.com/desktop/setup/allow-list/ "Allowlist")
  + [Explore Docker Desktop](https://docs.docker.com/desktop/use-desktop/)

    - [Containers](https://docs.docker.com/desktop/use-desktop/container/ "Containers")
    - [Images](https://docs.docker.com/desktop/use-desktop/images/ "Images")
    - [Volumes](https://docs.docker.com/desktop/use-desktop/volumes/ "Volumes")
    - [Builds](https://docs.docker.com/desktop/use-desktop/builds/ "Builds")
    - [Kubernetes](https://docs.docker.com/desktop/use-desktop/kubernetes/ "Kubernetes")
    - [Logs
      Beta](https://docs.docker.com/desktop/use-desktop/logs/ "Logs")
    - [Resource Saver mode](https://docs.docker.com/desktop/use-desktop/resource-saver/ "Resource Saver mode")
    - [Pause Docker Desktop](https://docs.docker.com/desktop/use-desktop/pause/ "Pause Docker Desktop")
  + Features and capabilities

    - [Networking](https://docs.docker.com/desktop/features/networking/)

      * [How-tos](https://docs.docker.com/desktop/features/networking/networking-how-tos/ "How-tos")
    - [GPU support](https://docs.docker.com/desktop/features/gpu/ "GPU support")
    - [USB/IP support](https://docs.docker.com/desktop/features/usbip/ "USB/IP support")
    - [Synchronized file shares](https://docs.docker.com/desktop/features/synchronized-file-sharing/ "Synchronized file shares")
    - [containerd image store](https://docs.docker.com/desktop/features/containerd/ "containerd image store")
    - [Wasm workloads
      Beta](https://docs.docker.com/desktop/features/wasm/ "Wasm workloads")
    - [Docker Desktop CLI](https://docs.docker.com/desktop/features/desktop-cli/ "Docker Desktop CLI")
    - [Virtual Machine Manager](https://docs.docker.com/desktop/features/vmm/ "Virtual Machine Manager")
    - [WSL](https://docs.docker.com/desktop/features/wsl/)

      * [Best practices](https://docs.docker.com/desktop/features/wsl/best-practices/ "Best practices")
      * [Custom kernels](https://docs.docker.com/desktop/features/wsl/custom-kernels/ "Custom kernels")
      * [Use WSL](https://docs.docker.com/desktop/features/wsl/use-wsl/ "Use WSL")
  + Settings and maintenance

    - [Change settings](https://docs.docker.com/desktop/settings-and-maintenance/settings/ "Change settings")
    - [Backup and restore data](https://docs.docker.com/desktop/settings-and-maintenance/backup-and-restore/ "Backup and restore data")
  + Troubleshoot and support

    - [Troubleshoot and diagnose](https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/)

      * [Common topics](https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/topics/ "Common topics")
      * [Known issues](https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/known-issues/ "Known issues")
      * [MacOS app damaged dialog](https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/mac-damaged-dialog/ "MacOS app damaged dialog")
    - FAQs

      * [General](https://docs.docker.com/desktop/troubleshoot-and-support/faqs/general/ "General")
      * [Mac](https://docs.docker.com/desktop/troubleshoot-and-support/faqs/macfaqs/ "Mac")
      * [Windows](https://docs.docker.com/desktop/troubleshoot-and-support/faqs/windowsfaqs/ "Windows")
      * [Linux](https://docs.docker.com/desktop/troubleshoot-and-support/faqs/linuxfaqs/ "Linux")
      * [Releases](https://docs.docker.com/desktop/troubleshoot-and-support/faqs/releases/ "Releases")
    - [Give feedback](https://docs.docker.com/desktop/troubleshoot-and-support/feedback/ "Give feedback")
  + [Uninstall](https://docs.docker.com/desktop/uninstall/ "Uninstall")
  + [Release notes](https://docs.docker.com/desktop/release-notes/ "Release notes")
* [Docker Offload](https://docs.docker.com/offload/)

  + [Quickstart](https://docs.docker.com/offload/quickstart/ "Quickstart")
  + [About](https://docs.docker.com/offload/about/ "About")
  + [Configure](https://docs.docker.com/offload/configuration/ "Configure")
  + [Usage](https://docs.docker.com/offload/usage/ "Usage")
  + [Optimize usage](https://docs.docker.com/offload/optimize/ "Optimize usage")
  + [Troubleshoot](https://docs.docker.com/offload/troubleshoot/ "Troubleshoot")
  + [Give feedback](https://docs.docker.com/offload/feedback/ "Give feedback")
* [Docker Build Cloud](https://docs.docker.com/build-cloud/)

  + [Setup](https://docs.docker.com/build-cloud/setup/ "Setup")
  + [Usage](https://docs.docker.com/build-cloud/usage/ "Usage")
  + [Continuous integration](https://docs.docker.com/build-cloud/ci/ "Continuous integration")
  + [Optimization](https://docs.docker.com/build-cloud/optimization/ "Optimization")
  + [Builder settings](https://docs.docker.com/build-cloud/builder-settings/ "Builder settings")
  + [Release notes](https://docs.docker.com/build-cloud/release-notes/ "Release notes")
* [Docker Hub](https://docs.docker.com/docker-hub/)

  + [Quickstart](https://docs.docker.com/docker-hub/quickstart/ "Quickstart")
  + [Library](https://docs.docker.com/docker-hub/image-library/)

    - [Search](https://docs.docker.com/docker-hub/image-library/search/ "Search")
    - [Trusted content](https://docs.docker.com/docker-hub/image-library/trusted-content/ "Trusted content")
    - [Catalogs](https://docs.docker.com/docker-hub/image-library/catalogs/ "Catalogs")
    - [Mirror](https://docs.docker.com/docker-hub/image-library/mirror/ "Mirror")
  + [Repositories](https://docs.docker.com/docker-hub/repos/)

    - [Create](https://docs.docker.com/docker-hub/repos/create/ "Create")
    - Manage

      * [Repository information](https://docs.docker.com/docker-hub/repos/manage/information/ "Repository information")
      * [Access](https://docs.docker.com/docker-hub/repos/manage/access/ "Access")
      * [Images](https://docs.docker.com/docker-hub/repos/manage/hub-images/)

        + [Tags](https://docs.docker.com/docker-hub/repos/manage/hub-images/tags/ "Tags")
        + [Immutable tags](https://docs.docker.com/docker-hub/repos/manage/hub-images/immutable-tags/ "Immutable tags")
        + [Image Management](https://docs.docker.com/docker-hub/repos/manage/hub-images/manage/ "Image Management")
        + [Software artifacts](https://docs.docker.com/docker-hub/repos/manage/hub-images/oci-artifacts/ "Software artifacts")
        + [Push images](https://docs.docker.com/docker-hub/repos/manage/hub-images/push/ "Push images")
        + [Move images](https://docs.docker.com/docker-hub/repos/manage/hub-images/move/ "Move images")
        + [Bulk migrate images](https://docs.docker.com/docker-hub/repos/manage/hub-images/bulk-migrate/ "Bulk migrate images")
      * [Image security insights](https://docs.docker.com/docker-hub/repos/manage/vulnerability-scanning/ "Image security insights")
      * [Webhooks](https://docs.docker.com/docker-hub/repos/manage/webhooks/ "Webhooks")
      * [Automated builds](https://docs.docker.com/docker-hub/repos/manage/builds/)

        + [Set up](https://docs.docker.com/docker-hub/repos/manage/builds/setup/ "Set up")
        + [Link accounts](https://docs.docker.com/docker-hub/repos/manage/builds/link-source/ "Link accounts")
        + [Automated repository tests](https://docs.docker.com/docker-hub/repos/manage/builds/automated-testing/ "Automated repository tests")
        + [Advanced options](https://docs.docker.com/docker-hub/repos/manage/builds/advanced/ "Advanced options")
        + [Manage autobuilds](https://docs.docker.com/docker-hub/repos/manage/builds/manage-builds/ "Manage autobuilds")
        + [Troubleshoot](https://docs.docker.com/docker-hub/repos/manage/builds/troubleshoot/ "Troubleshoot")
      * [Trusted content](https://docs.docker.com/docker-hub/repos/manage/trusted-content/)

        + [Docker Official Images](https://docs.docker.com/docker-hub/repos/manage/trusted-content/official-images/ "Docker Official Images")
        + [Docker Verified Publisher Program](https://docs.docker.com/docker-hub/repos/manage/trusted-content/dvp-program/ "Docker Verified Publisher Program")
        + [Docker-Sponsored Open Source Program](https://docs.docker.com/docker-hub/repos/manage/trusted-content/dsos-program/ "Docker-Sponsored Open Source Program")
        + [Insights and analytics](https://docs.docker.com/docker-hub/repos/manage/trusted-content/insights-analytics/ "Insights and analytics")
      * [Export repositories](https://docs.docker.com/docker-hub/repos/manage/export/ "Export repositories")
    - [Archive](https://docs.docker.com/docker-hub/repos/archive/ "Archive")
    - [Delete](https://docs.docker.com/docker-hub/repos/delete/ "Delete")
  + [Settings](https://docs.docker.com/docker-hub/settings/ "Settings")
  + [Usage and limits](https://docs.docker.com/docker-hub/usage/)

    - [Pulls](https://docs.docker.com/docker-hub/usage/pulls/ "Pulls")
    - [Optimize usage](https://docs.docker.com/docker-hub/usage/manage/ "Optimize usage")
  + [Troubleshoot](https://docs.docker.com/docker-hub/troubleshoot/ "Troubleshoot")
  + [Release notes](https://docs.docker.com/docker-hub/release-notes/ "Release notes")
* [Docker Scout](https://docs.docker.com/scout/)

  + [Install](https://docs.docker.com/scout/install/ "Install")
  + [Quickstart](https://docs.docker.com/scout/quickstart/ "Quickstart")
  + Explore

    - [Dashboard](https://docs.docker.com/scout/explore/dashboard/ "Dashboard")
    - [Docker Scout image analysis](https://docs.docker.com/scout/explore/analysis/ "Docker Scout image analysis")
    - [Docker Scout metrics exporter](https://docs.docker.com/scout/explore/metrics-exporter/ "Docker Scout metrics exporter")
    - [Image details view](https://docs.docker.com/scout/explore/image-details-view/ "Image details view")
    - [Manage vulnerability exceptions](https://docs.docker.com/scout/explore/exceptions/ "Manage vulnerability exceptions")
  + How-tos

    - [Create an exception using the GUI](https://docs.docker.com/scout/how-tos/create-exceptions-gui/ "Create an exception using the GUI")
    - [Create an exception using the VEX](https://docs.docker.com/scout/how-tos/create-exceptions-vex/ "Create an exception using the VEX")
    - [Docker Scout environment variables](https://docs.docker.com/scout/how-tos/configure-cli/ "Docker Scout environment variables")
    - [Docker Scout SBOMs](https://docs.docker.com/scout/how-tos/view-create-sboms/ "Docker Scout SBOMs")
    - [Use Scout with different artifact types](https://docs.docker.com/scout/how-tos/artifact-types/ "Use Scout with different artifact types")
  + Deep dive

    - [Advisory database sources and matching service](https://docs.docker.com/scout/deep-dive/advisory-db-sources/ "Advisory database sources and matching service")
    - [Data collection and storage in Docker Scout](https://docs.docker.com/scout/deep-dive/data-handling/ "Data collection and storage in Docker Scout")
  + [Policy Evaluation](https://docs.docker.com/scout/policy/)

    - [Configure policies](https://docs.docker.com/scout/policy/configure/ "Configure policies")
    - [Docker Scout health scores](https://docs.docker.com/scout/policy/scores/ "Docker Scout health scores")
    - [Evaluate policy compliance in CI](https://docs.docker.com/scout/policy/ci/ "Evaluate policy compliance in CI")
    - [Remediation with Docker Scout](https://docs.docker.com/scout/policy/remediation/ "Remediation with Docker Scout")
    - [View Docker Scout policy status](https://docs.docker.com/scout/policy/view/ "View Docker Scout policy status")
  + [Integrations](https://docs.docker.com/scout/integrations/)

    - Code quality

      * [SonarQube](https://docs.docker.com/scout/integrations/code-quality/sonarqube/ "SonarQube")
    - Container registries

      * [Amazon ECR](https://docs.docker.com/scout/integrations/registry/ecr/ "Amazon ECR")
      * [Artifactory Container Registry](https://docs.docker.com/scout/integrations/registry/artifactory/ "Artifactory Container Registry")
      * [Azure Container Registry](https://docs.docker.com/scout/integrations/registry/acr/ "Azure Container Registry")
    - [Continuous Integration](https://docs.docker.com/scout/integrations/ci/)

      * [Azure DevOps Pipelines](https://docs.docker.com/scout/integrations/ci/azure/ "Azure DevOps Pipelines")
      * [Circle CI](https://docs.docker.com/scout/integrations/ci/circle-ci/ "Circle CI")
      * [GitHub Actions](https://docs.docker.com/scout/integrations/ci/gha/ "GitHub Actions")
      * [GitLab CI/CD](https://docs.docker.com/scout/integrations/ci/gitlab/ "GitLab CI/CD")
      * [Jenkins](https://docs.docker.com/scout/integrations/ci/jenkins/ "Jenkins")
    - [Integrating Docker Scout with environments](https://docs.docker.com/scout/integrations/environment/)

      * [Generic (CLI)](https://docs.docker.com/scout/integrations/environment/cli/ "Generic (CLI)")
      * [Sysdig](https://docs.docker.com/scout/integrations/environment/sysdig/ "Sysdig")
    - Source code management

      * [GitHub](https://docs.docker.com/scout/integrations/source-code-management/github/ "GitHub")
    - Team collaboration

      * [Slack](https://docs.docker.com/scout/integrations/team-collaboration/slack/ "Slack")
  + Release notes

    - [CLI release notes](https://github.com/docker/scout-cli/releases "CLI release notes")
    - [Platform release notes](https://docs.docker.com/scout/release-notes/platform/ "Platform release notes")
* [Docker Extensions](https://docs.docker.com/extensions/)

  + [Marketplace extensions](https://docs.docker.com/extensions/marketplace/ "Marketplace extensions")
  + [Non-marketplace extensions](https://docs.docker.com/extensions/non-marketplace/ "Non-marketplace extensions")
  + [Configure a private marketplace](https://docs.docker.com/extensions/private-marketplace/ "Configure a private marketplace")
  + [Settings and feedback](https://docs.docker.com/extensions/settings-feedback/ "Settings and feedback")
  + [Extensions SDK](https://docs.docker.com/extensions/extensions-sdk/)

    - [The build and publish process](https://docs.docker.com/extensions/extensions-sdk/process/ "The build and publish process")
    - [Quickstart](https://docs.docker.com/extensions/extensions-sdk/quickstart/ "Quickstart")
    - Part one: Build

      * [Create a simple extension](https://docs.docker.com/extensions/extensions-sdk/build/minimal-frontend-extension/ "Create a simple extension")
      * [Create an advanced frontend extension](https://docs.docker.com/extensions/extensions-sdk/build/frontend-extension-tutorial/ "Create an advanced frontend extension")
      * [Add a backend to your extension](https://docs.docker.com/extensions/extensions-sdk/build/backend-extension-tutorial/ "Add a backend to your extension")
    - [Part two: Publish](https://docs.docker.com/extensions/extensions-sdk/extensions/)

      * [Add labels](https://docs.docker.com/extensions/extensions-sdk/extensions/labels/ "Add labels")
      * [Validate](https://docs.docker.com/extensions/extensions-sdk/extensions/validate/ "Validate")
      * [Package and release your extension](https://docs.docker.com/extensions/extensions-sdk/extensions/DISTRIBUTION/ "Package and release your extension")
      * [Share your extension](https://docs.docker.com/extensions/extensions-sdk/extensions/share/ "Share your extension")
      * [Publish in the Marketplace](https://docs.docker.com/extensions/extensions-sdk/extensions/publish/ "Publish in the Marketplace")
      * [Build multi-arch extensions](https://docs.docker.com/extensions/extensions-sdk/extensions/multi-arch/ "Build multi-arch extensions")
    - [Architecture](https://docs.docker.com/extensions/extensions-sdk/architecture/)

      * [Metadata](https://docs.docker.com/extensions/extensions-sdk/architecture/metadata/ "Metadata")
      * [Security](https://docs.docker.com/extensions/extensions-sdk/architecture/security/ "Security")
    - [Design and UI styling](https://docs.docker.com/extensions/extensions-sdk/design/)

      * [Guidelines](https://docs.docker.com/extensions/extensions-sdk/design/design-guidelines/ "Guidelines")
      * [Docker design principles](https://docs.docker.com/extensions/extensions-sdk/design/design-principles/ "Docker design principles")
      * [MUI best practices](https://docs.docker.com/extensions/extensions-sdk/design/mui-best-practices/ "MUI best practices")
    - Developer Guides

      * [Authentication](https://docs.docker.com/extensions/extensions-sdk/guides/oauth2-flow/ "Authentication")
      * [Interacting with Kubernetes](https://docs.docker.com/extensions/extensions-sdk/guides/kubernetes/ "Interacting with Kubernetes")
      * [Invoke host binaries](https://docs.docker.com/extensions/extensions-sdk/guides/invoke-host-binaries/ "Invoke host binaries")
      * [Use the Docker socket](https://docs.docker.com/extensions/extensions-sdk/guides/use-docker-socket-from-backend/ "Use the Docker socket")
    - Developer SDK tools

      * [Test and debug](https://docs.docker.com/extensions/extensions-sdk/dev/test-debug/ "Test and debug")
      * [Continuous Integration (CI)](https://docs.docker.com/extensions/extensions-sdk/dev/continuous-integration/ "Continuous Integration (CI)")
      * [CLI reference](https://docs.docker.com/extensions/extensions-sdk/dev/usage/ "CLI reference")
      * Extension APIs

        + [Dashboard](https://docs.docker.com/extensions/extensions-sdk/dev/api/dashboard/ "Dashboard")
        + [Docker](https://docs.docker.com/extensions/extensions-sdk/dev/api/docker/ "Docker")
        + [Extension Backend](https://docs.docker.com/extensions/extensions-sdk/dev/api/backend/ "Extension Backend")
        + [Extension UI API](https://docs.docker.com/extensions/extensions-sdk/dev/api/overview/ "Extension UI API")
        + [Navigation](https://docs.docker.com/extensions/extensions-sdk/dev/api/dashboard-routes-navigation/ "Navigation")
* [Testcontainers Cloud](https://testcontainers.com/cloud/docs/ "Testcontainers Cloud")
* [Deprecated products and features](https://docs.docker.com/retired/ "Deprecated products and features")
* [Release lifecycle](https://docs.docker.com/release-lifecycle/ "Release lifecycle")

* Platform
* [Support](https://docs.docker.com/support/)
* [Billing](https://docs.docker.com/billing/)

  + [Add or update a payment method](https://docs.docker.com/billing/payment-method/ "Add or update a payment method")
  + [Manage your billing information](https://docs.docker.com/billing/details/ "Manage your billing information")
  + [3D Secure authentication](https://docs.docker.com/billing/3d-secure/ "3D Secure authentication")
  + [Invoices and billing history](https://docs.docker.com/billing/history/ "Invoices and billing history")
  + [Change your billing cycle](https://docs.docker.com/billing/cycle/ "Change your billing cycle")
  + [Submit a tax exemption certificate](https://docs.docker.com/billing/tax-certificate/ "Submit a tax exemption certificate")
  + [FAQs](https://docs.docker.com/billing/faqs/ "FAQs")
* [Docker accounts](https://docs.docker.com/accounts/)

  + [Accounts](https://docs.docker.com/accounts/general-faqs/ "Accounts")
  + [Create an account](https://docs.docker.com/accounts/create-account/ "Create an account")
  + [Manage an account](https://docs.docker.com/accounts/manage-account/ "Manage an account")
  + [Deactivate an account](https://docs.docker.com/accounts/deactivate-user-account/ "Deactivate an account")
* [Security](https://docs.docker.com/security/)

  + [Personal access tokens](https://docs.docker.com/security/access-tokens/ "Personal access tokens")
  + [Two-factor authentication](https://docs.docker.com/security/2fa/)

    - [Recover your Docker account](https://docs.docker.com/security/2fa/recover-hub-account/ "Recover your Docker account")
  + FAQs

    - [General](https://docs.docker.com/security/faqs/general/ "General")
    - [Container](https://docs.docker.com/security/faqs/containers/ "Container")
    - [Network and VM](https://docs.docker.com/security/faqs/networking-and-vms/ "Network and VM")
  + [Security announcements](https://docs.docker.com/security/security-announcements/ "Security announcements")
* [Subscription](https://docs.docker.com/subscription/)

  + [Compare subscription](https://www.docker.com/pricing?ref=Docs&refAction=DocsSubscriptionDetails "Compare subscription")
  + [Set up your subscription](https://docs.docker.com/subscription/setup/ "Set up your subscription")
  + [Scale your subscription](https://docs.docker.com/subscription/scale/ "Scale your subscription")
  + [Manage seats](https://docs.docker.com/subscription/manage-seats/ "Manage seats")
  + [Change your subscription](https://docs.docker.com/subscription/change/ "Change your subscription")
  + [Docker Desktop license agreement](https://docs.docker.com/subscription/desktop-license/ "Docker Desktop license agreement")
  + [FAQs](https://docs.docker.com/subscription/faq/ "FAQs")
* [Release notes](https://docs.docker.com/platform-release-notes/ "Release notes")

* Enterprise
* [Administration](https://docs.docker.com/admin/)

  + [Organization administration](https://docs.docker.com/admin/organization/)

    - [Create your organization](https://docs.docker.com/admin/organization/orgs/ "Create your organization")
    - [Onboard your organization](https://docs.docker.com/admin/organization/onboard/ "Onboard your organization")
    - [Manage organization members](https://docs.docker.com/admin/organization/members/ "Manage organization members")
    - [Convert an account into an organization](https://docs.docker.com/admin/organization/convert-account/ "Convert an account into an organization")
    - [Create and manage a team](https://docs.docker.com/admin/organization/manage-a-team/ "Create and manage a team")
    - [Deactivate an organization](https://docs.docker.com/admin/organization/deactivate-account/ "Deactivate an organization")
    - [Manage Docker products](https://docs.docker.com/admin/organization/manage-products/ "Manage Docker products")
    - [Activity logs](https://docs.docker.com/admin/organization/activity-logs/ "Activity logs")
    - [Organization information](https://docs.docker.com/admin/organization/general-settings/ "Organization information")
    - [Insights](https://docs.docker.com/admin/organization/insights/ "Insights")
  + [Company administration overview](https://docs.docker.com/admin/company/)

    - [Create a company](https://docs.docker.com/admin/company/new-company/ "Create a company")
    - [Manage company members](https://docs.docker.com/admin/company/users/ "Manage company members")
    - [Manage company organizations](https://docs.docker.com/admin/company/organizations/ "Manage company organizations")
    - [Manage company owners](https://docs.docker.com/admin/company/owners/ "Manage company owners")
  + FAQ

    - [Organization](https://docs.docker.com/admin/faqs/organization-faqs/ "Organization")
    - [Company](https://docs.docker.com/admin/faqs/company-faqs/ "Company")
* [Deploy Docker Desktop](https://docs.docker.com/enterprise/enterprise-deployment/)

  + [MSI installer](https://docs.docker.com/enterprise/enterprise-deployment/msi-install-and-configure/ "MSI installer")
  + [PKG installer](https://docs.docker.com/enterprise/enterprise-deployment/pkg-install-and-configure/ "PKG installer")
  + [MS Store](https://docs.docker.com/enterprise/enterprise-deployment/ms-store/ "MS Store")
  + [Deploy with Intune](https://docs.docker.com/enterprise/enterprise-deployment/use-intune/ "Deploy with Intune")
  + [Deploy with Jamf Pro](https://docs.docker.com/enterprise/enterprise-deployment/use-jamf-pro/ "Deploy with Jamf Pro")
  + [Microsoft Dev Box](https://docs.docker.com/enterprise/enterprise-deployment/dev-box/ "Microsoft Dev Box")
  + [FAQs](https://docs.docker.com/enterprise/enterprise-deployment/faq/ "FAQs")
* [Security](https://docs.docker.com/enterprise/security/)

  + [Single sign-on](https://docs.docker.com/enterprise/security/single-sign-on/)

    - [Set up](https://docs.docker.com/enterprise/security/single-sign-on/connect/ "Set up")
    - [Manage connections](https://docs.docker.com/enterprise/security/single-sign-on/manage/ "Manage connections")
    - FAQs

      * [General](https://docs.docker.com/enterprise/security/single-sign-on/faqs/general/ "General")
      * [Domains](https://docs.docker.com/enterprise/security/single-sign-on/faqs/domain-faqs/ "Domains")
      * [Enforcement](https://docs.docker.com/enterprise/security/single-sign-on/faqs/enforcement-faqs/ "Enforcement")
      * [Identity providers](https://docs.docker.com/enterprise/security/single-sign-on/faqs/idp-faqs/ "Identity providers")
      * [User management](https://docs.docker.com/enterprise/security/single-sign-on/faqs/users-faqs/ "User management")
  + [Provision](https://docs.docker.com/enterprise/security/provisioning/)

    - [Just-in-Time](https://docs.docker.com/enterprise/security/provisioning/just-in-time/ "Just-in-Time")
    - [SCIM](https://docs.docker.com/enterprise/security/provisioning/scim/ "SCIM")
    - [Group mapping](https://docs.docker.com/enterprise/security/provisioning/group-mapping/ "Group mapping")
  + [Enforce sign-in](https://docs.docker.com/enterprise/security/enforce-sign-in/)

    - [Configure](https://docs.docker.com/enterprise/security/enforce-sign-in/methods/ "Configure")
  + [Roles and permissions](https://docs.docker.com/enterprise/security/roles-and-permissions/)

    - [Core roles](https://docs.docker.com/enterprise/security/roles-and-permissions/core-roles/ "Core roles")
    - [Custom roles](https://docs.docker.com/enterprise/security/roles-and-permissions/custom-roles/ "Custom roles")
  + [Manage domains](https://docs.docker.com/enterprise/security/domain-management/ "Manage domains")
  + [Hardened Docker Desktop](https://docs.docker.com/enterprise/security/hardened-desktop/)

    - [Enhanced Container Isolation](https://docs.docker.com/enterprise/security/hardened-desktop/enhanced-container-isolation/)

      * [Enable ECI](https://docs.docker.com/enterprise/security/hardened-desktop/enhanced-container-isolation/enable-eci/ "Enable ECI")
      * [Configure advanced settings](https://docs.docker.com/enterprise/security/hardened-desktop/enhanced-container-isolation/config/ "Configure advanced settings")
      * [Limitations](https://docs.docker.com/enterprise/security/hardened-desktop/enhanced-container-isolation/limitations/ "Limitations")
      * [FAQs](https://docs.docker.com/enterprise/security/hardened-desktop/enhanced-container-isolation/faq/ "FAQs")
    - [Settings Management](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/)

      * [Use a JSON file](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/configure-json-file/ "Use a JSON file")
      * [Use the Admin Console](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/configure-admin-console/ "Use the Admin Console")
      * [Desktop settings reporting](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/compliance-reporting/ "Desktop settings reporting")
      * [Settings reference](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/settings-reference/ "Settings reference")
    - [Air-gapped containers](https://docs.docker.com/enterprise/security/hardened-desktop/air-gapped-containers/ "Air-gapped containers")
    - [Registry Access Management](https://docs.docker.com/enterprise/security/hardened-desktop/registry-access-management/ "Registry Access Management")
    - [Image Access Management](https://docs.docker.com/enterprise/security/hardened-desktop/image-access-management/ "Image Access Management")
    - [Namespace access](https://docs.docker.com/enterprise/security/hardened-desktop/namespace-access/ "Namespace access")
  + [Organization access tokens](https://docs.docker.com/enterprise/security/access-tokens/ "Organization access tokens")
* Troubleshoot

  + [Troubleshoot provisioning](https://docs.docker.com/enterprise/troubleshoot/troubleshoot-provisioning/ "Troubleshoot provisioning")
  + [Troubleshoot SSO](https://docs.docker.com/enterprise/troubleshoot/troubleshoot-sso/ "Troubleshoot SSO")

[Home](https://docs.docker.com/)
/
[Manuals](https://docs.docker.com/manuals/)
/
[Docker Compose](https://docs.docker.com/compose/)
/
Quickstart

# Docker Compose Quickstart

Copy as Markdown

Open Markdown

Ask Docs AI

Claude
Open in Claude

function getCurrentPlaintextUrl(){const e=window.location.href.split("#")[0].replace(/\/$/,"");return`${e}.md`}function copyMarkdown(){fetch(getCurrentPlaintextUrl()).then(e=>e.text()).then(e=>{navigator.clipboard.writeText(e).then(()=>{const e=document.querySelector('[data-heap-id="copy-markdown-button"]');if(!e)return;const t=e.querySelectorAll(".icon-svg"),n=t[0],s=t[1];n.classList.add("hidden"),s.classList.remove("hidden"),setTimeout(()=>{n.classList.remove("hidden"),s.classList.add("hidden")},2e3)})}).catch(e=>{console.error("Error copying markdown:",e)})}function viewPlainText(){window.open(getCurrentPlaintextUrl(),"\_blank")}function openInDocsAI(){const e=document.querySelector(".open-kapa-widget");e?e.click():alert("Couldn't find Docs AI.")}function openInClaude(){const e=getCurrentPlaintextUrl(),t=`Read ${e} so I can ask questions about it.`,n=encodeURIComponent(t),s=`https://claude.ai/new?q=${n}`;window.open(s,"\_blank")}

Table of contents

* [Prerequisites](#prerequisites)
* [Step 1: Set up the project](#step-1-set-up-the-project)
* [Step 2: Define and start your services](#step-2-define-and-start-your-services)
* [Step 3: Fix the startup race with health checks](#step-3-fix-the-startup-race-with-health-checks)
* [Step 4: Enable Compose Watch for live updates](#step-4-enable-compose-watch-for-live-updates)
* [Step 5: Persist data with named volumes](#step-5-persist-data-with-named-volumes)
* [Step 6: Structure your project with multiple Compose files](#step-6-structure-your-project-with-multiple-compose-files)
* [Step 7: Inspect and debug your running stack](#step-7-inspect-and-debug-your-running-stack)

+ [Stream logs from all services](#stream-logs-from-all-services)
+ [Run commands inside a running container](#run-commands-inside-a-running-container)

* [Where to go next](#where-to-go-next)

---

This tutorial aims to introduce fundamental concepts of Docker Compose by guiding you through the development of a basic Python web application.

Using the Flask framework, the application features a hit counter in Redis, providing a practical example of how Docker Compose can be applied in web development scenarios. The concepts demonstrated here should be understandable even if you're not familiar with Python.

## [Prerequisites](#prerequisites)

Make sure you have:

* [Installed the latest version of Docker Compose](https://docs.docker.com/compose/install/)
* A basic understanding of Docker concepts and how Docker works

## [Step 1: Set up the project](#step-1-set-up-the-project)

1. Create a directory for the project:

   ```
   $ mkdir compose-demo
   $ cd compose-demo
   ```
2. Create `app.py` in your project directory and add the following:

   ```
   import os
   import redis
   from flask import Flask

   app = Flask(__name__)
   cache = redis.Redis(
       host=os.getenv("REDIS_HOST", "redis"),
       port=int(os.getenv("REDIS_PORT", "6379")),
   )

   @app.route("/")
   def hello():
       count = cache.incr("hits")
       return f"Hello from Docker! I have been seen {count} time(s).\n"
   ```

   The app reads its Redis connection details from environment variables, with sensible defaults so it works out of the box.
3. Create `requirements.txt` in your project directory and add the following:

   ```
   flask
   redis
   ```
4. Create a `Dockerfile`:

   ```
   # syntax=docker/dockerfile:1
   FROM python:3.12-alpine  # Builds an image with the Python 3.12 image
   WORKDIR /code  # Sets the working directory to `/code`
   ENV FLASK_APP=app.py  # Sets environment variables used by the `flask` command
   ENV FLASK_RUN_HOST=0.0.0.0
   RUN apk add --no-cache gcc musl-dev linux-headers  # Installs `gcc` and other dependencies
   COPY requirements.txt .  # Copies `requirements.txt`
   RUN pip install -r requirements.txt  # Installs the Python dependencies
   COPY . .  # Copies the current directory `.` in the project to the workdir `.` in the image
   EXPOSE 5000
   CMD ["flask", "run", "--debug"]  # Sets the default command for the container to `flask run --debug`
   ```

   > Important
   >
   > Make sure the file is named `Dockerfile` with no extension. Some editors add `.txt`
   > automatically, which causes the build to fail.

   For more information on how to write Dockerfiles, see the
   [Dockerfile reference](/reference/dockerfile/).
5. Create a `.env` file to hold configuration values:

   ```
   APP_PORT=8000
   REDIS_HOST=redis
   REDIS_PORT=6379
   ```

   Compose automatically reads `.env` and makes these values available for interpolation
   in your `compose.yaml`. For this example the gains are modest, but in practice,
   keeping configuration out of the Compose file makes it easier to:

   * Change values across environments without editing YAML
   * Avoid committing secrets to version control
   * Reuse values across multiple services
6. Create a `.dockerignore` file to keep unnecessary files out of your build context:

   ```
   .env
   *.pyc
   __pycache__
   redis-data
   ```

   Docker sends everything in your project directory to the daemon when it builds an image.
   Without `.dockerignore`, that includes your `.env` file (which may contain secrets) and
   any cached Python bytecode. Excluding them keeps builds fast and avoids accidentally
   baking sensitive values into an image layer.

## [Step 2: Define and start your services](#step-2-define-and-start-your-services)

Compose simplifies the control of your entire application stack, making it easy to manage services, networks, and volumes in a single YAML configuration file.

1. Create `compose.yaml` in your project directory and paste the following:

   ```
   services:
     web:
       build: .
       ports:
         - "${APP_PORT}:5000"
       environment:
         - REDIS_HOST=${REDIS_HOST}
         - REDIS_PORT=${REDIS_PORT}

     redis:
       image: redis:alpine
   ```

   This Compose file defines two services:

   * The `web` service uses an image that's built from the `Dockerfile` in the current directory. It maps port `8000` on the host to port `5000` on the container where Flask listens by default.
   * The `redis` service uses a public [Redis](https://registry.hub.docker.com/_/redis/) image pulled from the Docker Hub registry.

   For more information on the `compose.yaml` file, see [How Compose works](https://docs.docker.com/compose/intro/compose-application-model/).
2. Start up your application:

   ```
   $ docker compose up
   ```

   With a single command, you create and start all the services from your configuration file. Compose builds your web image, pulls the Redis image, and starts both containers.
3. Open `http://localhost:8000`. You should see:

   ```
   Hello from Docker! I have been seen 1 time(s).
   ```

   Refresh the page — the counter increments on each visit.

   This minimal setup works, but it has two problems you'll fix in the next steps:

   * Startup race: `web` starts at the same time as `redis`. If Redis isn't ready yet,
     the Flask app fails to connect and crashes.
   * No persistence: If you run `docker compose down` followed by `docker compose up`, the
     counter resets to zero. `docker compose down` removes the containers, and with them
     any data written to the container's writable layer. `docker compose stop` preserves
     the containers so data survives, but you can't rely on that in production where
     containers are regularly replaced.
4. Stop the stack before moving on:

   ```
   $ docker compose down
   ```

## [Step 3: Fix the startup race with health checks](#step-3-fix-the-startup-race-with-health-checks)

To fix the startup race, Compose needs to wait until `redis` is confirmed healthy before
starting `web`.

1. Update `compose.yaml`:

   ```
   services:
     web:
       build: .
       ports:
         - "${APP_PORT}:5000"
       environment:
         - REDIS_HOST=${REDIS_HOST}
         - REDIS_PORT=${REDIS_PORT}
       depends_on:
         redis:
           condition: service_healthy

     redis:
       image: redis:alpine
       healthcheck:
         test: ["CMD", "redis-cli", "ping"]
         interval: 5s
         timeout: 3s
         retries: 5
         start_period: 10s
   ```

   The `healthcheck` block tells Compose how to test whether Redis is ready:

   * `test` is the command Compose runs inside the container to check its health.
     `redis-cli ping` connects to Redis and expects a `PONG` response — if it gets one,
     the container is healthy.
   * `start_period` gives Redis 10 seconds to initialize before health checks begin.
     Any failures during this window don't count toward the retry limit.
   * `interval` runs the check every 5 seconds after the start period has elapsed.
   * `timeout` gives each check 3 seconds to respond before treating it as a failure.
   * `retries` sets how many consecutive failures are allowed before Compose marks the
     container as unhealthy. With `interval: 5s` and `retries: 5`, Compose will wait up
     to 25 seconds before giving up.
2. Start the stack to confirm the ordering is fixed:

   ```
   $ docker compose up
   ```

   You should see something similar to:

   ```
   [+] Running 2/2
   ✔ Container compose-demo-redis-1  Healthy                       0.0s
   ```
3. Open `http://localhost:8000` to confirm the app is still working, then stop the stack before moving on:

   ```
   $ docker compose down
   ```

## [Step 4: Enable Compose Watch for live updates](#step-4-enable-compose-watch-for-live-updates)

Without Compose Watch, every code change requires you to stop the stack, rebuild the image, and restart the containers. Compose Watch eliminates that cycle by automatically syncing changes into your running container as you save files.

1. Update `compose.yaml` to add the `develop.watch` block to the `web` service:

   ```
   services:
     web:
       build: .
       ports:
         - "${APP_PORT}:5000"
       environment:
         - REDIS_HOST=${REDIS_HOST}
         - REDIS_PORT=${REDIS_PORT}
       depends_on:
         redis:
           condition: service_healthy
       develop:
         watch:
           - action: sync+restart
             path: .
             target: /code
           - action: rebuild
             path: requirements.txt

     redis:
       image: redis:alpine
       healthcheck:
         test: ["CMD", "redis-cli", "ping"]
         interval: 5s
         timeout: 3s
         retries: 5
         start_period: 10s
   ```

   The `watch` block defines two rules:

   * The `sync+restart` action watches your project directory (`.`) on the host. When a file changes, Compose copies any changed files into `/code` inside the running container, then restarts the container. Because the container restarts with the updated files already in place, Flask starts up reading the new code directly — no manual rebuild or restart needed.
   * The `rebuild` action on `requirements.txt` triggers a full image rebuild whenever you add a new dependency, since installing packages requires rebuilding the image, not just syncing files.
2. Start the stack with Watch enabled:

   ```
   $ docker compose up --watch
   ```
3. Make a live change. Open `app.py` and update the greeting:

   ```
   return f"Hello from Compose Watch! I have been seen {count} time(s).\n"
   ```
4. Save the file. Compose Watch detects the change and syncs it immediately:

   ```
   Syncing service "web" after changes were detected
   ```
5. Refresh `http://localhost:8000`. The updated greeting appears without any restart
   and the counter should still be incrementing.
6. Stop the stack before moving on:

   ```
   $ docker compose down
   ```

   For more information on how Compose Watch works, see
   [Use Compose Watch](https://docs.docker.com/compose/how-tos/file-watch/).

## [Step 5: Persist data with named volumes](#step-5-persist-data-with-named-volumes)

Each time you stop and restart the stack the visit counter resets to zero. Redis data
lives inside the container, so it disappears when the container is removed. A named
volume fixes this by storing the data on the host, outside the container lifecycle.

1. Update `compose.yaml`:

   ```
   services:
     web:
       build: .
       ports:
         - "${APP_PORT}:5000"
       environment:
         - REDIS_HOST=${REDIS_HOST}
         - REDIS_PORT=${REDIS_PORT}
       depends_on:
         redis:
           condition: service_healthy
       develop:
         watch:
           - action: sync+restart
             path: .
             target: /code
           - action: rebuild
             path: requirements.txt

     redis:
       image: redis:alpine
       volumes:
         - redis-data:/data
       healthcheck:
         test: ["CMD", "redis-cli", "ping"]
         interval: 5s
         timeout: 3s
         retries: 5
         start_period: 10s

   volumes:
     redis-data:
   ```

   The `redis-data:/data` entry under `redis.volumes` mounts the named volume at `/data`, the path where Redis
   writes its data files. The top-level `volumes` key registers it with Docker so it
   persists between `compose down` and `compose up` cycles.
2. Start the stack with `docker compose up --watch` and refresh `http://localhost:8000` a few times to build up a count.
3. Tear down the stack with `docker compose down` and then bring it back up again with `docker compose up --watch`.
4. Open `http://localhost:8000` — the counter continues from where it left off.
5. Now reset the counter with `docker compose down -v`.

   The `-v` flag removes named volumes along with the containers. Use this intentionally — it permanently deletes the stored data.

## [Step 6: Structure your project with multiple Compose files](#step-6-structure-your-project-with-multiple-compose-files)

As applications grow, a single `compose.yaml` becomes harder to maintain. The `include`
top-level element lets you split services across multiple files while keeping them part of the
same application.

This is especially useful when different teams own different parts of the stack, or when
you want to reuse infrastructure definitions across projects.

1. Create a new file in your project directory called `infra.yaml` and move the Redis service and volume into it:

   ```
    services:
     redis:
       image: redis:alpine
       volumes:
         - redis-data:/data
       healthcheck:
         test: ["CMD", "redis-cli", "ping"]
         interval: 5s
         timeout: 3s
         retries: 5
         start_period: 10s

   volumes:
     redis-data:
   ```
2. Update `compose.yaml` to include `infra.yaml`:

   ```
   include:
      - path: ./infra.yaml
   services:
     web:
       build: .
       ports:
         - "${APP_PORT}:5000"
       environment:
         - REDIS_HOST=${REDIS_HOST}
         - REDIS_PORT=${REDIS_PORT}
       depends_on:
         redis:
           condition: service_healthy
       develop:
         watch:
           - action: sync+restart
             path: .
             target: /code
           - action: rebuild
             path: requirements.txt
   ```
3. Run the application to confirm everything still works:

   ```
   $ docker compose up --watch
   ```

   Compose merges both files at startup. The `web` service can still reference `redis`
   by name because all included services share the same default network.

   This is a simplified example, but it demonstrates the basic principle of `include` and how it can make it easier to modularize complex applications into sub-Compose files. For more information on `include` and working with multiple Compose files, see
   [Working with multiple Compose files](https://docs.docker.com/compose/how-tos/multiple-compose-files/).
4. Stop the stack before moving on:

   ```
   $ docker compose down
   ```

## [Step 7: Inspect and debug your running stack](#step-7-inspect-and-debug-your-running-stack)

With a fully configured stack, you can observe what's happening inside your containers
without stopping anything. This step covers the core commands for inspecting the resolved configuration, streaming logs, and running commands
inside a running container.

Before starting the stack, verify that Compose has resolved your `.env` variables and
merged all files correctly:

```
$ docker compose config
```

`docker compose config` doesn't require the stack to be running — it works purely from
your files. A few things worth noting in the output:

* `${APP_PORT}`, `${REDIS_HOST}`, and `${REDIS_PORT}` have all been replaced with the
  values from your `.env` file.
* Short-form port notation (`"8000:5000"`) is expanded into its canonical fields
  (`target`, `published`, `protocol`).
* The default network and volume names are made explicit, prefixed with the project name
  `compose-demo`.
* The output is the fully resolved configuration, with any files
  brought in via `include` merged into a single view.

Use `docker compose config` any time you want to confirm what Compose will actually
apply, especially when debugging variable substitution or working with multiple Compose files.

Now start the stack in detached mode so the terminal stays free for the commands that
follow:

```
$ docker compose up -d
```

### [Stream logs from all services](#stream-logs-from-all-services)

```
$ docker compose logs -f
```

The `-f` flag follows the log stream in real time, interleaving output from both
containers with color-coded service name prefixes. Refresh `http://localhost:8000` a
few times and watch the Flask request logs appear. To follow logs for a single service,
pass its name:

```
$ docker compose logs -f web
```

Press `Ctrl+C` to stop following logs. The containers keep running.

### [Run commands inside a running container](#run-commands-inside-a-running-container)

`docker compose exec` runs a command inside an already-running container without
starting a new one. This is the primary tool for live debugging.

#### [Verify environment variables are set correctly](#verify-environment-variables-are-set-correctly)

```
$ docker compose exec web env | grep REDIS
```

```
REDIS_HOST=redis
REDIS_PORT=6379
```

#### [Test that the `web` container can reach Redis using the service name as the hostname](#test-that-the-web-container-can-reach-redis-using-the-service-name-as-the-hostname)

```
$ docker compose exec web python -c "import redis; r = redis.Redis(host='redis'); print(r.ping())"
```

```
True
```

This uses the same `redis` library your app uses, so a `True` response confirms that
service discovery, networking, and the Redis connection are all working end to end.

#### [Inspect the live value of the hit counter in Redis](#inspect-the-live-value-of-the-hit-counter-in-redis)

```
$ docker compose exec redis redis-cli GET hits
```

## [Where to go next](#where-to-go-next)

* [Explore the full list of Compose commands](/reference/cli/docker/compose/)
* [Explore the Compose file reference](https://docs.docker.com/reference/compose-file/)
* [Check out the Learning Docker Compose video on LinkedIn Learning](https://www.linkedin.com/learning/learning-docker-compose/)
* [Learn how to set environment variables in Compose](/compose/how-tos/environment-variables/set-environment-variables/)
* [Learn how to package and distribute your Compose app](/compose/how-tos/oci-artifact/)

[Edit this page](https://github.com/docker/docs/edit/main/content/manuals/compose/gettingstarted.md)

[Request changes](https://github.com/docker/docs/issues/new?template=doc_issue.yml&location=https%3a%2f%2fdocs.docker.com%2fcompose%2fgettingstarted%2f&labels=status%2Ftriage)

Table of contents

* [Prerequisites](#prerequisites)
* [Step 1: Set up the project](#step-1-set-up-the-project)
* [Step 2: Define and start your services](#step-2-define-and-start-your-services)
* [Step 3: Fix the startup race with health checks](#step-3-fix-the-startup-race-with-health-checks)
* [Step 4: Enable Compose Watch for live updates](#step-4-enable-compose-watch-for-live-updates)
* [Step 5: Persist data with named volumes](#step-5-persist-data-with-named-volumes)
* [Step 6: Structure your project with multiple Compose files](#step-6-structure-your-project-with-multiple-compose-files)
* [Step 7: Inspect and debug your running stack](#step-7-inspect-and-debug-your-running-stack)

+ [Stream logs from all services](#stream-logs-from-all-services)
+ [Run commands inside a running container](#run-commands-inside-a-running-container)

* [Where to go next](#where-to-go-next)

[Product offerings](https://www.docker.com/)
[Pricing](https://www.docker.com/pricing?ref=Docs&refAction=DocsFooter)
[About us](https://www.docker.com/company/)
[llms.txt](/llms.txt)

Cookies Settings
|
[Terms of Service](https://www.docker.com/legal/docker-terms-service "Docker Terms of Service")
|
[Status](https://www.dockerstatus.com/ "Docker Systems Status Page")
|
[Legal](https://www.docker.com/legal "Docker Legal Terms")

Copyright © 2013-2026 Docker Inc. All rights
reserved.