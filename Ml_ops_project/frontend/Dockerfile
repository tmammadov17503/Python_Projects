FROM python:3.12-slim
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/* \
 && curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app
COPY pyproject.toml uv.lock* ./
RUN uv sync --no-dev --frozen
COPY frontend ./frontend

EXPOSE 8501
ENV BACKEND_URL=http://backend:8000
CMD ["uv", "run", "streamlit", "run", "frontend/app.py", "--server.address=0.0.0.0", "--server.port=8501"]
