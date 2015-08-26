#### Phase 1 Overall #####
    # The goal is to transform eGauge CSV files to device files.
    # An eGauge CSV file corresponds to a single eGauge and all the devices it monitors.
    # The header row consists of Date&Time, Device1 description, Device 1 Label...
    # The data in the first column is the timestamp.
    # The data in the remaining columns is the Wh power consumption value of the corresponding device at the corresponding timestamp.


import urllib2  	# Url library 2 module
import re       	# Regular expressions module
import time     	# Time module
import sys      	# Sys module
import os       	# Os module
import csv      	# Csv module
import array    	# Array module
import json         # JSON module
import ParsArgs     # Imports ParsArgs module

class MetaData(object):												# Creates class object aselkfjls
    def __init__(self, egauge_name, description, label):
        self.egauge_name = egauge_name
        self.description = description
        self.label = label


description_dict = {"Solar": ["solar", "panel", "photovoltaic", "array", "pv"],                        # Dict of keyphrases(the values) that match the desired label(the keys)
	"Dishwasher": ["dish", "dishwasher"],
	"Fridge": ["fridge", "refrigerator", "freeze", "cooler", "chiller", "mr. freeze", "ice", "rfgrtr"],
	"Geothermal": ["geothermal", "geo", "condenser", "copper pipes"],
	"Oven": ["oven", "kiln", "stove", "range", "roast"],
	"Microwave": ["microwave", "toast"],
	'AirConditioning': ["air cond", "aircond", "ac", "a/c"],
	'Heating': ["heat", "oil", "furnace", "radiator"],
	'Pump': ["pump"],
	'WaterHeater': ["waterheat", "water heat"],
	'Garage': ["garage", "park", "car",],
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
	'Bedroom': ["bedroom", "girls rooms", "boys room", "kids room", "guest"],
	'Stairs': ["upstairs", "downstairs", "stairs"],
	'Studio': ["studio"],
	"Wind": ["wind"]
	}

inv_dict = {value: key for key in description_dict for value in description_dict[key]}			# Inverses keys and values for the description_dict

# ***Change to return {columnNumber: metadata object} instead of [metadata object]***
def ExtractMetaData(csvfilename):																# ExtractMetaData function
	filename = csvfilename
	with open("sample_data/" + filename, 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='"')								# Converts the un-readable csv file into a more read able form

		description_list = reader.next()[1:]
		label_list = map(DescrToLabel,description_list)
		ColumnDict = dict()
		for z in range(len(label_list)):
			m = MetaData(filename, description_list[z], label_list[z])
			ColumnDict[z + 1] = m																# Creates list of desired MetaData objects for each circuit existing in the eGauge
	return ColumnDict


def DescrToLabel(description):
	for item in description.lower().split():
		label = inv_dict.get(item)		#####To fix:Checking for exact match. should check for exact match, if not exact match, then check for key in string
		if label:
			break
	if not label:
		print "No label found for: {}".format(description)
	return label


###### Write Device Info ######
	# Input - string,[metadata objects] - the full path of the file name of the eGauge CSV file, a list of metadata objects representing each device monitored by the eGauge.
	# Output - None - there's no real output only the side effect of creating the desired output files.
	# Description - Reads from the second line of the eGauge CSV file. Writes the metadata and (time, wH values) to the desired output files.

###Note: Need to create folder named "eGauge_metadata" manually before running script

folder = "eGauge_metadata"			# Defines folder named "eGauge_metadata" (does not create an actual folder)


def filterMetadata(metadatadict, sortbylabel, labellist):
	"""
	Returns a dictionary containing only the metadata objects for which we
	want output.
	parameters:
		metadatadict - A dictionary {columnNumber: metadataObject}
		sortbylabel - A boolean. True if output should be sorted by label.
			False if output should be sorted by eGauge.
		labellist - A list of labels for which we want output.
	returns:
		dictionary {columnNumber: (metadataObject, directory)}
		(label is name of directory if sortbylabel == True)
	"""

	filteredDict = dict()
	if sortbylabel:
		for columnNumber, metadata in metadatadict.items():
			if labellist == None or metadata.label in labellist:
				filteredDict[columnNumber] = [metadata, folder + "/" + (metadata.label if metadata.label else "UNKNOWN")]
		return filteredDict

	for columnNumber, metadata in metadatadict.items():
		filteredDict[columnNumber] = [metadata, folder + "/" + metadata.egauge_name]
	return filteredDict



def addFilesToMetadataDict(metadatadict):
	"""
	Augments the given dictionary by adding open files to the values in the
	dictionary. Creates directory if the directory does not exist.
	parameters:
		metadatadict - dictionary {columnNumber: (metadataObject, directory)}
	returns:
		dictionary {columnNumber: (metadataObject, directory, file)}
	"""

	FiledDict = dict()

	for columnNumber, metadata_and_directory in metadatadict.items():
		metadata = metadata_and_directory[0]
		directory = metadata_and_directory[1]
		name_of_egauge = metadata.egauge_name.replace(".csv", "")


		if not os.path.exists(directory):
			os.makedirs(directory)

		file_open = open(metadata_and_directory[1] + "/" + name_of_egauge + "-Column" + str(columnNumber) + ".txt", "w+")
		metadata_and_directory.append(file_open)
		metadata_and_directory.append(True)
		FiledDict[columnNumber] = metadata_and_directory
	#print FiledDict

	return FiledDict



# change metadatalist to metadata dict
def writeDeviceInfo(egauge_name, metadatalist, sortbylabel, labellist):
	metadatadict = filterMetadata(metadatalist, sortbylabel, labellist)
	metadatadict = addFilesToMetadataDict(metadatadict)
	#print 'metadatalist = {}'.format(metadatalist)
	

		#print metadatalist
	# ***End code to move to filterMetadata()***
	# print next(os.walk('./'))[1]
	with open("sample_data/" + egauge_name, 'rb') as csvFile:									# Converts the un-readable csv file into a more read able form
		reader = csv.reader(csvFile, delimiter=',', quotechar='"')
		skip_line = reader.next()																# Skips first line of csv file

		orig_dir = os.getcwd()																	# Returns current directory (2015 folder in this case)
		clean_egauge = egauge_name.replace(".csv", "")
		for line in reader:
			for columnnumber, metadata in metadatadict.items():
				f = metadata[2]
				if metadata[3]:
					jsond_MetaData = json.dumps(metadata[0].__dict__)
					f.write(jsond_MetaData)
					f.write("\n")
					metadata[3] = False
				f.write(str(line[0]))
				f.write(",")
				f.write(str(line[columnnumber]))
				f.write("\n")

		for columnnumber, metadata in metadatadict.items():
			f = metadata[2]
			f.close()																			# Closes files





####Following are contents of Main function####
def Main():
	args = ParsArgs.parseArgs(sys.argv)
	sortbylabel = args.sort == "label"
	Array = next(os.walk("sample_data"))[2]
	

	for item in Array:
		if item.endswith(".csv"):
			print "Writing device info"
			writeDeviceInfo(item, ExtractMetaData(item), sortbylabel, args.labellist)

if __name__ == '__main__':
	Main()


