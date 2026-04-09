# Embedding

Processo de transformar tokens (texto, áudio, vídeo) em [[Vetor|vetores]] numéricos no [[Espaço Amostral]]. A ponte entre linguagem humana e [[Álgebra Linear]].

---

## Definição

Embedding é a representação de objetos discretos (palavras, tokens) como vetores contínuos em R^n. O modelo de embedding "conhece" a [[Matriz M]] e posiciona cada token num ponto do espaço vetorial de forma que relações semânticas se traduzam em relações geométricas.

## Processo

1. [[Tokenização]] quebra o input em chunks (tokens)
2. Embedding transforma cada token num vetor em R^n
3. Os vetores ficam posicionados no [[Espaço Amostral]]
4. O modelo opera sobre esses vetores
5. Os vetores de output passam pelo embedding reverso
6. Tokens de output são decodificados de volta para texto

"Os vetores resultados se transformam em chunks, e por fim no formato do output esperado, usando o mesmo modelo de embedding. O processo reverso basicamente."

## Propriedades

Vetores próximos = conceitos similares. A similaridade por cosseno ([[Álgebra Linear]]) mede essa proximidade. Isso permite que o [[RAG]] funcione — busca por similaridade vetorial encontra conteúdo semanticamente relevante mesmo sem correspondência exata de palavras.

---

Relaciona-se com: [[Vetor]], [[Tokenização]], [[Matriz M]], [[Espaço Amostral]], [[Álgebra Linear]], [[RAG]]
