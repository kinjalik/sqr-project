FROM python:3.11-slim


RUN pip install poetry
COPY ./pyproject.toml ./pyproject.toml
RUN poetry install

WORKDIR /app
COPY ./run.sh /app/
COPY /app /app

HEALTHCHECK CMD curl --fail http://localhost:8080/_stcore/health

CMD './run.sh'
