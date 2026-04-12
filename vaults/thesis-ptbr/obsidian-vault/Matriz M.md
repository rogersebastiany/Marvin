# Matriz M

A estrutura matemática resultante do treinamento de um modelo de LLM. Contém toda a "inteligência" do modelo na forma de números — pesos, biases, embeddings — organizados em vetores e matrizes.

---

## Definição

M é composta por m [[Vetor|vetores]] em linha (em R^n) ou n vetores em coluna (R^m). Cada vetor representa uma dimensão do conhecimento aprendido durante o treinamento. O conjunto de todos os vetores de M forma o [[Espaço Amostral]] S.

Em termos concretos: um modelo como GPT-4 ou Claude tem bilhões de parâmetros. Esses parâmetros são números organizados em matrizes — de pesos das camadas de atenção, de embeddings de tokens, de projeções de query/key/value. A Matriz M é a abstração que engloba todas essas matrizes como um único objeto matemático.

## A Matriz como Conhecimento

Os números da Matriz M não precisam fazer sentido individualmente para um humano. Um peso de 0.0342 numa camada específica não tem significado isolado. Mas esses números fazem sentido entre si — suas relações codificam padrões de linguagem, raciocínio, fatos, e associações aprendidos durante o treinamento.

"A IA é um modelo, um programa, uma representação de um espaço vetorial gigantesco cheio de números estranhos — e esses números não precisam fazer sentido pra você, mas eles fazem sentido entre si."

## Relação com Contexto

O [[Contexto]] (prompt) seleciona um [[Subconjunto]] de [[Vetor|vetores]] dentro de M que são relevantes para a tarefa. O modelo não usa toda a Matriz M para cada resposta — ele ativa regiões específicas, guiado pelo input.

Na [[Álgebra Linear]]: o prompt é uma operação de projeção que mapeia o espaço completo M para um subespaço relevante. Quanto mais preciso o prompt, mais precisa a projeção, menor o subespaço, maior o [[Determinismo]].

## Treinamento e Rede Neural

A Matriz M é produzida pelo treinamento da [[Rede Neural]]. O processo de [[Backpropagation]] + [[Gradient Descent]] ajusta iterativamente os valores de M para minimizar a [[Loss Function]]. Quando o treinamento [[Convergência|converge]], M representa uma aproximação otimizada dos padrões nos dados de treinamento.

Após o treinamento, M é fixa (frozen). O que muda entre interações é o [[Contexto]] — que determina como M é consultada.

---

Relaciona-se com: [[Espaço Amostral]], [[Vetor]], [[Álgebra Linear]], [[Embedding]], [[Contexto]], [[Rede Neural]], [[Backpropagation]], [[Determinismo]]
