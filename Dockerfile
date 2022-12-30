FROM python:3.10

RUN apt-get update \
 && apt-get install nano \
 && pip install pip poetry --upgrade

COPY pyproject.toml /build/pyproject.toml
COPY poetry.lock /build/poetry.lock
COPY pipper.json /build/pipper.json

RUN --mount=type=secret,id=aws_credentials,dst=/root/.aws/credentials \
    --mount=type=secret,id=aws_config,dst=/root/.aws/config \
    poetry config virtualenvs.create false \
 && poetry install \
 && pip install pipper --upgrade \
 && pipper install -i /build/pipper.json \
    --upgrade \
    --bucket=pipper

COPY jed /project/jed

WORKDIR /project

ENTRYPOINT ["python3"]

CMD  ["--help"]