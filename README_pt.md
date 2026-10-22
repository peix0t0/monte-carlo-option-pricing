[English](README.md) | Português

# monte-carlo-option-pricing

Precificação de opções europeias por Monte Carlo, validada contra a solução analítica de Black-Scholes. Projeto pessoal construído a partir do curso de Processos Estocásticos (ENSEEIHT, MF2E), com foco em rigor numérico: validação contra solução exata, análise de convergência e separação entre erro estatístico e erro de discretização.

## O que o projeto faz

- Simula o movimento browniano geométrico (GBM), pela solução exata e pelo esquema de Euler-Maruyama
- Precifica uma call europeia por Monte Carlo e compara com a fórmula de Black-Scholes
- Mede a convergência do erro do Monte Carlo (taxa 1/sqrt(N))
- Mede o erro de discretização do Euler-Maruyama, separado do ruído estatístico
- Aplica variáveis antitéticas como técnica de redução de variância
- Precifica uma call asiática de média aritmética, que não tem fórmula fechada
- Testes automatizados com pytest

## Resultados

Parâmetros em todos os experimentos: S0 = 100, K = 100, r = 5%, sigma = 20%, T = 1 ano. Valor analítico da call (Black-Scholes): **10,4506**.

### Trajetórias simuladas

![trajetorias](trajetorias.png)

Vinte trajetórias do GBM. A dispersão cresce com o tempo, como esperado de um processo de Wiener.

### Monte Carlo contra Black-Scholes

| N | Monte Carlo | Erro padrão | Erro absoluto |
|---|---|---|---|
| 100 | 7,8258 | 1,0120 | 2,6248 |
| 1.000 | 9,9120 | 0,4483 | 0,5386 |
| 10.000 | 10,3452 | 0,1477 | 0,1054 |
| 100.000 | 10,4205 | 0,0468 | 0,0300 |
| 1.000.000 | 10,4532 | 0,0147 | 0,0026 |

### Convergência do Monte Carlo

![convergencia](convergencia.png)

Em escala log-log, o erro padrão acompanha a reta de inclinação -1/2, consequência do teorema central do limite: para reduzir o erro por 10 são necessárias 100 vezes mais simulações. O erro absoluto médio (30 repetições por N) segue a mesma inclinação, com ruído residual por ser média de poucas repetições.

### Erro de discretização do Euler-Maruyama

![euler](euler_convergencia.png)

Erro do preço da call usando Euler-Maruyama com 1 milhão de trajetórias e a mesma semente em todos os casos:

| Passos | Preço | Erro |
|---|---|---|
| 1 | 10,2070 | 0,2436 |
| 2 | 10,3743 | 0,0763 |
| 4 | 10,4125 | 0,0381 |
| 8 | 10,4345 | 0,0160 |
| 16 | 10,4590 | 0,0084 |
| 32 | 10,4513 | 0,0007 |
| 64 | 10,4589 | 0,0083 |

Entre 2 e 16 passos, o erro cai de forma compatível com ordem fraca 1, a esperada para o Euler-Maruyama. A partir de cerca de 16 passos, o erro de discretização fica menor que o ruído do Monte Carlo (erro padrão de aproximadamente 0,015 com N = 10^6), e a curva deixa de ser informativa: os valores de 32 e 64 passos refletem flutuação estatística, não o comportamento do método. Para verificar a ordem com mais nitidez seria preciso aumentar N ou usar o mesmo ruído browniano entre níveis de refinamento.

### Redução de variância com variáveis antitéticas

Usando pares (Z, -Z), o erro padrão cai de forma estável com o mesmo número de sorteios:

| N | Erro padrão simples | Erro padrão antitético | Redução |
|---|---|---|---|
| 1.000 | 0,4462 | 0,3074 | 1,45x |
| 10.000 | 0,1460 | 0,1050 | 1,39x |
| 100.000 | 0,0464 | 0,0328 | 1,41x |
| 1.000.000 | 0,0147 | 0,0104 | 1,41x |

A redução é de cerca de 1,4x no erro padrão, o que equivale a precisar de aproximadamente metade das simulações para a mesma precisão. A técnica melhora a constante do erro, não a taxa 1/sqrt(N).

### Call asiática (sem fórmula fechada)

Uma call asiática de média aritmética paga max(preço médio ao longo do ano - K, 0). Não existe preço fechado simples, então o Monte Carlo é necessário. Com 200.000 trajetórias e 252 passos diários:

| Opção | Preço | Erro padrão |
|---|---|---|
| Call europeia (Black-Scholes) | 10,4506 | - |
| Call asiática (Monte Carlo) | 5,7680 | 0,0179 |

O preço da asiática é cerca de 55% do da europeia, como esperado: a média suaviza a trajetória e reduz a chance de um ganho grande. Este resultado não foi validado contra um valor exato; uma verificação natural seria a asiática de média geométrica, que tem preço fechado.

## Como rodar

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m scripts.compare_prices
python -m scripts.plot_paths
python -m scripts.plot_convergence
python -m scripts.plot_euler
python -m scripts.compare_variance_reduction
python -m scripts.asian_option
python -m pytest
```

Os comandos acima são para Windows. No Linux ou macOS, ative o ambiente com `source .venv/bin/activate`.

## Estrutura

```
src/
  gbm.py        simulação do GBM (solução exata e Euler-Maruyama)
  pricing.py    Monte Carlo, antitéticas e Black-Scholes
scripts/        experimentos e geração dos gráficos
tests/          testes automatizados
```

## Teoria resumida

Sob a medida neutra ao risco, o preço do ativo segue

dS = r S dt + sigma S dW,

onde W é um processo de Wiener. A solução exata é

S_T = S0 exp((r - sigma^2 / 2) T + sigma sqrt(T) Z), com Z ~ N(0, 1).

O termo -sigma^2/2 é a correção do lema de Itô. O preço de uma call europeia é o valor esperado descontado do ganho final:

C = exp(-rT) E[max(S_T - K, 0)].

O Monte Carlo estima essa esperança por uma média amostral sobre N sorteios, com erro padrão s / sqrt(N), onde s é o desvio padrão amostral dos ganhos descontados. Para o caso europeu existe a fórmula fechada de Black-Scholes, usada aqui como referência de validação. A função de distribuição normal é calculada com `math.erf`, sem dependência do SciPy.

O esquema de Euler-Maruyama aproxima a EDE passo a passo:

S[k+1] = S[k] + r S[k] dt + sigma S[k] sqrt(dt) Z[k].

Ele introduz um erro de discretização que depende do passo dt, distinto do erro estatístico do Monte Carlo, que depende de N.

## Limitações

- Apenas opções com parâmetros constantes (sem volatilidade estocástica ou dividendos)
- A verificação da ordem do Euler-Maruyama é limitada pelo ruído do Monte Carlo para mais de 16 passos
- O preço da call asiática não foi validado contra um valor exato

## Licença

MIT
