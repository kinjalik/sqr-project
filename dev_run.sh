#!/bin/bash
set -e

BASEDIR=$(dirname "$0")

# Streamlit is cursed!
mkdir -p ~/.streamlit/
echo "[general]"  > ~/.streamlit/credentials.toml
echo "email = \"\""  >> ~/.streamlit/credentials.toml

pushd "$BASEDIR/app"
    bash ./run.sh
popd
