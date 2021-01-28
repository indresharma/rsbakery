FROM python:3.8.5-alpine

RUN pip install --upgrade pip

COPY ./requirements.txt .

RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers build-base jpeg-dev zlib-dev 
RUN pip install -r /requirements.txt

COPY ./rsbakery /app
WORKDIR /app

COPY ./entrypoint.sh /
ENTRYPOINT [ "sh", "/entrypoint.sh" ]

# WORKDIR /app
# COPY ./scripts /scripts

# RUN chmod +x /scripts/*

# RUN mkdir -p /vol/web/media
# RUN mkdir -p /vol/web/static

# RUN adduser -D indresharma
# RUN chown -R indresharma:indresharma /vol
# RUN chmod -R 755 /vol/web

# USER indresharma

# CMD ["entrypoint.sh"]



