import numpy as np
import matplotlib.pyplot as plt

from src.gbm import simulate_gbm_terminal_euler
from src.pricing import bs_call_price

S0, K, r, sigma, T = 100, 100, 0.05, 0.20, 1.0
analytic = bs_call_price(S0, K, r, sigma, T)

n_paths = 1_000_000
steps_list = [1, 2, 4, 8, 16, 32, 64]

errors = []
for n_steps in steps_list:
    # mesma semente em todos os casos, para o ruído do Monte Carlo ser comparável
    S_T = simulate_gbm_terminal_euler(S0, r, sigma, T, n_steps, n_paths, seed=123)
    price = np.exp(-r * T) * np.maximum(S_T - K, 0.0).mean()
    errors.append(abs(price - analytic))
    print(f"passos={n_steps:>4}  preço={price:.4f}  erro={errors[-1]:.4f}")

steps = np.array(steps_list)
ref = errors[0] * (steps / steps[0]) ** -1.0  # referência: inclinação -1

plt.figure(figsize=(8, 5))
plt.loglog(steps, errors, "o-", label="Erro do Euler-Maruyama")
plt.loglog(steps, ref, "k:", label="Referência: inclinação -1")
plt.xlabel("Número de passos de tempo")
plt.ylabel("Erro do preço da call")
plt.title("Erro de discretização: Euler-Maruyama vs Black-Scholes")
plt.legend()
plt.grid(True, which="both", alpha=0.3)
plt.tight_layout()
plt.savefig("euler_convergencia.png", dpi=150)
plt.show()