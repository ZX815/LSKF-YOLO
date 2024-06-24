# unmerge_geojson.py
# 
# Author: Varun Nair
# Organization: Duke University
#
# Description:
# Script to output the original geojson files from a given geojson file. Developed for
# use in the Energy Infrastructure Map of the World project at Duke University.
# 
# The original geojson files are recreated by sorting geojson features (http://wiki.geojson.org/GeoJSON_Features) 
# by their respective filename property.
#
# Usage:
# To use the script, run 
# $ unmerge_geojson.py examplefile.geojson
# in your cmd. The examplefile.geojson is then unmerged.
#
# coding: utf-8

from geojson import Feature, LineString, FeatureCollection, Polygon, GeometryCollection
import geojson
import json
import os
import pandas as pd
import sys

geojson_file = sys.argv[0]

with open(geojson_file) as file:
    data = json.load(file)
    image_file_names = []
        
    for feature in data['features']:
        if feature['properties']['filename'] not in image_file_names:
            image_file_names.append(feature['properties']['filename'])
        
    for image_file in image_file_names:
        current_features = []
        for feature in data['features']:
            if feature['properties']['filename'] == image_file:
                 current_features.append(feature)
            
        feature_collection = geojson.FeatureCollection(current_features)
        
        with open("recreated_" + image_file, 'w') as f:
            json.dump(feature_collection, f, indent = 2)

