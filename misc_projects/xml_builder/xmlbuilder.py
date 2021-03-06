import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from xml.dom import minidom


root = ET.Element('system', {'a500updaterate':"50", 'xmlns':"http://www.ptcusa.com", 'xmlns:xsi':"http://www.w3.org/2001/XMLSchema-instance", 'xsi:schemaLocation':"http://www.ptcusa.com A510.xsd",
  'type':"pyramid"})
hosts = ET.SubElement(root, 'hosts')
loopcontrollers = ET.SubElement(root, 'loopcontrollers')
interpreter = ET.SubElement(root, 'interpreter')
devices = ET.SubElement(interpreter, 'devices')
epicscas = ET.SubElement(devices, 'epicscas', {'type':'epicscas', 'name':'epicsserver'})
memblock = ET.SubElement(devices, 'memblock', {'type':'memblock', 'name':'tcttest', 'size':'512'})
channels = ET.SubElement(memblock, 'channels')

for x in range(1,512):
    #print x
    channel = ET.SubElement(channels, 'channel', {'name':'analog_out_' + str(x), 'wire':'analog_out_' + str(x)})
for x in range(1,512):
    #print x
    channel = ET.SubElement(channels, 'channel', {'name':'digital_out_' + str(x), 'wire':'digital_out_' + str(x)})
for x in range(1,512):
    #print x
    channel = ET.SubElement(channels, 'channel', {'name':'int_out_' + str(x), 'wire':'int_out_' + str(x)})
for x in range(1,512):
    #print x
    channel = ET.SubElement(channels, 'channel', {'name':'string_out_' + str(x), 'wire':'string_out_' + str(x)})
for x in range(1,512):
    #print x
    channel = ET.SubElement(channels, 'channel', {'name':'analog_in_' + str(x), 'wire':'analog_in_' + str(x)})
for x in range(1,512):
    #print x
    channel = ET.SubElement(channels, 'channel', {'name':'digital_in_' + str(x), 'wire':'digital_in_' + str(x)})
for x in range(1,512):
    #print x
    channel = ET.SubElement(channels, 'channel', {'name':'int_in_' + str(x), 'wire':'int_in_' + str(x)})
for x in range(1,512):
    #print x
    channel = ET.SubElement(channels, 'channel', {'name':'string_in_' + str(x), 'wire':'string_in_' + str(x)})
rough = ET.tostring(root)
parsed = minidom.parseString(rough)


with open("Output.xml", "w") as outputFile:
    print >>outputFile, parsed.toprettyxml(indent='  ')
