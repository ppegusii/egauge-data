###################### Phase 2 Overall ######################
### By Akshat, 

import urllib2  	# Url library 2 module
import time     	# Time module
import sys      	# Sys module
import os       	# Os module
import csv      	# Csv module
import array    	# Array module
import json         # JSON module
import ParsArgs2    # Imports ParsArgs2 module
import calendar		# Calendar module
import datetime		# DateTime module
from datetime import date, timedelta

def GetLiveDevices():
	list = urllib2.urlopen("http://egauge.net/cgi-bin/egauge-client-list/") #accesses list of egauge names (as one big string), but has extra characters
	unorg_devices = list.read()
	unorg1_devices = unorg_devices.replace("<c>", "http://").replace("</c>", ".egaug.es").replace("<clients>", "").replace("</clients>", "") #removes extra characters and changes it to urls
	egauges_url = unorg1_devices.split() #creates list of all urls
	egauges_url.sort()

	live_devices = []

	for device in egauges_url[1000:2000:250]:
		try:
			page = urllib2.urlopen(device, timeout = 20)  #access webpage html object
		except:                                           
			e = sys.exc_info()[0]
	   		print ( "Error: %s" % e )       #moves on if error with one device 
			continue
		status_code = page.getcode()                     #get status code
		if status_code >= 400 or status_code == None:    #checks whether or not egauge is live by checking if webpage is live
			print device + " is not live"
			pass
		else:
			print device + " is live"
			live_devices.append(device)
		time.sleep(3)                    #need to have at least 3-4 second intervals, or else it accesses egauge website too often and we would get BANNED (it's happened before)
	#return live_devices
	clients = open("live_devices_file.json", "w") #creates a file, and writes the live devices to it(below)
	json.dump(live_devices, clients)
	clients.close
GetLiveDevices()

FOLDER = "sample_data/"
def AccessXML(device, latesttime, earliesttime):
	num_of_tries = 5
	for i in xrange(num_of_tries):												#will try to access eGauge multiple times upon failure to access
		try:								#Below, accesses xml data using the eGauge API, parameters specified after the "?"
			xml = urllib2.urlopen(device + '/cgi-bin/egauge-show?c&m&f=' + str(latesttime) + '&t=' + str(earliesttime) + '&Z=LST0').read() #LDT4%2CM3.2.0%2F02%3A00%2CM11.1.0%2F02%3A00
			#print xml 						#'c' returns csv, 'm' returns minute resolution, 'f'and't' specify first and last timestamp returned, 'Z' converts to datetime
		except:
			e = sys.exc_info()[0]                    							#searches for errors, and continues over the error
			print "----------"
			print device + ":"
			print ( "ERROR: %s" % e )
			print "----------"
			continue

		device_name = device.replace("http://", "").replace(".egaug.es", "")
		if not os.path.exists(FOLDER + device_name + ".csv"):					#will write device descriptions and data to brand new file
			data = open(FOLDER + device_name + ".csv", "w+")
			data.write(xml)
		else:																	#will append additional data to existing file
			data = open(FOLDER + device_name + ".csv", "a")						
			sansfirstline = '\n'.join(xml.split('\n')[1:])
			data.write(sansfirstline)											#prevents re-writing device descriptions to existing file
		data.close()

		row_list = xml.splitlines()
		return len(row_list)													#returns amount of rows
	print "Unable to contact device after " + str(num_of_tries) + " requests"
	return 0																	#returns 0 for amount of rows if unable to access eGauge

def DatetimeToUnix(datetimeobject):												#Converts datetime object into unix timestamp format, to pass in as parameters to AccessXML
	d = datetimeobject
	timestamp=calendar.timegm(d.utctimetuple())
	return timestamp

def get_zero_time(any_time):													#Takes in a datetime object and returns first timestamp of given month
	zero_time = any_time.replace(day=1).replace(hour=0).replace(minute=0).replace(second=0).replace(microsecond=0)
	return zero_time

if len(sys.argv) < 2:															#checks if command-line argument provided
	sys.exit("Error: In command line, please provide a JSON list of eGauge urls to call")
else:
	args = ParsArgs2.parseArgs(sys.argv)										#Calls the jsonList provided as command-line argument
	file_cont = [x.strip() for x in args.eGauge_urls]							#List of eGauge urls from which to get data

for url in file_cont:
	counter = 0
	while True:
		if counter == 0:
			latesttime = datetime.datetime.utcnow()								#returns current time in UTC (Coordinated Universal Time)
		else:
			latesttime = firsttime - timedelta(minutes = 1)						#subtracts a minute from firsttime to get latesttime for the next iteration (next month)

		firsttime = get_zero_time(latesttime)
		rowsReturned = AccessXML(url, DatetimeToUnix(latesttime), DatetimeToUnix(firsttime))
		print rowsReturned
		if rowsReturned < 1:
			print "No more data for this eGauge before " + str(latesttime)
			break																#loop breaks once eGauge has no more data
		counter += 1

		if counter > 4:															#*Testing: controls how many months of data written
			break
		time.sleep(1)



