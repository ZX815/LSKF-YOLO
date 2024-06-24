# unmerge_geojson.py
# 
# Author: Varun Nair
# Organization: Duke University
#
# Description:
# Script to output one geojson file from a set of given geojson files. Developed for
# use in the Energy Infrastructure Map of the World project at Duke University.
# 
# The new geojson file is created by appending all geojson features (http://wiki.geojson.org/GeoJSON_Features) 
# to an array outputted as a geojson.
#
# Usage:
# To use the script, run 
# $ merge_geojson.py
# in your cmd. All geojson in the current working directory are then merged to merged_geojson.geojson .
#
# coding: utf-8

from geojson import Feature, LineString, FeatureCollection, Polygon, GeometryCollection
import geojson
import json
import os
import pandas as pd

geoJSONFiles = [g for g in os.listdir('.') if g.endswith(".geojson")]

all_features = []

for geoJSON in geoJSONFiles:
    with open(geoJSON) as file:
        data = json.load(file)
        for feature in data['features']:
            all_features.append(feature)
            
feature_collection = geojson.FeatureCollection(all_features)

with open("merged_geojson.geojson", 'w') as f:
        json.dump(feature_collection,f)

