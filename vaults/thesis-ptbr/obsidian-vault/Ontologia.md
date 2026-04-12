# Ontologia

O estudo do que existe e de como as entidades de um domínio se relacionam. Define a estrutura conceitual de um sistema — o "mapa" de tudo que é real dentro de um escopo.

---

## Origem Filosófica

Ontologia vem do grego *ontos* (ser) + *logos* (estudo). Na filosofia, é o ramo da metafísica que investiga a natureza do ser, da existência e da realidade. Aristóteles a chamava de "filosofia primeira" — o estudo das categorias fundamentais de tudo que existe.

A pergunta central da ontologia é: "o que existe?" E a resposta organiza o mundo em categorias, propriedades e relações entre entidades.

## Ontologia em Computação

Em ciência da computação, ontologia é a especificação formal e explícita de uma conceitualização compartilhada. Isso significa: definir todas as entidades de um domínio, suas propriedades, e as relações entre elas, de forma que um sistema computacional possa operar sobre essas definições.

Exemplos:
- Definir o que é um nó, o que é uma aresta, e o que é um [[Grafo Dirigido Completo]] — isso é ontologia de grafos
- Definir o que é um microsserviço, uma fila SQS, um endpoint, e como se conectam — isso é ontologia de uma arquitetura
- Definir todas as interações possíveis de um sistema de pagamento — isso é ontologia do domínio financeiro

## Ontologia como Contexto Completo

Na tese [[Tautologia Ontológica]], ontologia é sinônimo de [[Contexto]] completo. Quando todas as entidades, relações, comportamentos e restrições de um domínio estão definidas e acessíveis ao modelo via [[Tool|tools]] e [[MCP]], o modelo tem a ontologia completa daquele domínio.

A consequência direta: se a ontologia é completa, a [[Inferência]] se transforma em [[Dedução]], e o resultado é [[Tautologia|tautológico]].

## Ontologia e o Espaço Amostral

Na [[Teoria dos Conjuntos]], a ontologia define qual [[Subconjunto]] do [[Espaço Amostral]] é relevante. Sem ontologia, o modelo opera no espaço S inteiro — alta incerteza, alto risco de [[Alucinação]]. Com ontologia completa, opera num [[Subconjunto]] A ⊂ S tão preciso que a resposta correta é dedutível.

Cada camada de ontologia adicionada (specs, testes, ADRs, docs, logs) é uma restrição adicional sobre S — reduzindo dimensões, eliminando candidatos inválidos, aproximando A de um ponto único.

## Ontologia por Domínio

A ontologia universal não existe — ninguém mapeou tudo que existe em todos os domínios. Mas a ontologia por domínio é construível. Um pós-doutor em biologia possui a ontologia do campo da biologia. Se essa ontologia for traduzida em [[Tool|tools]] e servida via [[MCP]], um [[Agente]] operando nesse domínio atinge [[Determinismo]] quase total.

Isso é replicável para qualquer domínio: direito, medicina, engenharia, finanças. Muda a ontologia, muda as tools, o framework é o mesmo.

## Quando a Ontologia É Completa

A ontologia de um domínio é completa quando **todo método/processo do domínio tem uma [[Tool Tautológica]] correspondente**. Não existe método na empresa ou área que o agente precisaria executar mas não tem tool para fazê-lo.

Isso é verificável:
1. Enumere todos os métodos/processos do domínio
2. Para cada um, verifique: existe uma tool correspondente?
3. Para cada tool, verifique: é [[Tool Tautológica|tautológica]]? (contrato I/O completo, output finito, falha explícita)

Se sim para todos → ontologia completa → [[Tautologia]] por construção → [[Determinismo]] com acurácia.

A completude não é abstrata — é uma checklist concreta.

---

Relaciona-se com: [[Tautologia]], [[Contexto]], [[Espaço Amostral]], [[Teoria dos Conjuntos]], [[Tool]], [[Tool Tautológica]], [[MCP]], [[Determinismo]], [[Alucinação]], [[Tautologia Ontológica]]
