backpack
=======

See the [example](http://maximeh.github.com/backpack)

A very small website to track down all the places I have ever visited in the world.
Just fork the project and add features if you want to !

Actually, you just edit places_log.txt and the address of the new location.
The only limitation is one address per line.

Using a git pre-commit hook
---------------------------
Create a file in your .git/hooks directory like so :

    #!/bin/sh
    if [ "$(git name-rev --name-only HEAD)" == "master" ]; then
        python geocode.py
    fi

Each time you will commits, if something is new in places_log.txt, it will
be added into places_gps_log.json.

Enjoy ! :)

