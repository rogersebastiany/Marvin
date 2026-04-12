# Deterministic Trajectory Optimization

Artigo que reformula controle ótimo determinístico como inferência probabilística, demonstrando convergência garantida de políticas probabilísticas para a trajetória ótima determinística via Expectation-Maximization. O mesmo padrão da tese aplicado a sistemas dinâmicos.

---

## Referência

**Deterministic Trajectory Optimization through Probabilistic Optimal Control**
Mohammad Mahmoudi Filabadi, Tom Lefebvre, Guillaume Crevecoeur — Ghent University, Bélgica
https://arxiv.org/abs/2407.13316

## Contribuição

Reformula o problema de controle ótimo determinístico como um problema de Maximum Likelihood Estimation (MLE). Introduz variáveis de otimalidade latentes e usa EM para iterativamente refinar políticas probabilísticas até convergir para a política ótima determinística.

## O Mecanismo

1. **Começa probabilístico**: política inicial é uma distribuição sobre ações possíveis (o [[Espaço Amostral]] completo).
2. **E-step**: Avalia a política atual contra o modelo do sistema (a informação estruturada).
3. **M-step**: Refina a política maximizando o ELBO (Evidence Lower BOund).
4. **Itera**: A cada iteração, a política se torna menos incerta. O parâmetro de risco γ controla a velocidade de [[Convergência]].
5. **Converge**: O EM garante melhoria monotônica. As políticas probabilísticas convergem para a política ótima determinística.

## Dois Algoritmos

- **SP-PDP** (Sigma-Point Probabilistic Dynamic Programming): Forward pass avalia a política, backward pass atualiza. Relacionado ao DDP clássico.
- **SP-BSC** (Sigma-Point Bayesian Smoothing Control): Forward e backward passes acontecem simultaneamente. Convergência mais rápida.

Ambos usam sigma-point methods (unscented transform) em vez de gradientes — funcionam em sistemas não-lineares sem exigir diferenciabilidade.

## O Parâmetro γ

γ controla exploração vs explotação:
- γ alto → políticas mais exploratórias (mais probabilísticas)
- γ baixo → políticas mais determinísticas
- γ → 0 → política converge para o ótimo determinístico

É análogo à temperatura em LLMs: T alto → mais variação ([[Drift]]), T baixo → mais [[Determinismo]]. A estrutura do [[Contexto]] é o que faz T baixo funcionar bem em vez de colapsar.

## Convergência Garantida

O EM garante:
- Melhoria monotônica do log-likelihood a cada iteração
- Sequência de políticas probabilísticas que converge para o ótimo determinístico
- A incerteza da política escala com o grau de exploração necessário

Testado em pêndulo invertido e cart-pole — sistemas não-lineares. SP-BSC atinge melhor performance geral.

## Conexão com a Tese

O conceito é idêntico à [[Tautologia Ontológica]], só muda o domínio e o cálculo:

- **Este artigo**: sistema dinâmico + modelo + EM → trajetória determinística
- **A tese**: LLM + [[Ontologia]] completa + [[Tool|tools]] → output determinístico

O padrão: informação estruturada + refinamento iterativo → [[Convergência]] para [[Determinismo]]. Na tese, o "EM" é o [[Feedback Loop Determinístico]] — cada ciclo de tool call enriquece o [[Contexto]], reduz o [[Espaço Amostral]], e aproxima a resposta do determinístico.

"ESSE ARTIGO AQUI QUE FALA QUE O CONTEXTO COMPLETO (ONTOLOGIA) VC CONSEGUE CHEGAR EM 89% DE DETERMINISMO, SEM PRECISAR CALCULAR O MELHOR CAMINHO NO CÁLCULO QUE ELES TÃO FAZENDO LÁ OS NERD DE FÍSICA." A tese atinge determinismo pela completude da [[Ontologia]], não pelo cálculo ótimo — mas o padrão convergente é o mesmo.

---

Relaciona-se com: [[Determinismo]], [[Convergência]], [[Ontologia]], [[Tautologia Ontológica]], [[Espaço Amostral]], [[Drift]], [[Feedback Loop Determinístico]], [[Tool]]
