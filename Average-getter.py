__author__ = 'Sam'

import urllib2  #url library 2 module
import re       #regular expressions module
import time     #time module
import sys      #sys module
import os       #os module

valid = False
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


while not valid:
    print 'Enter device type'
    userin = raw_input('>:')
    userin = userin.lower()
    for key in circuit_dict:
        if userin == key.lower():
            valid = True
            userin = key


edevice = open(folder + "/" + userin + ".txt", "r")
devices = edevice.read()
devices = devices.split("\n")

total = 0
num = 0

for device in devices:
    device = "http://" + device.replace('.txt','') + ".egaug.es/cgi-bin/egauge?inst"

    device = device.strip()
    try:
		xml = urllib2.urlopen(device).read()
		#print xml
    except:
		e = sys.exc_info()[0]                    #searches for errors, and continues over the error
		'''print "----------"
		print device + ":"
   		print ( "ERROR: %s" % e )
   		print "----------"'''
   		continue

    circuit = re.findall(r' n=[^>]+', xml)
    circuitb = re.findall(r'<i>[^</i>]+', xml)

    circuit_list = []
    circuit_listb = []
    circuit_dictb = {}

    if circuitb:
        for item in circuitb:                   #appending circuits into the folder
            item = item[3:]
            item = item.lower()
            circuit_listb.append(item)
    else:
        circuitb = re.findall(r'<power>[^</power>]+', xml)
        for item in circuitb:                   #appending circuits into the folder
            item = item[7:]
            item = item.lower()
            circuit_listb.append(item)

    ind = 0
    if circuit:
        for item in circuit:                   #appending circuits into the folder
                item = item[4:]
                item = item[:-1]
                item = item.lower()
                if circuit_listb[ind] == '' or circuit_listb[ind] == '-':
                    circuit_listb[ind] = 0
                if '-' in str(circuit_listb[ind]):
                    circuit_listb[ind].replace('-','')
                    circuit_dictb[item] = 0 - float(circuit_listb[ind])
                else:
                    circuit_dictb[item] = float(circuit_listb[ind])
                ind += 1
    else:
        circuit = re.findall(r'title[^>]+', xml)
        for item in circuit:                   #appending circuits into the folder
                item = item[7:]
                #item = item[:-1]
                item = item.lower()
                if circuit_listb[ind] == '' or circuit_listb[ind] == '-':
                    circuit_listb[ind] = 0
                if '-' in str(circuit_listb[ind]):
                    circuit_listb[ind].replace('-','')
                    circuit_dictb[item] = 0 - float(circuit_listb[ind])
                else:
                    circuit_dictb[item] = float(circuit_listb[ind])
                ind += 1

    for keyb in circuit_dictb:
        for key in circuit_dict[userin]:
            lkey = key.lower()
            lkeyb = keyb.lower()
            if lkey in lkeyb:
                total += circuit_dictb[keyb]
                num += 1
print ''
print 'Current average '+userin+' power is:',total/num









