"""
Creates an Object for MetaData
"""

class MetaData(object):
   
    def __init__(self, egauge_name, description, label):
        self.egauge_name = egauge_name
        self.description = description
        self.label = label