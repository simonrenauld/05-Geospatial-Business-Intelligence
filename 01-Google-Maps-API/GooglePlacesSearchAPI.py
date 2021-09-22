# -*- coding: utf-8 -*-
"""
Created on Thu May 31 20:17:34 2018
@author: Simon Renauld
"""
#import librairies
import csv
import urllib
import urllib.request
import json

#radius=1000# optional
#rankby=distance
googleGeocodeUrl = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query={}&location={},{}&rankby=distance&key={}'
# For keywords https://developers.google.com/maps/documentation/places/web-service/supported_types
keyword = "XXXXXXX"
key = 'AIzaSyCgM5k5PMof2CZDI20HbYHxbTtwmxp0tsM'

with open('3.csv', newline='') as f_input, open('test.csv', 'w', newline='',encoding="utf-8") as f_output:
    csv_input = csv.reader(f_input)
    csv_output = csv.writer(f_output)
    csv_output.writerow(['Search place','fomatted_address','types','place_id','Long', 'Lat'])
    for search_place, lat, long in csv_input:
        url = googleGeocodeUrl.format(search_place, lat, long, key)
        json_response = urllib.request.urlopen(url)
        search = json_response.read()
        searchjson = json.loads(search)
        print(search_place, lat, long)
        print(search)
        print(url)
        
# Decode in lating 
        
        for place in searchjson['results']:
            row = [place['name'],place['formatted_address'],place['types'],place['place_id'], place['geometry']['location']['lng'], place['geometry']['location']['lat']]
            csv_output.writerow(row)
 
    
