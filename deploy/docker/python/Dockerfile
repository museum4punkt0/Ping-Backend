FROM 081960884429.dkr.ecr.eu-central-1.amazonaws.com/base_images:python

ARG DATABASE_URL
ARG DJANGO_SECRET_KEY
ARG PORT
ARG POSTGRES_HOST
ARG POSTGRES_NAME
ARG POSTGRES_PASSWORD
ARG POSTGRES_USER
ARG APP_PATH
ARG AWS_ACCESS_KEY_ID
ARG AWS_S3_REGION_NAME
ARG AWS_S3_SIGNATURE_VERSION
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_STORAGE_BUCKET_NAME

RUN mkdir -p ${APP_PATH}
COPY . ${APP_PATH}
RUN pip3 install -r ${APP_PATH}/requirements.txt \
  && mkdir -p /var/log/uwsgi \
  && touch access.log \
  && touch error.log
RUN python manage.py collectstatic --noinput
WORKDIR ${APP_PATH}
EXPOSE 8000
