from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse
import pandas as pd
import numpy as np
from scipy.optimize import minimize
from io import StringIO

app = FastAPI()


@app.post("/optimize-portfolio")
async def optimize_portfolio(
        file: UploadFile = File(...),
        risk_level: float = Form(...),
        max_weight: float = Form(...)
):
    # Read CSV file into pandas DataFrame
    content = await file.read()
    df = pd.read_csv(StringIO(content.decode('utf-8')), index_col=0)

    # Drop rows with NaNs (usually the first one)
    df = df.dropna()

    # Compute mean returns and covariance matrix
    mean_returns = df.mean()
    cov_matrix = df.cov()
    tickers = df.columns
    num_assets = len(tickers)

    # Objective: minimize negative Sharpe ratio (maximize Sharpe)
    def portfolio_variance(weights):
        return np.dot(weights.T, np.dot(cov_matrix, weights))

    def portfolio_return(weights):
        return np.dot(weights, mean_returns)

    # Constraints
    constraints = [
        {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},  # Weights must sum to 1
        {'type': 'ineq', 'fun': lambda w: risk_level - portfolio_variance(w)}  # Risk constraint
    ]

    bounds = tuple((0, max_weight) for _ in range(num_assets))
    initial_guess = num_assets * [1. / num_assets]

    # Solve optimization problem
    result = minimize(
        lambda w: -portfolio_return(w),  # Maximize return
        initial_guess,
        method='SLSQP',
        bounds=bounds,
        constraints=constraints
    )

    if not result.success:
        return JSONResponse(
            status_code=400,
            content={"error": "Optimization failed", "details": result.message}
        )

    weights = result.x
    optimal_portfolio = {ticker: round(weight, 4) for ticker, weight in zip(tickers, weights)}

    return {"optimal_portfolio": optimal_portfolio}
