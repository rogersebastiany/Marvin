# Determinismo

O estado em que, dado um input e um [[Contexto]], o output é previsível e reproduzível. Não há variação, não há surpresa — o resultado é consequência necessária das condições iniciais.

---

## Definição

Em filosofia e física, determinismo é a doutrina de que todo evento é causalmente determinado por uma cadeia ininterrupta de eventos anteriores. Dado o estado completo de um sistema num instante, todos os estados futuros são predizíveis.

Em sistemas computacionais, determinismo significa que a mesma entrada produz a mesma saída, sempre. Uma função pura é determinística. Um hash é determinístico. Um LLM com temperatura zero e [[Contexto]] completo se aproxima do determinístico.

## O Problema com LLMs

LLMs são probabilísticos por natureza — calculam distribuições de probabilidade sobre tokens e amostra o próximo. Mesmo com temperatura zero (escolhendo sempre o token mais provável), variações internas (precisão de ponto flutuante, batching, versão do modelo) podem causar [[Drift]] — respostas diferentes para o mesmo input.

O artigo [[LLM Output Drift]] formaliza esse fenômeno: sem [[Contexto]] rígido, a IA varia respostas mesmo com temperatura zero, especialmente cross-provider.

## Como Atingir Determinismo

A tese [[Tautologia Ontológica]] propõe que determinismo em LLMs não é um problema de modelo — é um problema de [[Contexto]]. O modelo é probabilístico, mas se o [[Espaço Amostral]] efetivo for reduzido a um ponto (via [[Ontologia]] completa), a probabilidade do token correto se aproxima de 1.

O artigo [[DFAH]] demonstra empiricamente: contexto estruturado (specs, harness, tools tipadas) produz 89-90%+ de determinismo de trajetória. Especificamente, é **schema-first architecture** — definições de tools com tipos explícitos e retornos formatados — que produz esse número. Três métricas formais capturam granularidades diferentes: ActDet (ações), SigDet (assinaturas), DecDet (decisões).

O artigo [[Ultra-Long-Horizon Agentic Science]] mostra que esse número cresce com [[Acumulação Cognitiva]] — não agregação linear, mas destilação progressiva de experiência em conhecimento em sabedoria (L1→L2→L3).

O caminho: [[Ontologia]] → [[Tautologia]] → Determinismo.

## Determinismo ≠ Acurácia (no caso geral)

O [[DFAH]] revela uma correlação nula (r = -0.11) entre determinismo e acurácia **em agentes com tools genéricas**. Modelos pequenos (7-20B) atingem 100% determinismo a T=0.0 mas erram muito. Modelos grandes são menos determinísticos mas mais capazes.

No caso geral: determinismo sem [[Ontologia]] completa é apenas consistência no erro.

## Determinismo = Acurácia (com Tools Tautológicas)

Quando as tools são [[Tool Tautológica|tautológicas]] — contrato I/O completo, output finito, falha explícita — determinismo **implica** acurácia. A tool só pode retornar a resposta certa ou "não sei". Se o sistema é determinístico com tools tautológicas, é deterministicamente correto.

O r = -0.11 do DFAH mede o caso geral. A tese [[Tautologia Ontológica]] opera no caso específico: [[Ontologia]] completa (cobertura total) com tools tautológicas (contratos completos). Nesse caso, a correlação entre determinismo e acurácia é positiva por construção.

## Determinismo vs Convergência

[[Convergência]] é o processo de se aproximar do determinismo. A [[Loss Function]] converge durante o treinamento — o erro diminui até um mínimo. De forma análoga, o [[Contexto]] converge o [[Espaço Amostral]] — reduz candidatos até que reste (idealmente) um.

Determinismo é o estado final. [[Convergência]] é o caminho até ele.

## Determinismo e Auditabilidade

Determinismo implica auditabilidade: se o resultado é reproduzível, pode ser verificado, testado, e validado. Em domínios regulados (finanças, saúde, direito), determinismo não é desejável — é obrigatório.

11% de indeterminismo (o complemento dos 89%) é gerenciável. 100% de indeterminismo (sem contexto) é inaceitável.

A métrica correta para domínios regulados é **pass^k** (todas as k tentativas devem ter sucesso), não pass@k (pelo menos uma). Um sistema com pass@5 = 95% e pass^5 = 40% parece confiável mas não é.

---

Relaciona-se com: [[Tautologia]], [[Ontologia]], [[Drift]], [[Convergência]], [[Contexto]], [[Espaço Amostral]], [[DFAH]], [[LLM Output Drift]], [[Ultra-Long-Horizon Agentic Science]], [[Acumulação Cognitiva]], [[Tautologia Ontológica]], [[Tool Tautológica]]
