# metric-forecaster


## Description

This API is intended to run a background process that queries sources like thanos, and submits that timeseries data to
prophet to forecast current values, and rexpose that metric to prometheus.

Intended for features like anomaly detection.

## Getting started

### Install dependencies

`poetry install`

### Run the app

`poetry run fastapi dev app/main.py`


### Run the tests

```shell
poetry run pytest --cov=app --cov-report=term-missing tests/
```

### References

[FastAPI](https://fastapi.tiangolo.com/)
[Prophet](https://facebook.github.io/prophet/)
[Thanos](https://thanos.io/)
[Prometheus](https://prometheus.io/)