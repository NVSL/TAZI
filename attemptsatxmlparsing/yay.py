import xml.etree.ElementTree as ET

#define classes
class AST():
    def __init__(self, root):
        self.root = root #root is ASTNode OR should we have a list instead?

class ASTNode():
    def __init__(self, name, depth, children):
        self.name = name
        self.depth = depth          #depth/how much to indent later
        self.children = children    #list of children nodes to access

tree = ET.parse("other.xml")
root = tree.getroot()

# Recursively go through tree, creating ast
# pass in ast vs astNode?
def recurseMake(node, spaces, astNode, astList):
	tag = node.tag.split("}")[1]
	if tag == "block":
                newNode = ASTNode(tag, 0)
                astList.append(newNode)
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
		recurseMake(child, spaces + "  ")

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
