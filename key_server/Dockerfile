FROM python:3.11
WORKDIR /app

COPY . /app

RUN apt update && apt upgrade -y \
    && pip install --upgrade pip \
    && pip install poetry

RUN poetry config virtualenvs.create false \
    && poetry install --no-root
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "12001", "--reload"]