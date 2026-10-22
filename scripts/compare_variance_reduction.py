from src.pricing import mc_call_price, mc_call_price_antithetic, bs_call_price

S0, K, r, sigma, T = 100, 100, 0.05, 0.20, 1.0
analytic = bs_call_price(S0, K, r, sigma, T)
print(f"Black-Scholes (analítico): {analytic:.4f}\n")
print(f"{'N':>9} {'EP padrão':>10} {'EP antitético':>14} {'Redução':>9}")

for n in [1_000, 10_000, 100_000, 1_000_000]:
    _, se_plain = mc_call_price(S0, K, r, sigma, T, n, seed=1)
    _, se_anti = mc_call_price_antithetic(S0, K, r, sigma, T, n, seed=1)
    print(f"{n:>9} {se_plain:>10.4f} {se_anti:>14.4f} {se_plain / se_anti:>8.2f}x")