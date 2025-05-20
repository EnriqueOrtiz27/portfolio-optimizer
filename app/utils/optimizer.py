import numpy as np
import pandas as pd
from scipy.optimize import minimize


def optimize_portfolio_weights(df: pd.DataFrame, risk_level: float, max_weight: float):
    mean_returns = df.mean()
    cov_matrix = df.cov()
    tickers = df.columns
    num_assets = len(tickers)

    def portfolio_variance(weights):
        return np.dot(weights.T, np.dot(cov_matrix, weights))

    def portfolio_return(weights):
        return np.dot(weights, mean_returns)

    constraints = [
        {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},  # Weights must sum to 1
        {'type': 'ineq', 'fun': lambda w: risk_level - portfolio_variance(w)}  # Risk constraint
    ]

    bounds = tuple((0, max_weight) for _ in range(num_assets))
    initial_guess = [1.0 / num_assets] * num_assets

    result = minimize(
        fun=lambda w: -portfolio_return(w),
        x0=initial_guess,
        method='SLSQP',
        bounds=bounds,
        constraints=constraints
    )

    if not result.success:
        raise ValueError(f"Optimization failed: {result.message}")

    return result.x
