from src.pricing import mc_call_price, bs_call_price


def test_mc_matches_black_scholes():
    S0, K, r, sigma, T = 100, 100, 0.05, 0.20, 1.0
    analytic = bs_call_price(S0, K, r, sigma, T)
    price, se = mc_call_price(S0, K, r, sigma, T, 200_000, seed=1)
    assert abs(price - analytic) < 4 * se


def test_black_scholes_known_value():
    assert abs(bs_call_price(100, 100, 0.05, 0.20, 1.0) - 10.4506) < 1e-3