FROM python:3.11-slim


RUN pip install poetry

WORKDIR /app
COPY src /app
RUN ls -lah

RUN poetry install

HEALTHCHECK CMD curl --fail http://localhost:8080/_stcore/health

CMD './run.sh'
