# Redução de Espaço na Prática

Cada tool call na POC é uma operação de [[Redução de Dimensionalidade]] sobre o [[Espaço Amostral]]. O modelo passa de operar em S inteiro para operar num [[Subconjunto]] A cada vez menor e mais preciso.

---

## Exemplo Concreto

Sem tools, o agente recebe: "como funciona autenticação no nosso sistema?"
O modelo opera em S inteiro — toda a [[Matriz M]] é candidata. Alta incerteza, risco de [[Alucinação]].

Com tools na POC:

```
1. list_docs() → ["api-reference.md", "architecture.md", "getting-started.md", ...]
   Redução: o modelo sabe quais docs existem. S → S₁ ⊂ S

2. search_docs("authentication") → matches em architecture.md linhas 45-52
   Redução: o modelo sabe o que os docs dizem sobre auth. S₁ → S₂ ⊂ S₁

3. get_doc_summary("architecture.md") → seção sobre JWT + middleware
   Redução: o modelo tem o contexto arquitetural. S₂ → S₃ ⊂ S₂

4. generate_diagram("auth flow with JWT") → diagrama com syntax refs
   Redução: o modelo tem a representação visual. S₃ → S₄ ⊂ S₃
```

Cada passo é um condicionamento na [[Probabilidade Condicional]]:
P(resposta|prompt) → P(resposta|prompt, docs) → P(resposta|prompt, docs, search) → P(resposta|prompt, docs, search, diagram)

## Os 4 Servers como 4 Dimensões de Redução

| Server | Dimensão que reduz |
|---|---|
| [[docs-server]] | "O que sabemos?" — elimina o desconhecido |
| [[web-to-docs]] | "O que podemos saber?" — expande e depois elimina |
| [[prompt-engineer]] | "Como perguntar?" — elimina ambiguidade |
| [[system-design]] | "Como se parece?" — elimina interpretações visuais erradas |

Juntos, os 4 servers atacam as 4 principais fontes de incerteza do [[Espaço Amostral]].

## Interseção de Subconjuntos

Na [[Teoria dos Conjuntos]], cada tool define um subconjunto T ⊂ S. A interseção de múltiplas tools refina:

- A (prompt) ∩ T₁ (docs) ∩ T₂ (search) ∩ T₃ (diagram) = subconjunto altamente preciso

Quando essa interseção contém poucos candidatos viáveis, a resposta é quase [[Tautologia|tautológica]] — verdadeira por construção, não por probabilidade.

---

Relaciona-se com: [[Espaço Amostral]], [[Subconjunto]], [[Redução de Dimensionalidade]], [[Probabilidade Condicional]], [[Teoria dos Conjuntos]], [[Cadeia de Servers]], [[docs-server]], [[web-to-docs]], [[prompt-engineer]], [[system-design]], [[Contexto Programático]], [[Tautologia]]
