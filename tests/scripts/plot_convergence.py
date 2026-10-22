import numpy as np
import matplotlib.pyplot as plt

from src.pricing import mc_call_price, bs_call_price

S0, K, r, sigma, T = 100, 100, 0.05, 0.20, 1.0
analytic = bs_call_price(S0, K, r, sigma, T)

Ns = np.logspace(2, 6, 9).astype(int)  # de 100 a 1.000.000
n_reps = 30  # repetições por N, para estimar o erro típico

mean_abs_err = []
mean_se = []
for n in Ns:
    errs, ses = [], []
    for rep in range(n_reps):
        price, se = mc_call_price(S0, K, r, sigma, T, n, seed=rep)
        errs.append(abs(price - analytic))
        ses.append(se)
    mean_abs_err.append(np.mean(errs))
    mean_se.append(np.mean(ses))

# Reta de referência com inclinação -1/2, ancorada no primeiro ponto
ref = mean_se[0] * (Ns / Ns[0]) ** -0.5

plt.figure(figsize=(8, 5))
plt.loglog(Ns, mean_abs_err, "o-", label="Erro absoluto médio (30 repetições)")
plt.loglog(Ns, mean_se, "s--", label="Erro padrão estimado")
plt.loglog(Ns, ref, "k:", label="Referência: inclinação -1/2")
plt.xlabel("Número de simulações N")
plt.ylabel("Erro")
plt.title("Convergência do Monte Carlo (call europeia)")
plt.legend()
plt.grid(True, which="both", alpha=0.3)
plt.tight_layout()
plt.savefig("convergencia.png", dpi=150)
plt.show()