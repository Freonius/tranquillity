FROM python:3.11.0a5-alpine AS build

WORKDIR /app/

ADD . .

RUN apk --update add --no-cache g++ bash libffi-dev && \
    pip install --no-cache-dir --upgrade pip && \
    bash setup.sh py -t -b -i -r -m shell utils exceptions settings  && \
    apk del g++ bash

CMD [ "python" ]

FROM python:3.11.0a5-alpine

WORKDIR /app/

COPY . .

RUN apk --update add --no-cache g++ bash libffi-dev && \
    pip install --no-cache-dir --upgrade pip && \
    bash setup.sh py -i -m shell utils exceptions settings  && \
    apk del g++ bash