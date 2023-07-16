#!/bin/bash

# Load environment variables from .env file
set -o allexport
source .env
set +o allexport

# Check if USE_OPENAI_EMBEDDINGS is true
if [ "$USE_OPENAI_EMBEDDINGS" = true ]; then
    # Run the Python script with OpenAI embeddings
    python write_docs_embeddings_openai.py
else
    # Run the Python script without OpenAI embeddings
    python write_docs_embeddings.py
fi
# entrypoint commands
echo "Starting makemigrations"
python3 manage.py flush --no-input
python3 manage.py makemigrations
# python3 manage.py collectstatic --no-input
echo "Finished makemigrations"

echo "Starting migrate"
python3 manage.py migrate
echo "Finished migrate"

gunicorn app.wsgi:application --bind 0.0.0.0:5000 --timeout 0