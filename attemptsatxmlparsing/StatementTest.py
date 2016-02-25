import xml.etree.ElementTree as ET
import argparse


#Can run with arguments for filename input OR requests filename input
parser = argparse.ArgumentParser()
parser.add_argument("-x", "--xml", required=True)
args = parser.parse_args()


tree = ET.parse(args.xml)
root = tree.getroot()

def getNext( node ):
    if node.find("next") is not None: return node.find("next")
    if node.tag == "statement": return node
def buildStatement( node ):
    currentNode = node
    nodeList = [ ]
    while( getNext(currentNode) is not None ):
        currentNode = getNext(currentNode).find("block")
	nodeList.append(currentNode)
    return nodeList
for block in root:
    if block.attrib["type"] == "main_loop":
        statements = buildStatement( (block) )
	for n in statements:
	    #print n.tag, n.attrib["type"]
	    if n.attrib["type"] == "controls_if":
	        l = buildStatement( n.find("statement") )
		for e in l:
		    print e.attrib["type"]
