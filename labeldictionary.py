# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 14:57:29 2015

@author: ST
"""

import urllib2  #url library 2 module
import re       #regular expressions module
import time     #time module
# Input: egauge-client-list
import sys      #sys module
import os       #os module
y = {'Solar': ["Solar [kW]", "Solar (Inverter 2) [kW]","Solar (Inverter 2)+ [kW]","Solar (Inverter 1) [kW]","Solar (Inverter 1)+ [kW]",],                                #creates a dictionary were all the key-names are stored, and everything is broken up into certain parts
	'Generator': ["gen [kW]", "Gen [kW]"],
	'Grid': ["Grid [kW]"], 
      'Use':["use [kW]"],
      'Air Conditioning':["A/C"],
      'Dryer':["Dryer [kW]"],
      'Stove':["Stove [kW]"],
      'Attic':["Loft [kW]"],
      '':["Living+Dining  [kW]"],
      'Bedroom':["Girls Rooms [kW]"],
      'refrigerator':["Fridge [kW]"],
      'Studio':["Studio [kW]"],
      'Assorted':["Garage+Freezer [kW]"],
      '2nd Floor':["Upstairs [kW]"]

	}
x = input()
print y[x]
 