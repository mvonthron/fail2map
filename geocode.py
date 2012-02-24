#! /usr/bin/python -B
# -*- coding: utf-8 -*-

import json
import sys
from time import sleep
import urllib2

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def main(path=""):

    locations_file = open("%slocations.txt" % path,'r')
    locations = locations_file.readlines()
    locations_file.close()

    holidays_file = open("%sholiday.json" % path,'r')
    try:
        holidays = json.load(holidays_file)
    except:
        holidays = {}
    holidays_file.close()

    new_holiday = {}
    url_base = "http://maps.google.com/maps/api/geocode/json?"
    # Don't try more than 5qps (it's the geocoding maps api limits for free)
    for addresses in chunks(locations, 5):
        for address in addresses:
            address_encode = address.replace(' ', '+')[:-1]
            # Check if address already exists in holiday
            if address_encode in holidays:
                continue
            url_param = "address=%s&sensor=false" % address_encode
            response = urllib2.urlopen("%s%s" % (url_base, url_param))
            jsongeocode = json.loads(response.read())
            # Parse the json we had to get only lat and lng
            if jsongeocode['status'] == 'ZERO_RESULTS':
                print "Geocoding failed for %s" % address[:-1]
                continue
            # Retry one time
            if jsongeocode['status'] == 'OVER_QUERY_LIMIT':
                sleep(1)
                response = urllib2.urlopen("%s%s" % (url_base, url_param))
                jsongeocode = json.loads(response.read())
            lat = jsongeocode['results'][0]['geometry']['location']['lat']
            lng = jsongeocode['results'][0]['geometry']['location']['lng']
            new_holiday[address_encode] = {'lat': lat, 'lng': lng}
        sleep(500/1000000.0) # Sleep 500ms to be sure

    # Merge new_holiday with holiday and dump it.
    final_holidays = dict(holidays.items() + new_holiday.items())

    holidays_file = open("%sholiday.json" % path,'w')
    holidays_file.write(json.dumps(final_holidays, sort_keys=True, indent=4))
    holidays_file.close()
    return 0

if __name__ == '__main__' :
    sys.exit(main())


