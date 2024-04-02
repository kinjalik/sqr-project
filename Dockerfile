FROM python:3.12-slim


COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app
COPY app /app
RUN ls -lah

HEALTHCHECK CMD curl --fail http://localhost:8080/_stcore/health

CMD './run.sh'
