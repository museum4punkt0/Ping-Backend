FROM python:3.7
ENV APP_PATH=/app
RUN mkdir ${APP_PATH}
ADD requirements.txt ${APP_PATH}
RUN cat ${APP_PATH}/requirements.txt \
  && pip3 install --upgrade pip \
  && pip3 install -r ${APP_PATH}/requirements.txt \
  && rm -rf ${APP_PATH}/requirements.txt \
  && pip3 install uwsgi
