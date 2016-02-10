import xml.etree.ElementTree as ET
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-x", "--xml", required=False)
args = parser.parse_args()
inp = None
if args.xml is not None:
    inp = args.xml
else:
    inp = raw_input("Filename: ")
tree = ET.parse(inp)
root = tree.getroot()

spaces = "  "

# There should be some degree of error checking
class BlocklyError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self, value):
        return repr(self.value)


# Recurse through the xml to translate
def recurseParse(node, depth):
    tag = node.tag.split("}")
    if (len(tag) > 1):
        tag = tag[1]
    else:
        tag = node.tag

    if tag == "xml":
        overallResult = ""
        for child in node:
            if (child.attrib["type"] == "main_loop" 
                    or child.attrib["type"] == "variable_declarations"):
                overallResult += "\n" + recurseParse(child, depth)
            else:
                overallResult += "\n" + recurseParse(child, depth)
        return overallResult

    elif tag == "block":
        return getBlock(node,depth)
    elif tag == "next":
        return "\n" + recurseParse(list(node)[0], depth)
    elif tag == "statement":
        return recurseParseCheck(list(node), depth)
    elif tag == "shadow":
        return getField(list(node)[0])
    else:
        return ""


# Safety net for checking if there is a next block
#shouldn't the if statement check if it's equal to 0?
def recurseParseCheck(nodeList, depth):
    if (len(nodeList) != 1):
        return ""
    else:
        return recurseParse(nodeList[0], depth)


# Sub functions

def getBlock(node,depth):
    blockType = node.attrib["type"]

    if (blockType == "main_loop"):
        # Should be a "next" block
        return "void loop () {" + recurseParseCheck(list(node), depth+1) + "\n}"

    if (blockType == "variable_declarations"):
        return recurseParseCheck(list(node), depth)

    if blockType in funcGet.keys():
        return funcGet[blockType](node,depth)

    if (blockType == "math_number"):
        return getField(list(node)[0])

    if (blockType == "variables_get"):
        return getField(list(node)[0])

    # Remainder block types that aren't built in, so it must be custom
    if (len(blockType.split("_")) < 3):
        raise BlocklyError("Block " + blockType + " is malformatted!")
        return ""

    instance = blockType.split("_")[1]
    method = blockType.split("_")[2]

    if (len(list(node)) == 0):
        return instance + "." + method + "();"

    # Iterate through the rest of the children; the last one may be a "next"
    hasNext = 0
    if (list(node)[-1].tag == "next"):
        hasNext = 1

    arguments = ""
    for i in range(len(list(node)) - hasNext):
        arguments += " " + recurseParse(list(node)[i])
        arguments = arguments.strip().replace(" ", ", ")
    if (hasNext == 0):
        return (spaces * depth ) + instance + "." + method + "(" + arguments + ");"
    else:
        return (spaces * depth ) + instance + "." + method + "(" + arguments + ");" + recurseParse(list(node)[-1], depth)

# Typing dictionary
typeDict = {
    "math_number": "double",
    "text": "string"
}
def getType(node):
    return typeDict[node.attrib["type"]]


def getField(node):
    return node.text

# Operator dictionary
opDict = {
    "EQ": "==",
    "NEQ": "!=",
    "LT": "<",
    "LTE": "<=",
    "GT": ">",
    "GTE": ">=",
    "AND": "&&",
    "OR": "||",
    "PLUS": "+",
    "MINUS": "-",
    "MULTIPLY": "*",
    "DIVIDE": "/",
    "POWER": "pow"
}
def getOp(node):
    return opDict[node.text]

# Function Get dictionary

#set variable
def setVar(node, depth):
    # First child is the field, contains name of the variable
    varName = getField(list(node)[0])
    if (len(list(node)) < 2):
        raise BlocklyError("Field " + varName + " does not have a value!")
        return ""
    varType = getType(list(list(node)[1])[0])
    varValue = getField(list(list(list(node)[1])[0])[0])
    nextBlock = ""
    # Now deal with possible "next" block
    if (len(list(node)) == 3):
        nextBlock = recurseParse(list(node)[2])
    return (spaces * depth )  + varType + " " + varName + " = " + varValue + ";" + nextBlock

#if statement
def ifBlock(node, depth):
    # First child is the boolean part
    booleanPart = recurseParse(list(list(node)[0])[0], 0)
    # Second child is the statement part
    statementPart = recurseParse(list(node)[1], depth+1)
    return (spaces * depth ) + "if (" + booleanPart + ") {\n" + (spaces*(depth+1)) + statementPart + "\n" + spaces*depth + "}"

#logic compare
def compLog(node,depth):
    # 3 children: operator, value A, value B
    operator = getOp(list(node)[0])
    if (len(list(node)) != 3):
        raise BlocklyError("Logic compare with operator '" + operator + "' requires 2 values to compare!")
        return ""
    valueA = recurseParse(list(list(node)[1])[0])
    valueB = recurseParse(list(list(node)[2])[0])
    return valueA + " " + operator + " " + valueB

#math arithmetic
def mathMetic(node,depth):
    # 3 children: operator, value A, value B
    operator = getOp(list(node)[0])
    if (len(list(node)) != 3):
        raise BlocklyError("Math block with operator '" + operator + "' requires 2 values to compute!")
        return ""
    valueA = recurseParse(list(list(node)[1])[-1])
    valueB = recurseParse(list(list(node)[2])[-1])
    if (operator == "pow"):
        return "pow(" + valueA + ", " + valueB + ")"
    return valueA + " " + operator + " " + valueB

#while loop
def whileUnt(node, depth):
    retString = (spaces * depth) + "while("
    if (list(node)[0]).text == "UNTIL":
        retString += "!("

    condit = recurseParse(list(list(node)[1])[0])
    retString += condit

    if (list(node)[0]).text == "UNTIL":
        retString += ")"

    retString += ") {\n"

    statement = recurseParse(list(node)[2], depth+1)

    retString += statement + "\n"+(spaces*depth)+"}\n"

    return retString + recurseParseCheck(list(node)[3], depth)

#delay
def delay(node,depth):
    retString = (spaces*depth)+"delay("

    varValue = getField(list(list(list(node)[0])[0])[0])

    retString += varValue + ");"

    return retString

funcGet = {
    "variables_set": setVar,
    "controls_if": ifBlock,
    "logic_compare": compLog,
    "math_arithmetic": mathMetic,
    "controls_whileUntil": whileUnt,
    "delay": delay
}


# main
try:
    print(recurseParse(root,0))
except BlocklyError as e:
    print("Error: " + e.value)

