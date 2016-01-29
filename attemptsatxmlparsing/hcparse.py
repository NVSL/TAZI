import xml.etree.ElementTree as ET

tree = ET.parse("other.xml")
root = tree.getroot()


# Recursively print the tree, with proper indentation
def recursePrint(node, spaces):
	tag = node.tag.split("}")[1]
	if tag == "block":
		whatToPrint = node.attrib["type"]
	elif tag == "field":
		whatToPrint = node.attrib["name"] + " " +  node.text
	elif tag == "value":
		whatToPrint = node.attrib["name"]
	elif tag == "shadow":
		whatToPrint = node.attrib["type"]
	elif tag == "statement":
		whatToPrint = node.attrib["name"]
	elif tag == "next":
		whatToPrint = "I assume this means just execute next instruction"
	else:
		whatToPrint = ""

	print(spaces + tag + " -- " + whatToPrint)
	if list(node) == []:
		return
	for child in node:
		recursePrint(child, spaces + "  ")
		

# Begin main		
recursePrint(root, "")