# MCP

Model Context Protocol. Endereçamento indireto O(1) para [[Contexto]] externo via gRPC. A porteira aberta entre a IA e os dados.

---

## Definição

O MCP coloca procedures diretamente no stdin/stdout via gRPC. É stream, não async. Para a IA, acessar um log no servidor de Frankfurt ou uma tabela no banco local tem o mesmo "custo" cognitivo. É O(1), como se fosse memória RAM.

"O modelo não precisa 'procurar' como acessar — a interface já está mapeada."

## Sem MCP vs Com MCP

**Sem**: integrar ferramenta externa exige criar APIs, lidar com autenticação complexa e latência. Cada integração é um projeto.

**Com**: contexto (logs, DB, métricas, [[Tool|tools]]) exposto via gRPC. Endereçamento indireto — o modelo aponta pro contexto, não copia.

## A Porteira Aberta

MCP é a porteira aberta entre a IA e o contexto. A porteira em si não tem segurança — é pipe puro. A segurança fica no terreno ao redor: VPN, mTLS, VPC, IAM, WAF, Cognito.

## Viabilizador da Ontologia

MCP é o que torna a [[Ontologia]] completa viável em tempo real. Sem MCP, acessar cada contexto externo teria latência variável, autenticação diferente, formatos incompatíveis. Com MCP, tudo é O(1), tudo é stream, tudo é padronizado.

É o componente de infraestrutura que transforma a teoria (ontologia completa) em prática (acesso instantâneo a todo contexto).

---

Relaciona-se com: [[Tool]], [[Contexto]], [[Agente]], [[Ontologia]], [[RAG]]
