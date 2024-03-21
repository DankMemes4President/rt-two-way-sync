FROM python:3-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV APP_HOME=/app
WORKDIR $APP_HOME

COPY requirements.txt $APP_HOME/requirements.txt

RUN apk add librdkafka-dev
RUN apk add postgresql-libs
RUN apk add --virtual .build-deps gcc musl-dev postgresql-dev
RUN python3 -m pip install -r requirements.txt
RUN apk --purge del .build-deps

COPY . $APP_HOME

CMD ["python", "postgres-to-kafka.py"]
