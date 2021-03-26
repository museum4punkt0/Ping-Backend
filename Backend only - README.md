# Meinobjekt backend
## Technology description
##### Our base technologies:
* Python == 3.7.1
* Django == 2.1.7
* PostgreSQL == 12.2
* POSTGIS == 2.5.3
* Docker (20.10.0)
* docker-compose (1.27.4)

##### How to run a project:
* Clone repo: `git clone https://github.com/museum4punkt0/Mein-Objekt-Backend.git`
* Enter inside of the project's directory: `cd python-backend`
* Copy the example of an environment file: `cp dotenv.example .env`
* Populate newly created `.env` file with additional fields:
    * `AWS_STORAGE_BUCKET_NAME`: bucket name containing all user's media files of a project (`meinobjekt`)
    * `AWS_TENSORFLOW_BUCKET_NAME`: bucket name containing all media files of a project for TensorFlow model generation(`mein-objekt-tensorflow`)
    * `AWS_ACCESS_KEY_ID`: Key ID for buckets
    * `AWS_SECRET_ACCESS_KEY`: Secret key for buckets
    * `AWS_S3_REGION_NAME`: Region for buckets (`eu-central-1`)
    * `WEB_APP_USER_KEY`: Key for EC2 instances, which generate TensorFLow models
    * `WEB_APP_USER_SECRET`: Secret key for EC2 instances, which generate TensorFLow models
* To run a project: `make develop`
* Open `localhost:8000`

`make test` - to run tests


## Conventions
### Compose files
* \*.override.yml files are meant to be used with main docker-compose.yml and overridden. e.g. `docker-compose -f docker-compose.yml -f docker-compose.test.override.yml run backend`
