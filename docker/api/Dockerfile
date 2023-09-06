FROM python:3.9.5

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN pip install poetry

COPY poetry.lock pyproject.toml /usr/src/app/

RUN poetry config virtualenvs.create false \
    && poetry install --only main

COPY . /usr/src/app/

