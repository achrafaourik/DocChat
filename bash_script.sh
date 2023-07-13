#!/bin/bash

# Update and install dependencies
apt-get update
apt-get upgrade -y
apt-get --assume-yes install postgresql postgresql-contrib unixodbc-dev python3-psycopg2 python3-dev gcc netcat vim git-lfs tmux htop jupyter

# Upgrade pip and install dependencies
# pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install --upgrade pip
# git clone https://github.com/PanQiWei/AutoGPTQ.git && pip install ./AutoGPTQ
pip install auto_gptq-0.2.2+cu117-cp310-cp310-linux_x86_64.whl
# git lfs clone https://huggingface.co/TheBloke/Wizard-Vicuna-13B-Uncensored-GPTQ
mkdir -p models
python3 download-model.py TheBloke/Manticore-13B-GPTQ
pip install -r requirements_prod.txt

# emtrypoint commands
echo "Starting makemigrations"
python3 manage.py flush --no-input
python3 manage.py makemigrations
# python3 manage.py collectstatic --no-input
echo "Finished makemigrations"

echo "Starting migrate"
python3 manage.py migrate
echo "Finished migrate"

gunicorn app.wsgi:application --bind 0.0.0.0:5000 --timeout 0