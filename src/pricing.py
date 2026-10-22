from math import erf, sqrt

import numpy as np


def norm_cdf(x):
    """Função de distribuição acumulada da normal padrão (sem SciPy)."""
    return 0.5 * (1.0 + erf(x / sqrt(2.0)))


def mc_call_price(S0, K, r, sigma, T, n_sims, seed=None):
    """Preço de uma call europeia por Monte Carlo.

    Retorna (preço estimado, erro padrão).
    """
    rng = np.random.default_rng(seed)

    # Z ~ N(0,1): um sorteio por simulação (só o preço final importa)
    Z = rng.standard_normal(n_sims)

    # Solução exata do movimento browniano geométrico em T
    S_T = S0 * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)

    # Ganho do contrato: só vale a pena exercer se S_T > K
    payoff = np.maximum(S_T - K, 0.0)

    # Desconta para o valor de hoje
    discounted = np.exp(-r * T) * payoff

    price = discounted.mean()
    std_error = discounted.std(ddof=1) / np.sqrt(n_sims)
    return price, std_error


def bs_call_price(S0, K, r, sigma, T):
    """Fórmula fechada de Black-Scholes para call europeia."""
    d1 = (np.log(S0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S0 * norm_cdf(d1) - K * np.exp(-r * T) * norm_cdf(d2)