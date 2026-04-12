# HTML para Markdown

O pipeline de conversão do [[web-to-docs]] que transforma páginas web em documentação pesquisável. `httpx` + `BeautifulSoup` + `markdownify` → arquivo `.md` em `docs/`.

---

## O Pipeline

```
URL → httpx.get(url, verify=False) → HTML
  → markdownify(html, heading_style="ATX", strip=["img", "script", "style"]) → Markdown bruto
  → regex cleanup (colapsar 3+ newlines em 2) → Markdown limpo
  → Path.write_text() → docs/{slug}.md
```

## Componentes

**httpx:** Cliente HTTP assíncrono. `follow_redirects=True`, `timeout=30`. O `verify=False` desabilita validação TLS — caveat para [[Arquitetura de Produção|produção]].

**BeautifulSoup:** Parser HTML usado pelo `crawl_docs` para extrair links (`<a href="...">`) e construir a fila BFS de crawling. Filtra por same-prefix para não sair do site.

**markdownify:** Converte HTML para Markdown com headings ATX (`#`, `##`). Strip de `img`, `script`, `style` — remove ruído, mantém conteúdo textual.

## Auto-Nomeação

O `crawl_docs` e `batch_convert` derivam filenames automaticamente:

```python
def _slugify(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[\s_]+", "-", text).strip("-")[:80]
```

Extrai o título do primeiro `# heading` do markdown, slugifica, e salva como `{slug}.md`. Se o arquivo já existe, adiciona contador: `{slug}-1.md`, `{slug}-2.md`.

## Papel na Tese

O pipeline é o mecanismo de **construção de [[Ontologia como Código|ontologia]]**. A web contém conhecimento, mas em formato não pesquisável pelo [[docs-server]]. O pipeline converte para markdown — formato que `search_docs` pode indexar.

Cada página convertida expande o [[Subconjunto]] A ⊂ S. O complemento S \ A (zona de [[Alucinação]]) diminui. É o [[Feedback Loop Determinístico]] materializado: web → markdown → searchable → mais [[Contexto Programático|contexto]] → mais [[Determinismo Mensurável|determinismo]].

## Limitações

- `verify=False` — sem validação TLS
- Sem autenticação — não busca docs atrás de SSO/login
- Sem rate limiting — pode sobrecarregar sites
- Keyword search, não semântica — [[RAG Implícito]], não RAG completo
- Sem deduplicação de conteúdo — crawl pode salvar páginas similares

Em [[Arquitetura de Produção|produção]], estas limitações são resolvidas: TLS validado, auth via headers, rate limiting, e potencialmente busca semântica com [[Embedding|embeddings]].

---

Relaciona-se com: [[web-to-docs]], [[Ontologia como Código]], [[Feedback Loop Determinístico]], [[RAG Implícito]], [[docs-server]], [[Arquitetura de Produção]], [[Contexto Programático]]
