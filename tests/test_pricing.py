import numpy as np

from src.gbm import simulate_gbm_terminal_euler
from src.pricing import mc_call_price, mc_call_price_antithetic, bs_call_price


def test_mc_matches_black_scholes():
    S0, K, r, sigma, T = 100, 100, 0.05, 0.20, 1.0
    analytic = bs_call_price(S0, K, r, sigma, T)
    price, se = mc_call_price(S0, K, r, sigma, T, 200_000, seed=1)
    assert abs(price - analytic) < 4 * se


def test_black_scholes_known_value():
    assert abs(bs_call_price(100, 100, 0.05, 0.20, 1.0) - 10.4506) < 1e-3


def test_euler_close_to_black_scholes():
    S0, K, r, sigma, T = 100, 100, 0.05, 0.20, 1.0
    analytic = bs_call_price(S0, K, r, sigma, T)
    S_T = simulate_gbm_terminal_euler(S0, r, sigma, T, 64, 200_000, seed=7)
    price = np.exp(-r * T) * np.maximum(S_T - K, 0.0).mean()
    assert abs(price - analytic) < 0.1


def test_antithetic_matches_black_scholes():
    S0, K, r, sigma, T = 100, 100, 0.05, 0.20, 1.0
    analytic = bs_call_price(S0, K, r, sigma, T)
    price, se = mc_call_price_antithetic(S0, K, r, sigma, T, 200_000, seed=3)
    assert abs(price - analytic) < 4 * se