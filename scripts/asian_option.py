import numpy as np

from src.gbm import simulate_gbm_paths

S0, K, r, sigma, T = 100, 100, 0.05, 0.20, 1.0
n_steps, n_paths = 252, 200_000

paths = simulate_gbm_paths(S0, r, sigma, T, n_steps, n_paths, seed=11)
avg_price = paths[:, 1:].mean(axis=1)  # média aritmética ao longo do ano
discounted = np.exp(-r * T) * np.maximum(avg_price - K, 0.0)

price = discounted.mean()
se = discounted.std(ddof=1) / np.sqrt(n_paths)
print(f"Call asiática (Monte Carlo): {price:.4f} +- {se:.4f}")
