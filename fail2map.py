#! /usr/bin/python -B
# -*- coding: utf-8 -*-

import json
import os
import sys
import urllib2

JSON_FILE = "places_gps_log.json"
GEOIP_API = "http://api.hostip.info/get_json.php?position=true&ip=%s"

def find_lat_lng(ipaddr):
    req = urllib2.urlopen(GEOIP_API % ipaddr)
    geo_value = json.loads(req.read())
    print(geo_value)
#    if len(geo_value) > 0:
#        return {'lat': geo_value['lat'], 'lng': geo_value['lon']}
#    return {'lat': None, 'lng': None}



def main(ipaddr):
    find_lat_lng(ipaddr)	
    
    # open GPS JSON file
    data = {}
    
    with open(JSON_FILE, "w+") as fh:
		data = json.loads(fh.read())
		
		if not ipaddr in data:
			data[ipaddr] = {}
	
		json.dump(data, fh)
	
    return 0

if __name__ == '__main__':
    if len(sys.argv) == 2:
        sys.exit(main(sys.argv[1]))
    else:
        print("%s must be called with a target IP as first and unique argument." % sys.argv[0])
        sys.exit(1)
