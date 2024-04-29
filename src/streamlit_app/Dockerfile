FROM python:3.11-slim

# Required for healthcheck
RUN apt-get -y update && apt-get -y install curl

RUN pip install poetry
COPY ./pyproject.toml ./pyproject.toml
RUN poetry install

WORKDIR /app
COPY ./run.sh /app/
COPY /app /app

HEALTHCHECK --interval=5s --timeout=10s --retries=3 CMD curl --fail http://localhost:8080/_stcore/health
CMD './run.sh'
