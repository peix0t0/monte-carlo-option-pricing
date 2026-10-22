import numpy as np
import matplotlib.pyplot as plt

from src.gbm import simulate_gbm_paths

S0, r, sigma, T = 100, 0.05, 0.20, 1.0
n_steps, n_paths = 252, 20

paths = simulate_gbm_paths(S0, r, sigma, T, n_steps, n_paths, seed=42)
t = np.linspace(0, T, n_steps + 1)

plt.figure(figsize=(9, 5))
plt.plot(t, paths.T, linewidth=0.9)
plt.xlabel("Tempo (anos)")
plt.ylabel("Preço do ativo")
plt.title("Trajetórias do movimento browniano geométrico")
plt.tight_layout()
plt.savefig("trajetorias.png", dpi=150)
plt.show()
