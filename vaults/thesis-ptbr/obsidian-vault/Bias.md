# Bias

Parâmetro que desloca o ponto de [[Activation Function|ativação]] de um neurônio. Cada neurônio calcula: `output = activation(peso × input + bias)`.

---

## Definição

Na [[Álgebra Linear]], bias é o termo constante numa transformação afim: y = Wx + b. Sem bias, a transformação é puramente linear e passa pela origem. Com bias, a transformação pode ser deslocada — o hiperplano de [[Decision Boundary|decisão]] pode ser posicionado em qualquer lugar do espaço.

## Bias como Tool

Na tese, o conceito de bias transcende a definição técnica. Cada [[Tool]] adicionada via [[MCP]] funciona como um bias para o sistema:

"A descrição da tool é um prompt que é tokenizado, embeddado, e esse conjunto vira um bias para o cálculo do próximo possível token."

Sem a tool (sem bias), o neurônio ativa no ponto padrão. Com a tool (com bias), o ponto de ativação é deslocado — favorecendo respostas alinhadas com o [[Contexto]] da tool.

## Visualização

Sem bias: a [[Activation Function]] ReLU ativa no zero — valores positivos passam, negativos não.

Com bias: o ponto de ativação desloca. Um bias positivo faz o neurônio ativar "mais cedo" (para valores menores). Um bias negativo faz ativar "mais tarde."

Cada [[Tool]] é um bias positivo que empurra a ativação na direção correta — reduzindo o espaço de respostas possíveis e aumentando o [[Determinismo]].

---

Relaciona-se com: [[Activation Function]], [[Álgebra Linear]], [[Tool]], [[MCP]], [[Rede Neural]], [[Decision Boundary]], [[Determinismo]]
