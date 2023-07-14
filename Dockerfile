###########
# BUILDER #
###########

# pull official base image
FROM huggingface/transformers-pytorch-gpu
# FROM python:3.9.16-slim
# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apt-get update \
    && apt-get upgrade -y && apt-get --assume-yes install postgresql postgresql-contrib unixodbc-dev python3-psycopg2 python3-dev gcc netcat vim git-lfs tmux htop jupyter


# install dependencies
RUN pip install --upgrade pip
RUN pip install auto_gptq-0.2.2+cu117-cp310-cp310-linux_x86_64.whl
RUN mkdir -p models && python3 download-model.py TheBloke/Wizard-Vicuna-30B-Uncensored-GPTQ
COPY ./requirements_prod.txt .
RUN pip install -r requirements_prod.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
