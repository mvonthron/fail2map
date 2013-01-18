#! /usr/bin/python -B
# -*- coding: utf-8 -*-

import json
import os
import sys
from time import sleep, time
import urllib2

NOMINATIM_URL = "http://open.mapquestapi.com/nominatim/v1/search?format=json&q=%s"

def find_lat_lng(place):
    # Don't try more than 5qps (it's the geocoding maps api limits for free)
    req = urllib2.urlopen(NOMINATIM_URL % place)
    geo_value = json.loads(req.read())
    if len(geo_value) > 0:
        return {'lat': geo_value[0]['lat'], 'lng': geo_value[0]['lon']}
    return {'lat': None, 'lng': None}

def main(path=""):

    with open("%splaces_log.txt" % path, 'r') as places_file:
        places = places_file.readlines()
    # Strip all \n from element in locations and replace space by +
    places = map(lambda s: s.replace(' ', '+').strip(), places)

    if not os.path.exists("%splaces_gps_log.json" % path):
        places_gps = {}
    else:
        with open("%splaces_gps_log.json" % path, 'r') as places_gps_file:
            try:
                places_gps = json.load(places_gps_file)
            except:
                # This will happen if the file does not contain valid JSON
                places_gps = {}

    new_places = {pl:find_lat_lng(pl) for pl in places if pl not in places_gps}
    # Merge places_gps with the new places and dump it.
    all_places = dict(places_gps.items() + new_places.items())

    # Rewrite totally the file, it's slow but let us handle deleted entry
    # in places_log.txt easily
    with open("%splaces_gps_log.json" % path, 'w') as places_file:
        places_file.write(json.dumps(all_places, sort_keys=True, indent=4))
    return 0

if __name__ == '__main__' :
    sys.exit(main())