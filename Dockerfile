FROM python:3.11-bookworm

WORKDIR /app
COPY . /app

RUN pip install poetry && poetry install --no-dev

ENTRYPOINT ["poetry", "run", "fastapi", "run", "main.py"]
