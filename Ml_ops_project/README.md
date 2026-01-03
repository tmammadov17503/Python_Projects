# MLOps Homework

![Build Status](https://github.com/tmammadov17503/ml_ops_project/actions/workflows/ci-build.yaml/badge.svg)

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![3.12](https://img.shields.io/badge/Python-3.12-green.svg)](https://shields.io/)

---

Homework project using uv + cookiecutter (EDA, FE1/2, Model Selection)

## Structure
------------

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── uv.lock   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `uv lock > uv.lock`
    │
    ├── pyptoject.toml    <- makes project uv installable (uv installs) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py


--------


## Getting started (uv)
```bash
uv sync

uv add numpy

uv run python -m src.models.train_model
```

## Code quality (ruff, isort, black via uvx)
### Run tools in ephemeral envs — no dev dependencies added to your project.

#### Lint (no changes)
```bash
uvx ruff check .
```

#### Auto-fix
```bash
uvx isort .

uvx black .

uvx ruff check --fix .
```
> Also remove unused imports/variables:
> ```bash
> uvx ruff check --fix --unsafe-fixes .
> ```

# ML Ops Project HW 2 Continue

End-to-end ML service with **FastAPI** (backend) + **Streamlit** (frontend), containerized with **Docker** and deployed on **AWS EC2** via a GitHub Actions **self-hosted runner**.  

---

## Live Deployment  

- **Frontend (Streamlit):** [http://13.223.221.154:8501](http://13.223.221.154:8501)  
- **Backend (FastAPI Docs):** [http://13.223.221.154:8000/docs](http://13.223.221.154:8000/docs)  

---

## Features  

- **Backend (FastAPI)**  
  - `/health` endpoint → returns service status.  
  - `/predict` endpoint → accepts structured JSON input, returns predictions.  

- **Frontend (Streamlit)**  
  - Simple UI for submitting `f1`, `f2`, and `city`.  
  - Displays prediction from the backend.  

- **DevOps**  
  - Docker Compose orchestrates backend + frontend.  
  - GitHub Actions with linting, formatting, and deploy jobs.  
  - Self-hosted runner on EC2 for CI/CD automation.  

---

## Setup  

### Local (with Docker Compose)  
```bash
docker compose up -d --build

docker ps --format "table {{.Names}}\t{{.Ports}}"
```

### EC2 Deployment (via GitHub Actions runner)

Every push to `main` triggers the deploy workflow and restarts containers on the EC2 instance.

- **Backend →** [http://13.223.221.154:8000/docs](http://13.223.221.154:8000/docs)  
- **Frontend →** [http://13.223.221.154:8501](http://13.223.221.154:8501)  

---

## API Usage

### Health check
```bash
curl http://127.0.0.1:8000/health
```

### Predict

Send a POST request with JSON input:

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "rows": [
      {"f1": 1.1, "f2": 11, "city": "a"},
      {"f1": 2.0, "f2": 17, "city": "c"}
    ]
  }'
```
Responces: {"predictions":[0,1],"n":2}

## Development

Install dependencies locally (if not using Docker):

```bash
uv sync --all-extras
```
Run checks:
uv run ruff check .
uv run isort . --profile black
uv run black . --check
pytest

## Screenshots

### Backend Swagger (`/docs`)
Here is the automatically generated API documentation from FastAPI:

![Backend Swagger](screenshots/Screenshot%202025-08-18%20121430.png)

---

### Frontend Streamlit
The Streamlit app allows the user to send inputs and view predictions interactively:

![Frontend Streamlit](screenshots/Screenshot%202025-08-18%20121437.png)
