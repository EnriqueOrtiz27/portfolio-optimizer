import pandas as pd
import numpy as np
from app.utils.optimizer import optimize_portfolio_weights


def test_optimize_portfolio_weights_valid():
    # Fake return data for 3 assets over 5 days
    data = {
        "AAPL": [0.01, 0.02, -0.005, 0.015, 0.007],
        "MSFT": [0.005, 0.01, -0.002, 0.012, 0.008],
        "GOOG": [0.002, 0.012, -0.003, 0.01, 0.006]
    }
    df = pd.DataFrame(data)

    risk_level = 0.0005
    max_weight = 0.7

    weights = optimize_portfolio_weights(df, risk_level, max_weight)

    # Check constraints
    assert isinstance(weights, np.ndarray)
    assert np.isclose(np.sum(weights), 1.0)
    assert all(0 <= w <= max_weight for w in weights)
