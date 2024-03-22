FROM python:3-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV APP_HOME=/app
WORKDIR $APP_HOME

RUN apk add librdkafka-dev
RUN apk add --virtual .build-deps gcc musl-dev
