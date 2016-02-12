import xml.etree.ElementTree as ET
import argparse

#Can run with arguments for filename input OR requests filename input
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
    elif tag == "value":
        return getBlock(list(node)[0], depth)
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

    if (blockType == "math_number" or blockType == "variables_get"):
        return getField(list(node)[0])

    if (blockType == "text"):
        return "\"" + getField(list(node)[0]) + "\""

    if (blockType == "math_constant"):
        return getConst(list(node)[0])

    return genericBlockGet(node,depth)
   
def genericBlockGet(node,depth):
    blockType = node.attrib["type"]
    # Remainder block types that aren't built in, so it must be custom
    if (len(blockType.split("_")) < 3):
        raise BlocklyError("Block " + blockType + " is malformatted!")
        return ""

    instance = blockType.split("_")[1]
    method = blockType.split("_")[2]

    if (len(list(node)) == 0):
        return instance + "." + method + "();"

    # Iterate through the rest of the children; the last one may be a "next"

    arguments = ""
    for i in range(len(list(node)) - hasNext(node)):
        arguments += " " + recurseParse(list(node)[i], 0)
        #strip semi-colon from args (temp fix?)
        arguments = arguments.strip().replace(";", "");

    if(method != "printText"):
        arguments = arguments.strip().replace(" ", ", ")

    blockSt = instance + "." + method + "(" + arguments + ");"
    return blockNext(node, depth, blockSt)

def blockNext(node, depth, nodeStr):
    thisNex = hasNext(node)

    if (thisNex == 0):
        return (spaces * depth) + nodeStr
    else:
        return (spaces * depth) + nodeStr + recurseParse(list(node)[-1], depth)

#iterate through the children; may have a "next"
def hasNext(node):
    if len(list(node)) == 0:
        return 0
    if (list(node)[-1].tag == "next"):
        return 1
    return 0

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
    "ADD": "+",
    "MINUS": "-",
    "MULTIPLY": "*",
    "DIVIDE": "/",
    "POWER": "pow",
    "ROOT": "sqrt",
    "BREAK": "break;",
    "CONTINUE": "continue;"
}
def getOp(node):
    return opDict[node.text]

#constant dictionary
constDict = {
    "PI": "3.14159265358979323846"
}
def getConst(node):
    return constDict[node.text]

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
        nextBlock = recurseParse(list(node)[2], depth)

    totString = varType + " " + varName + " = " + varValue + ";" + nextBlock
    return blockNext(node, depth, totString)

#if statement
def ifBlock(node, depth):
    # First child is the boolean part
    booleanPart = recurseParse(list(list(node)[0])[0], 0)
    
    #attempt to strip ;
    booleanPart = booleanPart.strip().replace(";", "")

    # Second child is the statement part
    statementPart = recurseParse(list(node)[1], depth+1)
    returnStr = "if(" + booleanPart + ") {\n"
    statements = statementPart.split('\n')
    for statement in statements:
        returnStr = returnStr + (spaces*(depth+1)) + statement.strip() + "\n"

    totString = returnStr + (spaces*depth) + "}"

    return blockNext(node, depth, totString)

#logic compare
def compLog(node,depth):
    # 3 children: operator, value A, value B
    operator = getOp(list(node)[0])
    if (len(list(node)) != 3):
        raise BlocklyError("Logic compare with operator '" + operator + "' requires 2 values to compare!")
        return ""
    valueA = recurseParse(list(list(node)[1])[0],depth)
    valueB = recurseParse(list(list(node)[2])[0],depth)

    return blockNext(node, depth, (valueA + " " + operator + " " + valueB))

#math arithmetic
def mathMetic(node,depth):
    # 3 children: operator, value A, value B
    operator = getOp(list(node)[0])
    if (len(list(node)) != 3):
        raise BlocklyError("Math block with operator '" + operator + "' requires 2 values to compute!")
        return ""
    valueA = recurseParse(list(list(node)[1])[-1],depth)
    valueB = recurseParse(list(list(node)[2])[-1],depth)
    if (operator == "pow"):
        return blockNext(node, depth, ("pow(" + valueA + ", " + valueB + ")"))

    return blockNext(node, depth, (valueA + " " + operator + " " + valueB))

#math single
def mathSingle(node, depth):
    operator = getOp(list(node)[0])

    valueOn = recurseParse(list(list(node)[1])[0], depth)
    if operator == "sqrt":
        return blockNext(node, depth, (operator + "(" + valueOn + ")"))

    return blockNext(node, depth, (operator + valueOn))

#while loop
def whileUnt(node, depth):
    retString = "while("
    if (list(node)[0]).text == "UNTIL":
        retString += "!("

    condit = recurseParse(list(list(node)[1])[0], 0)
    retString += condit

    if (list(node)[0]).text == "UNTIL":
        retString += ")"

    retString += ") {\n"

    statement = recurseParse(list(node)[2], depth+1)

    retString += (spaces*depth) + statement + "\n"+(spaces*depth)+"}\n"

    return blockNext(node, depth, retString)

#negate
def negate(node, depth):
    retString = "!("

    inner = recurseParse(list(list(node)[0])[0], 0)
    return blockNext(node, depth, (retString + inner + ")"))

#repeat for specified num of times
def repeatControl(node, depth):
    retString = "for(int count = 0; i < "
    count = recurseParse(list(node)[0], 0)
    retString += count + "; i++) {\n"

    statement = recurseParse(list(node)[1], depth+1)

    retString += (spaces*depth) + statement + "\n" + (spaces*depth) + "}\n"

    return blockNext(node, depth, retString)

#for loop
def forloop(node, depth):
    retString = "for("

    #from
    val = getField(list(node)[0])
    fromVal = recurseParse(list(node)[1], 0)

    retString += "int " + val + " = " + fromVal

    #to
    toVal = getField(list(list(list(node)[2])[0])[0])

    #increment
    incr = getField(list(list(list(node)[3])[0])[0])

    retString += "; " + val + "<= " + toVal + "; " + val + "+= " + incr + ") {\n"

    statement = recurseParse(list(node)[4], depth+1)

    retString += statement + "\n" + (spaces*depth) + "}\n"

    return blockNext(node, depth, retString)

#delay
def delay(node,depth):
    retString = "delay("

    varValue = getField(list(list(list(node)[0])[0])[0])

    retString += varValue + ");"

    return blockNext(node, depth, retString)

#millis
def millis(node, depth):
    return blockNext(node, depth, "millis();")

#controls_flow_statements
def flowcontrols(node, depth):
    flow = getOp(list(node)[0])
    return blockNext(node, depth, flow)

funcGet = {
    "variables_set": setVar,
    "controls_if": ifBlock,
    "logic_compare": compLog,
    "logic_operation": compLog,
    "math_arithmetic": mathMetic,
    "math_single": mathSingle,
    "controls_whileUntil": whileUnt,
    "controls_repeat_ext": repeatControl,
    "controls_for": forloop,
    "delay": delay,
    "millis": millis,
    "logic_negate": negate,
    "controls_flow_statements": flowcontrols
}


# main
try:
    print(recurseParse(root,0))
except BlocklyError as e:
    print("Error: " + e.value)

