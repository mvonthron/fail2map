bagpack
=======

See the [example](http://maximeh.github.com/bagpack)

A very small website to track down all the places I have ever visited in the world.
Just fork the project and add features if you want to !

Actually, you just edit locations.txt and the address of the new location.
The only limitation is one address per line.

You may make it work by two ways :

Using a git pre-commit hook
---------------------------
Create a file in your .git/hooks directory like so :

    #!/bin/sh
    if [ "$(git name-rev --name-only HEAD)" == "master" ]; then
        python geocode.py
    fi

Each time you will commits, if something is new in locations.txt, it will
be added into holiday.json.

The advantage of this way, is that your map loads VERY quickly.

F*** it I'll do it live
-----------------------
If it's too much bother for you, you just do that :

    $ mv maps.js maps_quick.js
    $ mv maps2.js maps.js

Then the locations.txt will be read each time someone access the website.
It can be pretty slow if you have a lot of locations.

It is slow, not by choice but only because the Google Web Service for geocoding
only allow 5qps for free. And... 10 if you pay. So, doing it live, is not the
way to go if you have a lot of places.

Enjoy ! :)

