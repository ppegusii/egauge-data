######## MODULE 1 ########
# Input: egauge-client-list
# Output: live_devices_file.txt

import urllib2  #url library 2 module
import re       #regular expressions module
import time     #time module
import sys      #sys module
import os       #os module

list = urllib2.urlopen("http://egauge.net/cgi-bin/egauge-client-list/") #accesses list of egauge names (as one big string), but has extra characters
print list
unorg_devices = list.read()
unorg1_devices = unorg_devices.replace("<c>", "http://").replace("</c>", ".egaug.es").replace("<clients>", "").replace("</clients>", "") #removes extra characters and changes it to urls
egauge_urls = unorg1_devices.split() #creates list of all urls
egauge_urls.sort()

live_devices = []

for device in egauge_urls[0:1000:50]:
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

clients = open("live_devices_file.txt", "w") #creates a file, and writes the live devices to it(below)
for device in live_devices:
	clients.write(device + "\n")
clients.close                               #always close file after opening
