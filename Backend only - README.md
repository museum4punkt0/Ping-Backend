# Meinobjekt

## Technology description
##### Our base technologies:
* Python == 3.7.1
* Django == 2.1.7
* PostgreSQL == 12.2
* POSTGIS == 2.5.3

##### How to run a project:
* Git clone repo
* Open project folder
* Edit stack file environment section for backend with values provided
* `cp dotenv.example .env`
* `make develop`
* Open `localhost:8000`

`make test` - to run tests


## Conventions
### Compose files
* \*.override.yml files are meant to be used with main docker-compose.yml and overrrieden. e.g. `docker-compose -f docker-compose.yml -f docker-compose.test.override.yml run backend
`
