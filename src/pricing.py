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


def mc_call_price_antithetic(S0, K, r, sigma, T, n_sims, seed=None):
    """Call europeia por Monte Carlo com variáveis antitéticas.

    Usa n_sims // 2 pares (Z, -Z). Retorna (preço estimado, erro padrão).
    """
    rng = np.random.default_rng(seed)
    n_pairs = n_sims // 2
    Z = rng.standard_normal(n_pairs)

    drift = (r - 0.5 * sigma**2) * T
    vol = sigma * np.sqrt(T)
    S_plus = S0 * np.exp(drift + vol * Z)
    S_minus = S0 * np.exp(drift - vol * Z)

    payoff_plus = np.maximum(S_plus - K, 0.0)
    payoff_minus = np.maximum(S_minus - K, 0.0)

    # Cada par vira UMA observação: a média dos dois ganhos
    pair_avg = np.exp(-r * T) * 0.5 * (payoff_plus + payoff_minus)

    price = pair_avg.mean()
    std_error = pair_avg.std(ddof=1) / np.sqrt(n_pairs)
    return price, std_error