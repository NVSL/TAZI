import xml.etree.ElementTree
gspec = xml.etree.ElementTree.parse('gspec.xml').getroot()
base = xml.etree.ElementTree.parse('Components.cat').getroot()

compList = []
finalList = []

#Parsing the components file from Gadgetron
for component in base.findall('component'):
    compStr = component.get('keyname');
    for child in component:
        if child.tag == 'API':
	    compList.append(compStr)
	    print 'API FOUND FOR ABOVE ELEMENT ', compStr


#Parsing the gspec (made in Jet)
for node in gspec:
    if node.tag == "component":
        attribStr = node.attrib["type"]
        if attribStr in compList:
             finalList.append(attribStr)
	     print 'FOUND IN BOTH ', node.attrib["type"]
