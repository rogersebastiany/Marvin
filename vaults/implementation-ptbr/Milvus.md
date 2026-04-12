# Milvus

Vector database que armazena a memória episódica do [[Agente na POC|agente]]. Cada tool call, decisão, e sessão é embeddada e armazenada. O agente consulta Milvus para encontrar ações similares do passado via [[mcp-memory-server]].

---

## Por que Vetores

O [[Agente na POC|agente]] precisa de memória semântica, não textual. "Qual foi a última vez que busquei documentação de AWS Lambda?" não é uma query de texto — é uma query de similaridade no espaço de [[Embedding|embeddings]]. Milvus faz busca por vizinhança em espaços de alta dimensão.

## Três Coleções

Três coleções simultâneas, cada uma capturando uma granularidade de memória:

**1. Tool Calls (~6KB cada)**
Cada invocação de tool: qual tool, parâmetros, resultado, timestamp, contexto. Granularidade mais fina. É o L1 (Experience) do HCC descrito em [[Acumulação Cognitiva]].

**2. Decisions (~6KB cada)**
Cada decisão de alto nível: qual objetivo, quais opções consideradas, qual escolhida, por quê. Granularidade média. É o L2 (Knowledge) do HCC.

**3. Sessions (~6KB cada)**
Resumo de cada sessão completa: objetivo, abordagem, resultado, lições aprendidas. Granularidade mais grossa. É o L3 (Wisdom) do HCC.

## Embeddings

OpenAI embeddings (`text-embedding-3-small` ou similar). Cada registro é embeddado no momento da ingestão. Busca por similaridade de cosseno com threshold configurável.

As três coleções armazenadas simultaneamente permitem busca em qualquer nível de abstração: "tool calls parecidas com esta", "decisões parecidas com esta", "sessões parecidas com esta".

## Paralelo com HCC

O artigo [[Ultra-Long-Horizon Agentic Science]] valida esta arquitetura. O HCC (Hierarchical Cognitive Caching) usa exatamente três camadas de memória — L1 (experiência), L2 (conhecimento), L3 (sabedoria). A ablation study mostra que todas as três são necessárias: sem L1, medal rate cai para 22.7%; sem L3, cai para 54.5%.

Nosso design mapeia diretamente:
- Tool calls → L1 (Evolving Experience)
- Decisions → L2 (Refined Knowledge)
- Sessions → L3 (Prior Wisdom)

## Papel na Arquitetura

Milvus é o backend do [[mcp-memory-server]]. O agente:
- **Loga** cada tool call, decisão, e sessão automaticamente
- **Busca** ações similares antes de agir ("já fiz algo parecido?")
- **Aprende** com o passado — se uma abordagem funcionou antes, reutiliza; se falhou, evita

É a memória que torna o [[Loop de Auto-Melhoria]] possível.

---

Relaciona-se com: [[mcp-memory-server]], [[Embedding]], [[Acumulação Cognitiva]], [[Loop de Auto-Melhoria]], [[Agente na POC]], [[MCP]]
