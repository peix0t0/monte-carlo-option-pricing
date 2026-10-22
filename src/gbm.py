import numpy as np


def simulate_gbm_paths(S0, r, sigma, T, n_steps, n_paths, seed=None):
    """Simula trajetórias do movimento browniano geométrico (solução exata).

    Retorna um array de formato (n_paths, n_steps + 1).
    """
    rng = np.random.default_rng(seed)
    dt = T / n_steps

    # Z: ruído normal padrão. Cada Z*sqrt(dt) é um incremento do processo de Wiener.
    Z = rng.standard_normal((n_paths, n_steps))

    # Incremento do log-preço em cada passo
    log_increments = (r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z

    # O log-preço acumulado é a soma dos incrementos
    log_paths = np.cumsum(log_increments, axis=1)
    paths = S0 * np.exp(log_paths)

    # Adiciona o preço inicial na coluna 0
    start = np.full((n_paths, 1), S0)
    return np.hstack([start, paths])