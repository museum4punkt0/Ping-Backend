Ping! Die Museumsapp
Copyright (C) 2021  Stiftung Humboldt Forum im Berliner Schloss; entwickelt von Humboldt Innovation GmbH, Thomas Lilge, Christian Stein, im Rahmen des Verbundprojekts museum4punkt0.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

# Name der Anwendung
Backend für „Ping! Die Museumsapp“

„Ping! Die Museumsapp“ ist eine Marke der Stiftung Humboldt Forum im Berliner Schloss. Die Marke kann von anderen Institutionen, die die App einsetzen, verwendet werden. In diesem Fall wird um Angabe des folgenden Nachweises gebeten:

    „Ping! Die Museumsapp“ ist eine Marke der Stiftung Humboldt Forum im Berliner Schloss.

# Kurzbeschreibung
Dieses Repository beinhaltete das Backend für Ping! Die Museumsapp und ist Teil des entsprechenden Meta-Repositories: https://github.com/museum4punkt0/Ping-Die-Museumsapp


# Entstehungskontext 
Die native App auf Basis des React Native Frameworks ist entstanden im Verbundprojekt museum4punkt0 – Digitale Strategien für das Museum der Zukunft, Teilprojekt: Der humboldt’sche Raum im digitalen Raum.


# Förderung 
Das Projekt museum4punkt0 wird gefördert durch die Beauftragte der Bundesregierung für Kultur und Medien aufgrund eines Beschlusses des Deutschen Bundestages.

# Inhaltsverzeichnis
1. Name der Anwendung 
2. Kurzbeschreibung 
3. Entstehungskontext
4. Förderung
5. Inhaltsverzeichnis 
6. Technologiebeschreibung
7. Installation
8. Credits
9. Lizenz 

# Meinobjekt backend
# Technologiebeschreibung
* Python == 3.7.1
* Django == 2.1.7
* PostgreSQL == 12.2
* POSTGIS == 2.5.3
* Docker (20.10.0)
* docker-compose (1.27.4)

# Installation
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


# Credits 
Auftraggeber*in/Rechteinhaber*in 
Stiftung Humboldt Forum im Berliner Schloss 
Urheber*innen 
Humboldt-Universität zu Berlin, gamelab.berlin am Helmholtz-Zentrum für Kulturtechnik, Zentralinstitut der HU. 


# Lizenz 
[![LICENSE.md](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/museum4punkt0/Mein-Objekt-Backend/blob/master/LICENSE.md)
