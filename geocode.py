#! /usr/bin/python -B
# -*- coding: utf-8 -*-

import json
import sys
from time import sleep
import urllib2

def chunks(l, n):
    """ 
    Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def main(path=""):

    with open("%slocations.txt" % path, 'r') as locations_file:
        locations = locations_file.readlines()
    # Strip all \n from element in locations and replace space by +
    locations = map(lambda s: s.replace(' ', '+').strip(), locations)

    with open("%sholiday.json" % path, 'r') as holidays_file:
        try:
            holidays = json.load(holidays_file)
        except:
            # Will happen if the file does not contain valid JSON
            holidays = {}

    new_holiday = {}
    url_base = "http://maps.google.com/maps/api/geocode/json?"
    # Don't try more than 5qps (it's the geocoding maps api limits for free)
    for addresses in chunks(locations, 5):
        for address in addresses:
            # Check if address already exists in holiday
            if address in holidays:
                continue
            url_param = "address=%s&sensor=false" % address
            response = urllib2.urlopen("%s%s" % (url_base, url_param))
            jsongeocode = json.loads(response.read())
            # Parse the json we had to get only lat and lng
            if jsongeocode['status'] == 'ZERO_RESULTS':
                print "Geocoding failed for %s" % address
                continue
            # Retry one time
            if jsongeocode['status'] == 'OVER_QUERY_LIMIT':
                sleep(1)
                response = urllib2.urlopen("%s%s" % (url_base, url_param))
                jsongeocode = json.loads(response.read())
            lat = jsongeocode['results'][0]['geometry']['location']['lat']
            lng = jsongeocode['results'][0]['geometry']['location']['lng']
            new_holiday[address] = {'lat': lat, 'lng': lng}
        sleep(500/1000000.0) # Sleep 500ms to not hammer Google (silly I know...)

    # Merge new_holiday with holiday and dump it.
    final_holidays = dict(holidays.items() + new_holiday.items())

    # Rewrite totally the file, it's slow but let us handle deleted entry 
    # in locations.txt easily
    with open("%sholiday.json" % path, 'w') as holidays_file:
        holidays_file.write(json.dumps(final_holidays, sort_keys=True, indent=4))
    return 0

if __name__ == '__main__' :
    sys.exit(main())


