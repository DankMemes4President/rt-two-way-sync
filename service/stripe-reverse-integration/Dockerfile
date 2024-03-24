FROM rtws-base:latest

COPY . $APP_HOME
#RUN apk add postgresql-libs
#RUN apk add --virtual .build-deps gcc musl-dev postgresql-dev
RUN python3 -m pip install -r requirements.txt
RUN apk --purge del .build-deps

RUN chmod +x entrypoint.sh

ENTRYPOINT ["sh","entrypoint.sh"]
