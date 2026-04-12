# Divergência

Quando uma série, processo ou sistema se afasta de um valor estável. O erro oscila ou aumenta. O oposto de [[Convergência]].

---

## Definição

Uma série diverge se não tende a um limite finito. Em otimização, divergência significa que o algoritmo está se afastando do mínimo — o erro cresce em vez de diminuir.

## Na Rede Neural

A [[Loss Function]] diverge quando o treinamento falha: learning rate muito alta, dados ruidosos, arquitetura inadequada. Os pesos oscilam em vez de convergir.

## Relação com Drift

Divergência no treinamento é análoga ao [[Drift]] na inferência. Sem [[Contexto]] rígido, o modelo "diverge" — produz respostas cada vez mais distantes do resultado correto.

Na observação sobre os [[Vetor|vetores]] não-lineares: "em momentos converge, outros diverge" — a rede precisa de mais estrutura (mais camadas, mais neurônios, melhor [[Activation Function]]) para resolver as regiões divergentes.

---

Relaciona-se com: [[Convergência]], [[Drift]], [[Loss Function]], [[Rede Neural]], [[Relação Não-Linear]]
