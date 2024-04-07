FROM python:3.11-slim


RUN pip install poetry

WORKDIR /app
COPY ./fastapi_app/ /app/
RUN poetry install

CMD './run.sh'
