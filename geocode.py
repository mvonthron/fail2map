#! /usr/bin/python -B
# -*- coding: utf-8 -*-

import json
import os
import sys
from time import sleep, time
import urllib2

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
                # Will happen if the file does not contain valid JSON
                places_gps = {}

    new_places = {}
    url = "http://maps.google.com/maps/api/geocode/json?address=%s&sensor=false"
    # Don't try more than 5qps (it's the geocoding maps api limits for free)
    start = time()
    for place in places:
        if place in places_gps:
            continue
        gmaps_req = urllib2.urlopen(url % place)
        geo_value = json.loads(gmaps_req.read())
        # Parse the json we had to get only lat and lng
        if geo_value['status'] == 'ZERO_RESULTS':
            print "Geocoding failed for %s" % place
            continue
        elif geo_value['status'] == 'OVER_QUERY_LIMIT':
            # Sent too many request in too short time, need to wait a little.
            sleep(1 - (time() - start))
            start = time()
            gmaps_req = urllib2.urlopen(url % place)
            geo_value = json.loads(gmaps_req.read())
        lat = geo_value['results'][0]['geometry']['location']['lat']
        lng = geo_value['results'][0]['geometry']['location']['lng']
        new_places[place] = {'lat': lat, 'lng': lng}

    # Merge places_gps with the new places and dump it.
    all_places = dict(places_gps.items() + new_places.items())

    # Rewrite totally the file, it's slow but let us handle deleted entry
    # in places_log.txt easily
    with open("%splaces_gps_log.json" % path, 'w') as places_file:
        places_file.write(json.dumps(all_places, sort_keys=True, indent=4))
    return 0

if __name__ == '__main__' :
    sys.exit(main())


