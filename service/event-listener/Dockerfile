FROM python:3-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV APP_HOME=/app
WORKDIR $APP_HOME

COPY requirements.txt $APP_HOME/requirements.txt

RUN python3 -m pip install -r requirements.txt

COPY . $APP_HOME

CMD ["python", "event-listener.py"]
