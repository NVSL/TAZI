import xml.etree.ElementTree
e = xml.etree.ElementTree.parse('gspec.xml').getroot()

for node in e:
    if node.tag == "component":
        print node.attrib["type"]
