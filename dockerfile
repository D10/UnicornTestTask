FROM python:3.9-slim-buster

ARG PERIOD
ARG DEBUG
ARG RUB
ARG EUR
ARG USD

ENV PERIOD $PERIOD
ENV DEBUG $DEBUG
ENV RUB $RUB
ENV EUR $EUR
ENV USD $USD

WORKDIR /app
COPY . /app

ENV PYTHONPATH $PYTHONPATH:$(pwd)

RUN pip3 install -r requirements.txt

CMD python3 -d common/scripts/currencies_monitoring.py --period=$PERIOD --debug=$DEBUG --usd=$USD --rub=$RUB --eur=$EUR & \
    python3 -d common/scripts/data_displayer.py & \
    python3 app.py
