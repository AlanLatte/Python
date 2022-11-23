FROM python:3.9.5

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN pip install poetry

COPY poetry.lock pyproject.toml poetry.toml /usr/src/app/

RUN poetry install --no-dev

COPY . /usr/src/app/

