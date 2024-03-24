FROM rtws-base:latest

# copying event_listener package and adding it to python path
COPY ./event_listener $APP_HOME/event_listener
RUN python3 -m pip install -e $APP_HOME/event_listener

COPY ./service/stripe-forward-integration $APP_HOME/service/stripe-forward-integration
WORKDIR $APP_HOME/service/stripe-forward-integration
RUN python3 -m pip install -r $APP_HOME/service/stripe-forward-integration/requirements.txt
#RUN apk --purge del .build-deps
RUN chmod +x entrypoint.sh

ENTRYPOINT ["sh", "entrypoint.sh"]
