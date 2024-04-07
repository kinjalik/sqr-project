#!/bin/sh
poetry run streamlit \
    run ./app/main.py \
    --server.address=0.0.0.0 \
    --server.port=8080
