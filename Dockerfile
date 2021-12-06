FROM python:3.10-alpine

WORKDIR /app/

ADD ./requirements.txt .

RUN apk --update add --no-cache g++ && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt && \
    rm -f /app/requirements.txt && \
    apk del g++

CMD [ "python" ]