# Name der Anwendung
Mein Objekt


# Kurzbeschreibung 
Mein Objekt ist eine eine mobile Anwendung auf dem Smartphone, die eine personalisierte und spielerische Exploration von Exponaten in Museen und Ausstellungen erlaubt. Im Mittelpunkt der User Experience steht das Kennenlernen von Exponaten über Chats und das Anlegen einer eigenen Sammlung von Objekten. 
Mit den Mitteln des Gamedesigns wird die Motivation der NutzerInnen zu einem eigenaktiven Erschließen der Exponate hergestellt: Die häufig überwältigende Masse an Objekten und die Komplexität des Wissens wird spielerisch reduziert und anschließend dialogisch vermittelt. Gleichzeitig erlaubt die App sowohl eine personalisierte Informationsübermittlung über die herkömmlichen museale Wissensvermittlung hinaus, als auch eine Konzentration auf eine individuelle Auswahl an Museumsobjekten. Der Besucher oder die Besucherin lernt das einzelne Objekt im wahrsten Sinne des Wortes persönlich kennen: Mein Objekt. 


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
6. Technische Dokumentation der Programmierung
7. Installation 
8. Benutzung 
9. Credits
10. Lizenz 


# Technische Dokumentation der Programmierung 
React Native 
Die technische Entwicklung basiert auf React Native. Diese Entscheidung wurde nach sorgfältiger Abwägung verschiedener Möglichkeiten gewählt und bietet die Performance nativer Komponenten sowohl von iOS als auch von Android sowie eine gemeinsame Codebasis unter Nutzung von Webtechnologie. Im Ergebnis ist eine performante, flüssige App mit nativem Look&Feel entstanden, die für beide wichtigen Betriebssysteme verwendet werden kann. Die App ist bereit, um im geschlossenen Betatest in den Appstores verfügbar gemacht zu werden. Technisch beinhaltet die App bereits folgende Module: 

1. Swiping Modul 
Über Wischgesten können Objekte ausgewählt und bewertet werden. 
Die Objekte werden mit Zoom-In-Animationen dargestellt und betonen so den gezeigten Detailausschnitt. Darüber hinaus stellen sie sich mit einem beschreibenden Spruch, einem Objekttyp und einer Distanzangabe zur letzten bekannten Position des/der Besuchers/Besucherin vor. 
2. Chat Modul 
Über eine Textengine können dynamische Dialoge mit dem/der BesucherIn integriert werden, die verzweigende Dialogstrukturen ermöglichen und sich so nach dem Interesse der/die NutzerIn ausrichten lassen. Der Chat kann zoombare Bilder enthalten, Emoticons und buttonbasierte Verzweigungen. Die Chats können darüber hinaus Quiz Elemente enthalten, Blickführung übernehmen, interessensbasiert informieren und den/die NutzerIn zu Aktionen im physischen Raum anregen. 
3. Kartenmodul 
Das Kartenmodul zeigt eine Übersichtskarte des Museumsraums, in der der/die NutzerIn alle gesammelten Objekte verzeichnet sieht. Zudem laden die Objekte den/die BesucherIn ein, in einer markierten Region der Karte nach ihnen zu suchen. Ebenfalls sichtbar sind Objekte mit semantischen Beziehungen zu bereits gesammelten Objekten. Auf diese Art wird Orientierung geschaffen und Beziehungen zwischen Objekten werden aufgezeigt. Die Karte ist zoombar und die Icons können per Tap eine Vollansicht aufrufen. Zudem unterstützt die Karte mehrere Stockwerke. 
4. Chatübersichts-Modul 
Im Chatübersichts-Modul werden werden alle Chats mit Objekten gezeigt, die begonnen und abgeschlossen wurden. So kann jederzeit in bereits geführte Dialoge gesprungen werden und unterbrochene können wiederaufgenommen werden. 
5. Sammlungsmodul 
Im Sammlungsmodul finden sich alle Objekte, die man bereits gefunden hat. Sie sind Kategorien zugeordnet, die man komplettieren kann, um so ein Level aufzusteigen. Ein tap auf ein Objekt ruft die detaillierten Objektinformationen auf. 
6. Tensor-Flow-Modul 
Durch die Integration des Bildererkennungsalgorithmus Tensor Flow können die von den NutzerInnen fotografierten Objekte erkannt und die passenden Objekte in der App aktiviert werden. Dazu werden pro Objekt ca. 100 Fotos als Trainingsdaten verwendet. 
7. Backend 
Das Backend ist als ein grafisches Content-Management-System umgesetzt.
8. Vorgehensmodell 
Verwendet wird circle.ui für automatisiertes building, testing, migrating and deployment. Im Anschluss wird die App und die dazugehörigen Daten auf Amazon Web Services installiert, der alle wesentlichen Services automatisch auf deutschen Servern bereitstellt. Ein Hosting auf einem eigenen Server oder einer VM ist jederzeit möglich. 


# Installation 
Zur Benutzung werden Smartphones benötigt, die entweder über ein iOS oder ein Android Betriebssystem verfügen. Die Anwendung läuft ab folgenden Betriebssystemen: Android Oreo 8.0 und iOS 10.3.3.. Nach Veröffentlichung der App im Playstore bzw. Appstore kann die Anwendung von jedem/r SmartphonebesitzerIn heruntergeladen und installiert werden. 
Der Sourcecode gliedert sich in zwei Repositorien: Mein-Objekt-Backend und Mein-Objekt-MOB-GPL. Mein-Objekt-Backend enthält das Python Backend, das TensorFlow Modul (Unterverzeichnis Tensorflow) zur Berechnung der Fotoerkennungs-KI und den Chatbuilder (Unterverzeichnis Chatbuilder) zum Verfassen und Bearbeiten von Dialogen. Das Repositorium Mein-Objekt-MOB-GPL enthält die React Native App zum Deployment auf iOS und Android.


# Installation Backend

## Technologiebeschreibung Basistechnologien:
* Python == 3.7.1
* Django == 2.1.7
* PostgreSQL == 12.2
* POSTGIS == 2.5.3

## So führen Sie ein Projekt aus
1. Git-Repository lokal herunterladen: git clone [Name des Respositories]
2. Projektverzeichnis öffnen
3. Edit stack file environment section for backend with values provided and create .env file
4. docker-compose up -d (start all containers in daemon mode in the background)
5. docker ps | grep postgis (display database container, copy container's ID)
6. docker cp <container_id>:/data.sql <path_to_sql_file> (copy database dump file to container)
7. docker exec -it <container_id> psql -U application -d application -f data.sql (use dump file)
8. Open 127.0.0.1:8000 and log in into admin using prod credentials

`make test` - um Tests auszuführen


## Konventionen Dateien zusammenstellen
* Die Dateien `docker-compose.override.yml` sind für die Verwendung mit der Hauptdatei docker-compose.yml und overrrieden gedacht. z.B. `docker-compose -f docker-compose.yml -f docker-compose.test.override.yml run backend
`


# Installation Chatbuilder 

Im Unterverzeichnis "Chatbuilder" befindet sich der Code für den unabhängigen Chatbuilder zum erstellen der Dialoge. Dieser kann als Webapplikation einfach auf einem herkömmlichen Webserver veröffentlicht werden. 

Im Projektverzeichnis können Sie Folgendes ausführen:

npm start

Führt die App im Entwicklungsmodus aus.
Öffnen Sie [http://localhost:3000](http://localhost:3000), um sie im Browser zu betrachten.

Die Seite wird neu geladen, wenn Sie Bearbeitungen vornehmen.
Sie werden auch alle Lint-Fehler in der Konsole sehen.

## `npm test`

Startet den Test-Runner im interaktiven Watch-Modus.
Weitere Informationen finden Sie im Abschnitt über das [Ausführen von Tests] (https://facebook.github.io/create-react-app/docs/running-tests).

## `npm run build`

Baut die App für die Produktion in den Ordner `build`.
Es bündelt React korrekt im Produktionsmodus und optimiert den Build für die beste Leistung.

Der Build ist minifiziert und die Dateinamen enthalten die Hashes.
Ihre App ist bereit, deployed zu werden!

Weitere Informationen finden Sie im Abschnitt über [deployment](https://facebook.github.io/create-react-app/docs/deployment).

## `npm run eject`

**Hinweis: Dies ist ein einseitiger Vorgang. Sobald Sie `eject` ausgeführt haben, können Sie nicht mehr zurückgehen!

Wenn Sie mit der Wahl des Build-Tools und der Konfiguration nicht zufrieden sind, können Sie jederzeit "eject" ausführen. Mit diesem Befehl wird die einzelne Build-Abhängigkeit aus Ihrem Projekt entfernt.

Stattdessen werden alle Konfigurationsdateien und die transitiven Abhängigkeiten (webpack, Babel, ESLint usw.) direkt in Ihr Projekt kopiert, so dass Sie die volle Kontrolle über sie haben. Alle Befehle außer "eject" werden weiterhin funktionieren, aber sie werden auf die kopierten Skripte verweisen, so dass Sie sie anpassen können. An diesem Punkt sind Sie auf sich allein gestellt.

Sie müssen `eject` nie benutzen. Der kuratierte Funktionssatz ist für kleine und mittlere Einsätze geeignet, und Sie sollten sich nicht verpflichtet fühlen, diese Funktion zu verwenden. Wir verstehen jedoch, dass dieses Werkzeug nicht nützlich wäre, wenn Sie es nicht anpassen könnten, wenn Sie dazu bereit sind.


# Deployment App Android und iOS

Zum Einsetzen der App sind folgende Schritte notwendig: 

##Quick Start

- npm i
- cd ios && pod install

For running on devices use:
- react-native run-ios
- react-native run-android
- 

## Bedingungen
Sie benötigen die folgenden Dinge, die ordnungsgemäß auf Ihrem Computer installiert sein müssen.

1. [Git](http://git-scm.com/)
2. [Node.js](http://nodejs.org/) (with NPM)
3. [React Native](https://facebook.github.io/react-native/docs/getting-started.html) (Getting Started -> Building Projects with Native Code)
4. [Android Studio](https://developer.android.com/studio/index.html) (for Android development)
5. [XCode](https://itunes.apple.com/app/xcode/id497799835) (for iOS development)

## Installation
 `git clone git@ssh.hub.teamvoy.com:mein-object/mobile.git mo-mobile`

 `cd mo-mobile && npm install`
 
## Running
### Android
Schließen Sie das Android-Gerät über USB an, wobei die Android Debugging Bridge (ADB) aktiviert ist. Führen Sie den nächsten Befehl im Terminal aus:

`adb devices`

Wenn Sie eine Meldung sehen, wie

`0427c24722390aa3	device`

your device connected successfully. If you see next message:

`List of devices attacheed`

Ihr Gerät wurde erfolgreich verbunden. Wenn Sie die nächste Meldung sehen:.

Führen Sie dann folgenden Befehl aus: `react-native run-android`

### Mögliche Probleme - Konnte keine Verbindung zum Entwicklungsserver herstellen
Lösung:
* Finden Sie Ihre Desktop-IP-Adresse heraus (Sie können folgenden Befehl im Terminal ausführen: `ifconfig | grep "inet " | grep -Fv 127.0.0.1 | awk '{print $2}'`)
* `npm start`
* Schütteln Sie das Telefon
* Wählen Sie `Dev Settings`
* Wählen Sie "Debug-Server-Host und -Port für das Gerät".
* Geben Sie dort Ihre IP-Adresse und den Port `8081` ein (zum Beispiel: `192.168.1.123:8081`) und übernehmen Sie die Änderungen.
* Schütteln Sie das Gerät und laden Sie es neu.

### iOS
Bevor Sie das Projekt erstellen und ausführen, führen Sie Folgendes im Terminal aus:
`cd ios && pod install`

#### Simulator-Ausführung
Führen Sie folgenden Befehl im Terminal aus: `react-native run-ios`

#### Ausführen auf dem Gerät
* Öffnen Sie die Datei `ios/MeinObjekt.xcworkspace` in XCode
* Wählen Sie das Gerät aus, auf dem Sie die App ausführen möchten.
* Drücken Sie auf die Schaltfläche "Run".



# Benutzung  
1. Start Screen: Sprachauswahl und Start der Anwendung 
2. Onboarding I: In den vier Onboarding-Screens wird die grundsätzliche Funktionsweise der App beschrieben.
3. Museums-Auswahl oder Planmodus: Hier stellt die App per GPS fest, dass sich der/die BesucherIn nicht im Museum befindet. Es wird der Wahl Screen mit folgenden Möglichkeiten angezeigt: a) Tour-Plan - Hier kann der/die BesucherIn z.B. von zuhause aus den nächsten Museumsbesuch mit Mein Objekt planen b) Wählen Sie Museum und Tour starten - Hier kann ein Museum händisch ausgesucht und die Anwendung für dieses Museum gestartet werden.
4. Museums-Auswahl: Hier können die in der App verfügbaren Museen ausgewählt werden. 
5. Begrüßung: Der/Die BesucherIn wird in der Chatlogik begrüßt. Die wesentliche Interaktion des Chats mit Auswahl von vorgegebenen Antworten wird erlernt. Der/Die UserIn gibt sich einen Namen. Ein eigener Avatar bzw. ein Selfie wird zur Verwendung in der App gewählt. 
6. Onboarding II: Erläuterung der Wischgesteninteraktion und der Schaltflächen. 
7. Wischgesteninteraktion: Der Screen bietet a) Wischen nach links oder alternativ das Berühren des linken Funktionsbuttons. Dies bedeutet: Dieses Exponat interessiert mich gerade nicht. b) Wischen nach rechts oder alternativ das Berühren des rechten Funktionsbuttons. Dies bedeutet: Dieses Exponat interessiert mich. 
8. Match mit dem Exponat: Ein auf das Userprofil passendes Exponat wird gefunden. Wahl zwischen: a) Unterhaltung starten. Der erste Chat mit einem Exponat wird gestartet. oder b) Nein.Danke. Rückkehr zur Wischengestenfunktion.
9. Chat mit dem Exponat I: In dem Chat unterhält sich der/die UserIn mit dem Exponat. Hier können über das Exponat auch Fragen bezüglich z.B der Besucherforschung gestellt werden. 
10. Aufsuchen des Exponats: Wenn der Chat nach beiderseitigem Verständnis positiv war, kann man sich zu einem Treffen verabreden. Auf der dann angezeigten Karte wird der Standort des Exponats nur ungefähr angezeigt, so dass der Museumsraum sich zum Suchraum wandelt.
11. Chat mit dem Exponat II: Hat der/die UserIn das Exponat gefunden, findet ein weiterer Chat statt. Hier können qua Chat u.a. folgende Aktionen stattfinden: Detail (Hinweisen des/der Users/Userin) auf z.B. Beschädigungen oder Restaurierungsspuren am Exponat), Werkinformationen (Hinweisen auf Bildaufbau, Komposition, Farbgebung, Sammlungsgeschichte), Sammlungszusammenhang (Hinweisen des/der Users/Userin auf die benachbarten Exponate und Kontextualisierung des Standortes), Architektur (Thematisieren der Ausstellungsarchitektur)
12. Abschluss des Chats und Beginnen der eigenen Sammlung: Zum Ende des Chats macht der/die UserIn ein Foto des Exponats. Dieses wird in die persönliche Sammlung eingefügt. Hier können auch Metainformationen über das Exponat zur Verfügung gestellt werden. 
13. Plan Modus: Auch hier werden zunächst die in der App verfügbaren Museen zur Auswahl vorgeschlagen. Nach der Wischgesteninteraktion (>>>7.), dem Match (>>>8.) und dem ersten Chat (>>>9.) wird das Exponat in die Sammlung integriert. Von hier aus kann der Chat im Museum (Chat mit dem Exponat II >>>11.) fortgesetzt werden. Im Planmodus gibt es unten den Reiter Mein Plan. Von hier aus können die bereits von außerhalb des Museums begonnenen Chats im Museum gestartet werden, der weitere Prozess ist dann wie >>>10 - >>>12. 
14. Info Screen: Der Info Screen ist über die untere Bedienleiste immer erreichbar und bietet folgende Funktionen: Name (Der/Die UserIn kann seinen/ihren Namen eintragen/ändern), Bild/ Avatar (Der/Die UserIn kann einen Avatar auswählen oder ein Foto von sich schießen), Sprachauswahl (Die Sprache der App kann ausgewählt werden), Font Size (Die Größe der Schrift kann ausgewählt werden), Chat Interval (Die Geschwindigkeit des Chatverlaufs kann variiert werden), Quit (Hierüber ist der Wechsel zwischen Discovery Modus und Plan Modus möglich), Geschäftsbedingungen (Anzeige der AGB), Visitor Guide (Möglichkeit in ein ergänzendes digitales Angebot zu wechseln), Gerät zurücksetzen (Alle Einstellungen und Vorgänge werden gelöscht) 


# Credits 
Auftraggeber*in/Rechteinhaber*in 
Stiftung Humboldt Forum im Berliner Schloss 
Urheber*innen 
Humboldt-Universität zu Berlin, gamelab.berlin am Helmholtz-Zentrum für Kulturtechnik, Zentralinstitut der HU. 


# Lizenz 
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)