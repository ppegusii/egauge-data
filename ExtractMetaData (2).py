"""
Created on Mon Jul 13 11:52:32 2015

@author: ST
"""
"""
import urllib2  #url library 2 module
import re       #regular expressions module
import time     #time module
# Input: egauge-client-list
import sys      #sys module
import os       #os module

"""
import MetaData
import csv
import labeldictionary
import json


def ExtractMetaData(csvfilename):
    filename = csvfilename
    with open(filename, 'rb') as csvfile:
         reader = csv.reader(csvfile, delimiter=',', quotechar='"')
                                 
         MD = reader.next()[1:]
         
         
        
         description_list =[]
         label_list = []
    
         for i in range(0, len(MD)):
             description_list.append(MD[i])
             
                     
    for x in description_list:
        label_list.append(labeldictionary.inv_dict[x])
    
    MetaData_list = []
    print
    print
    for z in range(len(label_list)):
        m = MetaData.MetaData(filename, description_list[z], label_list[z])
        MetaData_list.append(m)
        print json.dumps(m.__dict__)
        
        

csvname = raw_input("What is the name of the CSV File you want?: ")

ExtractMetaData(csvname)
