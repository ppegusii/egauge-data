###### Write Device Info ######
	# By Akshat & Tyler
	# Input - string,[metadata objects] - the full path of the file name of the eGauge CSV file, a list of metadata objects representing each device monitored by the eGauge.
	# Output - None - there's no real output only the side effect of creating the desired output files.
	# Description - Reads from the second line of the eGauge CSV file. Writes the metadata and (time, wH values) to the desired output files.

###Note: Need to create folder named "eGauge_metadata" manually before running script

import urllib2  	# Url library 2 module
import re       	# Regular expressions module
import time     	# Time module
import sys      	# Sys module
import os       	# Os module
import csv      	# Csv module
import array    	# Array module
import json         # JSON module

folder = "eGauge_metadata"			# Creates a new folder named ( eGauge_metadata )

"""
def writeDeviceInfo(egauge_name, metadata):
	with open("sample_data/" + egauge_name + ".csv", 'rb') as csvFile:								# Converts the un-readable csv file into a more read able form
		reader = csv.reader(csvFile, delimiter=',', quotechar='"')
		skip_line = reader.next()																# Skips first line of csv file

		file_list = []
		for column in xrange(len(skip_line[1:])):												# Iterates through the columns inside the number of columns that exist
			file_list.append(open(folder + "/Column" + str(column + 1) + ".txt", "w+"))			# Creates and adds files to the file_list

		for metaline in metadata:																# Iterates through metadata objects in list of metadata objects
			file_list.write(str(metaline))														

		for line in reader:
			for i in xrange(len(line[1:])):														# Iterates through the indeces in the number of indeces that exist
				file_list[i].write(str(line[0]))
				file_list[i].write(" ")
				file_list[i].write(str(line[i + 1]))
				file_list[i].write("\n")
		for files in file_list:
			files.close()																		# Closes files
"""

with open("sample_data/" + "AceStorage" + ".csv", 'rb') as csvFile:								# Converts the un-readable csv file into a more read able form
	reader = csv.reader(csvFile, delimiter=',', quotechar='"')
	print reader