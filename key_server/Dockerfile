FROM python:3.11
WORKDIR /app

COPY . /app

RUN apt update && apt upgrade -y \
    && pip install --upgrade pip

# RUN poetry config virtualenvs.create false \
#     && poetry install --no-root
RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "12001", "--reload"]