import xml.etree.ElementTree as ET

# Recursively print the tree, with proper indentation
def recursePrint(node, spaces):
    #tag = node.tag.split("}")[1]
    tag = node.tag
    if tag == "block":
        typeB = node.attrib["type"]
        if typeB in cmap:
            tag = ""
            whatToPrint = cmap[typeB]
        else:
            whatToPrint = typeB
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
treeR = raw_input("Which file would you like to read? ")

tree = ET.parse(treeR)
root = tree.getroot()

#creating maps
print "Testing out Maps: "
cmap = {"controls_if" : "if(", "math_arithmetic" : "math()", "_LEDArray_happyFace" : "happyFace()"}



recursePrint(root, "")
