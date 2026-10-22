from src.pricing import mc_call_price, bs_call_price

S0, K, r, sigma, T = 100, 100, 0.05, 0.20, 1.0

analytic = bs_call_price(S0, K, r, sigma, T)
print(f"Black-Scholes (analítico): {analytic:.4f}\n")
print(f"{'N':>10} {'Monte Carlo':>12} {'Erro padrão':>12} {'|Erro|':>10}")

for n in [100, 1_000, 10_000, 100_000, 1_000_000]:
    price, se = mc_call_price(S0, K, r, sigma, T, n, seed=42)
    print(f"{n:>10} {price:>12.4f} {se:>12.4f} {abs(price - analytic):>10.4f}")
    