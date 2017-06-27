import xml.etree.ElementTree
import json
from pprint import pprint
e = xml.etree.ElementTree.parse('results.xml').getroot()
output = {}

with open('reqs.json') as data_file:    
    data = json.load(data_file)


for atype in e.findall('testcase'):
    name = atype.get("classname") + ":" + atype.get("name")
    name = name[11:]
    #print name[11:] in data.keys()
    #print atype.find('failure')
    if name in data.keys():
        print data[name]
        if atype.find('failure') is None:
            output[data[name]] = True
            print message.attrib

        else:
             output[data[name]] = False


print output
            


