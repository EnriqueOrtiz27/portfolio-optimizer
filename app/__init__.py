from fastapi import FastAPI, File, Form, UploadFile
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.middleware import catch_exceptions_middleware, validation_exception_handler
from app.utils.optimizer import optimize_portfolio_weights
from app.utils.read_csv import read_returns_csv, InvalidFileError

app = FastAPI()

app.middleware("http")(catch_exceptions_middleware)
app.add_exception_handler(ValidationError, validation_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)


@app.post("/optimize-portfolio")
async def optimize_portfolio(
        file: UploadFile = File(...),
        risk_level: float = Form(...),
        max_weight: float = Form(...)
):
    try:
        df = read_returns_csv(file)
    except InvalidFileError as e:
        return JSONResponse(
            status_code=400,
            content={"error": str(e)}
        )

    try:
        weights = optimize_portfolio_weights(df, risk_level, max_weight)
    except ValueError as e:
        # Likely due to infeasible or bad user inputs
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        # Unexpected failure
        raise HTTPException(status_code=500, detail="Internal optimization error")

    optimal_portfolio = {
        ticker: round(weight, 4)
        for ticker, weight in zip(df.columns, weights)
    }

    return {"optimal_portfolio": optimal_portfolio}
