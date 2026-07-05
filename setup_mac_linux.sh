#!/usr/bin/env bash

set -e

echo "Creating a Python virtual environment..."
python3 -m venv .venv

echo "Activating the virtual environment..."
source .venv/bin/activate

echo "Installing dependencies..."
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if [ ! -f ".env" ]; then
    cp .env.example .env
    echo
    echo "Created .env from .env.example."
    echo "Open .env and add your Groq API key before running the agent."
fi

echo
echo "Setup complete."
echo "Activate the environment with: source .venv/bin/activate"
echo "Run the agent with: python app.py"
