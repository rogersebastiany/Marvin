What is Docker? | Docker Docs{"@context":"https://schema.org","@type":"TechArticle","articleSection":"get-started","author":{"@type":"Organization","name":"Docker Inc","url":"https://www.docker.com"},"dateModified":"2026-02-11T15:40:49+05:30","description":"Get an in-depth overview of the Docker platform including what it can be used for, the architecture it employs, and its underlying technology.","headline":"What is Docker?","inLanguage":"en","isPartOf":{"@id":"https://docs.docker.com/get-started/","@type":"WebPage","name":"Get started"},"keywords":["what","is","a","docker","docker","daemon","why","use","docker","docker","architecture","what","to","use","docker","for","docker","client","what","is","docker","for","why","docker","uses","for","docker","what","is","docker","container","used","for","what","are","docker","containers","used","for"],"mainEntityOfPage":{"@id":"https://docs.docker.com/get-started/docker-overview/","@type":"WebPage"},"publisher":{"@type":"Organization","logo":{"@type":"ImageObject","url":"https://docs.docker.com/assets/images/docker-logo.png"},"name":"Docker Inc","url":"https://www.docker.com"},"url":"https://docs.docker.com/get-started/docker-overview/"}{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","item":{"@id":"https://docs.docker.com/get-started/","name":"Get started"},"position":1},{"@type":"ListItem","item":{"@id":"https://docs.docker.com/get-started/docker-overview/","name":"What is Docker?"},"position":2}]}

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

[Get started](https://docs.docker.com/get-started/)

* [Guides](/guides/)
* [Manuals](/manuals/)
* [Reference](/reference/)

* [Get Docker](https://docs.docker.com/get-started/get-docker/ "Get Docker")
* [What is Docker?](https://docs.docker.com/get-started/docker-overview/ "What is Docker?")
* [Introduction](https://docs.docker.com/get-started/introduction/)

  + [Get Docker Desktop](https://docs.docker.com/get-started/introduction/get-docker-desktop/ "Get Docker Desktop")
  + [Develop with containers](https://docs.docker.com/get-started/introduction/develop-with-containers/ "Develop with containers")
  + [Build and push your first image](https://docs.docker.com/get-started/introduction/build-and-push-first-image/ "Build and push your first image")
  + [What's next](https://docs.docker.com/get-started/introduction/whats-next/ "What's next")
* Docker concepts

  + The basics

    - [What is a container?](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/ "What is a container?")
    - [What is an image?](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-an-image/ "What is an image?")
    - [What is a registry?](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-registry/ "What is a registry?")
    - [What is Docker Compose?](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-docker-compose/ "What is Docker Compose?")
  + [Building images](https://docs.docker.com/get-started/docker-concepts/building-images/)

    - [Understanding the image layers](https://docs.docker.com/get-started/docker-concepts/building-images/understanding-image-layers/ "Understanding the image layers")
    - [Writing a Dockerfile](https://docs.docker.com/get-started/docker-concepts/building-images/writing-a-dockerfile/ "Writing a Dockerfile")
    - [Build, tag, and publish an image](https://docs.docker.com/get-started/docker-concepts/building-images/build-tag-and-publish-an-image/ "Build, tag, and publish an image")
    - [Using the build cache](https://docs.docker.com/get-started/docker-concepts/building-images/using-the-build-cache/ "Using the build cache")
    - [Multi-stage builds](https://docs.docker.com/get-started/docker-concepts/building-images/multi-stage-builds/ "Multi-stage builds")
  + Running containers

    - [Publishing and exposing ports](https://docs.docker.com/get-started/docker-concepts/running-containers/publishing-ports/ "Publishing and exposing ports")
    - [Overriding container defaults](https://docs.docker.com/get-started/docker-concepts/running-containers/overriding-container-defaults/ "Overriding container defaults")
    - [Persisting container data](https://docs.docker.com/get-started/docker-concepts/running-containers/persisting-container-data/ "Persisting container data")
    - [Sharing local files with containers](https://docs.docker.com/get-started/docker-concepts/running-containers/sharing-local-files/ "Sharing local files with containers")
    - [Multi-container applications](https://docs.docker.com/get-started/docker-concepts/running-containers/multi-container-applications/ "Multi-container applications")
* [Docker workshop](https://docs.docker.com/get-started/workshop/)

  + [Part 1: Containerize an application](https://docs.docker.com/get-started/workshop/02_our_app/ "Part 1: Containerize an application")
  + [Part 2: Update the application](https://docs.docker.com/get-started/workshop/03_updating_app/ "Part 2: Update the application")
  + [Part 3: Share the application](https://docs.docker.com/get-started/workshop/04_sharing_app/ "Part 3: Share the application")
  + [Part 4: Persist the DB](https://docs.docker.com/get-started/workshop/05_persisting_data/ "Part 4: Persist the DB")
  + [Part 5: Use bind mounts](https://docs.docker.com/get-started/workshop/06_bind_mounts/ "Part 5: Use bind mounts")
  + [Part 6: Multi-container apps](https://docs.docker.com/get-started/workshop/07_multi_container/ "Part 6: Multi-container apps")
  + [Part 7: Use Docker Compose](https://docs.docker.com/get-started/workshop/08_using_compose/ "Part 7: Use Docker Compose")
  + [Part 8: Image-building best practices](https://docs.docker.com/get-started/workshop/09_image_best/ "Part 8: Image-building best practices")
  + [Part 9: What next](https://docs.docker.com/get-started/workshop/10_what_next/ "Part 9: What next")
* [Educational resources](https://docs.docker.com/get-started/resources/ "Educational resources")

[Home](https://docs.docker.com/)
/
[Get started](https://docs.docker.com/get-started/)
/
What is Docker?

# What is Docker?

Copy as Markdown

Open Markdown

Ask Docs AI

Claude
Open in Claude

function getCurrentPlaintextUrl(){const e=window.location.href.split("#")[0].replace(/\/$/,"");return`${e}.md`}function copyMarkdown(){fetch(getCurrentPlaintextUrl()).then(e=>e.text()).then(e=>{navigator.clipboard.writeText(e).then(()=>{const e=document.querySelector('[data-heap-id="copy-markdown-button"]');if(!e)return;const t=e.querySelectorAll(".icon-svg"),n=t[0],s=t[1];n.classList.add("hidden"),s.classList.remove("hidden"),setTimeout(()=>{n.classList.remove("hidden"),s.classList.add("hidden")},2e3)})}).catch(e=>{console.error("Error copying markdown:",e)})}function viewPlainText(){window.open(getCurrentPlaintextUrl(),"\_blank")}function openInDocsAI(){const e=document.querySelector(".open-kapa-widget");e?e.click():alert("Couldn't find Docs AI.")}function openInClaude(){const e=getCurrentPlaintextUrl(),t=`Read ${e} so I can ask questions about it.`,n=encodeURIComponent(t),s=`https://claude.ai/new?q=${n}`;window.open(s,"\_blank")}

Table of contents

* [The Docker platform](#the-docker-platform)
* [What can I use Docker for?](#what-can-i-use-docker-for)

+ [Fast, consistent delivery of your applications](#fast-consistent-delivery-of-your-applications)
+ [Responsive deployment and scaling](#responsive-deployment-and-scaling)
+ [Running more workloads on the same hardware](#running-more-workloads-on-the-same-hardware)

* [Docker architecture](#docker-architecture)

+ [The Docker daemon](#the-docker-daemon)
+ [The Docker client](#the-docker-client)
+ [Docker Desktop](#docker-desktop)
+ [Docker registries](#docker-registries)
+ [Docker objects](#docker-objects)

* [The underlying technology](#the-underlying-technology)
* [Next steps](#next-steps)

---

Docker is an open platform for developing, shipping, and running applications.
Docker enables you to separate your applications from your infrastructure so
you can deliver software quickly. With Docker, you can manage your infrastructure
in the same ways you manage your applications. By taking advantage of Docker's
methodologies for shipping, testing, and deploying code, you can
significantly reduce the delay between writing code and running it in production.

## [The Docker platform](#the-docker-platform)

Docker provides the ability to package and run an application in a loosely isolated
environment called a container. The isolation and security let you run many
containers simultaneously on a given host. Containers are lightweight and contain
everything needed to run the application, so you don't need to rely on what's
installed on the host. You can share containers while you work,
and be sure that everyone you share with gets the same container that works in the
same way.

Docker provides tooling and a platform to manage the lifecycle of your containers:

* Develop your application and its supporting components using containers.
* The container becomes the unit for distributing and testing your application.
* When you're ready, deploy your application into your production environment,
  as a container or an orchestrated service. This works the same whether your
  production environment is a local data center, a cloud provider, or a hybrid
  of the two.

## [What can I use Docker for?](#what-can-i-use-docker-for)

### [Fast, consistent delivery of your applications](#fast-consistent-delivery-of-your-applications)

Docker streamlines the development lifecycle by allowing developers to work in
standardized environments using local containers which provide your applications
and services. Containers are great for continuous integration and continuous
delivery (CI/CD) workflows.

Consider the following example scenario:

* Your developers write code locally and share their work with their colleagues
  using Docker containers.
* They use Docker to push their applications into a test environment and run
  automated and manual tests.
* When developers find bugs, they can fix them in the development environment
  and redeploy them to the test environment for testing and validation.
* When testing is complete, getting the fix to the customer is as simple as
  pushing the updated image to the production environment.

### [Responsive deployment and scaling](#responsive-deployment-and-scaling)

Docker's container-based platform allows for highly portable workloads. Docker
containers can run on a developer's local laptop, on physical or virtual
machines in a data center, on cloud providers, or in a mixture of environments.

Docker's portability and lightweight nature also make it easy to dynamically
manage workloads, scaling up or tearing down applications and services as
business needs dictate, in near real time.

### [Running more workloads on the same hardware](#running-more-workloads-on-the-same-hardware)

Docker is lightweight and fast. It provides a viable, cost-effective alternative
to hypervisor-based virtual machines, so you can use more of your server
capacity to achieve your business goals. Docker is perfect for high density
environments and for small and medium deployments where you need to do more with
fewer resources.

## [Docker architecture](#docker-architecture)

Docker uses a client-server architecture. The Docker client talks to the
Docker daemon, which does the heavy lifting of building, running, and
distributing your Docker containers. The Docker client and daemon can
run on the same system, or you can connect a Docker client to a remote Docker
daemon. The Docker client and daemon communicate using a REST API, over UNIX
sockets or a network interface. Another Docker client is Docker Compose,
that lets you work with applications consisting of a set of containers.

### [The Docker daemon](#the-docker-daemon)

The Docker daemon (`dockerd`) listens for Docker API requests and manages Docker
objects such as images, containers, networks, and volumes. A daemon can also
communicate with other daemons to manage Docker services.

### [The Docker client](#the-docker-client)

The Docker client (`docker`) is the primary way that many Docker users interact
with Docker. When you use commands such as `docker run`, the client sends these
commands to `dockerd`, which carries them out. The `docker` command uses the
Docker API. The Docker client can communicate with more than one daemon.

### [Docker Desktop](#docker-desktop)

Docker Desktop is an easy-to-install application for your Mac, Windows, or Linux environment that enables you to build and share containerized applications and microservices. Docker Desktop includes the Docker daemon (`dockerd`), the Docker client (`docker`), Docker Compose, Docker Content Trust, Kubernetes, and Credential Helper. For more information, see
[Docker Desktop](https://docs.docker.com/desktop/).

### [Docker registries](#docker-registries)

A Docker registry stores Docker images. Docker Hub is a public
registry that anyone can use, and Docker looks for images on
Docker Hub by default. You can even run your own private registry.

When you use the `docker pull` or `docker run` commands, Docker pulls the required images from your configured registry. When you use the `docker push` command, Docker pushes
your image to your configured registry.

### [Docker objects](#docker-objects)

When you use Docker, you are creating and using images, containers, networks,
volumes, plugins, and other objects. This section is a brief overview of some
of those objects.

#### [Images](#images)

An image is a read-only template with instructions for creating a Docker
container. Often, an image is based on another image, with some additional
customization. For example, you may build an image that is based on the Ubuntu image
but includes the Apache web server and your application, as well as the
configuration details needed to make your application run.

You might create your own images or you might only use those created by others
and published in a registry. To build your own image, you create a Dockerfile
with a simple syntax for defining the steps needed to create the image and run
it. Each instruction in a Dockerfile creates a layer in the image. When you
change the Dockerfile and rebuild the image, only those layers which have
changed are rebuilt. This is part of what makes images so lightweight, small,
and fast, when compared to other virtualization technologies.

#### [Containers](#containers)

A container is a runnable instance of an image. You can create, start, stop,
move, or delete a container using the Docker API or CLI. You can connect a
container to one or more networks, attach storage to it, or even create a new
image based on its current state.

By default, a container is relatively well isolated from other containers and
its host machine. You can control how isolated a container's network, storage,
or other underlying subsystems are from other containers or from the host
machine.

A container is defined by its image as well as any configuration options you
provide to it when you create or start it. When a container is removed, any changes to
its state that aren't stored in persistent storage disappear.

##### [Example `docker run` command](#example-docker-run-command)

The following command runs an `ubuntu` container, attaches interactively to your
local command-line session, and runs `/bin/bash`.

```
$ docker run -i -t ubuntu /bin/bash
```

When you run this command, the following happens (assuming you are using
the default registry configuration):

1. If you don't have the `ubuntu` image locally, Docker pulls it from your
   configured registry, as though you had run `docker pull ubuntu` manually.
2. Docker creates a new container, as though you had run a `docker container create`
   command manually.
3. Docker allocates a read-write filesystem to the container, as its final
   layer. This allows a running container to create or modify files and
   directories in its local filesystem.
4. Docker creates a network interface to connect the container to the default
   network, since you didn't specify any networking options. This includes
   assigning an IP address to the container. By default, containers can
   connect to external networks using the host machine's network connection.
5. Docker starts the container and executes `/bin/bash`. Because the container
   is running interactively and attached to your terminal (due to the `-i` and `-t`
   flags), you can provide input using your keyboard while Docker logs the output to
   your terminal.
6. When you run `exit` to terminate the `/bin/bash` command, the container
   stops but isn't removed. You can start it again or remove it.

## [The underlying technology](#the-underlying-technology)

Docker is written in the [Go programming language](https://golang.org/) and takes
advantage of several features of the Linux kernel to deliver its functionality.
Docker uses a technology called `namespaces` to provide the isolated workspace
called the container. When you run a container, Docker creates a set of
namespaces for that container.

These namespaces provide a layer of isolation. Each aspect of a container runs
in a separate namespace and its access is limited to that namespace.

## [Next steps](#next-steps)

* [Install Docker](https://docs.docker.com/get-started/get-docker/)
* [Get started with Docker](https://docs.docker.com/get-started/introduction/)

[Edit this page](https://github.com/docker/docs/edit/main/content/get-started/docker-overview.md)

[Request changes](https://github.com/docker/docs/issues/new?template=doc_issue.yml&location=https%3a%2f%2fdocs.docker.com%2fget-started%2fdocker-overview%2f&labels=status%2Ftriage)

Table of contents

* [The Docker platform](#the-docker-platform)
* [What can I use Docker for?](#what-can-i-use-docker-for)

+ [Fast, consistent delivery of your applications](#fast-consistent-delivery-of-your-applications)
+ [Responsive deployment and scaling](#responsive-deployment-and-scaling)
+ [Running more workloads on the same hardware](#running-more-workloads-on-the-same-hardware)

* [Docker architecture](#docker-architecture)

+ [The Docker daemon](#the-docker-daemon)
+ [The Docker client](#the-docker-client)
+ [Docker Desktop](#docker-desktop)
+ [Docker registries](#docker-registries)
+ [Docker objects](#docker-objects)

* [The underlying technology](#the-underlying-technology)
* [Next steps](#next-steps)

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