FROM python:3.11-slim


COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app
COPY src /app
RUN ls -lah

RUN poetry install

HEALTHCHECK CMD curl --fail http://localhost:8080/_stcore/health

CMD './run.sh'
