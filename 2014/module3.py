########MODULE 3########
	# Input: egauge-circuits/, FIND_CIRCUIT = '  '
	# Output: Solar.txt/, Wind.txt/, etc.
import urllib2  #url library 2 module
import re       #regular expressions module
import time     #time module
import sys      #sys module
import os       #os module

folder = 'egauges-by-circuit'                  #assigns folder key-name to the folder eguages-by-circuit
FOLDER = 'egauge-circuits'


circuit_dict = {'Solar': ["solar", "solar panel", "photovoltaic", "array"],                                #creates a dictionary were all the key-names are stored, and everything is broken up into certain parts
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
	'Humidifier': ["humidifier"]
	}

FIND_CIRCUIT = 'Lighting'

filenames = os.listdir(FOLDER)          #list of all file-names in folder egauge-circuits/

q = open(folder + "/" + FIND_CIRCUIT + ".txt", "a")

for filename in filenames:
	f = open(FOLDER + "/" + filename, "r")                       #reads each file
	list_o_circuits = f.read()
	list_o_circuits = list_o_circuits.split("\n")

	for single_circuit in list_o_circuits:
		found = False
		for synonym in circuit_dict[FIND_CIRCUIT]:
			if synonym in single_circuit:
				q.write(filename + "\n")                      #writes the single_circuit into the file of each circuit
				found = True
				break
		if found:
			break

	f.close()
q.close()
