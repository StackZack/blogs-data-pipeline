# blogs-data-pipeline

## Getting Started

### Requirements

For dev work this repo requires that the **pre-commit** package is installed ([info here](https://pre-commit.com/#install)).

### Development

Within a virtual environment run the below commands.

```bash
pip install -r requirements-dev.txt
pre-commit install
```

```bash
# Change value of TARGETARCH with your system's architecture; i.e. arm64, amd64, etc
docker compose -f docker-compose.airflow.yaml build --build-arg TARGETARCH=arm64
docker compose -f docker-compose.airflow.yaml -f docker-compose.common.yaml up -d
docker compose -f docker-compose.airflow.yaml -f docker-compose.common.yaml down
```
