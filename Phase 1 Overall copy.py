import urllib2  	# Url library 2 module
import re       	# Regular expressions module
import time     	# Time module
import sys      	# Sys module
import os       	# Os module
import csv      	# Csv module
import array    	# Array module
import json         # JSON module
import MetaData

class MetaData(object):												# Creates class object aselkfjls
    def __init__(self, egauge_name, description, label):
        self.egauge_name = egauge_name
        self.description = description
        self.label = label


description_dict = {'Solar': ["solar", "solar panel", "photovoltaic", "array"],                                #creates a dictionary were all the key-names are stored, and everything is broken up into certain parts
	'Wind': ["wind", "turbine"],
	'Dishwasher': ["dish", "dishwasher"], 
	'Fridge': ["fridge", "refrigerator", "freeze", "cooler", "chiller", "mr. freeze", "ice", "rfgrtr"],
	'Geothermal': ["geothermal", "geo", "condenser", "copper pipes"],
	'Oven': ["oven", "kiln", "stove", "range", "roast"],
	'Microwave': ["microwave", "toast"],
	'AirConditioning': ["aircond", "ac", "a/c"],
	'Heating': ["heat", "oil", "furnace", "radiator"],
	'Pump': ["pump"],
	'WaterHeater': ["waterheat", "water heat"],
	'Garage': ["garage", "park", "car"],
	'Apartment': ["apartment", "apt", "complex"],
	'Bath': ["bath", "shower", "tub"],
	'Kitchen': ["kitchen", "cook", "food"],
	'Lighting': ["light", "tube", "bulb"],
	'Laundry': ["laundry", "washer", "washing", "dryer"],
	'Barn': ["barn", "animal", "horse", "donkey", "hay"],
	'Fan': ["fan", "exhaust"],
	'VendingMachine': ["vending", "vend", "soda", "snack"],
	'Distiller': ["distill"],
	'StudentUsage': ["student", "dorm"],
	'Dining': ["dining"],
	'Elevator': ["elevator", "lift"],
	'Basement': ["basement", "cellar"],
	'ExerciseRoom': ["exercise", "weight"],
	'Pool': ["pool", "swim"],
	'Spa': ["spa", "hot tub", "hottub", "sauna"],
	'Computers': ["computer", "laptop", "desktop", "cpu"],
	'Humidifier': ["humidifier"],
	'Usage': ["use"],
	'Grid': ["grid"],
	'Generation': ["gen"],
	'Attic' : ["attic", "loft"],
	'Bedroom': ["bedroom", "girls room", "boys room", "kids room", "master bedroom"]
	}
 
inv_dict = {value: key for key in description_dict for value in description_dict[key]}			# Inverses keys and values for the description_dict

def ExtractMetaData(csvfilename):																# 
    filename = csvfilename
    with open("sample_data/" + filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
                                 
        MD = reader.next()[1:]
        description_list =[]
        label_list = []

        for chunk in MD:																
        	lower_chunk = chunk.lower()
        	clean_chunk = lower_chunk.replace("[kw]", "")
        	description_list.append(clean_chunk)												# Adds items to description_list
     
        	for key in inv_dict:			#######3# Sometimes Maps Wrong Description to Wrong Label ######3##
        		if key in clean_chunk:
        			label_list.append(inv_dict[key])
        			break
        		else:
        			pass

    	MetaData_list = []
   
    	for z in range(len(label_list)):
        	m = MetaData(filename, description_list[z], label_list[z])
        	MetaData_list.append(m)
 
    return MetaData_list 



###### Write Device Info ######
	# By Akshat & Tyler
	# Input - string,[metadata objects] - the full path of the file name of the eGauge CSV file, a list of metadata objects representing each device monitored by the eGauge.
	# Output - None - there's no real output only the side effect of creating the desired output files.
	# Description - Reads from the second line of the eGauge CSV file. Writes the metadata and (time, wH values) to the desired output files.

###Note: Need to create folder named "eGauge_metadata" manually before running script

folder = "eGauge_metadata"			# Defines folder named "eGauge_metadata" (does not create an actual folder)

def writeDeviceInfo(egauge_name, metadata):
	# print next(os.walk('./'))[1]
	with open("sample_data/" + egauge_name, 'rb') as csvFile:								# Converts the un-readable csv file into a more read able form
		reader = csv.reader(csvFile, delimiter=',', quotechar='"')
		skip_line = reader.next()																	# Skips first line of csv file
		
		orig_dir = os.getcwd()
		os.chdir(folder)
		clean_egauge = egauge_name.replace(".csv", "")
		if not os.path.exists(clean_egauge):
			os.makedirs(clean_egauge)
			os.chdir(orig_dir)
		else:
			os.chdir(orig_dir)


		file_list = []
		for column in xrange(len(skip_line[1:])):												# Iterates through the columns inside the number of columns that exist
			file_list.append(open(folder + "/" + clean_egauge + "/Column" + str(column + 1) + ".txt", "w+"))			# Creates and adds files to the file_list

		for i in xrange(len(metadata)):															# Iterates through metadata objects in list of metadata objects
			jsond_MetaData = json.dumps(metadata[i].__dict__)
			file_list[i].write(jsond_MetaData)														
			file_list[i].write("\n")

		for line in reader:
			for i in xrange(len(line[1:])):														# Iterates through the indeces in the number of indeces that exist
				file_list[i].write(str(line[0]))
				file_list[i].write(",")
				file_list[i].write(str(line[i + 1]))
				file_list[i].write("\n")
		for files in file_list:
			files.close()																		# Closes files


#writeDeviceInfo("eGauge115", ExtractMetaData("eGauge115"))


####Following are contents of Main function####
def Main():
	Array = next(os.walk("sample_data"))[2]
	for item in Array:
		if item.endswith(".csv"):
			writeDeviceInfo(item, ExtractMetaData(item))

Main()





