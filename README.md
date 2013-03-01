# EOL Recent Photo Browser

NASA's EOL library is a treasure trove of images
from space taken by astronauts during their missions.  Their database, the &ldquo;Gateway to
Astronaut Photography of Earth&rdquo; records the location and a description of over 600,000 astronaut 
photographs. The database can be queried by location, camera type, date, mission, etc.  Updates
are pushed into the database a few times a week as images are downloaded from the International
Space Station.

## Install

    $ sudo apt-get install python python-pip redis-server virtualenvwrapper
    $ mkvirtualenv eolphotos
    (eolphotos)$ pip install -r requirements.txt

## Scrape Data

    $ workon eolphotos
    (eolphotos)$ python update.py

## Run

    $ workon eolphotos
    (eolphotos)$ python app.py

