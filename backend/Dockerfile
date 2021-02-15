FROM python:3.7-slim
ENV PYTHONUNBUFFERED 1
WORKDIR /code
COPY . .

RUN apt-get update
RUN apt-get install -y postgresql-client libpq-dev
RUN apt-get install -y binutils libproj-dev gdal-bin

RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt

CMD [ "./entrypoint.sh" ]
