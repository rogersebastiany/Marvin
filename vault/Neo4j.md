# Neo4j

Graph database que armazena a [[Ontologia como Código|ontologia]] como knowledge graph. Cada conceito dos vaults vira um nó, cada link vira uma aresta. O [[Agente na POC|agente]] consulta e enriquece o grafo via [[mcp-ontology-server]].

---

## Por que Grafo

A [[Ontologia como Código|ontologia]] nos vaults Obsidian já é um grafo — notas são nós, wikilinks são arestas. Neo4j materializa esse grafo num banco consultável, traversável, e enriquecível pelo agente.

Diferente de um banco relacional, Neo4j permite queries de travessia (2 hops, 3 hops, caminho entre conceitos) em tempo constante relativo à vizinhança, não ao tamanho total do grafo.

## Schema Acordado

**Nós** — Label `:Concept`
- `name`: Nome do conceito (e.g. "Tautologia Ontológica")
- `vault`: De qual vault veio ("thesis", "implementation", ou "both" se merged)
- `summary`: Resumo de uma linha
- `content`: Conteúdo completo da nota markdown
- `ghost`: Boolean — true se o conceito é referenciado mas não tem nota própria (ghost node no Obsidian)
- `created_at`, `updated_at`: Timestamps

**Arestas** — Tipo único `:RELATES_TO` com property bag
- `type`: Tipo semântico da relação (e.g. "implements", "validates", "contradicts")
- `weight`: Força da relação (0.0 a 1.0)
- `reasoning`: Por que essa relação existe
- `discovered_by`: Quem criou — "vault_import", "agent", "user"

Flat edges com property bags em vez de múltiplos tipos de aresta. O agente pode criar relações não-lineares entre conceitos sem precisar de novos tipos de aresta — basta adicionar propriedades ao edge existente.

## Merge de Conceitos

Conceitos que aparecem em ambos os vaults (e.g. "Determinismo" no thesis vault e "Determinismo Mensurável" no implementation vault) são merged num único nó com `vault: "both"`. O conteúdo combina perspectivas — teórica e prática.

Ghost nodes (referenciados mas sem nota) viram nós com `ghost: true`. O agente pode preencher esses nós ao longo do tempo.

## Papel na Arquitetura

Neo4j é o backend do [[mcp-ontology-server]]. O agente consulta o grafo para:
- Entender conceitos e suas relações
- Traversar vizinhança (o que se relaciona com X?)
- Descobrir gaps (quais ghost nodes existem?)
- Enriquecer a ontologia (adicionar conceitos, relações, propriedades)

É a [[Ontologia como Código|ontologia]] viva — não estática, enriquecida a cada interação do [[Loop de Auto-Melhoria]].

---

Relaciona-se com: [[Ontologia como Código]], [[mcp-ontology-server]], [[Loop de Auto-Melhoria]], [[Agente na POC]], [[MCP]]
