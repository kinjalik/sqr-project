FROM python:3.11-slim

# Required for healthcheck
RUN apt-get -y update && apt-get -y install curl

RUN pip install poetry

WORKDIR /app
COPY ./fastapi_app/ /app/
RUN poetry install

HEALTHCHECK --interval=5s --timeout=10s --retries=3 CMD curl --fail http://localhost:8000/health
CMD './run.sh'
