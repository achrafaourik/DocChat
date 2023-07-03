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
    && apt-get upgrade -y && apt-get --assume-yes install postgresql postgresql-contrib \
    unixodbc-dev python3-psycopg2 python3-dev gcc netcat vim git-lfs

# install dependencies
RUN pip install --upgrade pip
RUN git clone https://github.com/PanQiWei/AutoGPTQ.git && pip install ./AutoGPTQ
RUN git lfs clone https://huggingface.co/TheBloke/Wizard-Vicuna-13B-Uncensored-GPTQ
COPY ./requirements_prod.txt .
RUN pip install -r requirements_prod.txt

# copy entrypoint.prod.sh
COPY ./entrypoint.prod.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.prod.sh
RUN chmod +x /usr/src/app/entrypoint.prod.sh

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.prod.sh"]
