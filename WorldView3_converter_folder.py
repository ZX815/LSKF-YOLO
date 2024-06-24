'''
WorldView3_converter_folder.py

Converts WorldView3 satellite imagery into viewable format, scaled according to global max and min
Example run: python WorldView3_converter_folder.py input_folder/ output_folder/

Author: Xiaolan You
Group: Duke Data+ and Energy Initiative
Date: June 20, 2018
'''

from osgeo import gdal
import glob, os
import sys
import subprocess

def iterateFiles(inputPath, outputPath):
	allMinMax = [[65535, 0] for i in range(3)]
	for f in os.listdir(inputPath):
		if f.endswith('.tif'):
			allMinMax = updateMinMax(inputPath+f, allMinMax)
	print('Global min and max is ', allMinMax)

	# ---- optional place to adjust color ----
	allMinMax[0][1] = allMinMax[0][1]-250
	allMinMax[1][1] = allMinMax[1][1]+150

	for f in os.listdir(inputPath):
		if f.endswith('.tif'):
			convertToRGB(inputPath+f, outputPath, allMinMax, 0.45)
	return

def updateMinMax(inputRaster, allMinMax):
	srcRaster = gdal.Open(inputRaster)
	for bandId in range(srcRaster.RasterCount):
		currentmin = allMinMax[bandId][0]
		currentmax = allMinMax[bandId][1]
		bandId = bandId+1
		band = srcRaster.GetRasterBand(bandId)
		bmin = band.GetMinimum()
		bmax = band.GetMaximum()
		if bmin is None or bmax is None:
			(bmin, bmax) = band.ComputeRasterMinMax(1)
		if bmin < allMinMax[bandId-1][0]:
			allMinMax[bandId-1][0] = bmin
		if bmax > allMinMax[bandId-1][1]:
			allMinMax[bandId-1][1] = bmax
	return allMinMax

def convertToRGB(inputRaster, outputPath,
					globalMinMax,
					brightnessScaler,
					outputPixType='Byte',
					outputFormat='GTiff'):
	fullFilename = inputRaster.split('.tif')[0]
	filename = fullFilename.split('/')[1]
	outputRaster = outputPath+filename+'_processed.tif'
	srcRaster = gdal.Open(inputRaster)
	cmd = ['gdal_translate', '-ot', outputPixType, '-of', outputFormat]
	print(srcRaster.RasterCount)
	for bandId in range(srcRaster.RasterCount):
		bandId = bandId+1
		band = srcRaster.GetRasterBand(bandId)
		cmd.append('-scale_{}'.format(bandId))
		cmd.append('{}'.format(globalMinMax[bandId-1][0]+150))
		cmd.append('{}'.format(globalMinMax[bandId-1][1]*brightnessScaler))
		cmd.append('{}'.format(0))
		cmd.append('{}'.format(255))
	cmd.append(inputRaster)
	cmd.append(outputRaster)
	print ("Conversin command:", cmd)
	subprocess.call(cmd)
	return

iterateFiles(sys.argv[1], sys.argv[2])




