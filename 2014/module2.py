########MODULE 2########
	# Input: live_devices_file.txt
	# Output: egauge-circuits/

import urllib2  #url library 2 module
import re       #regular expressions module
import time     #time module
import sys      #sys module
import os       #os module

FOLDER = 'egauge-circuits'            #makes a folder were the circuits will be kept

live_file = open("live_devices_file.txt", "r")               #creates a text document within the newly created folder
file_cont = live_file.readlines()

for device in file_cont:
	device = device.strip()
	try:
		xml = urllib2.urlopen(device + '/cgi-bin/egauge?tot').read()
		#print xml
	except:
		e = sys.exc_info()[0]                    #searches for errors, and continues over the error
		print "----------"
		print device + ":"
   		print ( "ERROR: %s" % e )
   		print "----------"
   		continue

	circuit = re.findall(r' n=[^>]+', xml)

	circuit_list = []
	if circuit:
		for item in circuit:                   #appending circuits into the folder
			item = item[4:]
			item = item[:-1]
			item = item.lower()
			circuit_list.append(item)
	else:
		circuit = re.findall(r' title=[^>]+', xml)
		for item in circuit:
			item = item[8:]
			item = item[:-1]
			item = item.lower()
			circuit_list.append(item)
	
	# print "{0}: {1}".format(device, circuit_list)
	
	device = device[7:]                 #reassigns device short-cut
	device = device[:-9]

	s =  "\n".join(circuit_list)

	circuit_file = open(FOLDER + "/" + device + ".txt", "w")             
	circuit_file.write(s)                                     #writing the circuit names into the text document in the folder
	circuit_file.close()
