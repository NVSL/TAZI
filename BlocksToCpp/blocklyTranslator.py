#!/usr/bin/env python

import xml.etree.ElementTree as ET
import argparse

DEBUG = 0
#Can run with arguments for filename input OR requests filename input


spaces = "  "
delimitter = ";"
main_loop = []

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

    if DEBUG:
        print "Current tag: " + tag, "Attributes: " + str(node.attrib)

    if tag == "xml":
        overallResult = ""
        funcsFirst = ""
        mainBod = ""
        for child in node:
            if ((child.attrib).get("type") != None and ((child.attrib["type"] == "procedures_defnoreturn")
                or (child.attrib["type"] == "procedures_defreturn"))):
                funcsFirst += ";\n" + recurseParse(child, depth)

        for child in node:
            if ((child.attrib).get("type") != None and (child.attrib["type"] == "main")):
                overallResult += recurseParse(child, depth)

        if (("void loop ()" not in overallResult)):
            overallResult += "void loop () {\n}\n"

        return overallResult #funcsFirst + overallResult

    elif tag == "block":
        return getBlock(node,depth)
    elif tag == "next":
        return ";\n" + recurseParse(list(node)[0], depth)
    elif tag == "statement":
        return recurseParse(list(node)[0], depth)
    elif tag == "shadow":
        return recurseParse(list(node)[0], depth)
        #return getField(list(node)[0])
    elif tag == "value":
        return recurseParse(list(node)[0], depth)
        #return getBlock(list(node)[0], depth)
    elif tag == "field":
        return getField(node)
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
	loopStr = recurseParseCheck(list(node), depth+1)+";"
	global main_loop
	main_loop = loopStr.split("\n")
        return "void loop () {" + loopStr + ";\n}"

    if (blockType == "variable_declarations"):
        return "void setup () {\n" + recurseParseCheck(list(node), depth + 1) + ";\n}\n"

    if blockType in funcGet.keys():
        return funcCheckGet(blockType, node, depth) #funcGet[blockType](node,depth)

    if (blockType == "math_number" or blockType == "variables_get"):
        return getField(list(node)[0])

    if (blockType == "text"):
        return "\"" + getField(list(node)[0]) + "\""

    if (blockType == "math_constant"):
        return getConst(list(node)[0])

    if (blockType == "logic_null"):
        return "0"

    if (blockType == "main"): 
        def refactorStatementToBlock( s ):
	    s.tag = "block"
	    s.attrib["type"] = s.attrib["name"]
	    return s
	lines = ""
	print node.tag
	for b in map( refactorStatementToBlock, node.findall("statement" )):
	    lines += recurseParse( b, depth ) + delimitter+ '\n'
        return lines

    return genericBlockGet(node,depth)
   
def genericBlockGet(node,depth):
    blockType = node.attrib["type"]
    # Remainder block types that aren't built in, so it must be custom
    if (len(blockType.split("$")) < 3):
        raise BlocklyError("Block " + blockType + " is malformatted!")
        return ""

    instance = blockType.split("$")[1]
    method = blockType.split("$")[2]

    if (len(list(node)) == 0):
        return blockNext(node, depth, instance + "." + method + "()")

    arguments = getArgs(node, method)

    blockSt = instance + "." + method + "(" + arguments + ")"
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

def getArgs(node, method="default"):
    arguments = ""

    for i in range(len(list(node)) - hasNext(node)):
        if(arguments != ""):
            arguments += ", "
        arguments += recurseParse(list(node)[i], 0)

    return arguments

# Typing dictionary
typeDict = {
    "math_number": "double",
    "text": "string",
    "logic_boolean": "boolean"
}
def getType(node):
    if ((node.attrib).get("type") != None and typeDict.get(node.attrib["type"]) != None):
        return typeDict[node.attrib["type"]]
    #else if (node.tag == "block"):
        #
    else:
        #edit this later to actually get the correct type for a block
        return "int"


def getField(node):
    if (node.attrib.get("name") != None and node.attrib["name"] == "BOOL"):
        if (node.text == "TRUE"):
            return "true"
        if (node.text == "FALSE"):
            return "false"
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
    "PI": "3.14159265358979323846",
    "SQRT": "sqrt"
}
def getConst(node):
    if ("SQRT" in getField(node)):
        return "sqrt(" + getField(node)[4:] + ")"

    return constDict[getField(node)]

# Function Get dictionary

#set variable
def setVar(node, depth):
    # First child is the field, contains name of the variable
    varName = getField(list(node)[0])
    if (len(list(node)) < 2):
        raise BlocklyError("Field " + varName + " does not have a value!")
        return ""

    #if((list(node)[1]).tag.split("}"))
    varType = getType(list(list(node)[1])[0])

    if((list(list(node)[1])[0]).tag == "block"):
        varValue = recurseParse(list(list(node)[1])[0], 0)
    else:
        varValue = getField(list(list(list(node)[1])[0])[0])

    totString = varType + " " + varName + " = " + varValue# + ";"
    return blockNext(node, depth, totString)

#if statement
def ifBlock(node, depth):
    numElsIfs = 0
    numElses = 0
    booleanPart = ""
    statementPart = ""
    ifBChild = 0

    for child in node:
        if(child.tag == "statement" or child.tag == "value"):
            ifBChild += 1

    # First child is either boolean or contains extra piece info
    fchildNode = list(node)[0]
    if (fchildNode.tag == "mutation"):
        if (fchildNode.attrib.get("elseif") != None):
            numElsIfs = int(fchildNode.attrib["elseif"])
        if (fchildNode.attrib.get("else") != None):
            numElses = 1

        if (ifBChild < (2*(1 + numElsIfs) + numElses)):
            raise BlocklyError("If-Statement requires a condition and statements!")

        booleanPart = getArgs(list(node)[1])
        statementPart = recurseParse(list(node)[2], depth+1)
    else:
        if (ifBChild < 2):
            raise BlocklyError("If-Statement requires a condition and statements!")

        booleanPart = getArgs(list(node)[0])
        statementPart = recurseParse(list(node)[1], depth+1)

    # Second child is the statement part
    returnStr = ";\n" + (spaces*depth) + "if(" + booleanPart + ") {;\n"

    totString = returnStr + statementPart + ";\n" + (spaces*depth) + "}"

    if (numElsIfs >= 1):
        totString += elseifBlock(node, numElsIfs, depth)

    if (numElses == 1):
        totString += " else {;\n" + recurseParse(list(node)[-1], depth + 1) + ";\n" + (spaces*depth) + "}"

    return blockNext(node, depth, totString)

#else if statements
def elseifBlock(node, numTimes, depth):
    elseifOpenString = ";\n" + (spaces*depth) + "else if("
    elseString = ""

    for i in range(3, 3 + (numTimes * 2)):
        if (((list(node)[i]).attrib["name"])[:2] == "IF"):
            elseString += elseifOpenString
            booleanPart = getArgs(list(node)[i])
            elseString += booleanPart + ") {;\n" + recurseParse((list(node)[i + 1]), depth + 1) + ";\n" + (spaces*depth) + "}"

    return elseString

#else statement
def elseBlock(node, depth):
    elseString = "else {;\n" + (spaces*depth) + "}"

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

#math property
def mathProp(node, depth):
    test = list(node)[1].text

    numToCheck = recurseParse(list(node)[2], 0)
    if (test == "EVEN"):
        modNum = 0
    else:
        modNum = 1
    #even, odd, prime, whole, positive, negative, divisible by

    total = numToCheck + "%2 == " + str(modNum)

    return blockNext(node, depth, total)

#math arithmetic
def mathMetic(node,depth):
    # 3 children: operator, value A, value B
    operator = getOp(list(node)[0])
    if (len(list(node)) != 3):
        raise BlocklyError("Math block with operator '" + operator + "' requires 2 values to compute!")
        return ""
    #valueA = recurseParse(list(list(node)[1])[-1],depth)
    #valueB = recurseParse(list(list(node)[2])[-1],depth)

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

    condit = getArgs(list(node)[1])
    retString += condit

    if (list(node)[0]).text == "UNTIL":
        retString += ")"

    retString += ") {\n"

    statement = recurseParse(list(node)[2], depth + 1)

    retString += statement + ";\n" + (spaces*depth) + "}"

    return blockNext(node, depth, retString)

#negate
def negate(node, depth):
    retString = "!("

    inner = recurseParse(list(list(node)[0])[0], 0)
    return blockNext(node, depth, (retString + inner + ")"))

#repeat for specified num of times
def repeatControl(node, depth):
    retString = ";\n" + (spaces*depth) + "for(int count = 0; i < "
    count = recurseParse(list(node)[0], 0)
    retString += count + "; i++) {;\n"

    statement = recurseParse(list(node)[1], depth+1)

    retString += statement + ";\n" + (spaces*depth) + "};\n"

    return blockNext(node, depth, retString)

#for loop
def forloop(node, depth):
    retString = ";\n" + (spaces*depth) + "for("

    #from
    val = getField(list(node)[0])
    fromVal = recurseParse(list(node)[1], 0)

    retString += "int " + val + " = " + fromVal

    #to
    toVal = getField(list(list(list(node)[2])[0])[0])

    #increment
    incr = getField(list(list(list(node)[3])[0])[0])

    retString += "; " + val + "<= " + toVal + "; " + val + "+= " + incr + ") {;\n"

    statement = recurseParse(list(node)[4], depth+1)

    retString += statement + ";\n" + (spaces*depth) + "};\n"

    return blockNext(node, depth, retString)

#delay
def delay(node,depth):
    retString = "delay("

    varValue = getArgs(list(node)[0])

    retString += varValue + ")"

    return blockNext(node, depth, retString)

#millis
def millis(node, depth):
    return blockNext(node, depth, "millis()")

#controls_flow_statements
def flowcontrols(node, depth):
    flow = getOp(list(node)[0])
    return blockNext(node, depth, flow)

#Function creation
def funcCreation(node, depth):
    params = ""
    paramNum = 0
    comment = "/* "
    funcName = ""
    funcBody = ""
    retType = "void"
    funcRet = ""

    for child in node:
        if (child.tag == "mutation"):
            for arg in child:
                if(params != ""):
                    params += ", "
                params += getType(arg) + " " + (arg.attrib["name"])
                paramNum += 1
        if (child.tag == "comment"):
            comment += child.text + ";\n" + (spaces*depth) + "*/;\n"
        if (child.tag == "field"):
            funcName = str.replace(child.text, " ", "")
        if (child.tag == "statement"):
            funcBody = recurseParse(list(child)[0], depth + 1) + ";\n"
        if (child.tag == "value"):
            retType = getType(list(child)[0])
            funcRet = (spaces*(depth + 1)) + "return " + recurseParse(list(child)[0], 0) + ";;\n"

    total = comment + retType + " " + funcName + "(" + params + ") {;\n" + funcBody + funcRet + (spaces*depth) + "};\n"

    madeFuncNames[funcName] = paramNum
    return blockNext(node, depth, total)

#call the method with correct arguments as stored by function dictionary
def callMethod(node, depth):
    methodName = str.replace((list(node)[0]).attrib["name"], " ", "")
    arguments = ""
    argNums = 0

    #check dictionary for params to pull
    call = methodName + "("

    #PQ TODO FIX THIS
    if (madeFuncNames[methodName] > 0):
        for arg in list(node)[0]:
            argNums += 1

        for child in node:
            if (child.tag == "value"):
                if(arguments != ""):
                    arguments += ", "
                arguments += recurseParse(child, 0)
        
        call += arguments

    return blockNext(node, depth, call + ")")

#make an if-return for function creation
def ifRet(node, depth):
    mainStr = ";\n" + (spaces*depth) + "if("

    boolPart = getArgs(list(node)[1])
    funcRet = (spaces*(depth + 1)) + "return " + recurseParse(list(list(node)[2])[0], 0) + ";"

    mainStr += boolPart + ") {;\n" + funcRet + ";\n" + (spaces*depth) + "};\n"

    return blockNext(node, depth, mainStr)

def funcCheckGet(blockType, node, depth):
    if (len(list(node)) > 0 and (list(node)[0]).tag == "next"):
        return blockNext(node, depth, "")
    
    return funcGet[blockType](node, depth)

funcGet = {
    "variables_set": setVar,
    "controls_if": ifBlock,
    "logic_compare": compLog,
    "logic_operation": compLog,
    "math_number_property": mathProp,
    "math_arithmetic": mathMetic,
    "math_single": mathSingle,
    "controls_whileUntil": whileUnt,
    "controls_repeat_ext": repeatControl,
    "controls_for": forloop,
    "delay": delay,
    "millis": millis,
    "logic_negate": negate,
    "controls_flow_statements": flowcontrols,
    "procedures_defreturn": funcCreation,
    "procedures_defnoreturn": funcCreation,
    "procedures_ifreturn": ifRet,
    "procedures_callreturn": callMethod,
    "procedures_callnoreturn": callMethod
}

madeFuncNames = {
}


def run( xml ):
    tree = ET.parse(xml)
    root = tree.getroot()
    try:
        if DEBUG: print("--- RUNNING IN DEBUG MODE ---")
        return (recurseParse(root,0))
    except BlocklyError as e:
        print("Error: " + e.value)
        raise
def getLoop(): 
    #global loop_body
    return main_loop

def getSplitDefinitions( xml ):
    import string
    global delimitter
    delimitter = "57"
    xml_str = run(xml)
    return string.split(xml_str, delimitter)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-x", "--xml", required=False, help="Specify xml file through command line")
    parser.add_argument("-d", action="store_true", help="Debug mode")
    args = parser.parse_args()
    inp = None
    if args.xml is not None:
        inp = args.xml
    else:
        inp = raw_input("Filename: ")

    if args.d:
        DEBUG = 1
    print run( inp )
    print
    print main_loop

