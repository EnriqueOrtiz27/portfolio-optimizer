# portfolio-optimizer 📈

This API performs portfolio optimization using the classical Markowitz Mean-Variance model.
It accepts daily returns and computes the optimal asset allocation that maximizes expected return while respecting a
maximum risk level and per-asset weight constraint.
Risk is measured as portfolio variance (unit: daily return variance). A risk level of 1.0 is typically very high; values
like 0.01–0.05 are more common for daily data.
The input must be a .csv file containing tickers in the header and rows of daily returns.

The project was developed in Python and uses [Ruff](https://docs.astral.sh/ruff/) as the code formatter of choice.

## The Use of ChatGPT 🤖

I am no expert in portfolio optimization, so I tasked ChatGPT with the development of that portion of the code.
**However, as a Backend Engineer, I AM responsible for code performance, so I wrote, to
the best of my ability, the corresponding unit tests
to ensure the code works as it is supposed to.** Since I studied Economics, I could get up to date on portfolio
optimization methods if given enough time to study 🤓.

## How to test the API 🕵🏻‍

The API was deployed using GCP's Cloud Run. CD was configured so that every commit to `main` triggers a deploy
and updates the API. Please bear in mind that the minimum number of instances was configured to 0 to minimize costs,
**so there might be a slight cold start in the first request you make to the API.** However, in local tests I have found
the API to be quick to respond.

The API url is `https://portfolio-optimizer-1034123727899.northamerica-south1.run.app/optimize-portfolio`

## How to run the project locally 🚀

```
docker build -t portfolio-optimizer .
docker run -p 8080:8080 portfolio-optimizer
```

Once running, the API will be available at `http://0.0.0.0:8080`.

This is an example cURL

```
curl --request POST \
  --url http://0.0.0.0:8080/optimize-portfolio \
  --header 'Content-Type: multipart/form-data' \
  --form risk_level=1.0 \
  --form max_weight=0.15 \
  --form file=@example_returns.csv

```

The file `example_returns.csv` can be found in the root of the project.
I recommend using an API platform like [Postman](https://www.postman.com/product/tools/) or [httpie](https://httpie.io/)
to quickly test this.

## Error Handling ⚠️

The API returns meaningful HTTP error codes depending on the type of issue:

- `400 Bad Request`: The CSV file is missing, unreadable, or contains non-numeric data (excluding the header).
- `422 Unprocessable Entity`: Inputs are valid in format but result in an infeasible optimization problem (e.g., too
  low `risk_level` or too restrictive `max_weight`).
- `500 Internal Server Error`: Unexpected failure during optimization.
  Please report this to enriqueortizcasillas@gmail.com (provide a sample curl and csv to facilitate debugging)
