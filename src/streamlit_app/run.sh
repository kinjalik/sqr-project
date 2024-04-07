#!/bin/sh
poetry run streamlit \
    run ./main.py \
    --server.address=0.0.0.0 \
    --server.port=8080
