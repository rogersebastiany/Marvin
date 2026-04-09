Dockerfile reference | Docker Docs{"@context":"https://schema.org","@type":"TechArticle","articleSection":"reference","author":{"@type":"Organization","name":"Docker Inc","url":"https://www.docker.com"},"dateModified":"2026-03-31T15:35:07Z","description":"Find all the available commands you can use in a Dockerfile and learn how to use them, including COPY, ARG, ENTRYPOINT, and more.","headline":"Dockerfile reference","inLanguage":"en","isPartOf":{"@id":"https://docs.docker.com/reference/","@type":"WebPage","name":"Reference"},"keywords":["dockerfile","docker file","docker copy","dockerfile exec","docker entrypoint","dockerfile entrypoint","dockerfile arg","docker args","entrypoint","shell dockerfile"],"mainEntityOfPage":{"@id":"https://docs.docker.com/reference/dockerfile/","@type":"WebPage"},"publisher":{"@type":"Organization","logo":{"@type":"ImageObject","url":"https://docs.docker.com/assets/images/docker-logo.png"},"name":"Docker Inc","url":"https://www.docker.com"},"url":"https://docs.docker.com/reference/dockerfile/"}{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","item":{"@id":"https://docs.docker.com/reference/","name":"Reference"},"position":1},{"@type":"ListItem","item":{"@id":"https://docs.docker.com/reference/dockerfile/","name":"Dockerfile reference"},"position":2}]}

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

[Reference](https://docs.docker.com/reference/)

* [Get started](/get-started/)
* [Guides](/guides/)
* [Manuals](/manuals/)

* CLI reference

  + [docker](https://docs.docker.com/reference/cli/docker/)

    - [docker build](/reference/cli/docker/buildx/build/ "docker build")
    - [docker builder](https://docs.docker.com/reference/cli/docker/builder/)

      * [docker builder build](https://docs.docker.com/reference/cli/docker/builder/build/ "docker builder build")
      * [docker builder prune](https://docs.docker.com/reference/cli/docker/builder/prune/ "docker builder prune")
    - [docker buildx](https://docs.docker.com/reference/cli/docker/buildx/)

      * [docker buildx bake](https://docs.docker.com/reference/cli/docker/buildx/bake/ "docker buildx bake")
      * [docker buildx build](https://docs.docker.com/reference/cli/docker/buildx/build/ "docker buildx build")
      * [docker buildx create](https://docs.docker.com/reference/cli/docker/buildx/create/ "docker buildx create")
      * [docker buildx dap](https://docs.docker.com/reference/cli/docker/buildx/dap/)

        + [docker buildx dap build](https://docs.docker.com/reference/cli/docker/buildx/dap/build/ "docker buildx dap build")
      * [docker buildx debug](https://docs.docker.com/reference/cli/docker/buildx/debug/)

        + [docker buildx debug build](https://docs.docker.com/reference/cli/docker/buildx/debug/build/ "docker buildx debug build")
      * [docker buildx dial-stdio](https://docs.docker.com/reference/cli/docker/buildx/dial-stdio/ "docker buildx dial-stdio")
      * [docker buildx du](https://docs.docker.com/reference/cli/docker/buildx/du/ "docker buildx du")
      * [docker buildx history](https://docs.docker.com/reference/cli/docker/buildx/history/)

        + [docker buildx history export](https://docs.docker.com/reference/cli/docker/buildx/history/export/ "docker buildx history export")
        + [docker buildx history import](https://docs.docker.com/reference/cli/docker/buildx/history/import/ "docker buildx history import")
        + [docker buildx history inspect](https://docs.docker.com/reference/cli/docker/buildx/history/inspect/)

          - [docker buildx history inspect attachment](https://docs.docker.com/reference/cli/docker/buildx/history/inspect/attachment/ "docker buildx history inspect attachment")
        + [docker buildx history logs](https://docs.docker.com/reference/cli/docker/buildx/history/logs/ "docker buildx history logs")
        + [docker buildx history ls](https://docs.docker.com/reference/cli/docker/buildx/history/ls/ "docker buildx history ls")
        + [docker buildx history open](https://docs.docker.com/reference/cli/docker/buildx/history/open/ "docker buildx history open")
        + [docker buildx history rm](https://docs.docker.com/reference/cli/docker/buildx/history/rm/ "docker buildx history rm")
        + [docker buildx history trace](https://docs.docker.com/reference/cli/docker/buildx/history/trace/ "docker buildx history trace")
      * [docker buildx imagetools](https://docs.docker.com/reference/cli/docker/buildx/imagetools/)

        + [docker buildx imagetools create](https://docs.docker.com/reference/cli/docker/buildx/imagetools/create/ "docker buildx imagetools create")
        + [docker buildx imagetools inspect](https://docs.docker.com/reference/cli/docker/buildx/imagetools/inspect/ "docker buildx imagetools inspect")
      * [docker buildx inspect](https://docs.docker.com/reference/cli/docker/buildx/inspect/ "docker buildx inspect")
      * [docker buildx ls](https://docs.docker.com/reference/cli/docker/buildx/ls/ "docker buildx ls")
      * [docker buildx policy](https://docs.docker.com/reference/cli/docker/buildx/policy/)

        + [docker buildx policy eval](https://docs.docker.com/reference/cli/docker/buildx/policy/eval/ "docker buildx policy eval")
        + [docker buildx policy test](https://docs.docker.com/reference/cli/docker/buildx/policy/test/ "docker buildx policy test")
      * [docker buildx prune](https://docs.docker.com/reference/cli/docker/buildx/prune/ "docker buildx prune")
      * [docker buildx rm](https://docs.docker.com/reference/cli/docker/buildx/rm/ "docker buildx rm")
      * [docker buildx stop](https://docs.docker.com/reference/cli/docker/buildx/stop/ "docker buildx stop")
      * [docker buildx use](https://docs.docker.com/reference/cli/docker/buildx/use/ "docker buildx use")
      * [docker buildx version](https://docs.docker.com/reference/cli/docker/buildx/version/ "docker buildx version")
    - [docker checkpoint](https://docs.docker.com/reference/cli/docker/checkpoint/)

      * [docker checkpoint create](https://docs.docker.com/reference/cli/docker/checkpoint/create/ "docker checkpoint create")
      * [docker checkpoint ls](https://docs.docker.com/reference/cli/docker/checkpoint/ls/ "docker checkpoint ls")
      * [docker checkpoint rm](https://docs.docker.com/reference/cli/docker/checkpoint/rm/ "docker checkpoint rm")
    - [docker compose](https://docs.docker.com/reference/cli/docker/compose/)

      * [docker compose alpha dry-run](https://docs.docker.com/reference/cli/docker/compose/alpha/dry-run/ "docker compose alpha dry-run")
      * [docker compose alpha scale](https://docs.docker.com/reference/cli/docker/compose/alpha/scale/ "docker compose alpha scale")
      * [docker compose alpha watch](https://docs.docker.com/reference/cli/docker/compose/alpha/watch/ "docker compose alpha watch")
      * [docker compose attach](https://docs.docker.com/reference/cli/docker/compose/attach/ "docker compose attach")
      * [docker compose bridge](https://docs.docker.com/reference/cli/docker/compose/bridge/)

        + [docker compose bridge convert](https://docs.docker.com/reference/cli/docker/compose/bridge/convert/ "docker compose bridge convert")
        + [docker compose bridge transformations](https://docs.docker.com/reference/cli/docker/compose/bridge/transformations/)

          - [docker compose bridge transformations create](https://docs.docker.com/reference/cli/docker/compose/bridge/transformations/create/ "docker compose bridge transformations create")
          - [docker compose bridge transformations list](https://docs.docker.com/reference/cli/docker/compose/bridge/transformations/list/ "docker compose bridge transformations list")
      * [docker compose build](https://docs.docker.com/reference/cli/docker/compose/build/ "docker compose build")
      * [docker compose commit](https://docs.docker.com/reference/cli/docker/compose/commit/ "docker compose commit")
      * [docker compose config](https://docs.docker.com/reference/cli/docker/compose/config/ "docker compose config")
      * [docker compose convert](https://docs.docker.com/reference/cli/docker/compose/convert/ "docker compose convert")
      * [docker compose cp](https://docs.docker.com/reference/cli/docker/compose/cp/ "docker compose cp")
      * [docker compose create](https://docs.docker.com/reference/cli/docker/compose/create/ "docker compose create")
      * [docker compose down](https://docs.docker.com/reference/cli/docker/compose/down/ "docker compose down")
      * [docker compose events](https://docs.docker.com/reference/cli/docker/compose/events/ "docker compose events")
      * [docker compose exec](https://docs.docker.com/reference/cli/docker/compose/exec/ "docker compose exec")
      * [docker compose export](https://docs.docker.com/reference/cli/docker/compose/export/ "docker compose export")
      * [docker compose images](https://docs.docker.com/reference/cli/docker/compose/images/ "docker compose images")
      * [docker compose kill](https://docs.docker.com/reference/cli/docker/compose/kill/ "docker compose kill")
      * [docker compose logs](https://docs.docker.com/reference/cli/docker/compose/logs/ "docker compose logs")
      * [docker compose ls](https://docs.docker.com/reference/cli/docker/compose/ls/ "docker compose ls")
      * [docker compose pause](https://docs.docker.com/reference/cli/docker/compose/pause/ "docker compose pause")
      * [docker compose port](https://docs.docker.com/reference/cli/docker/compose/port/ "docker compose port")
      * [docker compose ps](https://docs.docker.com/reference/cli/docker/compose/ps/ "docker compose ps")
      * [docker compose publish](https://docs.docker.com/reference/cli/docker/compose/publish/ "docker compose publish")
      * [docker compose pull](https://docs.docker.com/reference/cli/docker/compose/pull/ "docker compose pull")
      * [docker compose push](https://docs.docker.com/reference/cli/docker/compose/push/ "docker compose push")
      * [docker compose restart](https://docs.docker.com/reference/cli/docker/compose/restart/ "docker compose restart")
      * [docker compose rm](https://docs.docker.com/reference/cli/docker/compose/rm/ "docker compose rm")
      * [docker compose run](https://docs.docker.com/reference/cli/docker/compose/run/ "docker compose run")
      * [docker compose scale](https://docs.docker.com/reference/cli/docker/compose/scale/ "docker compose scale")
      * [docker compose start](https://docs.docker.com/reference/cli/docker/compose/start/ "docker compose start")
      * [docker compose stats](https://docs.docker.com/reference/cli/docker/compose/stats/ "docker compose stats")
      * [docker compose stop](https://docs.docker.com/reference/cli/docker/compose/stop/ "docker compose stop")
      * [docker compose top](https://docs.docker.com/reference/cli/docker/compose/top/ "docker compose top")
      * [docker compose unpause](https://docs.docker.com/reference/cli/docker/compose/unpause/ "docker compose unpause")
      * [docker compose up](https://docs.docker.com/reference/cli/docker/compose/up/ "docker compose up")
      * [docker compose version](https://docs.docker.com/reference/cli/docker/compose/version/ "docker compose version")
      * [docker compose volumes](https://docs.docker.com/reference/cli/docker/compose/volumes/ "docker compose volumes")
      * [docker compose wait](https://docs.docker.com/reference/cli/docker/compose/wait/ "docker compose wait")
      * [docker compose watch](https://docs.docker.com/reference/cli/docker/compose/watch/ "docker compose watch")
    - [docker config](https://docs.docker.com/reference/cli/docker/config/)

      * [docker config create](https://docs.docker.com/reference/cli/docker/config/create/ "docker config create")
      * [docker config inspect](https://docs.docker.com/reference/cli/docker/config/inspect/ "docker config inspect")
      * [docker config ls](https://docs.docker.com/reference/cli/docker/config/ls/ "docker config ls")
      * [docker config rm](https://docs.docker.com/reference/cli/docker/config/rm/ "docker config rm")
    - [docker container](https://docs.docker.com/reference/cli/docker/container/)

      * [docker container attach](https://docs.docker.com/reference/cli/docker/container/attach/ "docker container attach")
      * [docker container commit](https://docs.docker.com/reference/cli/docker/container/commit/ "docker container commit")
      * [docker container cp](https://docs.docker.com/reference/cli/docker/container/cp/ "docker container cp")
      * [docker container create](https://docs.docker.com/reference/cli/docker/container/create/ "docker container create")
      * [docker container diff](https://docs.docker.com/reference/cli/docker/container/diff/ "docker container diff")
      * [docker container exec](https://docs.docker.com/reference/cli/docker/container/exec/ "docker container exec")
      * [docker container export](https://docs.docker.com/reference/cli/docker/container/export/ "docker container export")
      * [docker container inspect](https://docs.docker.com/reference/cli/docker/container/inspect/ "docker container inspect")
      * [docker container kill](https://docs.docker.com/reference/cli/docker/container/kill/ "docker container kill")
      * [docker container logs](https://docs.docker.com/reference/cli/docker/container/logs/ "docker container logs")
      * [docker container ls](https://docs.docker.com/reference/cli/docker/container/ls/ "docker container ls")
      * [docker container pause](https://docs.docker.com/reference/cli/docker/container/pause/ "docker container pause")
      * [docker container port](https://docs.docker.com/reference/cli/docker/container/port/ "docker container port")
      * [docker container prune](https://docs.docker.com/reference/cli/docker/container/prune/ "docker container prune")
      * [docker container rename](https://docs.docker.com/reference/cli/docker/container/rename/ "docker container rename")
      * [docker container restart](https://docs.docker.com/reference/cli/docker/container/restart/ "docker container restart")
      * [docker container rm](https://docs.docker.com/reference/cli/docker/container/rm/ "docker container rm")
      * [docker container run](https://docs.docker.com/reference/cli/docker/container/run/ "docker container run")
      * [docker container start](https://docs.docker.com/reference/cli/docker/container/start/ "docker container start")
      * [docker container stats](https://docs.docker.com/reference/cli/docker/container/stats/ "docker container stats")
      * [docker container stop](https://docs.docker.com/reference/cli/docker/container/stop/ "docker container stop")
      * [docker container top](https://docs.docker.com/reference/cli/docker/container/top/ "docker container top")
      * [docker container unpause](https://docs.docker.com/reference/cli/docker/container/unpause/ "docker container unpause")
      * [docker container update](https://docs.docker.com/reference/cli/docker/container/update/ "docker container update")
      * [docker container wait](https://docs.docker.com/reference/cli/docker/container/wait/ "docker container wait")
    - [docker context](https://docs.docker.com/reference/cli/docker/context/)

      * [docker context create](https://docs.docker.com/reference/cli/docker/context/create/ "docker context create")
      * [docker context export](https://docs.docker.com/reference/cli/docker/context/export/ "docker context export")
      * [docker context import](https://docs.docker.com/reference/cli/docker/context/import/ "docker context import")
      * [docker context inspect](https://docs.docker.com/reference/cli/docker/context/inspect/ "docker context inspect")
      * [docker context ls](https://docs.docker.com/reference/cli/docker/context/ls/ "docker context ls")
      * [docker context rm](https://docs.docker.com/reference/cli/docker/context/rm/ "docker context rm")
      * [docker context show](https://docs.docker.com/reference/cli/docker/context/show/ "docker context show")
      * [docker context update](https://docs.docker.com/reference/cli/docker/context/update/ "docker context update")
      * [docker context use](https://docs.docker.com/reference/cli/docker/context/use/ "docker context use")
    - [docker debug](https://docs.docker.com/reference/cli/docker/debug/ "docker debug")
    - [docker desktop](https://docs.docker.com/reference/cli/docker/desktop/)

      * [docker desktop diagnose](https://docs.docker.com/reference/cli/docker/desktop/diagnose/ "docker desktop diagnose")
      * [docker desktop disable](https://docs.docker.com/reference/cli/docker/desktop/disable/)

        + [docker desktop disable model-runner](https://docs.docker.com/reference/cli/docker/desktop/disable/model-runner/ "docker desktop disable model-runner")
      * [docker desktop enable](https://docs.docker.com/reference/cli/docker/desktop/enable/)

        + [docker desktop enable model-runner](https://docs.docker.com/reference/cli/docker/desktop/enable/model-runner/ "docker desktop enable model-runner")
      * [docker desktop engine](https://docs.docker.com/reference/cli/docker/desktop/engine/)

        + [docker desktop engine ls](https://docs.docker.com/reference/cli/docker/desktop/engine/ls/ "docker desktop engine ls")
        + [docker desktop engine use](https://docs.docker.com/reference/cli/docker/desktop/engine/use/ "docker desktop engine use")
      * [docker desktop kubernetes](https://docs.docker.com/reference/cli/docker/desktop/kubernetes/)

        + [docker desktop kubernetes images](https://docs.docker.com/reference/cli/docker/desktop/kubernetes/images/ "docker desktop kubernetes images")
      * [docker desktop logs](https://docs.docker.com/reference/cli/docker/desktop/logs/ "docker desktop logs")
      * [docker desktop restart](https://docs.docker.com/reference/cli/docker/desktop/restart/ "docker desktop restart")
      * [docker desktop start](https://docs.docker.com/reference/cli/docker/desktop/start/ "docker desktop start")
      * [docker desktop status](https://docs.docker.com/reference/cli/docker/desktop/status/ "docker desktop status")
      * [docker desktop stop](https://docs.docker.com/reference/cli/docker/desktop/stop/ "docker desktop stop")
      * [docker desktop update](https://docs.docker.com/reference/cli/docker/desktop/update/ "docker desktop update")
      * [docker desktop version](https://docs.docker.com/reference/cli/docker/desktop/version/ "docker desktop version")
    - [docker dhi](https://docs.docker.com/reference/cli/docker/dhi/)

      * [docker dhi auth](https://docs.docker.com/reference/cli/docker/dhi/auth/)

        + [docker dhi auth apk](https://docs.docker.com/reference/cli/docker/dhi/auth/apk/ "docker dhi auth apk")
      * [docker dhi catalog](https://docs.docker.com/reference/cli/docker/dhi/catalog/)

        + [docker dhi catalog get](https://docs.docker.com/reference/cli/docker/dhi/catalog/get/ "docker dhi catalog get")
        + [docker dhi catalog list](https://docs.docker.com/reference/cli/docker/dhi/catalog/list/ "docker dhi catalog list")
      * [docker dhi customization](https://docs.docker.com/reference/cli/docker/dhi/customization/)

        + [docker dhi customization build](https://docs.docker.com/reference/cli/docker/dhi/customization/build/)

          - [docker dhi customization build get](https://docs.docker.com/reference/cli/docker/dhi/customization/build/get/ "docker dhi customization build get")
          - [docker dhi customization build list](https://docs.docker.com/reference/cli/docker/dhi/customization/build/list/ "docker dhi customization build list")
          - [docker dhi customization build logs](https://docs.docker.com/reference/cli/docker/dhi/customization/build/logs/ "docker dhi customization build logs")
        + [docker dhi customization create](https://docs.docker.com/reference/cli/docker/dhi/customization/create/ "docker dhi customization create")
        + [docker dhi customization delete](https://docs.docker.com/reference/cli/docker/dhi/customization/delete/ "docker dhi customization delete")
        + [docker dhi customization edit](https://docs.docker.com/reference/cli/docker/dhi/customization/edit/ "docker dhi customization edit")
        + [docker dhi customization get](https://docs.docker.com/reference/cli/docker/dhi/customization/get/ "docker dhi customization get")
        + [docker dhi customization list](https://docs.docker.com/reference/cli/docker/dhi/customization/list/ "docker dhi customization list")
        + [docker dhi customization prepare](https://docs.docker.com/reference/cli/docker/dhi/customization/prepare/ "docker dhi customization prepare")
      * [docker dhi mirror](https://docs.docker.com/reference/cli/docker/dhi/mirror/)

        + [docker dhi mirror list](https://docs.docker.com/reference/cli/docker/dhi/mirror/list/ "docker dhi mirror list")
        + [docker dhi mirror start](https://docs.docker.com/reference/cli/docker/dhi/mirror/start/ "docker dhi mirror start")
        + [docker dhi mirror stop](https://docs.docker.com/reference/cli/docker/dhi/mirror/stop/ "docker dhi mirror stop")
    - [docker exec](/reference/cli/docker/container/exec/ "docker exec")
    - [docker image](https://docs.docker.com/reference/cli/docker/image/)

      * [docker image build](https://docs.docker.com/reference/cli/docker/image/build/ "docker image build")
      * [docker image history](https://docs.docker.com/reference/cli/docker/image/history/ "docker image history")
      * [docker image import](https://docs.docker.com/reference/cli/docker/image/import/ "docker image import")
      * [docker image inspect](https://docs.docker.com/reference/cli/docker/image/inspect/ "docker image inspect")
      * [docker image load](https://docs.docker.com/reference/cli/docker/image/load/ "docker image load")
      * [docker image ls](https://docs.docker.com/reference/cli/docker/image/ls/ "docker image ls")
      * [docker image prune](https://docs.docker.com/reference/cli/docker/image/prune/ "docker image prune")
      * [docker image pull](https://docs.docker.com/reference/cli/docker/image/pull/ "docker image pull")
      * [docker image push](https://docs.docker.com/reference/cli/docker/image/push/ "docker image push")
      * [docker image rm](https://docs.docker.com/reference/cli/docker/image/rm/ "docker image rm")
      * [docker image save](https://docs.docker.com/reference/cli/docker/image/save/ "docker image save")
      * [docker image tag](https://docs.docker.com/reference/cli/docker/image/tag/ "docker image tag")
    - [docker images](/reference/cli/docker/image/ls/ "docker images")
    - [docker info](/reference/cli/docker/system/info/ "docker info")
    - [docker init](https://docs.docker.com/reference/cli/docker/init/ "docker init")
    - [docker inspect](https://docs.docker.com/reference/cli/docker/inspect/ "docker inspect")
    - [docker login](https://docs.docker.com/reference/cli/docker/login/ "docker login")
    - [docker logout](https://docs.docker.com/reference/cli/docker/logout/ "docker logout")
    - [docker manifest](https://docs.docker.com/reference/cli/docker/manifest/)

      * [docker manifest annotate](https://docs.docker.com/reference/cli/docker/manifest/annotate/ "docker manifest annotate")
      * [docker manifest create](https://docs.docker.com/reference/cli/docker/manifest/create/ "docker manifest create")
      * [docker manifest inspect](https://docs.docker.com/reference/cli/docker/manifest/inspect/ "docker manifest inspect")
      * [docker manifest push](https://docs.docker.com/reference/cli/docker/manifest/push/ "docker manifest push")
      * [docker manifest rm](https://docs.docker.com/reference/cli/docker/manifest/rm/ "docker manifest rm")
    - [docker mcp](https://docs.docker.com/reference/cli/docker/mcp/)

      * [docker mcp catalog](https://docs.docker.com/reference/cli/docker/mcp/catalog/)

        + [docker mcp catalog create](https://docs.docker.com/reference/cli/docker/mcp/catalog/create/ "docker mcp catalog create")
        + [docker mcp catalog list](https://docs.docker.com/reference/cli/docker/mcp/catalog/list/ "docker mcp catalog list")
        + [docker mcp catalog ls](https://docs.docker.com/reference/cli/docker/mcp/catalog/ls/ "docker mcp catalog ls")
        + [docker mcp catalog pull](https://docs.docker.com/reference/cli/docker/mcp/catalog/pull/ "docker mcp catalog pull")
        + [docker mcp catalog push](https://docs.docker.com/reference/cli/docker/mcp/catalog/push/ "docker mcp catalog push")
        + [docker mcp catalog remove](https://docs.docker.com/reference/cli/docker/mcp/catalog/remove/ "docker mcp catalog remove")
        + [docker mcp catalog rm](https://docs.docker.com/reference/cli/docker/mcp/catalog/rm/ "docker mcp catalog rm")
        + [docker mcp catalog server](https://docs.docker.com/reference/cli/docker/mcp/catalog/server/)

          - [docker mcp catalog server add](https://docs.docker.com/reference/cli/docker/mcp/catalog/server/add/ "docker mcp catalog server add")
          - [docker mcp catalog server inspect](https://docs.docker.com/reference/cli/docker/mcp/catalog/server/inspect/ "docker mcp catalog server inspect")
          - [docker mcp catalog server ls](https://docs.docker.com/reference/cli/docker/mcp/catalog/server/ls/ "docker mcp catalog server ls")
          - [docker mcp catalog server remove](https://docs.docker.com/reference/cli/docker/mcp/catalog/server/remove/ "docker mcp catalog server remove")
        + [docker mcp catalog show](https://docs.docker.com/reference/cli/docker/mcp/catalog/show/ "docker mcp catalog show")
        + [docker mcp catalog tag](https://docs.docker.com/reference/cli/docker/mcp/catalog/tag/ "docker mcp catalog tag")
      * [docker mcp client](https://docs.docker.com/reference/cli/docker/mcp/client/)

        + [docker mcp client connect](https://docs.docker.com/reference/cli/docker/mcp/client/connect/ "docker mcp client connect")
        + [docker mcp client disconnect](https://docs.docker.com/reference/cli/docker/mcp/client/disconnect/ "docker mcp client disconnect")
        + [docker mcp client ls](https://docs.docker.com/reference/cli/docker/mcp/client/ls/ "docker mcp client ls")
      * [docker mcp feature](https://docs.docker.com/reference/cli/docker/mcp/feature/)

        + [docker mcp feature disable](https://docs.docker.com/reference/cli/docker/mcp/feature/disable/ "docker mcp feature disable")
        + [docker mcp feature enable](https://docs.docker.com/reference/cli/docker/mcp/feature/enable/ "docker mcp feature enable")
        + [docker mcp feature list](https://docs.docker.com/reference/cli/docker/mcp/feature/list/ "docker mcp feature list")
        + [docker mcp feature ls](https://docs.docker.com/reference/cli/docker/mcp/feature/ls/ "docker mcp feature ls")
      * [docker mcp gateway](https://docs.docker.com/reference/cli/docker/mcp/gateway/)

        + [docker mcp gateway run](https://docs.docker.com/reference/cli/docker/mcp/gateway/run/ "docker mcp gateway run")
      * [docker mcp profile](https://docs.docker.com/reference/cli/docker/mcp/profile/)

        + [docker mcp profile config](https://docs.docker.com/reference/cli/docker/mcp/profile/config/ "docker mcp profile config")
        + [docker mcp profile create](https://docs.docker.com/reference/cli/docker/mcp/profile/create/ "docker mcp profile create")
        + [docker mcp profile export](https://docs.docker.com/reference/cli/docker/mcp/profile/export/ "docker mcp profile export")
        + [docker mcp profile import](https://docs.docker.com/reference/cli/docker/mcp/profile/import/ "docker mcp profile import")
        + [docker mcp profile list](https://docs.docker.com/reference/cli/docker/mcp/profile/list/ "docker mcp profile list")
        + [docker mcp profile pull](https://docs.docker.com/reference/cli/docker/mcp/profile/pull/ "docker mcp profile pull")
        + [docker mcp profile push](https://docs.docker.com/reference/cli/docker/mcp/profile/push/ "docker mcp profile push")
        + [docker mcp profile remove](https://docs.docker.com/reference/cli/docker/mcp/profile/remove/ "docker mcp profile remove")
        + [docker mcp profile server](https://docs.docker.com/reference/cli/docker/mcp/profile/server/)

          - [docker mcp profile server add](https://docs.docker.com/reference/cli/docker/mcp/profile/server/add/ "docker mcp profile server add")
          - [docker mcp profile server ls](https://docs.docker.com/reference/cli/docker/mcp/profile/server/ls/ "docker mcp profile server ls")
          - [docker mcp profile server remove](https://docs.docker.com/reference/cli/docker/mcp/profile/server/remove/ "docker mcp profile server remove")
        + [docker mcp profile show](https://docs.docker.com/reference/cli/docker/mcp/profile/show/ "docker mcp profile show")
        + [docker mcp profile tools](https://docs.docker.com/reference/cli/docker/mcp/profile/tools/ "docker mcp profile tools")
      * [docker mcp secret](https://docs.docker.com/reference/cli/docker/mcp/secret/)

        + [docker mcp secret ls](https://docs.docker.com/reference/cli/docker/mcp/secret/ls/ "docker mcp secret ls")
        + [docker mcp secret rm](https://docs.docker.com/reference/cli/docker/mcp/secret/rm/ "docker mcp secret rm")
        + [docker mcp secret set](https://docs.docker.com/reference/cli/docker/mcp/secret/set/ "docker mcp secret set")
      * [docker mcp server](https://docs.docker.com/reference/cli/docker/mcp/server/)

        + [docker mcp server init](https://docs.docker.com/reference/cli/docker/mcp/server/init/ "docker mcp server init")
      * [docker mcp tools](https://docs.docker.com/reference/cli/docker/mcp/tools/)

        + [docker mcp tools call](https://docs.docker.com/reference/cli/docker/mcp/tools/call/ "docker mcp tools call")
        + [docker mcp tools count](https://docs.docker.com/reference/cli/docker/mcp/tools/count/ "docker mcp tools count")
        + [docker mcp tools inspect](https://docs.docker.com/reference/cli/docker/mcp/tools/inspect/ "docker mcp tools inspect")
        + [docker mcp tools list](https://docs.docker.com/reference/cli/docker/mcp/tools/list/ "docker mcp tools list")
        + [docker mcp tools ls](https://docs.docker.com/reference/cli/docker/mcp/tools/ls/ "docker mcp tools ls")
      * [docker mcp version](https://docs.docker.com/reference/cli/docker/mcp/version/ "docker mcp version")
    - [docker model](https://docs.docker.com/reference/cli/docker/model/)

      * [docker model bench](https://docs.docker.com/reference/cli/docker/model/bench/ "docker model bench")
      * [docker model df](https://docs.docker.com/reference/cli/docker/model/df/ "docker model df")
      * [docker model inspect](https://docs.docker.com/reference/cli/docker/model/inspect/ "docker model inspect")
      * [docker model install-runner](https://docs.docker.com/reference/cli/docker/model/install-runner/ "docker model install-runner")
      * [docker model launch](https://docs.docker.com/reference/cli/docker/model/launch/ "docker model launch")
      * [docker model list](https://docs.docker.com/reference/cli/docker/model/list/ "docker model list")
      * [docker model logs](https://docs.docker.com/reference/cli/docker/model/logs/ "docker model logs")
      * [docker model package](https://docs.docker.com/reference/cli/docker/model/package/ "docker model package")
      * [docker model ps](https://docs.docker.com/reference/cli/docker/model/ps/ "docker model ps")
      * [docker model pull](https://docs.docker.com/reference/cli/docker/model/pull/ "docker model pull")
      * [docker model purge](https://docs.docker.com/reference/cli/docker/model/purge/ "docker model purge")
      * [docker model push](https://docs.docker.com/reference/cli/docker/model/push/ "docker model push")
      * [docker model reinstall-runner](https://docs.docker.com/reference/cli/docker/model/reinstall-runner/ "docker model reinstall-runner")
      * [docker model requests](https://docs.docker.com/reference/cli/docker/model/requests/ "docker model requests")
      * [docker model restart-runner](https://docs.docker.com/reference/cli/docker/model/restart-runner/ "docker model restart-runner")
      * [docker model rm](https://docs.docker.com/reference/cli/docker/model/rm/ "docker model rm")
      * [docker model run](https://docs.docker.com/reference/cli/docker/model/run/ "docker model run")
      * [docker model search](https://docs.docker.com/reference/cli/docker/model/search/ "docker model search")
      * [docker model show](https://docs.docker.com/reference/cli/docker/model/show/ "docker model show")
      * [docker model skills](https://docs.docker.com/reference/cli/docker/model/skills/ "docker model skills")
      * [docker model start-runner](https://docs.docker.com/reference/cli/docker/model/start-runner/ "docker model start-runner")
      * [docker model status](https://docs.docker.com/reference/cli/docker/model/status/ "docker model status")
      * [docker model stop-runner](https://docs.docker.com/reference/cli/docker/model/stop-runner/ "docker model stop-runner")
      * [docker model tag](https://docs.docker.com/reference/cli/docker/model/tag/ "docker model tag")
      * [docker model uninstall-runner](https://docs.docker.com/reference/cli/docker/model/uninstall-runner/ "docker model uninstall-runner")
      * [docker model unload](https://docs.docker.com/reference/cli/docker/model/unload/ "docker model unload")
      * [docker model version](https://docs.docker.com/reference/cli/docker/model/version/ "docker model version")
    - [docker network](https://docs.docker.com/reference/cli/docker/network/)

      * [docker network connect](https://docs.docker.com/reference/cli/docker/network/connect/ "docker network connect")
      * [docker network create](https://docs.docker.com/reference/cli/docker/network/create/ "docker network create")
      * [docker network disconnect](https://docs.docker.com/reference/cli/docker/network/disconnect/ "docker network disconnect")
      * [docker network inspect](https://docs.docker.com/reference/cli/docker/network/inspect/ "docker network inspect")
      * [docker network ls](https://docs.docker.com/reference/cli/docker/network/ls/ "docker network ls")
      * [docker network prune](https://docs.docker.com/reference/cli/docker/network/prune/ "docker network prune")
      * [docker network rm](https://docs.docker.com/reference/cli/docker/network/rm/ "docker network rm")
    - [docker node](https://docs.docker.com/reference/cli/docker/node/)

      * [docker node demote](https://docs.docker.com/reference/cli/docker/node/demote/ "docker node demote")
      * [docker node inspect](https://docs.docker.com/reference/cli/docker/node/inspect/ "docker node inspect")
      * [docker node ls](https://docs.docker.com/reference/cli/docker/node/ls/ "docker node ls")
      * [docker node promote](https://docs.docker.com/reference/cli/docker/node/promote/ "docker node promote")
      * [docker node ps](https://docs.docker.com/reference/cli/docker/node/ps/ "docker node ps")
      * [docker node rm](https://docs.docker.com/reference/cli/docker/node/rm/ "docker node rm")
      * [docker node update](https://docs.docker.com/reference/cli/docker/node/update/ "docker node update")
    - [docker offload](https://docs.docker.com/reference/cli/docker/offload/)

      * [docker offload diagnose](https://docs.docker.com/reference/cli/docker/offload/diagnose/ "docker offload diagnose")
      * [docker offload start](https://docs.docker.com/reference/cli/docker/offload/start/ "docker offload start")
      * [docker offload status](https://docs.docker.com/reference/cli/docker/offload/status/ "docker offload status")
      * [docker offload stop](https://docs.docker.com/reference/cli/docker/offload/stop/ "docker offload stop")
      * [docker offload version](https://docs.docker.com/reference/cli/docker/offload/version/ "docker offload version")
    - [docker pass](https://docs.docker.com/reference/cli/docker/pass/)

      * [docker pass get](https://docs.docker.com/reference/cli/docker/pass/get/ "docker pass get")
      * [docker pass ls](https://docs.docker.com/reference/cli/docker/pass/ls/ "docker pass ls")
      * [docker pass rm](https://docs.docker.com/reference/cli/docker/pass/rm/ "docker pass rm")
      * [docker pass set](https://docs.docker.com/reference/cli/docker/pass/set/ "docker pass set")
    - [docker plugin](https://docs.docker.com/reference/cli/docker/plugin/)

      * [docker plugin create](https://docs.docker.com/reference/cli/docker/plugin/create/ "docker plugin create")
      * [docker plugin disable](https://docs.docker.com/reference/cli/docker/plugin/disable/ "docker plugin disable")
      * [docker plugin enable](https://docs.docker.com/reference/cli/docker/plugin/enable/ "docker plugin enable")
      * [docker plugin inspect](https://docs.docker.com/reference/cli/docker/plugin/inspect/ "docker plugin inspect")
      * [docker plugin install](https://docs.docker.com/reference/cli/docker/plugin/install/ "docker plugin install")
      * [docker plugin ls](https://docs.docker.com/reference/cli/docker/plugin/ls/ "docker plugin ls")
      * [docker plugin push](https://docs.docker.com/reference/cli/docker/plugin/push/ "docker plugin push")
      * [docker plugin rm](https://docs.docker.com/reference/cli/docker/plugin/rm/ "docker plugin rm")
      * [docker plugin set](https://docs.docker.com/reference/cli/docker/plugin/set/ "docker plugin set")
      * [docker plugin upgrade](https://docs.docker.com/reference/cli/docker/plugin/upgrade/ "docker plugin upgrade")
    - [docker ps](/reference/cli/docker/container/ls/ "docker ps")
    - [docker pull](/reference/cli/docker/image/pull/ "docker pull")
    - [docker push](/reference/cli/docker/image/push/ "docker push")
    - [docker run](/reference/cli/docker/container/run/ "docker run")
    - [docker sandbox](https://docs.docker.com/reference/cli/docker/sandbox/)

      * [docker sandbox create](https://docs.docker.com/reference/cli/docker/sandbox/create/)

        + [docker sandbox create cagent](https://docs.docker.com/reference/cli/docker/sandbox/create/cagent/ "docker sandbox create cagent")
        + [docker sandbox create claude](https://docs.docker.com/reference/cli/docker/sandbox/create/claude/ "docker sandbox create claude")
        + [docker sandbox create codex](https://docs.docker.com/reference/cli/docker/sandbox/create/codex/ "docker sandbox create codex")
        + [docker sandbox create copilot](https://docs.docker.com/reference/cli/docker/sandbox/create/copilot/ "docker sandbox create copilot")
        + [docker sandbox create gemini](https://docs.docker.com/reference/cli/docker/sandbox/create/gemini/ "docker sandbox create gemini")
        + [docker sandbox create kiro](https://docs.docker.com/reference/cli/docker/sandbox/create/kiro/ "docker sandbox create kiro")
        + [docker sandbox create opencode](https://docs.docker.com/reference/cli/docker/sandbox/create/opencode/ "docker sandbox create opencode")
        + [docker sandbox create shell](https://docs.docker.com/reference/cli/docker/sandbox/create/shell/ "docker sandbox create shell")
      * [docker sandbox exec](https://docs.docker.com/reference/cli/docker/sandbox/exec/ "docker sandbox exec")
      * [docker sandbox inspect](https://docs.docker.com/reference/cli/docker/sandbox/inspect/ "docker sandbox inspect")
      * [docker sandbox ls](https://docs.docker.com/reference/cli/docker/sandbox/ls/ "docker sandbox ls")
      * [docker sandbox network](https://docs.docker.com/reference/cli/docker/sandbox/network/)

        + [docker sandbox network log](https://docs.docker.com/reference/cli/docker/sandbox/network/log/ "docker sandbox network log")
        + [docker sandbox network proxy](https://docs.docker.com/reference/cli/docker/sandbox/network/proxy/ "docker sandbox network proxy")
      * [docker sandbox reset](https://docs.docker.com/reference/cli/docker/sandbox/reset/ "docker sandbox reset")
      * [docker sandbox rm](https://docs.docker.com/reference/cli/docker/sandbox/rm/ "docker sandbox rm")
      * [docker sandbox run](https://docs.docker.com/reference/cli/docker/sandbox/run/ "docker sandbox run")
      * [docker sandbox save](https://docs.docker.com/reference/cli/docker/sandbox/save/ "docker sandbox save")
      * [docker sandbox stop](https://docs.docker.com/reference/cli/docker/sandbox/stop/ "docker sandbox stop")
      * [docker sandbox version](https://docs.docker.com/reference/cli/docker/sandbox/version/ "docker sandbox version")
    - [docker scout](https://docs.docker.com/reference/cli/docker/scout/)

      * [docker scout attestation](https://docs.docker.com/reference/cli/docker/scout/attestation/)

        + [docker scout attestation add](https://docs.docker.com/reference/cli/docker/scout/attestation/add/ "docker scout attestation add")
        + [docker scout attestation get](https://docs.docker.com/reference/cli/docker/scout/attestation/get/ "docker scout attestation get")
        + [docker scout attestation list](https://docs.docker.com/reference/cli/docker/scout/attestation/list/ "docker scout attestation list")
      * [docker scout cache](https://docs.docker.com/reference/cli/docker/scout/cache/)

        + [docker scout cache df](https://docs.docker.com/reference/cli/docker/scout/cache/df/ "docker scout cache df")
        + [docker scout cache prune](https://docs.docker.com/reference/cli/docker/scout/cache/prune/ "docker scout cache prune")
      * [docker scout compare](https://docs.docker.com/reference/cli/docker/scout/compare/ "docker scout compare")
      * [docker scout config](https://docs.docker.com/reference/cli/docker/scout/config/ "docker scout config")
      * [docker scout cves](https://docs.docker.com/reference/cli/docker/scout/cves/ "docker scout cves")
      * [docker scout enroll](https://docs.docker.com/reference/cli/docker/scout/enroll/ "docker scout enroll")
      * [docker scout environment](https://docs.docker.com/reference/cli/docker/scout/environment/ "docker scout environment")
      * [docker scout help](https://docs.docker.com/reference/cli/docker/scout/help/ "docker scout help")
      * [docker scout integration](https://docs.docker.com/reference/cli/docker/scout/integration/)

        + [docker scout integration configure](https://docs.docker.com/reference/cli/docker/scout/integration/configure/ "docker scout integration configure")
        + [docker scout integration delete](https://docs.docker.com/reference/cli/docker/scout/integration/delete/ "docker scout integration delete")
        + [docker scout integration list](https://docs.docker.com/reference/cli/docker/scout/integration/list/ "docker scout integration list")
      * [docker scout policy](https://docs.docker.com/reference/cli/docker/scout/policy/ "docker scout policy")
      * [docker scout push](https://docs.docker.com/reference/cli/docker/scout/push/ "docker scout push")
      * [docker scout quickview](https://docs.docker.com/reference/cli/docker/scout/quickview/ "docker scout quickview")
      * [docker scout recommendations](https://docs.docker.com/reference/cli/docker/scout/recommendations/ "docker scout recommendations")
      * [docker scout repo](https://docs.docker.com/reference/cli/docker/scout/repo/)

        + [docker scout repo disable](https://docs.docker.com/reference/cli/docker/scout/repo/disable/ "docker scout repo disable")
        + [docker scout repo enable](https://docs.docker.com/reference/cli/docker/scout/repo/enable/ "docker scout repo enable")
        + [docker scout repo list](https://docs.docker.com/reference/cli/docker/scout/repo/list/ "docker scout repo list")
      * [docker scout sbom](https://docs.docker.com/reference/cli/docker/scout/sbom/ "docker scout sbom")
      * [docker scout stream](https://docs.docker.com/reference/cli/docker/scout/stream/ "docker scout stream")
      * [docker scout version](https://docs.docker.com/reference/cli/docker/scout/version/ "docker scout version")
      * [docker scout vex](https://docs.docker.com/reference/cli/docker/scout/vex/)

        + [docker scout vex get](https://docs.docker.com/reference/cli/docker/scout/vex/get/ "docker scout vex get")
      * [docker scout watch](https://docs.docker.com/reference/cli/docker/scout/watch/ "docker scout watch")
    - [docker search](https://docs.docker.com/reference/cli/docker/search/ "docker search")
    - [docker secret](https://docs.docker.com/reference/cli/docker/secret/)

      * [docker secret create](https://docs.docker.com/reference/cli/docker/secret/create/ "docker secret create")
      * [docker secret inspect](https://docs.docker.com/reference/cli/docker/secret/inspect/ "docker secret inspect")
      * [docker secret ls](https://docs.docker.com/reference/cli/docker/secret/ls/ "docker secret ls")
      * [docker secret rm](https://docs.docker.com/reference/cli/docker/secret/rm/ "docker secret rm")
    - [docker service](https://docs.docker.com/reference/cli/docker/service/)

      * [docker service create](https://docs.docker.com/reference/cli/docker/service/create/ "docker service create")
      * [docker service inspect](https://docs.docker.com/reference/cli/docker/service/inspect/ "docker service inspect")
      * [docker service logs](https://docs.docker.com/reference/cli/docker/service/logs/ "docker service logs")
      * [docker service ls](https://docs.docker.com/reference/cli/docker/service/ls/ "docker service ls")
      * [docker service ps](https://docs.docker.com/reference/cli/docker/service/ps/ "docker service ps")
      * [docker service rm](https://docs.docker.com/reference/cli/docker/service/rm/ "docker service rm")
      * [docker service rollback](https://docs.docker.com/reference/cli/docker/service/rollback/ "docker service rollback")
      * [docker service scale](https://docs.docker.com/reference/cli/docker/service/scale/ "docker service scale")
      * [docker service update](https://docs.docker.com/reference/cli/docker/service/update/ "docker service update")
    - [docker stack](https://docs.docker.com/reference/cli/docker/stack/)

      * [docker stack config](https://docs.docker.com/reference/cli/docker/stack/config/ "docker stack config")
      * [docker stack deploy](https://docs.docker.com/reference/cli/docker/stack/deploy/ "docker stack deploy")
      * [docker stack ls](https://docs.docker.com/reference/cli/docker/stack/ls/ "docker stack ls")
      * [docker stack ps](https://docs.docker.com/reference/cli/docker/stack/ps/ "docker stack ps")
      * [docker stack rm](https://docs.docker.com/reference/cli/docker/stack/rm/ "docker stack rm")
      * [docker stack services](https://docs.docker.com/reference/cli/docker/stack/services/ "docker stack services")
    - [docker swarm](https://docs.docker.com/reference/cli/docker/swarm/)

      * [docker swarm ca](https://docs.docker.com/reference/cli/docker/swarm/ca/ "docker swarm ca")
      * [docker swarm init](https://docs.docker.com/reference/cli/docker/swarm/init/ "docker swarm init")
      * [docker swarm join](https://docs.docker.com/reference/cli/docker/swarm/join/ "docker swarm join")
      * [docker swarm join-token](https://docs.docker.com/reference/cli/docker/swarm/join-token/ "docker swarm join-token")
      * [docker swarm leave](https://docs.docker.com/reference/cli/docker/swarm/leave/ "docker swarm leave")
      * [docker swarm unlock](https://docs.docker.com/reference/cli/docker/swarm/unlock/ "docker swarm unlock")
      * [docker swarm unlock-key](https://docs.docker.com/reference/cli/docker/swarm/unlock-key/ "docker swarm unlock-key")
      * [docker swarm update](https://docs.docker.com/reference/cli/docker/swarm/update/ "docker swarm update")
    - [docker system](https://docs.docker.com/reference/cli/docker/system/)

      * [docker system df](https://docs.docker.com/reference/cli/docker/system/df/ "docker system df")
      * [docker system events](https://docs.docker.com/reference/cli/docker/system/events/ "docker system events")
      * [docker system info](https://docs.docker.com/reference/cli/docker/system/info/ "docker system info")
      * [docker system prune](https://docs.docker.com/reference/cli/docker/system/prune/ "docker system prune")
    - [docker trust](https://docs.docker.com/reference/cli/docker/trust/)

      * [docker trust inspect](https://docs.docker.com/reference/cli/docker/trust/inspect/ "docker trust inspect")
      * [docker trust key](https://docs.docker.com/reference/cli/docker/trust/key/)

        + [docker trust key generate](https://docs.docker.com/reference/cli/docker/trust/key/generate/ "docker trust key generate")
        + [docker trust key load](https://docs.docker.com/reference/cli/docker/trust/key/load/ "docker trust key load")
      * [docker trust revoke](https://docs.docker.com/reference/cli/docker/trust/revoke/ "docker trust revoke")
      * [docker trust sign](https://docs.docker.com/reference/cli/docker/trust/sign/ "docker trust sign")
      * [docker trust signer](https://docs.docker.com/reference/cli/docker/trust/signer/)

        + [docker trust signer add](https://docs.docker.com/reference/cli/docker/trust/signer/add/ "docker trust signer add")
        + [docker trust signer remove](https://docs.docker.com/reference/cli/docker/trust/signer/remove/ "docker trust signer remove")
    - [docker version](https://docs.docker.com/reference/cli/docker/version/ "docker version")
    - [docker volume](https://docs.docker.com/reference/cli/docker/volume/)

      * [docker volume create](https://docs.docker.com/reference/cli/docker/volume/create/ "docker volume create")
      * [docker volume inspect](https://docs.docker.com/reference/cli/docker/volume/inspect/ "docker volume inspect")
      * [docker volume ls](https://docs.docker.com/reference/cli/docker/volume/ls/ "docker volume ls")
      * [docker volume prune](https://docs.docker.com/reference/cli/docker/volume/prune/ "docker volume prune")
      * [docker volume rm](https://docs.docker.com/reference/cli/docker/volume/rm/ "docker volume rm")
      * [docker volume update](https://docs.docker.com/reference/cli/docker/volume/update/ "docker volume update")
  + [dockerd](https://docs.docker.com/reference/cli/dockerd/ "dockerd")
  + [sbx](https://docs.docker.com/reference/cli/sbx/)

    - [sbx completion](https://docs.docker.com/reference/cli/sbx/completion/)

      * [sbx completion bash](https://docs.docker.com/reference/cli/sbx/completion/bash/ "sbx completion bash")
      * [sbx completion fish](https://docs.docker.com/reference/cli/sbx/completion/fish/ "sbx completion fish")
      * [sbx completion powershell](https://docs.docker.com/reference/cli/sbx/completion/powershell/ "sbx completion powershell")
      * [sbx completion zsh](https://docs.docker.com/reference/cli/sbx/completion/zsh/ "sbx completion zsh")
    - [sbx create](https://docs.docker.com/reference/cli/sbx/create/)

      * [sbx create claude](https://docs.docker.com/reference/cli/sbx/create/claude/ "sbx create claude")
      * [sbx create codex](https://docs.docker.com/reference/cli/sbx/create/codex/ "sbx create codex")
      * [sbx create copilot](https://docs.docker.com/reference/cli/sbx/create/copilot/ "sbx create copilot")
      * [sbx create docker-agent](https://docs.docker.com/reference/cli/sbx/create/docker-agent/ "sbx create docker-agent")
      * [sbx create gemini](https://docs.docker.com/reference/cli/sbx/create/gemini/ "sbx create gemini")
      * [sbx create kiro](https://docs.docker.com/reference/cli/sbx/create/kiro/ "sbx create kiro")
      * [sbx create opencode](https://docs.docker.com/reference/cli/sbx/create/opencode/ "sbx create opencode")
      * [sbx create shell](https://docs.docker.com/reference/cli/sbx/create/shell/ "sbx create shell")
    - [sbx exec](https://docs.docker.com/reference/cli/sbx/exec/ "sbx exec")
    - [sbx login](https://docs.docker.com/reference/cli/sbx/login/ "sbx login")
    - [sbx logout](https://docs.docker.com/reference/cli/sbx/logout/ "sbx logout")
    - [sbx ls](https://docs.docker.com/reference/cli/sbx/ls/ "sbx ls")
    - [sbx policy](https://docs.docker.com/reference/cli/sbx/policy/)

      * [sbx policy allow](https://docs.docker.com/reference/cli/sbx/policy/allow/)

        + [sbx policy allow network](https://docs.docker.com/reference/cli/sbx/policy/allow/network/ "sbx policy allow network")
      * [sbx policy deny](https://docs.docker.com/reference/cli/sbx/policy/deny/)

        + [sbx policy deny network](https://docs.docker.com/reference/cli/sbx/policy/deny/network/ "sbx policy deny network")
      * [sbx policy log](https://docs.docker.com/reference/cli/sbx/policy/log/ "sbx policy log")
      * [sbx policy ls](https://docs.docker.com/reference/cli/sbx/policy/ls/ "sbx policy ls")
      * [sbx policy reset](https://docs.docker.com/reference/cli/sbx/policy/reset/ "sbx policy reset")
      * [sbx policy rm](https://docs.docker.com/reference/cli/sbx/policy/rm/)

        + [sbx policy rm network](https://docs.docker.com/reference/cli/sbx/policy/rm/network/ "sbx policy rm network")
      * [sbx policy set-default](https://docs.docker.com/reference/cli/sbx/policy/set-default/ "sbx policy set-default")
    - [sbx ports](https://docs.docker.com/reference/cli/sbx/ports/ "sbx ports")
    - [sbx reset](https://docs.docker.com/reference/cli/sbx/reset/ "sbx reset")
    - [sbx rm](https://docs.docker.com/reference/cli/sbx/rm/ "sbx rm")
    - [sbx run](https://docs.docker.com/reference/cli/sbx/run/ "sbx run")
    - [sbx save](https://docs.docker.com/reference/cli/sbx/save/ "sbx save")
    - [sbx secret](https://docs.docker.com/reference/cli/sbx/secret/)

      * [sbx secret ls](https://docs.docker.com/reference/cli/sbx/secret/ls/ "sbx secret ls")
      * [sbx secret rm](https://docs.docker.com/reference/cli/sbx/secret/rm/ "sbx secret rm")
      * [sbx secret set](https://docs.docker.com/reference/cli/sbx/secret/set/ "sbx secret set")
    - [sbx stop](https://docs.docker.com/reference/cli/sbx/stop/ "sbx stop")
    - [sbx version](https://docs.docker.com/reference/cli/sbx/version/ "sbx version")
* API reference

  + [Docker Engine API](https://docs.docker.com/reference/api/engine/)

    - [SDK](https://docs.docker.com/reference/api/engine/sdk/)

      * [Examples](https://docs.docker.com/reference/api/engine/sdk/examples/ "Examples")
    - [Latest](/reference/api/engine/latest/ "Latest")
    - API reference by version

      * [v1.54](https://docs.docker.com/reference/api/engine/version/v1.54/ "v1.54")
      * [v1.53](https://docs.docker.com/reference/api/engine/version/v1.53/ "v1.53")
      * [v1.52](https://docs.docker.com/reference/api/engine/version/v1.52/ "v1.52")
      * [v1.51](https://docs.docker.com/reference/api/engine/version/v1.51/ "v1.51")
      * [v1.50](https://docs.docker.com/reference/api/engine/version/v1.50/ "v1.50")
      * [v1.49](https://docs.docker.com/reference/api/engine/version/v1.49/ "v1.49")
      * [v1.48](https://docs.docker.com/reference/api/engine/version/v1.48/ "v1.48")
      * [v1.47](https://docs.docker.com/reference/api/engine/version/v1.47/ "v1.47")
      * [v1.46](https://docs.docker.com/reference/api/engine/version/v1.46/ "v1.46")
      * [v1.45](https://docs.docker.com/reference/api/engine/version/v1.45/ "v1.45")
      * [v1.44](https://docs.docker.com/reference/api/engine/version/v1.44/ "v1.44")
    - [Engine API version history](https://docs.docker.com/reference/api/engine/version-history/ "Engine API version history")
  + Docker Hub API

    - [Latest](https://docs.docker.com/reference/api/hub/latest/ "Latest")
    - [Changelog](https://docs.docker.com/reference/api/hub/changelog/ "Changelog")
    - [Deprecated](https://docs.docker.com/reference/api/hub/deprecated/ "Deprecated")
  + DVP Data API

    - [Latest](https://docs.docker.com/reference/api/dvp/latest/ "Latest")
    - [Changelog](https://docs.docker.com/reference/api/dvp/changelog/ "Changelog")
    - [Deprecated](https://docs.docker.com/reference/api/dvp/deprecated/ "Deprecated")
  + [Extensions API](https://docs.docker.com/reference/api/extensions-sdk/)

    - [Interface: BackendV0](https://docs.docker.com/reference/api/extensions-sdk/BackendV0/ "Interface: BackendV0")
    - [Interface: DesktopUI](https://docs.docker.com/reference/api/extensions-sdk/DesktopUI/ "Interface: DesktopUI")
    - [Interface: Dialog](https://docs.docker.com/reference/api/extensions-sdk/Dialog/ "Interface: Dialog")
    - [Interface: Docker](https://docs.docker.com/reference/api/extensions-sdk/Docker/ "Interface: Docker")
    - [Interface: DockerCommand](https://docs.docker.com/reference/api/extensions-sdk/DockerCommand/ "Interface: DockerCommand")
    - [Interface: DockerDesktopClient](https://docs.docker.com/reference/api/extensions-sdk/DockerDesktopClient/ "Interface: DockerDesktopClient")
    - [Interface: Exec](https://docs.docker.com/reference/api/extensions-sdk/Exec/ "Interface: Exec")
    - [Interface: ExecOptions](https://docs.docker.com/reference/api/extensions-sdk/ExecOptions/ "Interface: ExecOptions")
    - [Interface: ExecProcess](https://docs.docker.com/reference/api/extensions-sdk/ExecProcess/ "Interface: ExecProcess")
    - [Interface: ExecResult](https://docs.docker.com/reference/api/extensions-sdk/ExecResult/ "Interface: ExecResult")
    - [Interface: ExecResultV0](https://docs.docker.com/reference/api/extensions-sdk/ExecResultV0/ "Interface: ExecResultV0")
    - [Interface: ExecStreamOptions](https://docs.docker.com/reference/api/extensions-sdk/ExecStreamOptions/ "Interface: ExecStreamOptions")
    - [Interface: Extension](https://docs.docker.com/reference/api/extensions-sdk/Extension/ "Interface: Extension")
    - [Interface: ExtensionCli](https://docs.docker.com/reference/api/extensions-sdk/ExtensionCli/ "Interface: ExtensionCli")
    - [Interface: ExtensionHost](https://docs.docker.com/reference/api/extensions-sdk/ExtensionHost/ "Interface: ExtensionHost")
    - [Interface: ExtensionVM](https://docs.docker.com/reference/api/extensions-sdk/ExtensionVM/ "Interface: ExtensionVM")
    - [Interface: Host](https://docs.docker.com/reference/api/extensions-sdk/Host/ "Interface: Host")
    - [Interface: HttpService](https://docs.docker.com/reference/api/extensions-sdk/HttpService/ "Interface: HttpService")
    - [Interface: NavigationIntents](https://docs.docker.com/reference/api/extensions-sdk/NavigationIntents/ "Interface: NavigationIntents")
    - [Interface: OpenDialogResult](https://docs.docker.com/reference/api/extensions-sdk/OpenDialogResult/ "Interface: OpenDialogResult")
    - [Interface: RawExecResult](https://docs.docker.com/reference/api/extensions-sdk/RawExecResult/ "Interface: RawExecResult")
    - [Interface: RequestConfig](https://docs.docker.com/reference/api/extensions-sdk/RequestConfig/ "Interface: RequestConfig")
    - [Interface: RequestConfigV0](https://docs.docker.com/reference/api/extensions-sdk/RequestConfigV0/ "Interface: RequestConfigV0")
    - [Interface: ServiceError](https://docs.docker.com/reference/api/extensions-sdk/ServiceError/ "Interface: ServiceError")
    - [Interface: SpawnOptions](https://docs.docker.com/reference/api/extensions-sdk/SpawnOptions/ "Interface: SpawnOptions")
    - [Interface: Toast](https://docs.docker.com/reference/api/extensions-sdk/Toast/ "Interface: Toast")
  + Registry API

    - [Latest](https://docs.docker.com/reference/api/registry/latest/ "Latest")
    - [Registry authentication](https://docs.docker.com/reference/api/registry/auth/ "Registry authentication")
* [Build checks](https://docs.docker.com/reference/build-checks/)

  + [ConsistentInstructionCasing](https://docs.docker.com/reference/build-checks/consistent-instruction-casing/ "ConsistentInstructionCasing")
  + [CopyIgnoredFile](https://docs.docker.com/reference/build-checks/copy-ignored-file/ "CopyIgnoredFile")
  + [DuplicateStageName](https://docs.docker.com/reference/build-checks/duplicate-stage-name/ "DuplicateStageName")
  + [ExposeInvalidFormat](https://docs.docker.com/reference/build-checks/expose-invalid-format/ "ExposeInvalidFormat")
  + [ExposeProtoCasing](https://docs.docker.com/reference/build-checks/expose-proto-casing/ "ExposeProtoCasing")
  + [FromAsCasing](https://docs.docker.com/reference/build-checks/from-as-casing/ "FromAsCasing")
  + [FromPlatformFlagConstDisallowed](https://docs.docker.com/reference/build-checks/from-platform-flag-const-disallowed/ "FromPlatformFlagConstDisallowed")
  + [InvalidDefaultArgInFrom](https://docs.docker.com/reference/build-checks/invalid-default-arg-in-from/ "InvalidDefaultArgInFrom")
  + [InvalidDefinitionDescription](https://docs.docker.com/reference/build-checks/invalid-definition-description/ "InvalidDefinitionDescription")
  + [JSONArgsRecommended](https://docs.docker.com/reference/build-checks/json-args-recommended/ "JSONArgsRecommended")
  + [LegacyKeyValueFormat](https://docs.docker.com/reference/build-checks/legacy-key-value-format/ "LegacyKeyValueFormat")
  + [MaintainerDeprecated](https://docs.docker.com/reference/build-checks/maintainer-deprecated/ "MaintainerDeprecated")
  + [MultipleInstructionsDisallowed](https://docs.docker.com/reference/build-checks/multiple-instructions-disallowed/ "MultipleInstructionsDisallowed")
  + [NoEmptyContinuation](https://docs.docker.com/reference/build-checks/no-empty-continuation/ "NoEmptyContinuation")
  + [RedundantTargetPlatform](https://docs.docker.com/reference/build-checks/redundant-target-platform/ "RedundantTargetPlatform")
  + [ReservedStageName](https://docs.docker.com/reference/build-checks/reserved-stage-name/ "ReservedStageName")
  + [SecretsUsedInArgOrEnv](https://docs.docker.com/reference/build-checks/secrets-used-in-arg-or-env/ "SecretsUsedInArgOrEnv")
  + [StageNameCasing](https://docs.docker.com/reference/build-checks/stage-name-casing/ "StageNameCasing")
  + [UndefinedArgInFrom](https://docs.docker.com/reference/build-checks/undefined-arg-in-from/ "UndefinedArgInFrom")
  + [UndefinedVar](https://docs.docker.com/reference/build-checks/undefined-var/ "UndefinedVar")
  + [WorkdirRelativePath](https://docs.docker.com/reference/build-checks/workdir-relative-path/ "WorkdirRelativePath")
* [Compose file reference](https://docs.docker.com/reference/compose-file/)

  + [Version and name top-level elements](https://docs.docker.com/reference/compose-file/version-and-name/ "Version and name top-level elements")
  + [Services](https://docs.docker.com/reference/compose-file/services/ "Services")
  + [Networks](https://docs.docker.com/reference/compose-file/networks/ "Networks")
  + [Volumes](https://docs.docker.com/reference/compose-file/volumes/ "Volumes")
  + [Configs](https://docs.docker.com/reference/compose-file/configs/ "Configs")
  + [Secrets](https://docs.docker.com/reference/compose-file/secrets/ "Secrets")
  + [Fragments](https://docs.docker.com/reference/compose-file/fragments/ "Fragments")
  + [Extensions](https://docs.docker.com/reference/compose-file/extension/ "Extensions")
  + [Interpolation](https://docs.docker.com/reference/compose-file/interpolation/ "Interpolation")
  + [Merge](https://docs.docker.com/reference/compose-file/merge/ "Merge")
  + [Include](https://docs.docker.com/reference/compose-file/include/ "Include")
  + [Models](https://docs.docker.com/reference/compose-file/models/ "Models")
  + [Profiles](https://docs.docker.com/reference/compose-file/profiles/ "Profiles")
  + [Compose Build Specification](https://docs.docker.com/reference/compose-file/build/ "Compose Build Specification")
  + [Compose Deploy Specification](https://docs.docker.com/reference/compose-file/deploy/ "Compose Deploy Specification")
  + [Compose Develop Specification](https://docs.docker.com/reference/compose-file/develop/ "Compose Develop Specification")
  + [Legacy versions](https://docs.docker.com/reference/compose-file/legacy-versions/ "Legacy versions")
* [Dockerfile reference](https://docs.docker.com/reference/dockerfile/ "Dockerfile reference")
* [Glossary](https://docs.docker.com/reference/glossary/ "Glossary")
* [Samples](https://docs.docker.com/reference/samples/)

  + [.NET samples](https://docs.docker.com/reference/samples/dotnet/ ".NET samples")
  + [Agentic AI samples](https://docs.docker.com/reference/samples/agentic-ai/ "Agentic AI samples")
  + [AI/ML samples](https://docs.docker.com/reference/samples/ai-ml/ "AI/ML samples")
  + [Angular samples](https://docs.docker.com/reference/samples/angular/ "Angular samples")
  + [Cloudflared samples](https://docs.docker.com/reference/samples/cloudflared/ "Cloudflared samples")
  + [Django samples](https://docs.docker.com/reference/samples/django/ "Django samples")
  + [Elasticsearch / Logstash / Kibana samples](https://docs.docker.com/reference/samples/elasticsearch/ "Elasticsearch / Logstash / Kibana samples")
  + [Express samples](https://docs.docker.com/reference/samples/express/ "Express samples")
  + [FastAPI samples](https://docs.docker.com/reference/samples/fastapi/ "FastAPI samples")
  + [Flask samples](https://docs.docker.com/reference/samples/flask/ "Flask samples")
  + [Gitea samples](https://docs.docker.com/reference/samples/gitea/ "Gitea samples")
  + [Go samples](https://docs.docker.com/reference/samples/go/ "Go samples")
  + [Java samples](https://docs.docker.com/reference/samples/java/ "Java samples")
  + [JavaScript samples](https://docs.docker.com/reference/samples/javascript/ "JavaScript samples")
  + [MariaDB samples](https://docs.docker.com/reference/samples/mariadb/ "MariaDB samples")
  + [Minecraft samples](https://docs.docker.com/reference/samples/minecraft/ "Minecraft samples")
  + [MongoDB samples](https://docs.docker.com/reference/samples/mongodb/ "MongoDB samples")
  + [MS-SQL samples](https://docs.docker.com/reference/samples/ms-sql/ "MS-SQL samples")
  + [MySQL samples](https://docs.docker.com/reference/samples/mysql/ "MySQL samples")
  + [Nextcloud samples](https://docs.docker.com/reference/samples/nextcloud/ "Nextcloud samples")
  + [NGINX samples](https://docs.docker.com/reference/samples/nginx/ "NGINX samples")
  + [Node.js samples](https://docs.docker.com/reference/samples/nodejs/ "Node.js samples")
  + [PHP samples](https://docs.docker.com/reference/samples/php/ "PHP samples")
  + [Pi-hole samples](https://docs.docker.com/reference/samples/pi-hole/ "Pi-hole samples")
  + [Plex samples](https://docs.docker.com/reference/samples/plex/ "Plex samples")
  + [Portainer samples](https://docs.docker.com/reference/samples/portainer/ "Portainer samples")
  + [PostgreSQL samples](https://docs.docker.com/reference/samples/postgres/ "PostgreSQL samples")
  + [Prometheus samples](https://docs.docker.com/reference/samples/prometheus/ "Prometheus samples")
  + [Python samples](https://docs.docker.com/reference/samples/python/ "Python samples")
  + [Rails samples](https://docs.docker.com/reference/samples/rails/ "Rails samples")
  + [React samples](https://docs.docker.com/reference/samples/react/ "React samples")
  + [Redis samples](https://docs.docker.com/reference/samples/redis/ "Redis samples")
  + [Ruby samples](https://docs.docker.com/reference/samples/ruby/ "Ruby samples")
  + [Rust samples](https://docs.docker.com/reference/samples/rust/ "Rust samples")
  + [Spark samples](https://docs.docker.com/reference/samples/spark/ "Spark samples")
  + [Spring Boot samples](https://docs.docker.com/reference/samples/spring/ "Spring Boot samples")
  + [Traefik samples](https://docs.docker.com/reference/samples/traefik/ "Traefik samples")
  + [TypeScript samples](https://docs.docker.com/reference/samples/typescript/ "TypeScript samples")
  + [Vue.js samples](https://docs.docker.com/reference/samples/vuejs/ "Vue.js samples")
  + [WireGuard samples](https://docs.docker.com/reference/samples/wireguard/ "WireGuard samples")
  + [WordPress samples](https://docs.docker.com/reference/samples/wordpress/ "WordPress samples")

[Home](https://docs.docker.com/)
/
[Reference](https://docs.docker.com/reference/)
/
Dockerfile reference

# Dockerfile reference

Copy as Markdown

Open Markdown

Ask Docs AI

Claude
Open in Claude

function getCurrentPlaintextUrl(){const e=window.location.href.split("#")[0].replace(/\/$/,"");return`${e}.md`}function copyMarkdown(){fetch(getCurrentPlaintextUrl()).then(e=>e.text()).then(e=>{navigator.clipboard.writeText(e).then(()=>{const e=document.querySelector('[data-heap-id="copy-markdown-button"]');if(!e)return;const t=e.querySelectorAll(".icon-svg"),n=t[0],s=t[1];n.classList.add("hidden"),s.classList.remove("hidden"),setTimeout(()=>{n.classList.remove("hidden"),s.classList.add("hidden")},2e3)})}).catch(e=>{console.error("Error copying markdown:",e)})}function viewPlainText(){window.open(getCurrentPlaintextUrl(),"\_blank")}function openInDocsAI(){const e=document.querySelector(".open-kapa-widget");e?e.click():alert("Couldn't find Docs AI.")}function openInClaude(){const e=getCurrentPlaintextUrl(),t=`Read ${e} so I can ask questions about it.`,n=encodeURIComponent(t),s=`https://claude.ai/new?q=${n}`;window.open(s,"\_blank")}

Table of contents

* [Overview](#overview)
* [Format](#format)
* [Parser directives](#parser-directives)

+ [syntax](#syntax)
+ [escape](#escape)
+ [check](#check)

* [Environment replacement](#environment-replacement)
* [.dockerignore file](#dockerignore-file)
* [Shell and exec form](#shell-and-exec-form)

+ [Exec form](#exec-form)

+ [Shell form](#shell-form)
+ [Use a different shell](#use-a-different-shell)

* [FROM](#from)

+ [Understand how ARG and FROM interact](#understand-how-arg-and-from-interact)

* [RUN](#run)

+ [Cache invalidation for RUN instructions](#cache-invalidation-for-run-instructions)
+ [RUN --device](#run---device)

+ [RUN --mount](#run---mount)
+ [RUN --mount=type=bind](#run---mounttypebind)
+ [RUN --mount=type=cache](#run---mounttypecache)

+ [RUN --mount=type=tmpfs](#run---mounttypetmpfs)
+ [RUN --mount=type=secret](#run---mounttypesecret)

+ [RUN --mount=type=ssh](#run---mounttypessh)

+ [RUN --network](#run---network)
+ [RUN --network=default](#run---networkdefault)
+ [RUN --network=none](#run---networknone)

+ [RUN --network=host](#run---networkhost)
+ [RUN --security](#run---security)

* [CMD](#cmd)
* [LABEL](#label)
* [MAINTAINER (deprecated)](#maintainer-deprecated)
* [EXPOSE](#expose)
* [ENV](#env)
* [ADD](#add)

+ [Source](#source)

+ [Destination](#destination)
+ [ADD --keep-git-dir](#add---keep-git-dir)
+ [ADD --checksum](#add---checksum)
+ [ADD --chmod](#add---chmod)
+ [ADD --chown](#add---chown)
+ [ADD --link](#add---link)
+ [ADD --unpack](#add---unpack)
+ [ADD --exclude](#add---exclude)

* [COPY](#copy)

+ [Source](#source-1)

+ [Destination](#destination-1)
+ [COPY --from](#copy---from)
+ [COPY --chmod](#copy---chmod)
+ [COPY --chown](#copy---chown)
+ [COPY --link](#copy---link)

+ [COPY --parents](#copy---parents)
+ [COPY --exclude](#copy---exclude)

* [ENTRYPOINT](#entrypoint)

+ [Exec form ENTRYPOINT example](#exec-form-entrypoint-example)
+ [Shell form ENTRYPOINT example](#shell-form-entrypoint-example)
+ [Understand how CMD and ENTRYPOINT interact](#understand-how-cmd-and-entrypoint-interact)

* [VOLUME](#volume)

+ [Notes about specifying volumes](#notes-about-specifying-volumes)

* [USER](#user)
* [WORKDIR](#workdir)
* [ARG](#arg)

+ [Default values](#default-values)
+ [Scope](#scope)
+ [Using ARG variables](#using-arg-variables)
+ [Predefined ARGs](#predefined-args)
+ [Automatic platform ARGs in the global scope](#automatic-platform-args-in-the-global-scope)
+ [BuildKit built-in build args](#buildkit-built-in-build-args)

+ [Impact on build caching](#impact-on-build-caching)

* [ONBUILD](#onbuild)

+ [Copy or mount from stage, image, or context](#copy-or-mount-from-stage-image-or-context)
+ [ONBUILD limitations](#onbuild-limitations)

* [STOPSIGNAL](#stopsignal)
* [HEALTHCHECK](#healthcheck)
* [SHELL](#shell)
* [Here-Documents](#here-documents)

+ [Example: Running a multi-line script](#example-running-a-multi-line-script)
+ [Example: Creating inline files](#example-creating-inline-files)

* [Dockerfile examples](#dockerfile-examples)

---

Docker can build images automatically by reading the instructions from a
Dockerfile. A Dockerfile is a text document that contains all the commands a
user could call on the command line to assemble an image. This page describes
the commands you can use in a Dockerfile.

## [Overview](#overview)

The Dockerfile supports the following instructions:

| Instruction | Description |
| --- | --- |
| [`ADD`](#add) | Add local or remote files and directories. |
| [`ARG`](#arg) | Use build-time variables. |
| [`CMD`](#cmd) | Specify default commands. |
| [`COPY`](#copy) | Copy files and directories. |
| [`ENTRYPOINT`](#entrypoint) | Specify default executable. |
| [`ENV`](#env) | Set environment variables. |
| [`EXPOSE`](#expose) | Describe which ports your application is listening on. |
| [`FROM`](#from) | Create a new build stage from a base image. |
| [`HEALTHCHECK`](#healthcheck) | Check a container's health on startup. |
| [`LABEL`](#label) | Add metadata to an image. |
| [`MAINTAINER`](#maintainer-deprecated) | Specify the author of an image. |
| [`ONBUILD`](#onbuild) | Specify instructions for when the image is used in a build. |
| [`RUN`](#run) | Execute build commands. |
| [`SHELL`](#shell) | Set the default shell of an image. |
| [`STOPSIGNAL`](#stopsignal) | Specify the system call signal for exiting a container. |
| [`USER`](#user) | Set user and group ID. |
| [`VOLUME`](#volume) | Create volume mounts. |
| [`WORKDIR`](#workdir) | Change working directory. |

## [Format](#format)

Here is the format of the Dockerfile:

```
# Comment
INSTRUCTION arguments
```

The instruction is not case-sensitive. However, convention is for them to
be UPPERCASE to distinguish them from arguments more easily.

Docker runs instructions in a Dockerfile in order. A Dockerfile **must
begin with a `FROM` instruction**. This may be after [parser
directives](#parser-directives), [comments](#format), and globally scoped
[ARGs](#arg). The `FROM` instruction specifies the [base
image](https://docs.docker.com/glossary/#base-image) from which you are
building. `FROM` may only be preceded by one or more `ARG` instructions, which
declare arguments that are used in `FROM` lines in the Dockerfile.

BuildKit treats lines that begin with `#` as a comment, unless the line is
a valid [parser directive](#parser-directives). A `#` marker anywhere
else in a line is treated as an argument. This allows statements like:

```
# Comment
RUN echo 'we are running some # of cool things'
```

Comment lines are removed before the Dockerfile instructions are executed.
The comment in the following example is removed before the shell executes
the `echo` command.

```
RUN echo hello \
# comment
world
```

The following examples is equivalent.

```
RUN echo hello \
world
```

Comments don't support line continuation characters.

> Note
>
> **Note on whitespace**
>
> For backward compatibility, leading whitespace before comments (`#`) and
> instructions (such as `RUN`) are ignored, but discouraged. Leading whitespace
> is not preserved in these cases, and the following examples are therefore
> equivalent:
>
> ```
>         # this is a comment-line
>     RUN echo hello
> RUN echo world
> ```
>
> ```
> # this is a comment-line
> RUN echo hello
> RUN echo world
> ```
>
> Whitespace in instruction arguments, however, isn't ignored.
> The following example prints `hello world`
> with leading whitespace as specified:
>
> ```
> RUN echo "\
>      hello\
>      world"
> ```

## [Parser directives](#parser-directives)

Parser directives are optional, and affect the way in which subsequent lines
in a Dockerfile are handled. Parser directives don't add layers to the build,
and don't show up as build steps. Parser directives are written as a
special type of comment in the form `# directive=value`. A single directive
may only be used once.

The following parser directives are supported:

* [`syntax`](#syntax)
* [`escape`](#escape)
* [`check`](#check) (since Dockerfile v1.8.0)

Once a comment, empty line or builder instruction has been processed, BuildKit
no longer looks for parser directives. Instead it treats anything formatted
as a parser directive as a comment and doesn't attempt to validate if it might
be a parser directive. Therefore, all parser directives must be at the
top of a Dockerfile.

Parser directive keys, such as `syntax` or `check`, aren't case-sensitive, but
they're lowercase by convention. Values for a directive are case-sensitive and
must be written in the appropriate case for the directive. For example,
`#check=skip=jsonargsrecommended` is invalid because the check name must use
Pascal case, not lowercase. It's also conventional to include a blank line
following any parser directives. Line continuation characters aren't supported
in parser directives.

Due to these rules, the following examples are all invalid:

Invalid due to line continuation:

```
# direc \
tive=value
```

Invalid due to appearing twice:

```
# directive=value1
# directive=value2

FROM ImageName
```

Treated as a comment because it appears after a builder instruction:

```
FROM ImageName
# directive=value
```

Treated as a comment because it appears after a comment that isn't a parser
directive:

```
# About my dockerfile
# directive=value
FROM ImageName
```

The following `unknowndirective` is treated as a comment because it isn't
recognized. The known `syntax` directive is treated as a comment because it
appears after a comment that isn't a parser directive.

```
# unknowndirective=value
# syntax=value
```

Non line-breaking whitespace is permitted in a parser directive. Hence, the
following lines are all treated identically:

```
#directive=value
# directive =value
#	directive= value
# directive = value
#	  dIrEcTiVe=value
```

### [syntax](#syntax)

Use the `syntax` parser directive to declare the Dockerfile syntax version to
use for the build. If unspecified, BuildKit uses a bundled version of the
Dockerfile frontend. Declaring a syntax version lets you automatically use the
latest Dockerfile version without having to upgrade BuildKit or Docker Engine,
or even use a custom Dockerfile implementation.

Most users will want to set this parser directive to `docker/dockerfile:1`,
which causes BuildKit to pull the latest stable version of the Dockerfile
syntax before the build.

```
# syntax=docker/dockerfile:1
```

For more information about how the parser directive works, see
[Custom Dockerfile syntax](https://docs.docker.com/build/buildkit/dockerfile-frontend/).

### [escape](#escape)

```
# escape=\
```

Or

```
# escape=`
```

The `escape` directive sets the character used to escape characters in a
Dockerfile. If not specified, the default escape character is `\`.

The escape character is used both to escape characters in a line, and to
escape a newline. This allows a Dockerfile instruction to
span multiple lines. Note that regardless of whether the `escape` parser
directive is included in a Dockerfile, escaping is not performed in
a `RUN` command, except at the end of a line.

Setting the escape character to `` ` `` is especially useful on
`Windows`, where `\` is the directory path separator. `` ` `` is consistent
with [Windows PowerShell](https://technet.microsoft.com/en-us/library/hh847755.aspx).

Consider the following example which would fail in a non-obvious way on
Windows. The second `\` at the end of the second line would be interpreted as an
escape for the newline, instead of a target of the escape from the first `\`.
Similarly, the `\` at the end of the third line would, assuming it was actually
handled as an instruction, cause it be treated as a line continuation. The result
of this Dockerfile is that second and third lines are considered a single
instruction:

```
FROM microsoft/nanoserver
COPY testfile.txt c:\\
RUN dir c:\
```

Results in:

```
PS E:\myproject> docker build -t cmd .

Sending build context to Docker daemon 3.072 kB
Step 1/2 : FROM microsoft/nanoserver
 ---> 22738ff49c6d
Step 2/2 : COPY testfile.txt c:\RUN dir c:
GetFileAttributesEx c:RUN: The system cannot find the file specified.
PS E:\myproject>
```

One solution to the above would be to use `/` as the target of both the `COPY`
instruction, and `dir`. However, this syntax is, at best, confusing as it is not
natural for paths on Windows, and at worst, error prone as not all commands on
Windows support `/` as the path separator.

By adding the `escape` parser directive, the following Dockerfile succeeds as
expected with the use of natural platform semantics for file paths on Windows:

```
# escape=`

FROM microsoft/nanoserver
COPY testfile.txt c:\
RUN dir c:\
```

Results in:

```
PS E:\myproject> docker build -t succeeds --no-cache=true .

Sending build context to Docker daemon 3.072 kB
Step 1/3 : FROM microsoft/nanoserver
 ---> 22738ff49c6d
Step 2/3 : COPY testfile.txt c:\
 ---> 96655de338de
Removing intermediate container 4db9acbb1682
Step 3/3 : RUN dir c:\
 ---> Running in a2c157f842f5
 Volume in drive C has no label.
 Volume Serial Number is 7E6D-E0F7

 Directory of c:\

10/05/2016  05:04 PM             1,894 License.txt
10/05/2016  02:22 PM    <DIR>          Program Files
10/05/2016  02:14 PM    <DIR>          Program Files (x86)
10/28/2016  11:18 AM                62 testfile.txt
10/28/2016  11:20 AM    <DIR>          Users
10/28/2016  11:20 AM    <DIR>          Windows
           2 File(s)          1,956 bytes
           4 Dir(s)  21,259,096,064 bytes free
 ---> 01c7f3bef04f
Removing intermediate container a2c157f842f5
Successfully built 01c7f3bef04f
PS E:\myproject>
```

### [check](#check)

```
# check=skip=<checks|all>
# check=error=<boolean>
```

The `check` directive is used to configure how [build checks](https://docs.docker.com/build/checks/)
are evaluated. By default, all checks are run, and failures are treated as
warnings.

You can disable specific checks using `#check=skip=<check-name>`. To specify
multiple checks to skip, separate them with a comma:

```
# check=skip=JSONArgsRecommended,StageNameCasing
```

To disable all checks, use `#check=skip=all`.

By default, builds with failing build checks exit with a zero status code
despite warnings. To make the build fail on warnings, set `#check=error=true`.

```
# check=error=true
```

> Note
>
> When using the `check` directive, with `error=true` option, it is recommended
> to pin the [Dockerfile syntax](#syntax) to a specific version. Otherwise, your build may
> start to fail when new checks are added in the future versions.

To combine both the `skip` and `error` options, use a semi-colon to separate
them:

```
# check=skip=JSONArgsRecommended;error=true
```

To see all available checks, see the [build checks reference](https://docs.docker.com/reference/build-checks/).
Note that the checks available depend on the Dockerfile syntax version. To make
sure you're getting the most up-to-date checks, use the [`syntax`](#syntax)
directive to specify the Dockerfile syntax version to the latest stable
version.

## [Environment replacement](#environment-replacement)

Environment variables (declared with [the `ENV` statement](#env)) can also be
used in certain instructions as variables to be interpreted by the
Dockerfile. Escapes are also handled for including variable-like syntax
into a statement literally.

Environment variables are notated in the Dockerfile either with
`$variable_name` or `${variable_name}`. They are treated equivalently and the
brace syntax is typically used to address issues with variable names with no
whitespace, like `${foo}_bar`.

The `${variable_name}` syntax also supports a few of the standard `bash`
modifiers as specified below:

* `${variable:-word}` indicates that if `variable` is set and non-empty then
  the result will be that value. If `variable` is unset or empty then `word`
  will be the result.
* `${variable-word}` indicates that if `variable` is set (even if empty) then
  the result will be that value. If `variable` is unset then `word` will be
  the result.
* `${variable:+word}` indicates that if `variable` is set and non-empty then
  `word` will be the result, otherwise the result is the empty string.
* `${variable+word}` indicates that if `variable` is set (even if empty) then
  `word` will be the result, otherwise the result is the empty string.

The following variable replacements are supported in a pre-release version of
Dockerfile syntax, when using the `# syntax=docker/dockerfile-upstream:master` syntax
directive in your Dockerfile:

* `${variable#pattern}` removes the shortest match of `pattern` from `variable`,
  seeking from the start of the string.

  ```
  str=foobarbaz echo ${str#f*b}     # arbaz
  ```
* `${variable##pattern}` removes the longest match of `pattern` from `variable`,
  seeking from the start of the string.

  ```
  str=foobarbaz echo ${str##f*b}    # az
  ```
* `${variable%pattern}` removes the shortest match of `pattern` from `variable`,
  seeking backwards from the end of the string.

  ```
  string=foobarbaz echo ${string%b*}    # foobar
  ```
* `${variable%%pattern}` removes the longest match of `pattern` from `variable`,
  seeking backwards from the end of the string.

  ```
  string=foobarbaz echo ${string%%b*}   # foo
  ```
* `${variable/pattern/replacement}` replace the first occurrence of `pattern`
  in `variable` with `replacement`

  ```
  string=foobarbaz echo ${string/ba/fo}  # fooforbaz
  ```
* `${variable//pattern/replacement}` replaces all occurrences of `pattern`
  in `variable` with `replacement`

  ```
  string=foobarbaz echo ${string//ba/fo}  # fooforfoz
  ```

In all cases, `word` can be any string, including additional environment
variables.

`pattern` is a glob pattern where `?` matches any single character
and `*` any number of characters (including zero). To match literal `?` and `*`,
use a backslash escape: `\?` and `\*`.

You can escape whole variable names by adding a `\` before the variable: `\$foo` or `\${foo}`,
for example, will translate to `$foo` and `${foo}` literals respectively.

Example (parsed representation is displayed after the `#`):

```
FROM busybox
ENV FOO=/bar
WORKDIR ${FOO}   # WORKDIR /bar
ADD . $FOO       # ADD . /bar
COPY \$FOO /quux # COPY $FOO /quux
```

Environment variables are supported by the following list of instructions in
the Dockerfile:

* `ADD`
* `COPY`
* `ENV`
* `EXPOSE`
* `FROM`
* `LABEL`
* `STOPSIGNAL`
* `USER`
* `VOLUME`
* `WORKDIR`
* `ONBUILD` (when combined with one of the supported instructions above)

You can also use environment variables with `RUN`, `CMD`, and `ENTRYPOINT`
instructions, but in those cases the variable substitution is handled by the
command shell, not the builder. Note that instructions using the exec form
don't invoke a command shell automatically. See [Variable
substitution](#variable-substitution).

Environment variable substitution use the same value for each variable
throughout the entire instruction. Changing the value of a variable only takes
effect in subsequent instructions. Consider the following example:

```
ENV abc=hello
ENV abc=bye def=$abc
ENV ghi=$abc
```

* The value of `def` becomes `hello`
* The value of `ghi` becomes `bye`

## [.dockerignore file](#dockerignore-file)

You can use `.dockerignore` file to exclude files and directories from the
build context. For more information, see
[.dockerignore file](https://docs.docker.com/build/building/context/#dockerignore-files).

## [Shell and exec form](#shell-and-exec-form)

The `RUN`, `CMD`, and `ENTRYPOINT` instructions all have two possible forms:

* `INSTRUCTION ["executable","param1","param2"]` (exec form)
* `INSTRUCTION command param1 param2` (shell form)

The exec form makes it possible to avoid shell string munging, and to invoke
commands using a specific command shell, or any other executable. It uses a
JSON array syntax, where each element in the array is a command, flag, or
argument.

The shell form is more relaxed, and emphasizes ease of use, flexibility, and
readability. The shell form automatically uses a command shell, whereas the
exec form does not.

### [Exec form](#exec-form)

The exec form is parsed as a JSON array, which means that
you must use double-quotes (") around words, not single-quotes (').

```
ENTRYPOINT ["/bin/bash", "-c", "echo hello"]
```

The exec form is best used to specify an `ENTRYPOINT` instruction, combined
with `CMD` for setting default arguments that can be overridden at runtime. For
more information, see [ENTRYPOINT](#entrypoint).

#### [Variable substitution](#variable-substitution)

Using the exec form doesn't automatically invoke a command shell. This means
that normal shell processing, such as variable substitution, doesn't happen.
For example, `RUN [ "echo", "$HOME" ]` won't handle variable substitution for
`$HOME`.

If you want shell processing then either use the shell form or execute a shell
directly with the exec form, for example: `RUN [ "sh", "-c", "echo $HOME" ]`.
When using the exec form and executing a shell directly, as in the case for the
shell form, it's the shell that's doing the environment variable substitution,
not the builder.

#### [Backslashes](#backslashes)

In exec form, you must escape backslashes. This is particularly relevant on
Windows where the backslash is the path separator. The following line would
otherwise be treated as shell form due to not being valid JSON, and fail in an
unexpected way:

```
RUN ["c:\windows\system32\tasklist.exe"]
```

The correct syntax for this example is:

```
RUN ["c:\\windows\\system32\\tasklist.exe"]
```

### [Shell form](#shell-form)

Unlike the exec form, instructions using the shell form always use a command
shell. The shell form doesn't use the JSON array format, instead it's a regular
string. The shell form string lets you escape newlines using the [escape
character](#escape) (backslash by default) to continue a single instruction
onto the next line. This makes it easier to use with longer commands, because
it lets you split them up into multiple lines. For example, consider these two
lines:

```
RUN source $HOME/.bashrc && \
echo $HOME
```

They're equivalent to the following line:

```
RUN source $HOME/.bashrc && echo $HOME
```

You can also use heredocs with the shell form to break up supported commands.

```
RUN <<EOF
  source $HOME/.bashrc
  echo $HOME
EOF
```

For more information about heredocs, see [Here-documents](#here-documents).

### [Use a different shell](#use-a-different-shell)

You can change the default shell using the `SHELL` command. For example:

```
SHELL ["/bin/bash", "-c"]
RUN echo hello
```

For more information, see [SHELL](#shell).

## [FROM](#from)

```
FROM [--platform=<platform>] <image> [AS <name>]
```

Or

```
FROM [--platform=<platform>] <image>[:<tag>] [AS <name>]
```

Or

```
FROM [--platform=<platform>] <image>[@<digest>] [AS <name>]
```

The `FROM` instruction initializes a new build stage and sets the
[base image](https://docs.docker.com/glossary/#base-image) for subsequent
instructions. As such, a valid Dockerfile must start with a `FROM` instruction.
The image can be any valid image.

* `ARG` is the only instruction that may precede `FROM` in the Dockerfile.
  See [Understand how ARG and FROM interact](#understand-how-arg-and-from-interact).
* `FROM` can appear multiple times within a single Dockerfile to
  create multiple images or use one build stage as a dependency for another.
  Simply make a note of the last image ID output by the commit before each new
  `FROM` instruction. Each `FROM` instruction clears any state created by previous
  instructions.
* Optionally a name can be given to a new build stage by adding `AS name` to the
  `FROM` instruction. The name can be used in subsequent `FROM <name>`,
  [`COPY --from=<name>`](#copy---from),
  and [`RUN --mount=type=bind,from=<name>`](#run---mounttypebind) instructions
  to refer to the image built in this stage.

  Using a previous build stage as the base for a subsequent stage is a common
  pattern for sharing a common base environment:

  ```
  FROM ubuntu AS base
  RUN apt-get update && apt-get install -y shared-tooling

  FROM base AS dev
  RUN apt-get install -y dev-tooling

  FROM base AS prod
  COPY --from=build /app /app
  ```
* The `tag` or `digest` values are optional. If you omit either of them, the
  builder assumes a `latest` tag by default. The builder returns an error if it
  can't find the `tag` value.

The optional `--platform` flag can be used to specify the platform of the image
in case `FROM` references a multi-platform image. For example, `linux/amd64`,
`linux/arm64`, or `windows/amd64`. By default, the target platform of the build
request is used. Global build arguments can be used in the value of this flag,
for example [automatic platform ARGs](#automatic-platform-args-in-the-global-scope)
allow you to force a stage to native build platform (`--platform=$BUILDPLATFORM`),
and use it to cross-compile to the target platform inside the stage.

### [Understand how ARG and FROM interact](#understand-how-arg-and-from-interact)

`FROM` instructions support variables that are declared by any `ARG`
instructions that occur before the first `FROM`.

```
ARG  CODE_VERSION=latest
FROM base:${CODE_VERSION}
CMD  /code/run-app

FROM extras:${CODE_VERSION}
CMD  /code/run-extras
```

An `ARG` declared before a `FROM` is outside of a build stage, so it
can't be used in any instruction after a `FROM`. To use the default value of
an `ARG` declared before the first `FROM` use an `ARG` instruction without
a value inside of a build stage:

```
ARG VERSION=latest
FROM busybox:$VERSION
ARG VERSION
RUN echo $VERSION > image_version
```

## [RUN](#run)

The `RUN` instruction will execute any commands to create a new layer on top of
the current image. The added layer is used in the next step in the Dockerfile.
`RUN` has two forms:

```
# Shell form:
RUN [OPTIONS] <command> ...
# Exec form:
RUN [OPTIONS] [ "<command>", ... ]
```

For more information about the differences between these two forms, see
[shell or exec forms](#shell-and-exec-form).

The shell form is most commonly used, and lets you break up longer
instructions into multiple lines, either using newline [escapes](#escape), or
with [heredocs](#here-documents):

```
RUN <<EOF
apt-get update
apt-get install -y curl
EOF
```

The available `[OPTIONS]` for the `RUN` instruction are:

| Option | Minimum Dockerfile version |
| --- | --- |
| [`--device`](#run---device) | 1.14-labs |
| [`--mount`](#run---mount) | 1.2 |
| [`--network`](#run---network) | 1.3 |
| [`--security`](#run---security) | 1.20 |

### [Cache invalidation for RUN instructions](#cache-invalidation-for-run-instructions)

The cache for `RUN` instructions isn't invalidated automatically during
the next build. The cache for an instruction like
`RUN apt-get dist-upgrade -y` will be reused during the next build. The
cache for `RUN` instructions can be invalidated by using the `--no-cache`
flag, for example `docker build --no-cache`.

See the [Dockerfile Best Practices
guide](https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/) for more information.

The cache for `RUN` instructions can be invalidated by [`ADD`](#add) and [`COPY`](#copy) instructions.

### [RUN --device](#run---device)

> Note
>
> Not yet available in stable syntax, use [`docker/dockerfile:1-labs`](#syntax)
> version. It also needs BuildKit 0.20.0 or later.

```
RUN --device=name,[required]
```

`RUN --device` allows build to request [CDI devices](https://github.com/moby/buildkit/blob/master/docs/cdi.md)
to be available to the build step.

> Warning
>
> The use of `--device` is protected by the `device` entitlement, which needs
> to be enabled when starting the buildkitd daemon with
> `--allow-insecure-entitlement device` flag or in [buildkitd config](https://github.com/moby/buildkit/blob/master/docs/buildkitd.toml.md),
> and for a build request with [`--allow device` flag](https://docs.docker.com/engine/reference/commandline/buildx_build/#allow).

The device `name` is provided by the CDI specification registered in BuildKit.

In the following example, multiple devices are registered in the CDI
specification for the `vendor1.com/device` vendor.

```
cdiVersion: "0.6.0"
kind: "vendor1.com/device"
devices:
  - name: foo
    containerEdits:
      env:
        - FOO=injected
  - name: bar
    annotations:
      org.mobyproject.buildkit.device.class: class1
    containerEdits:
      env:
        - BAR=injected
  - name: baz
    annotations:
      org.mobyproject.buildkit.device.class: class1
    containerEdits:
      env:
        - BAZ=injected
  - name: qux
    annotations:
      org.mobyproject.buildkit.device.class: class2
    containerEdits:
      env:
        - QUX=injected
annotations:
  org.mobyproject.buildkit.device.autoallow: true
```

The device name format is flexible and accepts various patterns to support
multiple device configurations:

* `vendor1.com/device`: request the first device found for this vendor
* `vendor1.com/device=foo`: request a specific device
* `vendor1.com/device=*`: request all devices for this vendor
* `class1`: request devices by `org.mobyproject.buildkit.device.class` annotation

> Note
>
> Annotations are supported by the CDI specification since 0.6.0.

> Note
>
> To automatically allow all devices registered in the CDI specification, you
> can set the `org.mobyproject.buildkit.device.autoallow` annotation. You can
> also set this annotation for a specific device.

#### [Example: CUDA-Powered LLaMA Inference](#example-cuda-powered-llama-inference)

In this example we use the `--device` flag to run `llama.cpp` inference using
an NVIDIA GPU device through CDI:

```
# syntax=docker/dockerfile:1-labs

FROM scratch AS model
ADD https://huggingface.co/bartowski/Llama-3.2-1B-Instruct-GGUF/resolve/main/Llama-3.2-1B-Instruct-Q4_K_M.gguf /model.gguf

FROM scratch AS prompt
COPY <<EOF prompt.txt
Q: Generate  a list of 10 unique biggest countries by population in JSON with their estimated poulation in 1900 and 2024. Answer only newline formatted JSON with keys "country", "population_1900", "population_2024" with 10 items.
A:
[
    {

EOF

FROM ghcr.io/ggml-org/llama.cpp:full-cuda-b5124
RUN --device=nvidia.com/gpu=all \
    --mount=from=model,target=/models \
    --mount=from=prompt,target=/tmp \
    ./llama-cli -m /models/model.gguf -no-cnv -ngl 99 -f /tmp/prompt.txt
```

### [RUN --mount](#run---mount)

```
RUN --mount=[type=<TYPE>][,option=<value>[,option=<value>]...]
```

`RUN --mount` allows you to create filesystem mounts that the build can access.
This can be used to:

* Create bind mount to the host filesystem or other build stages
* Access build secrets or ssh-agent sockets
* Use a persistent package management cache to speed up your build

The supported mount types are:

| Type | Description |
| --- | --- |
| [`bind`](#run---mounttypebind) (default) | Bind-mount context directories (read-only). |
| [`cache`](#run---mounttypecache) | Mount a temporary directory to cache directories for compilers and package managers. |
| [`tmpfs`](#run---mounttypetmpfs) | Mount a `tmpfs` in the build container. |
| [`secret`](#run---mounttypesecret) | Allow the build container to access secure files such as private keys without baking them into the image or build cache. |
| [`ssh`](#run---mounttypessh) | Allow the build container to access SSH keys via SSH agents, with support for passphrases. |

### [RUN --mount=type=bind](#run---mounttypebind)

This mount type allows binding files or directories to the build container. A
bind mount is read-only by default.

| Option | Description |
| --- | --- |
| `target`, `dst`, `destination`[1](#fn:1) | Mount path. |
| `source` | Source path in the `from`. Defaults to the root of the `from`. |
| `from` | Build stage, context, or image name for the root of the source. Defaults to the build context. |
| `rw`,`readwrite` | Allow writes on the mount. Written data will be discarded after the `RUN` instruction completes and will not be committed to the image layer. |

### [RUN --mount=type=cache](#run---mounttypecache)

This mount type allows the build container to cache directories for compilers
and package managers.

| Option | Description |
| --- | --- |
| `id` | Optional ID to identify separate/different caches. Defaults to value of `target`. |
| `target`, `dst`, `destination`[1](#fn:1) | Mount path. |
| `ro`,`readonly` | Read-only if set. |
| `sharing` | One of `shared`, `private`, or `locked`. Defaults to `shared`. A `shared` cache mount can be used concurrently by multiple writers. `private` creates a new mount if there are multiple writers. `locked` pauses the second writer until the first one releases the mount. |
| `from` | Build stage, context, or image name to use as a base of the cache mount. Defaults to empty directory. |
| `source` | Subpath in the `from` to mount. Defaults to the root of the `from`. |
| `mode` | File mode for new cache directory in octal. Default `0755`. |
| `uid` | User ID for new cache directory. Default `0`. |
| `gid` | Group ID for new cache directory. Default `0`. |

Contents of the cache directories persists between builder invocations without
invalidating the instruction cache. Cache mounts should only be used for better
performance. Your build should work with any contents of the cache directory as
another build may overwrite the files or GC may clean it if more storage space
is needed.

#### [Example: cache Go packages](#example-cache-go-packages)

```
# syntax=docker/dockerfile:1
FROM golang
RUN --mount=type=cache,target=/root/.cache/go-build \
  go build ...
```

#### [Example: cache apt packages](#example-cache-apt-packages)

```
# syntax=docker/dockerfile:1
FROM ubuntu
RUN rm -f /etc/apt/apt.conf.d/docker-clean; echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
  --mount=type=cache,target=/var/lib/apt,sharing=locked \
  apt-get update && apt-get --no-install-recommends install -y gcc
```

Apt needs exclusive access to its data, so the caches use the option
`sharing=locked`, which will make sure multiple parallel builds using
the same cache mount will wait for each other and not access the same
cache files at the same time. You could also use `sharing=private` if
you prefer to have each build create another cache directory in this
case.

### [RUN --mount=type=tmpfs](#run---mounttypetmpfs)

This mount type allows mounting `tmpfs` in the build container.

| Option | Description |
| --- | --- |
| `target`, `dst`, `destination`[1](#fn:1) | Mount path. |
| `size` | Specify an upper limit on the size of the filesystem. |

### [RUN --mount=type=secret](#run---mounttypesecret)

This mount type allows the build container to access secret values, such as
tokens or private keys, without baking them into the image.

By default, the secret is mounted as a file. You can also mount the secret as
an environment variable by setting the `env` option.

| Option | Description |
| --- | --- |
| `id` | ID of the secret. Defaults to basename of the target path. |
| `target`, `dst`, `destination` | Mount the secret to the specified path. Defaults to `/run/secrets/` + `id` if unset and if `env` is also unset. |
| `env` | Mount the secret to an environment variable instead of a file, or both. (since Dockerfile v1.10.0) |
| `required` | If set to `true`, the instruction errors out when the secret is unavailable. Defaults to `false`. |
| `mode` | File mode for secret file in octal. Default `0400`. |
| `uid` | User ID for secret file. Default `0`. |
| `gid` | Group ID for secret file. Default `0`. |

#### [Example: access to S3](#example-access-to-s3)

```
# syntax=docker/dockerfile:1
FROM python:3
RUN pip install awscli
RUN --mount=type=secret,id=aws,target=/root/.aws/credentials \
  aws s3 cp s3://... ...
```

```
$ docker buildx build --secret id=aws,src=$HOME/.aws/credentials .
```

#### [Example: Mount as environment variable](#example-mount-as-environment-variable)

The following example takes the secret `API_KEY` and mounts it as an
environment variable with the same name.

```
# syntax=docker/dockerfile:1
FROM alpine
RUN --mount=type=secret,id=API_KEY,env=API_KEY \
    some-command --token-from-env $API_KEY
```

Assuming that the `API_KEY` environment variable is set in the build
environment, you can build this with the following command:

```
$ docker buildx build --secret id=API_KEY .
```

### [RUN --mount=type=ssh](#run---mounttypessh)

This mount type allows the build container to access SSH keys via SSH agents,
with support for passphrases.

| Option | Description |
| --- | --- |
| `id` | ID of SSH agent socket or key. Defaults to "default". |
| `target`, `dst`, `destination` | SSH agent socket path. Defaults to `/run/buildkit/ssh_agent.${N}`. |
| `required` | If set to `true`, the instruction errors out when the key is unavailable. Defaults to `false`. |
| `mode` | File mode for socket in octal. Default `0600`. |
| `uid` | User ID for socket. Default `0`. |
| `gid` | Group ID for socket. Default `0`. |

#### [Example: access to GitLab](#example-access-to-gitlab)

```
# syntax=docker/dockerfile:1
FROM alpine
RUN apk add --no-cache openssh-client
RUN mkdir -p -m 0700 ~/.ssh && ssh-keyscan gitlab.com >> ~/.ssh/known_hosts
RUN --mount=type=ssh \
  ssh -q -T git@gitlab.com 2>&1 | tee /hello
# "Welcome to GitLab, @GITLAB_USERNAME_ASSOCIATED_WITH_SSHKEY" should be printed here
# with the type of build progress is defined as `plain`.
```

```
$ eval $(ssh-agent)
$ ssh-add ~/.ssh/id_rsa
(Input your passphrase here)
$ docker buildx build --ssh default=$SSH_AUTH_SOCK .
```

You can also specify a path to `*.pem` file on the host directly instead of `$SSH_AUTH_SOCK`.
However, pem files with passphrases are not supported.

### [RUN --network](#run---network)

```
RUN --network=<TYPE>
```

`RUN --network` allows control over which networking environment the command
is run in.

The supported network types are:

| Type | Description |
| --- | --- |
| [`default`](#run---networkdefault) (default) | Run in the default network. |
| [`none`](#run---networknone) | Run with no network access. |
| [`host`](#run---networkhost) | Run in the host's network environment. |

### [RUN --network=default](#run---networkdefault)

Equivalent to not supplying a flag at all, the command is run in the default
network for the build.

### [RUN --network=none](#run---networknone)

The command is run with no network access (`lo` is still available, but is
isolated to this process)

#### [Example: isolating external effects](#example-isolating-external-effects)

```
# syntax=docker/dockerfile:1
FROM python:3.6
ADD mypackage.tgz wheels/
RUN --network=none pip install --find-links wheels mypackage
```

`pip` will only be able to install the packages provided in the tarfile, which
can be controlled by an earlier build stage.

### [RUN --network=host](#run---networkhost)

The command is run in the host's network environment (similar to
`docker build --network=host`, but on a per-instruction basis)

> Warning
>
> The use of `--network=host` is protected by the `network.host` entitlement,
> which needs to be enabled when starting the buildkitd daemon with
> `--allow-insecure-entitlement network.host` flag or in [buildkitd config](https://github.com/moby/buildkit/blob/master/docs/buildkitd.toml.md),
> and for a build request with [`--allow network.host` flag](https://docs.docker.com/engine/reference/commandline/buildx_build/#allow).

### [RUN --security](#run---security)

```
RUN --security=<sandbox|insecure>
```

The default security mode is `sandbox`.
With `--security=insecure`, the builder runs the command without sandbox in insecure
mode, which allows to run flows requiring elevated privileges (e.g. containerd).
This is equivalent to running `docker run --privileged`.

> Warning
>
> In order to access this feature, entitlement `security.insecure` should be
> enabled when starting the buildkitd daemon with
> `--allow-insecure-entitlement security.insecure` flag or in [buildkitd config](https://github.com/moby/buildkit/blob/master/docs/buildkitd.toml.md),
> and for a build request with [`--allow security.insecure` flag](https://docs.docker.com/engine/reference/commandline/buildx_build/#allow).

Default sandbox mode can be activated via `--security=sandbox`, but that is no-op.

#### [Example: check entitlements](#example-check-entitlements)

```
# syntax=docker/dockerfile:1
FROM ubuntu
RUN --security=insecure cat /proc/self/status | grep CapEff
```

```
#84 0.093 CapEff:	0000003fffffffff
```

## [CMD](#cmd)

The `CMD` instruction sets the command to be executed when running a container
from an image.

You can specify `CMD` instructions using
[shell or exec forms](#shell-and-exec-form):

* `CMD ["executable","param1","param2"]` (exec form)
* `CMD ["param1","param2"]` (exec form, as default parameters to `ENTRYPOINT`)
* `CMD command param1 param2` (shell form)

There can only be one `CMD` instruction in a Dockerfile. If you list more than
one `CMD`, only the last one takes effect.

The purpose of a `CMD` is to provide defaults for an executing container. These
defaults can include an executable, or they can omit the executable, in which
case you must specify an `ENTRYPOINT` instruction as well.

If you would like your container to run the same executable every time, then
you should consider using `ENTRYPOINT` in combination with `CMD`. See
[`ENTRYPOINT`](#entrypoint). If the user specifies arguments to `docker run`
then they will override the default specified in `CMD`, but still use the
default `ENTRYPOINT`.

If `CMD` is used to provide default arguments for the `ENTRYPOINT` instruction,
both the `CMD` and `ENTRYPOINT` instructions should be specified in the
[exec form](#exec-form).

> Note
>
> Don't confuse `RUN` with `CMD`. `RUN` actually runs a command and commits
> the result; `CMD` doesn't execute anything at build time, but specifies
> the intended command for the image.

## [LABEL](#label)

```
LABEL <key>=<value> [<key>=<value>...]
```

The `LABEL` instruction adds metadata to an image. A `LABEL` is a
key-value pair. To include spaces within a `LABEL` value, use quotes and
backslashes as you would in command-line parsing. A few usage examples:

```
LABEL "com.example.vendor"="ACME Incorporated"
LABEL com.example.label-with-value="foo"
LABEL version="1.0"
LABEL description="This text illustrates \
that label-values can span multiple lines."
```

An image can have more than one label. You can specify multiple labels on a
single line. Prior to Docker 1.10, this decreased the size of the final image,
but this is no longer the case. You may still choose to specify multiple labels
in a single instruction, in one of the following two ways:

```
LABEL multi.label1="value1" multi.label2="value2" other="value3"
```

```
LABEL multi.label1="value1" \
      multi.label2="value2" \
      other="value3"
```

> Note
>
> Be sure to use double quotes and not single quotes. Particularly when you are
> using string interpolation (e.g. `LABEL example="foo-$ENV_VAR"`), single
> quotes will take the string as is without unpacking the variable's value.

Labels included in base images (images in the `FROM` line) are inherited by
your image. If a label already exists but with a different value, the
most-recently-applied value overrides any previously-set value.

In a multi-stage build, labels from intermediate stages are only present in
the final image if the final stage is directly or indirectly based on them
(via `FROM`). Labels from a stage that you only reference with
`COPY --from` or `RUN --mount=from=` are not included in the output image.
Labels from the base image specified in the final `FROM` instruction are
always inherited.

To view an image's labels, use the `docker image inspect` command. You can use
the `--format` option to show just the labels;

```
$ docker image inspect --format='{{json .Config.Labels}}' myimage
```

```
{
  "com.example.vendor": "ACME Incorporated",
  "com.example.label-with-value": "foo",
  "version": "1.0",
  "description": "This text illustrates that label-values can span multiple lines.",
  "multi.label1": "value1",
  "multi.label2": "value2",
  "other": "value3"
}
```

## [MAINTAINER (deprecated)](#maintainer-deprecated)

```
MAINTAINER <name>
```

The `MAINTAINER` instruction sets the *Author* field of the generated images.
The `LABEL` instruction is a much more flexible version of this and you should use
it instead, as it enables setting any metadata you require, and can be viewed
easily, for example with `docker inspect`. To set a label corresponding to the
`MAINTAINER` field you could use:

```
LABEL org.opencontainers.image.authors="SvenDowideit@home.org.au"
```

This will then be visible from `docker inspect` with the other labels.

## [EXPOSE](#expose)

```
EXPOSE <port> [<port>/<protocol>...]
```

The `EXPOSE` instruction informs Docker that the container listens on the
specified network ports at runtime. You can specify whether the port listens on
TCP or UDP, and the default is TCP if you don't specify a protocol.

The `EXPOSE` instruction doesn't actually publish the port. It functions as a
type of documentation between the person who builds the image and the person who
runs the container, about which ports are intended to be published. To
publish the port when running the container, use the `-p` flag on `docker run`
to publish and map one or more ports, or the `-P` flag to publish all exposed
ports and map them to high-order ports.

By default, `EXPOSE` assumes TCP. You can also specify UDP:

```
EXPOSE 80/udp
```

To expose on both TCP and UDP, include two lines:

```
EXPOSE 80/tcp
EXPOSE 80/udp
```

In this case, if you use `-P` with `docker run`, the port will be exposed once
for TCP and once for UDP. Remember that `-P` uses an ephemeral high-ordered host
port on the host, so TCP and UDP doesn't use the same port.

Regardless of the `EXPOSE` settings, you can override them at runtime by using
the `-p` flag. For example

```
$ docker run -p 80:80/tcp -p 80:80/udp ...
```

To set up port redirection on the host system, see [using the -P flag](https://docs.docker.com/reference/cli/docker/container/run/#publish).
The `docker network` command supports creating networks for communication among
containers without the need to expose or publish specific ports, because the
containers connected to the network can communicate with each other over any
port. For detailed information, see the
[overview of this feature](https://docs.docker.com/engine/userguide/networking/).

## [ENV](#env)

```
ENV <key>=<value> [<key>=<value>...]
```

The `ENV` instruction sets the environment variable `<key>` to the value
`<value>`. This value will be in the environment for all subsequent instructions
in the build stage and can be [replaced inline](#environment-replacement) in
many as well. The value will be interpreted for other environment variables, so
quote characters will be removed if they are not escaped. Like command line parsing,
quotes and backslashes can be used to include spaces within values.

Example:

```
ENV MY_NAME="John Doe"
ENV MY_DOG=Rex\ The\ Dog
ENV MY_CAT=fluffy
```

The `ENV` instruction allows for multiple `<key>=<value> ...` variables to be set
at one time, and the example below will yield the same net results in the final
image:

```
ENV MY_NAME="John Doe" MY_DOG=Rex\ The\ Dog \
    MY_CAT=fluffy
```

The environment variables set using `ENV` will persist when a container is run
from the resulting image. You can view the values using `docker inspect`, and
change them using `docker run --env <key>=<value>`.

A stage inherits any environment variables that were set using `ENV` by its
parent stage or any ancestor. Refer to the [multi-stage builds section](https://docs.docker.com/build/building/multi-stage/)
in the manual for more information.

Environment variable persistence can cause unexpected side effects. For example,
setting `ENV DEBIAN_FRONTEND=noninteractive` changes the behavior of `apt-get`,
and may confuse users of your image.

If an environment variable is only needed during build, and not in the final
image, consider setting a value for a single command instead:

```
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y ...
```

Or using [`ARG`](#arg), which is not persisted in the final image:

```
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y ...
```

> Note
>
> **Alternative syntax**
>
> The `ENV` instruction also allows an alternative syntax `ENV <key> <value>`,
> omitting the `=`. For example:
>
> ```
> ENV MY_VAR my-value
> ```
>
> This syntax does not allow for multiple environment-variables to be set in a
> single `ENV` instruction, and can be confusing. For example, the following
> sets a single environment variable (`ONE`) with value `"TWO= THREE=world"`:
>
> ```
> ENV ONE TWO= THREE=world
> ```
>
> The alternative syntax is supported for backward compatibility, but discouraged
> for the reasons outlined above, and may be removed in a future release.

## [ADD](#add)

ADD has two forms.
The latter form is required for paths containing whitespace.

```
ADD [OPTIONS] <src> ... <dest>
ADD [OPTIONS] ["<src>", ... "<dest>"]
```

The available `[OPTIONS]` are:

| Option | Minimum Dockerfile version |
| --- | --- |
| [`--keep-git-dir`](#add---keep-git-dir) | 1.1 |
| [`--checksum`](#add---checksum) | 1.6 |
| [`--chmod`](#add---chmod) | 1.2 |
| [`--chown`](#add---chown) |  |
| [`--link`](#add---link) | 1.4 |
| [`--unpack`](#add---unpack) | 1.17 |
| [`--exclude`](#add---exclude) | 1.19 |

The `ADD` instruction copies new files or directories from `<src>` and adds
them to the filesystem of the image at the path `<dest>`. Files and directories
can be copied from the build context, a remote URL, or a Git repository.

The `ADD` and `COPY` instructions are functionally similar, but serve slightly different purposes.
Learn more about the [differences between `ADD` and `COPY`](https://docs.docker.com/build/building/best-practices/#add-or-copy).

### [Source](#source)

You can specify multiple source files or directories with `ADD`. The last
argument must always be the destination. For example, to add two files,
`file1.txt` and `file2.txt`, from the build context to `/usr/src/things/` in
the build container:

```
ADD file1.txt file2.txt /usr/src/things/
```

If you specify multiple source files, either directly or using a wildcard, then
the destination must be a directory (must end with a slash `/`).

To add files from a remote location, you can specify a URL or the address of a
Git repository as the source. For example:

```
ADD https://example.com/archive.zip /usr/src/things/
ADD git@github.com:user/repo.git /usr/src/things/
```

BuildKit detects the type of `<src>` and processes it accordingly.

* If `<src>` is a local file or directory, the contents of the directory are
  copied to the specified destination. See [Adding files from the build context](#adding-files-from-the-build-context).
* If `<src>` is a local tar archive, it is decompressed and extracted to the
  specified destination. See [Adding local tar archives](#adding-local-tar-archives).
* If `<src>` is a URL, the contents of the URL are downloaded and placed at
  the specified destination. See [Adding files from a URL](#adding-files-from-a-url).
* If `<src>` is a Git repository, the repository is cloned to the specified
  destination. See [Adding files from a Git repository](#adding-files-from-a-git-repository).

#### [Adding files from the build context](#adding-files-from-the-build-context)

Any relative or local path that doesn't begin with a `http://`, `https://`, or
`git@` protocol prefix is considered a local file path. The local file path is
relative to the build context. For example, if the build context is the current
directory, `ADD file.txt /` adds the file at `./file.txt` to the root of the
filesystem in the build container.

Specifying a source path with a leading slash or one that navigates outside the
build context, such as `ADD ../something /something`, automatically removes any
parent directory navigation (`../`). Trailing slashes in the source path are
also disregarded, making `ADD something/ /something` equivalent to `ADD something /something`.

If the source is a directory, the contents of the directory are copied,
including filesystem metadata. The directory itself isn't copied, only its
contents. If it contains subdirectories, these are also copied, and merged with
any existing directories at the destination. Any conflicts are resolved in
favor of the content being added, on a file-by-file basis, except if you're
trying to copy a directory onto an existing file, in which case an error is
raised.

If the source is a file, the file and its metadata are copied to the
destination. File permissions are preserved. If the source is a file and a
directory with the same name exists at the destination, an error is raised.

If you pass a Dockerfile through stdin to the build (`docker build - < Dockerfile`), there is no build context. In this case, you can only use the
`ADD` instruction to copy remote files. You can also pass a tar archive through
stdin: (`docker build - < archive.tar`), the Dockerfile at the root of the
archive and the rest of the archive will be used as the context of the build.

##### [Pattern matching](#pattern-matching)

For local files, each `<src>` may contain wildcards and matching will be done
using Go's [filepath.Match](https://golang.org/pkg/path/filepath#Match) rules.

For example, to add all files and directories in the root of the build context
ending with `.png`:

```
ADD *.png /dest/
```

In the following example, `?` is a single-character wildcard, matching e.g.
`index.js` and `index.ts`.

```
ADD index.?s /dest/
```

When adding files or directories that contain special characters (such as `[`
and `]`), you need to escape those paths following the Golang rules to prevent
them from being treated as a matching pattern. For example, to add a file
named `arr[0].txt`, use the following;

```
ADD arr[[]0].txt /dest/
```

#### [Adding local tar archives](#adding-local-tar-archives)

When using a local tar archive as the source for `ADD`, and the archive is in a
recognized compression format (`gzip`, `bzip2` or `xz`, or uncompressed), the
archive is decompressed and extracted into the specified destination. Local tar
archives are extracted by default, see the [`ADD --unpack` flag].

When a directory is extracted, it has the same behavior as `tar -x`.
The result is the union of:

1. Whatever existed at the destination path, and
2. The contents of the source tree, with conflicts resolved in favor of the
   content being added, on a file-by-file basis.

> Note
>
> Whether a file is identified as a recognized compression format or not is
> done solely based on the contents of the file, not the name of the file. For
> example, if an empty file happens to end with `.tar.gz` this isn't recognized
> as a compressed file and doesn't generate any kind of decompression error
> message, rather the file will simply be copied to the destination.

#### [Adding files from a URL](#adding-files-from-a-url)

In the case where source is a remote file URL, the destination will have
permissions of 600. If the HTTP response contains a `Last-Modified` header, the
timestamp from that header will be used to set the `mtime` on the destination
file. However, like any other file processed during an `ADD`, `mtime` isn't
included in the determination of whether or not the file has changed and the
cache should be updated.

If remote file is a tar archive, the archive is not extracted by default. To
download and extract the archive, use the [`ADD --unpack` flag].

If the destination ends with a trailing slash, then the filename is inferred
from the URL path. For example, `ADD http://example.com/foobar /` would create
the file `/foobar`. The URL must have a nontrivial path so that an appropriate
filename can be discovered (`http://example.com` doesn't work).

If the destination doesn't end with a trailing slash, the destination path
becomes the filename of the file downloaded from the URL. For example, `ADD http://example.com/foo /bar` creates the file `/bar`.

If your URL files are protected using authentication, you need to use `RUN wget`,
`RUN curl` or use another tool from within the container as the `ADD` instruction
doesn't support authentication.

#### [Adding files from a Git repository](#adding-files-from-a-git-repository)

To use a Git repository as the source for `ADD`, you can reference the
repository's HTTP or SSH address as the source. The repository is cloned to the
specified destination in the image.

```
ADD https://github.com/user/repo.git /mydir/
```

You can use URL fragments to specify a specific branch, tag, commit, or
subdirectory. For example, to add the `docs` directory of the `v0.14.1` tag of
the `buildkit` repository:

```
ADD git@github.com:moby/buildkit.git#v0.14.1:docs /buildkit-docs
```

For more information about Git URL fragments,
see [URL fragments](https://docs.docker.com/build/building/context/#url-fragments).

When adding from a Git repository, the permissions bits for files
are 644. If a file in the repository has the executable bit set, it will have
permissions set to 755. Directories have permissions set to 755.

When using a Git repository as the source, the repository must be accessible
from the build context. To add a repository via SSH, whether public or private,
you must pass an SSH key for authentication. For example, given the following
Dockerfile:

```
# syntax=docker/dockerfile:1
FROM alpine
ADD git@git.example.com:foo/bar.git /bar
```

To build this Dockerfile, pass the `--ssh` flag to the `docker build` to mount
the SSH agent socket to the build. For example:

```
$ docker build --ssh default .
```

For more information about building with secrets,
see [Build secrets](https://docs.docker.com/build/building/secrets/).

### [Destination](#destination)

If the destination path begins with a forward slash, it's interpreted as an
absolute path, and the source files are copied into the specified destination
relative to the root of the current build stage.

```
# create /abs/test.txt
ADD test.txt /abs/
```

Trailing slashes are significant. For example, `ADD test.txt /abs` creates a
file at `/abs`, whereas `ADD test.txt /abs/` creates `/abs/test.txt`.

If the destination path doesn't begin with a leading slash, it's interpreted as
relative to the working directory of the build container.

```
WORKDIR /usr/src/app
# create /usr/src/app/rel/test.txt
ADD test.txt rel/
```

If destination doesn't exist, it's created, along with all missing directories
in its path.

If the source is a file, and the destination doesn't end with a trailing slash,
the source file will be written to the destination path as a file.

### [ADD --keep-git-dir](#add---keep-git-dir)

```
ADD [--keep-git-dir=<boolean>] <src> ... <dir>
```

When `<src>` is the HTTP or SSH address of a remote Git repository,
BuildKit adds the contents of the Git repository to the image
excluding the `.git` directory by default.

The `--keep-git-dir=true` flag lets you preserve the `.git` directory.

```
# syntax=docker/dockerfile:1
FROM alpine
ADD --keep-git-dir=true https://github.com/moby/buildkit.git#v0.10.1 /buildkit
```

### [ADD --checksum](#add---checksum)

```
ADD [--checksum=<hash>] <src> ... <dir>
```

The `--checksum` flag lets you verify the checksum of a remote Git or HTTP
resource:

* For Git sources, the checksum is the commit SHA. It can be the full commit
  SHA or match on the prefix (1 or more characters).
* For HTTP sources, the checksum is the SHA-256 content digest, formatted as
  `sha256:<hash>`. SHA-256 is the only supported hash algorithm.

```
ADD --checksum=be1f38e https://github.com/moby/buildkit.git#v0.26.2 /
ADD --checksum=sha256:24454f830cdb571e2c4ad15481119c43b3cafd48dd869a9b2945d1036d1dc68d https://mirrors.edge.kernel.org/pub/linux/kernel/Historic/linux-0.01.tar.gz /
```

### [ADD --chmod](#add---chmod)

See [`COPY --chmod`](#copy---chmod).

### [ADD --chown](#add---chown)

See [`COPY --chown`](#copy---chown).

### [ADD --link](#add---link)

See [`COPY --link`](#copy---link).

### [ADD --unpack](#add---unpack)

```
ADD [--unpack=<bool>] <src> ... <dir>
```

The `--unpack` flag controls whether or not to automatically unpack tar
archives (including compressed formats like `gzip` or `bzip2`) when adding them
to the image. Local tar archives are unpacked by default, whereas remote tar
archives (where `src` is a URL) are downloaded without unpacking.

```
# syntax=docker/dockerfile:1
FROM alpine
# Download and unpack archive.tar.gz into /download:
ADD --unpack=true https://example.com/archive.tar.gz /download
# Add local tar without unpacking:
ADD --unpack=false my-archive.tar.gz .
```

### [ADD --exclude](#add---exclude)

See [`COPY --exclude`](#copy---exclude).

## [COPY](#copy)

COPY has two forms.
The latter form is required for paths containing whitespace.

```
COPY [OPTIONS] <src> ... <dest>
COPY [OPTIONS] ["<src>", ... "<dest>"]
```

The available `[OPTIONS]` are:

| Option | Minimum Dockerfile version |
| --- | --- |
| [`--from`](#copy---from) |  |
| [`--chmod`](#copy---chmod) | 1.2 |
| [`--chown`](#copy---chown) |  |
| [`--link`](#copy---link) | 1.4 |
| [`--parents`](#copy---parents) | 1.20 |
| [`--exclude`](#copy---exclude) | 1.19 |

The `COPY` instruction copies new files or directories from `<src>` and adds
them to the filesystem of the image at the path `<dest>`. Files and directories
can be copied from the build context, build stage, named context, or an image.

The `ADD` and `COPY` instructions are functionally similar, but serve slightly different purposes.
Learn more about the [differences between `ADD` and `COPY`](https://docs.docker.com/build/building/best-practices/#add-or-copy).

### [Source](#source-1)

You can specify multiple source files or directories with `COPY`. The last
argument must always be the destination. For example, to copy two files,
`file1.txt` and `file2.txt`, from the build context to `/usr/src/things/` in
the build container:

```
COPY file1.txt file2.txt /usr/src/things/
```

If you specify multiple source files, either directly or using a wildcard, then
the destination must be a directory (must end with a slash `/`).

`COPY` accepts a flag `--from=<name>` that lets you specify the source location
to be a build stage, context, or image. The following example copies files from
a stage named `build`:

```
FROM golang AS build
WORKDIR /app
RUN --mount=type=bind,target=. go build -o /myapp ./cmd

COPY --from=build /myapp /usr/bin/
```

For more information about copying from named sources, see the
[`--from` flag](#copy---from).

#### [Copying from the build context](#copying-from-the-build-context)

When copying source files from the build context, paths are interpreted as
relative to the root of the context.

Specifying a source path with a leading slash or one that navigates outside the
build context, such as `COPY ../something /something`, automatically removes
any parent directory navigation (`../`). Trailing slashes in the source path
are also disregarded, making `COPY something/ /something` equivalent to `COPY something /something`.

If the source is a directory, the contents of the directory are copied,
including filesystem metadata. The directory itself isn't copied, only its
contents. If it contains subdirectories, these are also copied, and merged with
any existing directories at the destination. Any conflicts are resolved in
favor of the content being added, on a file-by-file basis, except if you're
trying to copy a directory onto an existing file, in which case an error is
raised.

If the source is a file, the file and its metadata are copied to the
destination. File permissions are preserved. If the source is a file and a
directory with the same name exists at the destination, an error is raised.

If you pass a Dockerfile through stdin to the build (`docker build - < Dockerfile`), there is no build context. In this case, you can only use the
`COPY` instruction to copy files from other stages, named contexts, or images,
using the [`--from` flag](#copy---from). You can also pass a tar archive
through stdin: (`docker build - < archive.tar`), the Dockerfile at the root of
the archive and the rest of the archive will be used as the context of the
build.

When using a Git repository as the build context, the permissions bits for
copied files are 644. If a file in the repository has the executable bit set,
it will have permissions set to 755. Directories have permissions set to 755.

##### [Pattern matching](#pattern-matching-1)

For local files, each `<src>` may contain wildcards and matching will be done
using Go's [filepath.Match](https://golang.org/pkg/path/filepath#Match) rules.

For example, to add all files and directories in the root of the build context
ending with `.png`:

```
COPY *.png /dest/
```

In the following example, `?` is a single-character wildcard, matching e.g.
`index.js` and `index.ts`.

```
COPY index.?s /dest/
```

When adding files or directories that contain special characters (such as `[`
and `]`), you need to escape those paths following the Golang rules to prevent
them from being treated as a matching pattern. For example, to add a file
named `arr[0].txt`, use the following;

```
COPY arr[[]0].txt /dest/
```

### [Destination](#destination-1)

If the destination path begins with a forward slash, it's interpreted as an
absolute path, and the source files are copied into the specified destination
relative to the root of the current build stage.

```
# create /abs/test.txt
COPY test.txt /abs/
```

Trailing slashes are significant. For example, `COPY test.txt /abs` creates a
file at `/abs`, whereas `COPY test.txt /abs/` creates `/abs/test.txt`.

If the destination path doesn't begin with a leading slash, it's interpreted as
relative to the working directory of the build container.

```
WORKDIR /usr/src/app
# create /usr/src/app/rel/test.txt
COPY test.txt rel/
```

If destination doesn't exist, it's created, along with all missing directories
in its path.

If the source is a file, and the destination doesn't end with a trailing slash,
the source file will be written to the destination path as a file.

### [COPY --from](#copy---from)

By default, the `COPY` instruction copies files from the build context. The
`COPY --from` flag lets you copy files from an image, a build stage,
or a named context instead.

```
COPY [--from=<image|stage|context>] <src> ... <dest>
```

To copy from a build stage in a
[multi-stage build](https://docs.docker.com/build/building/multi-stage/),
specify the name of the stage you want to copy from. You specify stage names
using the `AS` keyword with the `FROM` instruction.

```
# syntax=docker/dockerfile:1
FROM alpine AS build
COPY . .
RUN apk add clang
RUN clang -o /hello hello.c

FROM scratch
COPY --from=build /hello /
```

You can also copy files directly from named contexts (specified with
`--build-context <name>=<source>`) or images. The following example copies an
`nginx.conf` file from the official Nginx image.

```
COPY --from=nginx:latest /etc/nginx/nginx.conf /nginx.conf
```

The source path of `COPY --from` is always resolved from filesystem root of the
image or stage that you specify.

### [COPY --chmod](#copy---chmod)

```
COPY [--chmod=<perms>] <src> ... <dest>
```

The `--chmod` flag supports octal notation (e.g., `755`, `644`) and symbolic
notation (e.g., `+x`, `g=u`). Symbolic notation (added in Dockerfile version 1.14)
is useful when octal isn't flexible enough. For example, `u=rwX,go=rX` sets
directories to 755 and files to 644, while preserving the executable bit on files
that already have it. (Capital `X` means "executable only if it's a directory or
already executable.")

For more information about symbolic notation syntax, see the
[chmod(1) manual](https://man.freebsd.org/cgi/man.cgi?chmod).

Examples using octal notation:

```
COPY --chmod=755 app.sh /app/
COPY --chmod=644 file.txt /data/
ARG MODE=440
COPY --chmod=$MODE . .
```

Examples using symbolic notation:

```
COPY --chmod=+x script.sh /app/
COPY --chmod=u=rwX,go=rX . /app/
COPY --chmod=g=u config/ /config/
```

The `--chmod` flag is not supported when building Windows containers.

### [COPY --chown](#copy---chown)

```
COPY [--chown=<user>:<group>] <src> ... <dest>
```

Sets ownership of copied files. Without this flag, files are created with UID
and GID of 0.

The flag accepts usernames, group names, UIDs, or GIDs in any combination.
If you specify only a user, the GID is set to the same numeric value as the UID.

```
COPY --chown=55:mygroup files* /somedir/
COPY --chown=bin files* /somedir/
COPY --chown=1 files* /somedir/
COPY --chown=10:11 files* /somedir/
COPY --chown=myuser:mygroup --chmod=644 files* /somedir/
```

When using names instead of numeric IDs, BuildKit resolves them using
`/etc/passwd` and `/etc/group` in the container's root filesystem. If these
files are missing or don't contain the specified names, the build fails.
Numeric IDs don't require this lookup.

The `--chown` flag is not supported when building Windows containers.

### [COPY --link](#copy---link)

```
COPY [--link[=<boolean>]] <src> ... <dest>
```

Enabling this flag in `COPY` or `ADD` commands allows you to copy files with
enhanced semantics where your files remain independent on their own layer and
don't get invalidated when commands on previous layers are changed.

When `--link` is used your source files are copied into an empty destination
directory. That directory is turned into a layer that is linked on top of your
previous state.

```
# syntax=docker/dockerfile:1
FROM alpine
COPY --link /foo /bar
```

Is equivalent of doing two builds:

```
FROM alpine
```

and

```
FROM scratch
COPY /foo /bar
```

and merging all the layers of both images together.

#### [Benefits of using `--link`](#benefits-of-using---link)

Use `--link` to reuse already built layers in subsequent builds with
`--cache-from` even if the previous layers have changed. This is especially
important for multi-stage builds where a `COPY --from` statement would
previously get invalidated if any previous commands in the same stage changed,
causing the need to rebuild the intermediate stages again. With `--link` the
layer the previous build generated is reused and merged on top of the new
layers. This also means you can easily rebase your images when the base images
receive updates, without having to execute the whole build again. In backends
that support it, BuildKit can do this rebase action without the need to push or
pull any layers between the client and the registry. BuildKit will detect this
case and only create new image manifest that contains the new layers and old
layers in correct order.

The same behavior where BuildKit can avoid pulling down the base image can also
happen when using `--link` and no other commands that would require access to
the files in the base image. In that case BuildKit will only build the layers
for the `COPY` commands and push them to the registry directly on top of the
layers of the base image.

#### [Incompatibilities with `--link=false`](#incompatibilities-with---linkfalse)

When using `--link` the `COPY/ADD` commands are not allowed to read any files
from the previous state. This means that if in previous state the destination
directory was a path that contained a symlink, `COPY/ADD` can not follow it.
In the final image the destination path created with `--link` will always be a
path containing only directories.

If you don't rely on the behavior of following symlinks in the destination
path, using `--link` is always recommended. The performance of `--link` is
equivalent or better than the default behavior and, it creates much better
conditions for cache reuse.

### [COPY --parents](#copy---parents)

```
COPY [--parents[=<boolean>]] <src> ... <dest>
```

The `--parents` flag preserves parent directories for `src` entries. This flag defaults to `false`.

```
# syntax=docker/dockerfile:1
FROM scratch

COPY ./x/a.txt ./y/a.txt /no_parents/
COPY --parents ./x/a.txt ./y/a.txt /parents/

# /no_parents/a.txt
# /parents/x/a.txt
# /parents/y/a.txt
```

This behavior is similar to the [Linux `cp` utility's](https://www.man7.org/linux/man-pages/man1/cp.1.html)
`--parents` or [`rsync`](https://man7.org/linux/man-pages/man1/rsync.1.html) `--relative` flag.

As with Rsync, it is possible to limit which parent directories are preserved by
inserting a dot and a slash (`./`) into the source path. If such point exists, only parent
directories after it will be preserved. This may be especially useful copies between stages
with `--from` where the source paths need to be absolute.

```
# syntax=docker/dockerfile:1
FROM scratch

COPY --parents ./x/./y/*.txt /parents/

# Build context:
# ./x/y/a.txt
# ./x/y/b.txt
#
# Output:
# /parents/y/a.txt
# /parents/y/b.txt
```

The `**` wildcard matches any number of path components, including none, and
can be used to recursively match files across directory levels:

```
# syntax=docker/dockerfile:1
FROM scratch

COPY --parents ./src/**/*.txt /parents/

# Build context:
# ./src/a.txt
# ./src/x/b.txt
# ./src/x/y/c.txt
#
# Output:
# /parents/src/a.txt
# /parents/src/x/b.txt
# /parents/src/x/y/c.txt
```

Note that, without the `--parents` flag specified, any filename collision will
fail the Linux `cp` operation with an explicit error message
(`cp: will not overwrite just-created './x/a.txt' with './y/a.txt'`), where the
Buildkit will silently overwrite the target file at the destination.

While it is possible to preserve the directory structure for `COPY`
instructions consisting of only one `src` entry, usually it is more beneficial
to keep the layer count in the resulting image as low as possible. Therefore,
with the `--parents` flag, the Buildkit is capable of packing multiple
`COPY` instructions together, keeping the directory structure intact.

### [COPY --exclude](#copy---exclude)

```
COPY [--exclude=<path> ...] <src> ... <dest>
```

The `--exclude` flag lets you specify a path expression for files to be excluded.

The path expression follows the same format as `<src>`,
supporting wildcards and matching using Go's
[filepath.Match](https://golang.org/pkg/path/filepath#Match) rules.
For example, to add all files starting with "hom", excluding files with a `.txt` extension:

```
# syntax=docker/dockerfile:1
FROM scratch

COPY --exclude=*.txt hom* /mydir/
```

You can specify the `--exclude` option multiple times for a `COPY` instruction.
Multiple `--excludes` are files matching its patterns not to be copied,
even if the files paths match the pattern specified in `<src>`.
To add all files starting with "hom", excluding files with either `.txt` or `.md` extensions:

```
# syntax=docker/dockerfile:1
FROM scratch

COPY --exclude=*.txt --exclude=*.md hom* /mydir/
```

## [ENTRYPOINT](#entrypoint)

An `ENTRYPOINT` allows you to configure a container that will run as an executable.

`ENTRYPOINT` has two possible forms:

* The exec form, which is the preferred form:

  ```
  ENTRYPOINT ["executable", "param1", "param2"]
  ```
* The shell form:

  ```
  ENTRYPOINT command param1 param2
  ```

For more information about the different forms, see [Shell and exec form](#shell-and-exec-form).

The following command starts a container from the `nginx` with its default
content, listening on port 80:

```
$ docker run -i -t --rm -p 80:80 nginx
```

Command line arguments to `docker run <image>` will be appended after all
elements in an exec form `ENTRYPOINT`, and will override all elements specified
using `CMD`.

This allows arguments to be passed to the entry point, i.e., `docker run <image> -d` will pass the `-d` argument to the entry point. You can override
the `ENTRYPOINT` instruction using the `docker run --entrypoint` flag.

The shell form of `ENTRYPOINT` ignores any `CMD` or `docker run` command line
arguments. It also starts your `ENTRYPOINT` as a subcommand of `/bin/sh -c`,
which does not pass signals. This means that the executable will not be the
container's `PID 1`, and will not receive Unix signals. In this case, your
executable doesn't receive a `SIGTERM` from `docker stop <container>`.

Only the last `ENTRYPOINT` instruction in the Dockerfile will have an effect.

### [Exec form ENTRYPOINT example](#exec-form-entrypoint-example)

You can use the exec form of `ENTRYPOINT` to set fairly stable default commands
and arguments and then use `CMD` to set additional defaults that are more
likely to be changed.

When combining exec form `ENTRYPOINT` with `CMD`, use the exec form of `CMD`
as well. Using the shell form of `CMD` causes it to be wrapped in
`/bin/sh -c`, which means the `ENTRYPOINT` receives a shell invocation as its
argument rather than the bare command and parameters. See
[Understand how CMD and ENTRYPOINT interact](#understand-how-cmd-and-entrypoint-interact).

```
FROM ubuntu
ENTRYPOINT ["top", "-b"]
CMD ["-c"]
```

When you run the container, you can see that `top` is the only process:

```
$ docker run -it --rm --name test  top -H

top - 08:25:00 up  7:27,  0 users,  load average: 0.00, 0.01, 0.05
Threads:   1 total,   1 running,   0 sleeping,   0 stopped,   0 zombie
%Cpu(s):  0.1 us,  0.1 sy,  0.0 ni, 99.7 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
KiB Mem:   2056668 total,  1616832 used,   439836 free,    99352 buffers
KiB Swap:  1441840 total,        0 used,  1441840 free.  1324440 cached Mem

  PID USER      PR  NI    VIRT    RES    SHR S %CPU %MEM     TIME+ COMMAND
    1 root      20   0   19744   2336   2080 R  0.0  0.1   0:00.04 top
```

To examine the result further, you can use `docker exec`:

```
$ docker exec -it test ps aux

USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  2.6  0.1  19752  2352 ?        Ss+  08:24   0:00 top -b -H
root         7  0.0  0.1  15572  2164 ?        R+   08:25   0:00 ps aux
```

And you can gracefully request `top` to shut down using `docker stop test`.

The following Dockerfile shows using the `ENTRYPOINT` to run Apache in the
foreground (i.e., as `PID 1`):

```
FROM debian:stable
RUN apt-get update && apt-get install -y --force-yes apache2
EXPOSE 80 443
VOLUME ["/var/www", "/var/log/apache2", "/etc/apache2"]
ENTRYPOINT ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]
```

If you need to write a starter script for a single executable, you can ensure that
the final executable receives the Unix signals by using `exec` and `gosu`
commands:

```
#!/usr/bin/env bash
set -e

if [ "$1" = 'postgres' ]; then
    chown -R postgres "$PGDATA"

    if [ -z "$(ls -A "$PGDATA")" ]; then
        gosu postgres initdb
    fi

    exec gosu postgres "$@"
fi

exec "$@"
```

Lastly, if you need to do some extra cleanup (or communicate with other containers)
on shutdown, or are co-ordinating more than one executable, you may need to ensure
that the `ENTRYPOINT` script receives the Unix signals, passes them on, and then
does some more work:

```
#!/bin/sh
# Note: I've written this using sh so it works in the busybox container too

# USE the trap if you need to also do manual cleanup after the service is stopped,
#     or need to start multiple services in the one container
trap "echo TRAPed signal" HUP INT QUIT TERM

# start service in background here
/usr/sbin/apachectl start

echo "[hit enter key to exit] or run 'docker stop <container>'"
read

# stop service and clean up here
echo "stopping apache"
/usr/sbin/apachectl stop

echo "exited $0"
```

If you run this image with `docker run -it --rm -p 80:80 --name test apache`,
you can then examine the container's processes with `docker exec`, or `docker top`,
and then ask the script to stop Apache:

```
$ docker exec -it test ps aux

USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.1  0.0   4448   692 ?        Ss+  00:42   0:00 /bin/sh /run.sh 123 cmd cmd2
root        19  0.0  0.2  71304  4440 ?        Ss   00:42   0:00 /usr/sbin/apache2 -k start
www-data    20  0.2  0.2 360468  6004 ?        Sl   00:42   0:00 /usr/sbin/apache2 -k start
www-data    21  0.2  0.2 360468  6000 ?        Sl   00:42   0:00 /usr/sbin/apache2 -k start
root        81  0.0  0.1  15572  2140 ?        R+   00:44   0:00 ps aux

$ docker top test

PID                 USER                COMMAND
10035               root                {run.sh} /bin/sh /run.sh 123 cmd cmd2
10054               root                /usr/sbin/apache2 -k start
10055               33                  /usr/sbin/apache2 -k start
10056               33                  /usr/sbin/apache2 -k start

$ /usr/bin/time docker stop test

test
real	0m 0.27s
user	0m 0.03s
sys	0m 0.03s
```

> Note
>
> You can override the `ENTRYPOINT` setting using `--entrypoint`,
> but this can only set the binary to exec (no `sh -c` will be used).

### [Shell form ENTRYPOINT example](#shell-form-entrypoint-example)

You can specify a plain string for the `ENTRYPOINT` and it will execute in `/bin/sh -c`.
This form will use shell processing to substitute shell environment variables,
and will ignore any `CMD` or `docker run` command line arguments.
To ensure that `docker stop` will signal any long running `ENTRYPOINT` executable
correctly, you need to remember to start it with `exec`:

```
FROM ubuntu
ENTRYPOINT exec top -b
```

When you run this image, you'll see the single `PID 1` process:

```
$ docker run -it --rm --name test top

Mem: 1704520K used, 352148K free, 0K shrd, 0K buff, 140368121167873K cached
CPU:   5% usr   0% sys   0% nic  94% idle   0% io   0% irq   0% sirq
Load average: 0.08 0.03 0.05 2/98 6
  PID  PPID USER     STAT   VSZ %VSZ %CPU COMMAND
    1     0 root     R     3164   0%   0% top -b
```

Which exits cleanly on `docker stop`:

```
$ /usr/bin/time docker stop test

test
real	0m 0.20s
user	0m 0.02s
sys	0m 0.04s
```

If you forget to add `exec` to the beginning of your `ENTRYPOINT`:

```
FROM ubuntu
ENTRYPOINT top -b
CMD -- --ignored-param1
```

You can then run it (giving it a name for the next step):

```
$ docker run -it --name test top --ignored-param2

top - 13:58:24 up 17 min,  0 users,  load average: 0.00, 0.00, 0.00
Tasks:   2 total,   1 running,   1 sleeping,   0 stopped,   0 zombie
%Cpu(s): 16.7 us, 33.3 sy,  0.0 ni, 50.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
MiB Mem :   1990.8 total,   1354.6 free,    231.4 used,    404.7 buff/cache
MiB Swap:   1024.0 total,   1024.0 free,      0.0 used.   1639.8 avail Mem

  PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
    1 root      20   0    2612    604    536 S   0.0   0.0   0:00.02 sh
    6 root      20   0    5956   3188   2768 R   0.0   0.2   0:00.00 top
```

You can see from the output of `top` that the specified `ENTRYPOINT` is not `PID 1`.

If you then run `docker stop test`, the container will not exit cleanly - the
`stop` command will be forced to send a `SIGKILL` after the timeout:

```
$ docker exec -it test ps waux

USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.4  0.0   2612   604 pts/0    Ss+  13:58   0:00 /bin/sh -c top -b --ignored-param2
root         6  0.0  0.1   5956  3188 pts/0    S+   13:58   0:00 top -b
root         7  0.0  0.1   5884  2816 pts/1    Rs+  13:58   0:00 ps waux

$ /usr/bin/time docker stop test

test
real	0m 10.19s
user	0m 0.04s
sys	0m 0.03s
```

### [Understand how CMD and ENTRYPOINT interact](#understand-how-cmd-and-entrypoint-interact)

Both `CMD` and `ENTRYPOINT` instructions define what command gets executed when running a container.
There are few rules that describe their co-operation.

1. Dockerfile should specify at least one of `CMD` or `ENTRYPOINT` commands.
2. `ENTRYPOINT` should be defined when using the container as an executable.
3. `CMD` should be used as a way of defining default arguments for an `ENTRYPOINT` command
   or for executing an ad-hoc command in a container.
4. `CMD` will be overridden when running the container with alternative arguments.

The table below shows what command is executed for different `ENTRYPOINT` / `CMD` combinations:

|  | No ENTRYPOINT | ENTRYPOINT exec\_entry p1\_entry | ENTRYPOINT ["exec\_entry", "p1\_entry"] |
| --- | --- | --- | --- |
| **No CMD** | error, not allowed | /bin/sh -c exec\_entry p1\_entry | exec\_entry p1\_entry |
| **CMD ["exec\_cmd", "p1\_cmd"]** | exec\_cmd p1\_cmd | /bin/sh -c exec\_entry p1\_entry | exec\_entry p1\_entry exec\_cmd p1\_cmd |
| **CMD exec\_cmd p1\_cmd** | /bin/sh -c exec\_cmd p1\_cmd | /bin/sh -c exec\_entry p1\_entry | exec\_entry p1\_entry /bin/sh -c exec\_cmd p1\_cmd |

> Note
>
> If `CMD` is defined from the base image, setting `ENTRYPOINT` will
> reset `CMD` to an empty value. In this scenario, `CMD` must be defined in the
> current image to have a value.

## [VOLUME](#volume)

```
VOLUME ["/data"]
```

The `VOLUME` instruction creates a mount point with the specified name
and marks it as holding externally mounted volumes from native host or other
containers. The value can be a JSON array, `VOLUME ["/var/log/"]`, or a plain
string with multiple arguments, such as `VOLUME /var/log` or `VOLUME /var/log /var/db`. For more information/examples and mounting instructions via the
Docker client, refer to
[*Share Directories via Volumes*](https://docs.docker.com/storage/volumes/)
documentation.

The `docker run` command initializes the newly created volume with any data
that exists at the specified location within the base image. For example,
consider the following Dockerfile snippet:

```
FROM ubuntu
RUN mkdir /myvol
RUN echo "hello world" > /myvol/greeting
VOLUME /myvol
```

This Dockerfile results in an image that causes `docker run` to
create a new mount point at `/myvol` and copy the `greeting` file
into the newly created volume.

### [Notes about specifying volumes](#notes-about-specifying-volumes)

Keep the following things in mind about volumes in the Dockerfile.

* **Volumes on Windows-based containers**: When using Windows-based containers,
  the destination of a volume inside the container must be one of:

  + a non-existing or empty directory
  + a drive other than `C:`
* **Changing the volume from within the Dockerfile**: If any build steps change the
  data within the volume after it has been declared, those changes will be discarded
  when using the legacy builder. When using Buildkit, the changes will instead be kept.
* **JSON formatting**: The list is parsed as a JSON array.
  You must enclose words with double quotes (`"`) rather than single quotes (`'`).
* **The host directory is declared at container run-time**: The host directory
  (the mountpoint) is, by its nature, host-dependent. This is to preserve image
  portability, since a given host directory can't be guaranteed to be available
  on all hosts. For this reason, you can't mount a host directory from
  within the Dockerfile. The `VOLUME` instruction does not support specifying a `host-dir`
  parameter. You must specify the mountpoint when you create or run the container.

## [USER](#user)

```
USER <user>[:<group>]
```

or

```
USER <UID>[:<GID>]
```

The `USER` instruction sets the user name (or UID) and optionally the user
group (or GID) to use as the default user and group for the remainder of the
current stage. The specified user is used for `RUN` instructions and at
runtime runs the relevant `ENTRYPOINT` and `CMD` commands.

> Note that when specifying a group for the user, the user will have *only* the
> specified group membership. Any other configured group memberships will be ignored.

> Warning
>
> When the user doesn't have a primary group then the image (or the next
> instructions) will be run with the `root` group.
>
> On Windows, the user must be created first if it's not a built-in account.
> This can be done with the `net user` command called as part of a Dockerfile.

```
FROM microsoft/windowsservercore
# Create Windows user in the container
RUN net user /add patrick
# Set it for subsequent commands
USER patrick
```

## [WORKDIR](#workdir)

```
WORKDIR /path/to/workdir
```

The `WORKDIR` instruction sets the working directory for any `RUN`, `CMD`,
`ENTRYPOINT`, `COPY` and `ADD` instructions that follow it in the Dockerfile.
If the `WORKDIR` doesn't exist, it will be created even if it's not used in any
subsequent Dockerfile instruction.

The `WORKDIR` instruction can be used multiple times in a Dockerfile. If a
relative path is provided, it will be relative to the path of the previous
`WORKDIR` instruction. For example:

```
WORKDIR /a
WORKDIR b
WORKDIR c
RUN pwd
```

The output of the final `pwd` command in this Dockerfile would be `/a/b/c`.

The `WORKDIR` instruction can resolve environment variables previously set using
`ENV`. You can only use environment variables explicitly set in the Dockerfile.
For example:

```
ENV DIRPATH=/path
WORKDIR $DIRPATH/$DIRNAME
RUN pwd
```

The output of the final `pwd` command in this Dockerfile would be
`/path/$DIRNAME`

If not specified, the default working directory is `/`. In practice, if you aren't building a Dockerfile from scratch (`FROM scratch`),
the `WORKDIR` may likely be set by the base image you're using.

Therefore, to avoid unintended operations in unknown directories, it's best practice to set your `WORKDIR` explicitly.

## [ARG](#arg)

```
ARG <name>[=<default value>] [<name>[=<default value>]...]
```

The `ARG` instruction defines a variable that users can pass at build time to
the builder with the `docker build` command using the `--build-arg <varname>=<value>`
flag. This variable can be used in subsequent instructions such as `FROM`, `ENV`,
`WORKDIR`, and others using the `${VAR}` or `$VAR` template syntax.
It is also passed to all subsequent `RUN` instructions as a build-time
environment variable.

Unlike `ENV`, an `ARG` variable is not embedded in the image and is not available
in the final container.

> Warning
>
> It isn't recommended to use build arguments for passing secrets such as
> user credentials, API tokens, etc. Build arguments are visible in the
> `docker history` command and in `max` mode provenance attestations,
> which are attached to the image by default if you use the Buildx GitHub Actions
> and your GitHub repository is public.
>
> Refer to the [`RUN --mount=type=secret`](#run---mounttypesecret) section to
> learn about secure ways to use secrets when building images.

A Dockerfile may include one or more `ARG` instructions. For example,
the following is a valid Dockerfile:

```
FROM busybox
ARG user1
ARG buildno
# ...
```

### [Default values](#default-values)

An `ARG` instruction can optionally include a default value:

```
FROM busybox
ARG user1=someuser
ARG buildno=1
# ...
```

If an `ARG` instruction has a default value and if there is no value passed
at build-time, the builder uses the default.

### [Scope](#scope)

An `ARG` variable comes into effect from the line on which it is declared in
the Dockerfile. For example, consider this Dockerfile:

```
FROM busybox
USER ${username:-some_user}
ARG username
USER $username
# ...
```

A user builds this file by calling:

```
$ docker build --build-arg username=what_user .
```

* The `USER` instruction on line 2 evaluates to the `some_user` fallback,
  because the `username` variable is not yet declared.
* The `username` variable is declared on line 3, and available for reference in
  Dockerfile instruction from that point onwards.
* The `USER` instruction on line 4 evaluates to `what_user`, since at that
  point the `username` argument has a value of `what_user` which was passed on
  the command line. Prior to its definition by an `ARG` instruction, any use of
  a variable results in an empty string.

An `ARG` variable declared within a build stage is automatically inherited by
other stages based on that stage. Unrelated build stages do not have access to
the variable. To use an argument in multiple distinct stages, each stage must
include the `ARG` instruction, or they must both be based on a shared base
stage in the same Dockerfile where the variable is declared.

For more information, refer to [variable scoping](https://docs.docker.com/build/building/variables/#scoping).

### [Using ARG variables](#using-arg-variables)

You can use an `ARG` or an `ENV` instruction to specify variables that are
available to the `RUN` instruction. Environment variables defined using the
`ENV` instruction always override an `ARG` instruction of the same name. Consider
this Dockerfile with an `ENV` and `ARG` instruction.

```
FROM ubuntu
ARG CONT_IMG_VER
ENV CONT_IMG_VER=v1.0.0
RUN echo $CONT_IMG_VER
```

Then, assume this image is built with this command:

```
$ docker build --build-arg CONT_IMG_VER=v2.0.1 .
```

In this case, the `RUN` instruction uses `v1.0.0` instead of the `ARG` setting
passed by the user:`v2.0.1` This behavior is similar to a shell
script where a locally scoped variable overrides the variables passed as
arguments or inherited from environment, from its point of definition.

Using the example above but a different `ENV` specification you can create more
useful interactions between `ARG` and `ENV` instructions:

```
FROM ubuntu
ARG CONT_IMG_VER
ENV CONT_IMG_VER=${CONT_IMG_VER:-v1.0.0}
RUN echo $CONT_IMG_VER
```

Unlike an `ARG` instruction, `ENV` values are always persisted in the built
image. Consider a docker build without the `--build-arg` flag:

```
$ docker build .
```

Using this Dockerfile example, `CONT_IMG_VER` is still persisted in the image but
its value would be `v1.0.0` as it is the default set in line 3 by the `ENV` instruction.

The variable expansion technique in this example allows you to pass arguments
from the command line and persist them in the final image by leveraging the
`ENV` instruction. Variable expansion is only supported for [a limited set of
Dockerfile instructions.](#environment-replacement)

### [Predefined ARGs](#predefined-args)

Docker has a set of predefined `ARG` variables that you can use without a
corresponding `ARG` instruction in the Dockerfile.

* `HTTP_PROXY`
* `http_proxy`
* `HTTPS_PROXY`
* `https_proxy`
* `FTP_PROXY`
* `ftp_proxy`
* `NO_PROXY`
* `no_proxy`
* `ALL_PROXY`
* `all_proxy`

To use these, pass them on the command line using the `--build-arg` flag, for
example:

```
$ docker build --build-arg HTTPS_PROXY=https://my-proxy.example.com .
```

By default, these pre-defined variables are excluded from the output of
`docker history`. Excluding them reduces the risk of accidentally leaking
sensitive authentication information in an `HTTP_PROXY` variable.

For example, consider building the following Dockerfile using
`--build-arg HTTP_PROXY=http://user:pass@proxy.lon.example.com`

```
FROM ubuntu
RUN echo "Hello World"
```

In this case, the value of the `HTTP_PROXY` variable is not available in the
`docker history` and is not cached. If you were to change location, and your
proxy server changed to `http://user:pass@proxy.sfo.example.com`, a subsequent
build does not result in a cache miss.

If you need to override this behaviour then you may do so by adding an `ARG`
statement in the Dockerfile as follows:

```
FROM ubuntu
ARG HTTP_PROXY
RUN echo "Hello World"
```

When building this Dockerfile, the `HTTP_PROXY` is preserved in the
`docker history`, and changing its value invalidates the build cache.

### [Automatic platform ARGs in the global scope](#automatic-platform-args-in-the-global-scope)

This feature is only available when using the [BuildKit](https://docs.docker.com/build/buildkit/)
backend.

BuildKit supports a predefined set of `ARG` variables with information on the platform of
the node performing the build (build platform) and on the platform of the
resulting image (target platform). The target platform can be specified with
the `--platform` flag on `docker build`.

The following `ARG` variables are set automatically:

* `TARGETPLATFORM` - platform of the build result. Eg `linux/amd64`, `linux/arm/v7`, `windows/amd64`.
* `TARGETOS` - OS component of TARGETPLATFORM
* `TARGETARCH` - architecture component of TARGETPLATFORM
* `TARGETVARIANT` - variant component of TARGETPLATFORM
* `BUILDPLATFORM` - platform of the node performing the build.
* `BUILDOS` - OS component of BUILDPLATFORM
* `BUILDARCH` - architecture component of BUILDPLATFORM
* `BUILDVARIANT` - variant component of BUILDPLATFORM

These arguments are defined in the global scope so are not automatically
available inside build stages or for your `RUN` commands. To expose one of
these arguments inside the build stage redefine it without value.

For example:

```
FROM alpine
ARG TARGETPLATFORM
RUN echo "I'm building for $TARGETPLATFORM"
```

### [BuildKit built-in build args](#buildkit-built-in-build-args)

| Arg | Type | Description |
| --- | --- | --- |
| `BUILDKIT_BUILD_NAME` | String | Override the build name shown in [`buildx history` command](https://docs.docker.com/reference/cli/docker/buildx/history/) and [Docker Desktop Builds view](https://docs.docker.com/desktop/use-desktop/builds/). |
| `BUILDKIT_CACHE_MOUNT_NS` | String | Set optional cache ID namespace. |
| `BUILDKIT_CONTEXT_KEEP_GIT_DIR` | Bool | Trigger Git context to keep the `.git` directory. |
| `BUILDKIT_INLINE_CACHE`[2](#fn:2) | Bool | Inline cache metadata to image config or not. |
| `BUILDKIT_MULTI_PLATFORM` | Bool | Opt into deterministic output regardless of multi-platform output or not. |
| `BUILDKIT_SANDBOX_HOSTNAME` | String | Set the hostname (default `buildkitsandbox`) |
| `BUILDKIT_SYNTAX` | String | Set frontend image |
| `SOURCE_DATE_EPOCH` | Int | Set the Unix timestamp for created image and layers. More info from [reproducible builds](https://reproducible-builds.org/docs/source-date-epoch/). Supported since Dockerfile 1.5, BuildKit 0.11 |

#### [Example: keep `.git` dir](#example-keep-git-dir)

When using a Git context, `.git` dir is not kept on checkouts. It can be
useful to keep it around if you want to retrieve git information during
your build:

```
# syntax=docker/dockerfile:1
FROM alpine
WORKDIR /src
RUN --mount=target=. \
  make REVISION=$(git rev-parse HEAD) build
```

```
$ docker build --build-arg BUILDKIT_CONTEXT_KEEP_GIT_DIR=1 https://github.com/user/repo.git#main
```

### [Impact on build caching](#impact-on-build-caching)

`ARG` variables are not persisted into the built image as `ENV` variables are.
However, `ARG` variables do impact the build cache in similar ways. If a
Dockerfile defines an `ARG` variable whose value is different from a previous
build, then a "cache miss" occurs upon its first usage, not its definition. In
particular, all `RUN` instructions following an `ARG` instruction use the `ARG`
variable implicitly (as an environment variable), thus can cause a cache miss.
All predefined `ARG` variables are exempt from caching unless there is a
matching `ARG` statement in the Dockerfile.

For example, consider these two Dockerfile:

```
FROM ubuntu
ARG CONT_IMG_VER
RUN echo $CONT_IMG_VER
```

```
FROM ubuntu
ARG CONT_IMG_VER
RUN echo hello
```

If you specify `--build-arg CONT_IMG_VER=<value>` on the command line, in both
cases, the specification on line 2 doesn't cause a cache miss; line 3 does
cause a cache miss. `ARG CONT_IMG_VER` causes the `RUN` line to be identified
as the same as running `CONT_IMG_VER=<value> echo hello`, so if the `<value>`
changes, you get a cache miss.

Consider another example under the same command line:

```
FROM ubuntu
ARG CONT_IMG_VER
ENV CONT_IMG_VER=$CONT_IMG_VER
RUN echo $CONT_IMG_VER
```

In this example, the cache miss occurs on line 3. The miss happens because
the variable's value in the `ENV` references the `ARG` variable and that
variable is changed through the command line. In this example, the `ENV`
command causes the image to include the value.

If an `ENV` instruction overrides an `ARG` instruction of the same name, like
this Dockerfile:

```
FROM ubuntu
ARG CONT_IMG_VER
ENV CONT_IMG_VER=hello
RUN echo $CONT_IMG_VER
```

Line 3 doesn't cause a cache miss because the value of `CONT_IMG_VER` is a
constant (`hello`). As a result, the environment variables and values used on
the `RUN` (line 4) doesn't change between builds.

## [ONBUILD](#onbuild)

```
ONBUILD <INSTRUCTION>
```

The `ONBUILD` instruction adds to the image a trigger instruction to
be executed at a later time, when the image is used as the base for
another build. The trigger will be executed in the context of the
downstream build, as if it had been inserted immediately after the
`FROM` instruction in the downstream Dockerfile.

This is useful if you are building an image which will be used as a base
to build other images, for example an application build environment or a
daemon which may be customized with user-specific configuration.

For example, if your image is a reusable Python application builder, it
will require application source code to be added in a particular
directory, and it might require a build script to be called after
that. You can't just call `ADD` and `RUN` now, because you don't yet
have access to the application source code, and it will be different for
each application build. You could simply provide application developers
with a boilerplate Dockerfile to copy-paste into their application, but
that's inefficient, error-prone and difficult to update because it
mixes with application-specific code.

The solution is to use `ONBUILD` to register advance instructions to
run later, during the next build stage.

Here's how it works:

1. When it encounters an `ONBUILD` instruction, the builder adds a
   trigger to the metadata of the image being built. The instruction
   doesn't otherwise affect the current build.
2. At the end of the build, a list of all triggers is stored in the
   image manifest, under the key `OnBuild`. They can be inspected with
   the `docker inspect` command.
3. Later the image may be used as a base for a new build, using the
   `FROM` instruction. As part of processing the `FROM` instruction,
   the downstream builder looks for `ONBUILD` triggers, and executes
   them in the same order they were registered. If any of the triggers
   fail, the `FROM` instruction is aborted which in turn causes the
   build to fail. If all triggers succeed, the `FROM` instruction
   completes and the build continues as usual.
4. Triggers are cleared from the final image after being executed. In
   other words they aren't inherited by "grand-children" builds.

For example you might add something like this:

```
ONBUILD ADD . /app/src
ONBUILD RUN /usr/local/bin/python-build --dir /app/src
```

### [Copy or mount from stage, image, or context](#copy-or-mount-from-stage-image-or-context)

As of Dockerfile syntax 1.11, you can use `ONBUILD` with instructions that copy
or mount files from other stages, images, or build contexts. For example:

```
# syntax=docker/dockerfile:1.11
FROM alpine AS baseimage
ONBUILD COPY --from=build /usr/bin/app /app
ONBUILD RUN --mount=from=config,target=/opt/appconfig ...
```

If the source of `from` is a build stage, the stage must be defined in the
Dockerfile where `ONBUILD` gets triggered. If it's a named context, that
context must be passed to the downstream build.

### [ONBUILD limitations](#onbuild-limitations)

* Chaining `ONBUILD` instructions using `ONBUILD ONBUILD` isn't allowed.
* The `ONBUILD` instruction may not trigger `FROM` or `MAINTAINER` instructions.

## [STOPSIGNAL](#stopsignal)

```
STOPSIGNAL signal
```

The `STOPSIGNAL` instruction sets the system call signal that will be sent to the
container to exit. This signal can be a signal name in the format `SIG<NAME>`,
for instance `SIGKILL`, or an unsigned number that matches a position in the
kernel's syscall table, for instance `9`. The default is `SIGTERM` if not
defined.

`STOPSIGNAL` applies to the signal sent by `docker stop` (and by the Docker
daemon when stopping a container). It does not affect signals sent by keyboard
shortcuts such as Ctrl+C, which sends `SIGINT` directly to the process
regardless of the `STOPSIGNAL` setting.

The image's default stopsignal can be overridden per container, using the
`--stop-signal` flag on `docker run` and `docker create`.

## [HEALTHCHECK](#healthcheck)

The `HEALTHCHECK` instruction has two forms:

* `HEALTHCHECK [OPTIONS] CMD command` (check container health by running a command inside the container)
* `HEALTHCHECK NONE` (disable any healthcheck inherited from the base image)

The `HEALTHCHECK` instruction tells Docker how to test a container to check that
it's still working. This can detect cases such as a web server stuck in
an infinite loop and unable to handle new connections, even though the server
process is still running.

When a container has a healthcheck specified, it has a health status in
addition to its normal status. This status is initially `starting`. Whenever a
health check passes, it becomes `healthy` (whatever state it was previously in).
After a certain number of consecutive failures, it becomes `unhealthy`.

The options that can appear before `CMD` are:

* `--interval=DURATION` (default: `30s`)
* `--timeout=DURATION` (default: `30s`)
* `--start-period=DURATION` (default: `0s`)
* `--start-interval=DURATION` (default: `5s`)
* `--retries=N` (default: `3`)

The health check will first run **interval** seconds after the container is
started, and then again **interval** seconds after each previous check completes.
During the **start period**, health checks run at **start interval** frequency
instead.

If a single run of the check takes longer than **timeout** seconds then the check
is considered to have failed. The process performing the check is abruptly stopped
with a `SIGKILL`.

It takes **retries** consecutive failures of the health check for the container
to be considered `unhealthy`.

**start period** provides initialization time for containers that need time to bootstrap.
Probe failure during that period will not be counted towards the maximum number of retries.
However, if a health check succeeds during the start period, the container is considered
started and all consecutive failures will be counted towards the maximum number of retries.

**start interval** is the time between health checks during the start period.
This option requires Docker Engine version 25.0 or later.

There can only be one `HEALTHCHECK` instruction in a Dockerfile. If you list
more than one then only the last `HEALTHCHECK` will take effect.

The command after the `CMD` keyword can be either a shell command (e.g. `HEALTHCHECK CMD /bin/check-running`) or an exec array (as with other Dockerfile commands;
see e.g. `ENTRYPOINT` for details).

The command's exit status indicates the health status of the container.
The possible values are:

* 0: success - the container is healthy and ready for use
* 1: unhealthy - the container isn't working correctly
* 2: reserved - don't use this exit code

For example, to check every five minutes or so that a web-server is able to
serve the site's main page within three seconds:

```
HEALTHCHECK --interval=5m --timeout=3s \
  CMD curl -f http://localhost/ || exit 1
```

To help debug failing probes, any output text (UTF-8 encoded) that the command writes
on stdout or stderr will be stored in the health status and can be queried with
`docker inspect`. Such output should be kept short (only the first 4096 bytes
are stored currently).

When the health status of a container changes, a `health_status` event is
generated with the new status.

## [SHELL](#shell)

```
SHELL ["executable", "parameters"]
```

The `SHELL` instruction allows the default shell used for the shell form of
commands to be overridden. The default shell on Linux is `["/bin/sh", "-c"]`, and on
Windows is `["cmd", "/S", "/C"]`. The `SHELL` instruction must be written in JSON
form in a Dockerfile.

The `SHELL` instruction is particularly useful on Windows where there are
two commonly used and quite different native shells: `cmd` and `powershell`, as
well as alternate shells available including `sh`.

The `SHELL` instruction can appear multiple times. Each `SHELL` instruction overrides
all previous `SHELL` instructions, and affects all subsequent instructions. For example:

```
FROM microsoft/windowsservercore

# Executed as cmd /S /C echo default
RUN echo default

# Executed as cmd /S /C powershell -command Write-Host default
RUN powershell -command Write-Host default

# Executed as powershell -command Write-Host hello
SHELL ["powershell", "-command"]
RUN Write-Host hello

# Executed as cmd /S /C echo hello
SHELL ["cmd", "/S", "/C"]
RUN echo hello
```

The following instructions can be affected by the `SHELL` instruction when the
shell form of them is used in a Dockerfile: `RUN`, `CMD` and `ENTRYPOINT`.

The following example is a common pattern found on Windows which can be
streamlined by using the `SHELL` instruction:

```
RUN powershell -command Execute-MyCmdlet -param1 "c:\foo.txt"
```

The command invoked by the builder will be:

```
cmd /S /C powershell -command Execute-MyCmdlet -param1 "c:\foo.txt"
```

This is inefficient for two reasons. First, there is an unnecessary `cmd.exe`
command processor (aka shell) being invoked. Second, each `RUN` instruction in
the shell form requires an extra `powershell -command` prefixing the command.

To make this more efficient, one of two mechanisms can be employed. One is to
use the JSON form of the `RUN` command such as:

```
RUN ["powershell", "-command", "Execute-MyCmdlet", "-param1 \"c:\\foo.txt\""]
```

While the JSON form is unambiguous and does not use the unnecessary `cmd.exe`,
it does require more verbosity through double-quoting and escaping. The alternate
mechanism is to use the `SHELL` instruction and the shell form,
making a more natural syntax for Windows users, especially when combined with
the `escape` parser directive:

```
# escape=`

FROM microsoft/nanoserver
SHELL ["powershell","-command"]
RUN New-Item -ItemType Directory C:\Example
ADD Execute-MyCmdlet.ps1 c:\example\
RUN c:\example\Execute-MyCmdlet -sample 'hello world'
```

Resulting in:

```
PS E:\myproject> docker build -t shell .

Sending build context to Docker daemon 4.096 kB
Step 1/5 : FROM microsoft/nanoserver
 ---> 22738ff49c6d
Step 2/5 : SHELL powershell -command
 ---> Running in 6fcdb6855ae2
 ---> 6331462d4300
Removing intermediate container 6fcdb6855ae2
Step 3/5 : RUN New-Item -ItemType Directory C:\Example
 ---> Running in d0eef8386e97

    Directory: C:\

Mode         LastWriteTime              Length Name
----         -------------              ------ ----
d-----       10/28/2016  11:26 AM              Example

 ---> 3f2fbf1395d9
Removing intermediate container d0eef8386e97
Step 4/5 : ADD Execute-MyCmdlet.ps1 c:\example\
 ---> a955b2621c31
Removing intermediate container b825593d39fc
Step 5/5 : RUN c:\example\Execute-MyCmdlet 'hello world'
 ---> Running in be6d8e63fe75
hello world
 ---> 8e559e9bf424
Removing intermediate container be6d8e63fe75
Successfully built 8e559e9bf424
PS E:\myproject>
```

The `SHELL` instruction could also be used to modify the way in which
a shell operates. For example, using `SHELL cmd /S /C /V:ON|OFF` on Windows, delayed
environment variable expansion semantics could be modified.

The `SHELL` instruction can also be used on Linux should an alternate shell be
required such as `zsh`, `csh`, `tcsh` and others.

## [Here-Documents](#here-documents)

Here-documents allow redirection of subsequent Dockerfile lines to the input of
`RUN` or `COPY` commands. If such command contains a [here-document](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html#tag_18_07_04)
the Dockerfile considers the next lines until the line only containing a
here-doc delimiter as part of the same command.

### [Example: Running a multi-line script](#example-running-a-multi-line-script)

```
# syntax=docker/dockerfile:1
FROM debian
RUN <<EOT bash
  set -ex
  apt-get update
  apt-get install -y vim
EOT
```

If the command only contains a here-document, its contents is evaluated with
the default shell.

```
# syntax=docker/dockerfile:1
FROM debian
RUN <<EOT
  mkdir -p foo/bar
EOT
```

Alternatively, shebang header can be used to define an interpreter.

```
# syntax=docker/dockerfile:1
FROM python:3.6
RUN <<EOT
#!/usr/bin/env python
print("hello world")
EOT
```

More complex examples may use multiple here-documents.

```
# syntax=docker/dockerfile:1
FROM alpine
RUN <<FILE1 cat > file1 && <<FILE2 cat > file2
I am
first
FILE1
I am
second
FILE2
```

### [Example: Creating inline files](#example-creating-inline-files)

With `COPY` instructions, you can replace the source parameter with a here-doc
indicator to write the contents of the here-document directly to a file. The
following example creates a `greeting.txt` file containing `hello world` using
a `COPY` instruction.

```
# syntax=docker/dockerfile:1
FROM alpine
COPY <<EOF greeting.txt
hello world
EOF
```

Regular here-doc [variable expansion and tab stripping rules](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html#tag_18_07_04) apply.
The following example shows a small Dockerfile that creates a `hello.sh` script
file using a `COPY` instruction with a here-document.

```
# syntax=docker/dockerfile:1
FROM alpine
ARG FOO=bar
COPY <<-EOT /script.sh
  echo "hello ${FOO}"
EOT
ENTRYPOINT ash /script.sh
```

In this case, file script prints "hello bar", because the variable is expanded
when the `COPY` instruction gets executed.

```
$ docker build -t heredoc .
$ docker run heredoc
hello bar
```

If instead you were to quote any part of the here-document word `EOT`, the
variable would not be expanded at build-time.

```
# syntax=docker/dockerfile:1
FROM alpine
ARG FOO=bar
COPY <<-"EOT" /script.sh
  echo "hello ${FOO}"
EOT
ENTRYPOINT ash /script.sh
```

Note that `ARG FOO=bar` is excessive here, and can be removed. The variable
gets interpreted at runtime, when the script is invoked:

```
$ docker build -t heredoc .
$ docker run -e FOO=world heredoc
hello world
```

## [Dockerfile examples](#dockerfile-examples)

For examples of Dockerfiles, refer to:

* The [building best practices page](https://docs.docker.com/build/building/best-practices/)
* The ["get started" tutorials](https://docs.docker.com/get-started/)
* The [language-specific getting started guides](https://docs.docker.com/guides/language/)

---

1. Value required [↩︎](#fnref:1) [↩︎](#fnref1:1) [↩︎](#fnref2:1)
2. For Docker-integrated [BuildKit](https://docs.docker.com/build/buildkit/#getting-started) and `docker buildx build` [↩︎](#fnref:2)

[Request changes](https://github.com/docker/docs/issues/new?template=doc_issue.yml&location=https%3a%2f%2fdocs.docker.com%2freference%2fdockerfile%2f&labels=status%2Ftriage)

Table of contents

* [Overview](#overview)
* [Format](#format)
* [Parser directives](#parser-directives)

+ [syntax](#syntax)
+ [escape](#escape)
+ [check](#check)

* [Environment replacement](#environment-replacement)
* [.dockerignore file](#dockerignore-file)
* [Shell and exec form](#shell-and-exec-form)

+ [Exec form](#exec-form)

+ [Shell form](#shell-form)
+ [Use a different shell](#use-a-different-shell)

* [FROM](#from)

+ [Understand how ARG and FROM interact](#understand-how-arg-and-from-interact)

* [RUN](#run)

+ [Cache invalidation for RUN instructions](#cache-invalidation-for-run-instructions)
+ [RUN --device](#run---device)

+ [RUN --mount](#run---mount)
+ [RUN --mount=type=bind](#run---mounttypebind)
+ [RUN --mount=type=cache](#run---mounttypecache)

+ [RUN --mount=type=tmpfs](#run---mounttypetmpfs)
+ [RUN --mount=type=secret](#run---mounttypesecret)

+ [RUN --mount=type=ssh](#run---mounttypessh)

+ [RUN --network](#run---network)
+ [RUN --network=default](#run---networkdefault)
+ [RUN --network=none](#run---networknone)

+ [RUN --network=host](#run---networkhost)
+ [RUN --security](#run---security)

* [CMD](#cmd)
* [LABEL](#label)
* [MAINTAINER (deprecated)](#maintainer-deprecated)
* [EXPOSE](#expose)
* [ENV](#env)
* [ADD](#add)

+ [Source](#source)

+ [Destination](#destination)
+ [ADD --keep-git-dir](#add---keep-git-dir)
+ [ADD --checksum](#add---checksum)
+ [ADD --chmod](#add---chmod)
+ [ADD --chown](#add---chown)
+ [ADD --link](#add---link)
+ [ADD --unpack](#add---unpack)
+ [ADD --exclude](#add---exclude)

* [COPY](#copy)

+ [Source](#source-1)

+ [Destination](#destination-1)
+ [COPY --from](#copy---from)
+ [COPY --chmod](#copy---chmod)
+ [COPY --chown](#copy---chown)
+ [COPY --link](#copy---link)

+ [COPY --parents](#copy---parents)
+ [COPY --exclude](#copy---exclude)

* [ENTRYPOINT](#entrypoint)

+ [Exec form ENTRYPOINT example](#exec-form-entrypoint-example)
+ [Shell form ENTRYPOINT example](#shell-form-entrypoint-example)
+ [Understand how CMD and ENTRYPOINT interact](#understand-how-cmd-and-entrypoint-interact)

* [VOLUME](#volume)

+ [Notes about specifying volumes](#notes-about-specifying-volumes)

* [USER](#user)
* [WORKDIR](#workdir)
* [ARG](#arg)

+ [Default values](#default-values)
+ [Scope](#scope)
+ [Using ARG variables](#using-arg-variables)
+ [Predefined ARGs](#predefined-args)
+ [Automatic platform ARGs in the global scope](#automatic-platform-args-in-the-global-scope)
+ [BuildKit built-in build args](#buildkit-built-in-build-args)

+ [Impact on build caching](#impact-on-build-caching)

* [ONBUILD](#onbuild)

+ [Copy or mount from stage, image, or context](#copy-or-mount-from-stage-image-or-context)
+ [ONBUILD limitations](#onbuild-limitations)

* [STOPSIGNAL](#stopsignal)
* [HEALTHCHECK](#healthcheck)
* [SHELL](#shell)
* [Here-Documents](#here-documents)

+ [Example: Running a multi-line script](#example-running-a-multi-line-script)
+ [Example: Creating inline files](#example-creating-inline-files)

* [Dockerfile examples](#dockerfile-examples)

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