#! /bin/bash

cd "$(dirname "$0")"
if [ -f "./py-env/bin/activate" ]; then
    . ./py-env/bin/activate
else
    mkdir -p py-env
    python3 -m venv py-env
    . py-env/bin/activate
    pip install selenium requests webdriver_manager
fi

if [ -f "./order.json" ]; then
    python order.py
else
    echo "order.json file not found, please create it before running the script"
fi