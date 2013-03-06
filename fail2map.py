#! /usr/bin/python -B
# -*- coding: utf-8 -*-

import json
import os
import sys
import urllib2

JSON_FILE = "places.geojson"
GEOIP_API = "http://freegeoip.net/json/%s"

def find_lat_lng(ipaddr):
    point = { "type": "Feature",
      "geometry": {"type": "Point", "coordinates": [None, None]},
      "properties": {"name": ipaddr, "place": "", "show_on_map": False}
    }
    req = urllib2.urlopen(GEOIP_API % ipaddr)
    geo_value = json.loads(req.read())
    
    if len(geo_value) > 0:
        point["geometry"]["coordinates"] = [
                float(geo_value['longitude']),
                float(geo_value['latitude'])]
        point["properties"]["place"] = "%s, %s" % (geo_value['city'], geo_value['country_name'])
        point["properties"]["show_on_map"] = True
        
    return point


def main(ipaddr):
    newPoint = find_lat_lng(ipaddr)
    
    # open GPS JSON file
    data = {
            "type": "FeatureCollection",
            "features": [],
    }
    
    try:
        with open(JSON_FILE, "r") as fh:
            data = json.loads(fh.read())
    except:
        pass
        
    data["features"].append(newPoint)
        
    with open(JSON_FILE, 'w') as fh:
        fh.write(json.dumps(data, sort_keys=True, indent=4))

    return 0


if __name__ == '__main__':
    if len(sys.argv) == 2:
        sys.exit(main(sys.argv[1]))
    else:
        print("%s must be called with a target IP as first and unique argument." % sys.argv[0])
        sys.exit(1)