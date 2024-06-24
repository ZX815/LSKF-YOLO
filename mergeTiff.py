'''
mergeTiff.py

Merges all tif files in given folder, using geo-coordinates, into a single image 'output.tif'
Run with 'python mergeTiff.py folder_name/'

Author: Xiaolan You
Group: Duke Data+ and Energy Initiative
Date: June 15, 2018
'''

import glob
import os
import sys

folder_name = sys.argv[1]
file_list = glob.glob(folder_name+"*.tif")

files_string = " ".join(file_list)

command = "gdal_merge.py -o output.tif -of gtiff " + files_string

os.system(command)