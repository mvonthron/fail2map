#! /usr/bin/python -B
# -*- coding: utf-8 -*-

import json
import os
import sys
from urllib import urlopen, urlencode

NOMINATIM_URL = "http://open.mapquestapi.com/nominatim/v1/search?format=json&%s"
JSON_FILENAME = "places.geojson"

def find_lat_lng(place):
    point = { "type": "Feature",
      "geometry": {"type": "Point", "coordinates": [None, None]},
      "properties": {"name": place, 'show_on_map': False}
    }
    req = urlopen(NOMINATIM_URL % urlencode({'q':place}))
    geo_value = json.loads(req.read())
    if len(geo_value) > 0:
        point["geometry"]["coordinates"] = [
                float(geo_value[0]['lon']),
                float(geo_value[0]['lat'])]
        point["properties"]["show_on_map"] = True
    return point

def main(path=""):

    json_path = "%s%s" % (path, JSON_FILENAME)
    try:
        with open("%splaces_log.txt" % path, 'r') as places_file:
            places = places_file.readlines()
        places = map(lambda s: s.strip(), places)
    except IOError as err:
        print "I/O error({0}): {1}".format(err.errno, err.strerror)
        return 1

    places_gps = {
            "type": "FeatureCollection",
            "features": [],
    }

    try:
        with open(json_path, 'r') as places_gps_file:
            places_gps = json.load(places_gps_file)
    except:
        # Either the file was not here on the JSON was invalid.
        # We will rewrite the whole file then.
        pass

    for pl in places_gps['features']:
        if pl['properties']['name'] in places:
            # We already know that place
            places.remove(pl['properties']['name'])
        else:
            # This place should not be here anymore
            places_gps['features'].remove(pl)

    # Find the gps coordinates of the new places
    for pl in places:
        places_gps['features'].append(find_lat_lng(pl))

    # Rewrite totally the file, it's slow but let us handle deleted entry
    # in places_log.txt easily
    with open(json_path, 'w') as places_file:
        places_file.write(json.dumps(places_gps, sort_keys=True, indent=4))
    return 0

if __name__ == '__main__' :
    sys.exit(main())
