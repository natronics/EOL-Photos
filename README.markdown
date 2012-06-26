# EOL Photo Browsing Tool

A tool to scrape recent photos from the NASA EOL photo database and show them in
a more browsable format.

## Install:

    # apt-get install python python-beautifulsoup python-pysqlite2
    # easy_install web.py
    $ cd db
    $ ./create_tables.py

## Get Photos

    $ ./get_photos.py

## Run Browser

    $ ./server.py

Then open a browser window to http://localhost:8080
