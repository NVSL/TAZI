#!/usr/bin/env python

from translation_dictionaries import *

import xml.etree.ElementTree as ET
import argparse

DEBUG = 0
#Can run with arguments for filename input OR requests filename input


spaces = "  "
delimitter = ";"
declaredVars = []
main_loop = []
definedFuncs = []
declaredObjs = set()
declaredFuncs = []
main_setup = []
main_funcs = ""
use_c_lib = True
isCpp = False
c_lib = "#include <iostream>\n#include <cmath>"
c_lib += "\n#include <stdlib.h>\nusing namespace std;\n"
program_name = "Prog"

# There should be some degree of error checking
class BlocklyError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self, value):
        return repr(self.value)

def refactorStatementToBlock( s ):
    s.tag = "block"
    s.attrib["type"] = s.attrib["name"]
    return s

def is_node_of_type( node, type_name ):
    atb = (node.attrib).get("type")
    return atb != None and atb == type_name

# Recurse through the xml to translate
def parseBlocksRecursively(node, depth):
    tag = node.tag.split("}")
    tag = tag[1] if (len(tag) > 1) else node.tag

    if DEBUG:
        print "Current tag: " + tag, "Attributes: " + str(node.attrib)

    if tag == "xml":
        global definedFuncs
        global declaredFuncs
        global declaredVars
        global main_loop 
        global main_setup
        definedFuncs = []
        declaredFuncs = []
        main_loop = []
        main_setup = []
        overallResult = ""
        mainBod = ""
        global main_funcs
        for child in node.iter('block'):
            if is_node_of_type(child, "procedures_defnoreturn") or is_node_of_type(child, "procedures_defreturn"):
                findDefine(child)

        for child in node:
            if is_node_of_type(child, "procedures_defnoreturn") or is_node_of_type(child, "procedures_defreturn"):
                main_funcs += ";\n" + parseBlocksRecursively(child, depth)

        for child in node:
            if is_node_of_type(child, "main") or is_node_of_type(child, "root_node"):
                overallResult += parseBlocksRecursively(child, depth)

    # Handle the case for Blockly CPP
    c_main = [ ns for ns in node.findall("block") if ns.attrib["type"] == "c_main" ]
    if( len( c_main ) == 1): 
        main = refactorStatementToBlock(c_main[0].find("statement"))
        overallResult += parseBlocksRecursively(main, 0)

        #Why do we need this?
        #if (("void loop ()" not in overallResult)):
            #overallResult += "void loop () {\n}\n"

        return main_funcs + overallResult

    elif tag == "block":
        return getBlock(node,depth)
    elif tag == "next":
        return ";\n" + parseBlocksRecursively(list(node)[0], depth)
    elif tag == "statement":
        return parseBlocksRecursively(list(node)[0], depth)
    elif tag == "shadow":
        return parseBlocksRecursively(list(node)[0], depth)
        #return getField(list(node)[0])
    elif tag == "value":
        return parseBlocksRecursively(list(node)[0], depth)
        #return getBlock(list(node)[0], depth)
    elif tag == "field":
        return getField(node)
    else:
        return ""

# Safety net for checking if there is a next block
#shouldn't the if statement check if it's equal to 0?
def recurseParseCheck(nodeList, depth, remove_white_space=False):
    if (len(nodeList) != 1):
        return ""
    else:
        return parseBlocksRecursively(nodeList[0], depth)

# Sub functions

def getBlock(node,depth):
    blockType = node.attrib["type"]

    if (blockType == "main_loop"):
        # Should be a "next" block
        loopStr = recurseParseCheck(list(node), depth+1)+";"
        global main_loop
        main_loop = loopStr.split("\n")
        return "void loop () {\n" + loopStr + "\n}"

    if (blockType == "main_body"):
        mainStr = "int main() {\n " 
        mainStr += recurseParseCheck(list(node), depth+1) + ";\n"
        mainStr += spaces + " return 0;\n}"
        global isCpp
        isCpp = True
        return mainStr

    #TODO PQ will move this to its own separate function later lol
    if (blockType == "text_print"):
        nextNode = (node.find("value").find("block"))
        function = depth*spaces + "cout << ("
        #function += recurseParse([nextNode], depth+1, remove_white_space=True)
        function += parseBlocksRecursively(nextNode, depth + 1)
        return parseNextBlock(node, depth, function + ") << endl")

    if (blockType == "variable_declarations"):
        setupStr = recurseParseCheck(list(node), depth + 1) + ";"
        global main_setup
        main_setup = setupStr.split("\n")
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

    if (blockType == "logic_boolean"):
        if list(node)[0].text == "TRUE":
            return "true"
        else:
            return "false"
    if (blockType == "main"): 
        lines = ""
        for b in map( refactorStatementToBlock, node.findall("statement" )):
            lines += parseBlocksRecursively( b, depth ) + delimitter+ '\n'
        return lines
    if blockType == "root_node": 
        from behavior_parser import BehaviorParser
        behavior_parser = BehaviorParser(program_name) 
        behavior_parser.parse_node( node )
        return ""

    return genericBlockGet(node,depth)
   
def genericBlockGet(node,depth):
    blockType = node.attrib["type"]
    # Remainder block types that aren't built in, so it must be custom
    if (len(blockType.split("$")) < 3):
        print blockType
        raise BlocklyError("Block " + blockType + " is malformatted!")
        return ""

    object_instance = blockType.split("$")[1]
    global declaredObjs
    declaredObjs.add(object_instance)
    method_name = blockType.split("$")[2]

    if (len(list(node)) == 0):
        return parseNextBlock(node, depth, object_instance + "." + method_name + "()")

    arguments = getArgs(node)

    block_code_value = object_instance + "." + method_name + "(" + arguments + ")"
    return parseNextBlock(node, depth, block_code_value)

def parseNextBlock(node, depth, nodeStr):
    if not hasNext(node): return (spaces * depth) + nodeStr
    else: return (spaces * depth) + nodeStr + parseBlocksRecursively(list(node)[-1], depth)

#iterate through the children; may have a "next"
def hasNext(node):
    if len(list(node)) == 0:
        return False
    if (list(node)[-1].tag == "next"):
        return True
    return False

def getArgs(node ):
    arguments = ""
    argList = filter(lambda n: n.tag == "block" or n.tag == "value", (list(node)))
    if len( argList ) == 0:
        argList = filter(lambda n: n.tag == "shadow", (list(node)))
    for i in range(len(argList)):
        curr = argList[i]
        if(arguments != ""):
            arguments += ", "
        if curr.tag == "value": arguments += getValue( curr )
        else: arguments += parseBlocksRecursively(argList[i], 0)

    return arguments

# Typing dictionary
typeDict = {
    "math_number": "int",
    "text": "string",
    "logic_boolean": "bool"
}
def getType(node):
    if ((node.attrib).get("type") != None and typeDict.get(node.attrib["type"]) != None):
        return typeDict[node.attrib["type"]]
    #else if (node.tag == "block"):
        #
    else:
        #default int
        return "int"


def getField(node):
    if (node.attrib.get("name") != None and node.attrib["name"] == "BOOL"):
        if (node.text == "TRUE"):
            return "true"
        if (node.text == "FALSE"):
            return "false"
    return node.text

def getValue( val ):
    node = val.find("block")
    if node is None: node = val.find("shadow")
    return parseBlocksRecursively( node, 0 )

    return opDict[node.text]


def getConst(node):
    for k in mathDict.keys():
        if k in getField(node): return mathDict[k] + "(" + getField(node[4:]) + ")"
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
    if varName in declaredVars: pass
        # Already declared, we don't need to redo it
    else:
        # Not declared yet, put it in thing
        varType = getType(list(list(node)[1])[0]) + " "
        declaredVars.append(varType + varName + ";")

    if((list(list(node)[1])[0]).tag == "block"):
        varValue = parseBlocksRecursively(list(list(node)[1])[0], 0)
    else:
        varValue = getField(list(list(list(node)[1])[0])[0])

    totString = varName + " = " + varValue# + ";"
    return parseNextBlock(node, depth, totString)

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
        statementPart = parseBlocksRecursively(list(node)[2], depth+1)
    else:
        if (ifBChild < 2):
            raise BlocklyError("If-Statement requires a condition and statements!")

        booleanPart = getArgs(list(node)[0])
        statementPart = parseBlocksRecursively(list(node)[1], depth+1)

    # Second child is the statement part
    returnStr = "if(" + booleanPart + ") {\n"

    totString = returnStr + statementPart + ";\n" + (spaces*depth) + "}"

    if (numElsIfs >= 1):
        totString += elseifBlock(node, numElsIfs, depth)

    if (numElses == 1):
        stmtList = [ s for s in list(node) if s.tag == "statement" ]
        stmt = parseBlocksRecursively( stmtList[-1], depth + 1) 
        totString += "\n" + (spaces*depth) + "else {\n" + stmt + ";\n" + (spaces*depth) + "}"

    return parseNextBlock(node, depth, totString)

#else if statements
def elseifBlock(node, numTimes, depth):
    elseifOpenString = "\n" + (spaces*depth) + "else if("
    elseString = ""

    for i in range(3, 3 + (numTimes * 2)):
        if (((list(node)[i]).attrib["name"])[:2] == "IF"):
            elseString += elseifOpenString
            booleanPart = getArgs(list(node)[i])
            elseString += booleanPart + ") {\n" + parseBlocksRecursively((list(node)[i + 1]), depth + 1) + ";\n" + (spaces*depth) + "}"

    return elseString

#else statement
def elseBlock(node, depth):
    elseString = "else {\n" + (spaces*depth) + "}"

#logic compare
def compLog(node,depth):
    # 3 children: operator, value A, value B
    operator = getOp(list(node)[0])
    if (len(list(node)) != 3):
        raise BlocklyError("Logic compare with operator '" + operator + "' requires 2 values to compare!")
        return ""
    valueA = parseBlocksRecursively(list(list(node)[1])[0],depth)
    valueB = parseBlocksRecursively(list(list(node)[2])[0],depth)

    return parseNextBlock(node, depth, (valueA + " " + operator + " " + valueB))

#math property
def mathProp(node, depth):
    test = list(node)[1].text

    numToCheck = parseBlocksRecursively(list(node)[2], 0)
    if (test == "EVEN"): modNum = 0
    else: modNum = 1
    #even, odd, prime, whole, positive, negative, divisible by

    total = numToCheck + "%2 == " + str(modNum)

    return parseNextBlock(node, depth, total)

#math arithmetic
def mathMetic(node,depth):
    # 3 children: operator, value A, value B
    operator = getOp(list(node)[0])
    if (len(list(node)) != 3):
        raise BlocklyError("Math block with operator '" + operator + "' requires 2 values to compute!")
        return ""
    #valueA = recurseParse(list(list(node)[1])[-1],depth)
    #valueB = recurseParse(list(list(node)[2])[-1],depth)

    valueA = parseBlocksRecursively(list(list(node)[1])[-1],depth)
    valueB = parseBlocksRecursively(list(list(node)[2])[-1],depth)

    if (operator == "pow"):
        return parseNextBlock(node, depth, ("pow(" + valueA + ", " + valueB + ")"))

    return parseNextBlock(node, depth, (valueA + " " + operator + " " + valueB))

#math single
def mathSingle(node, depth):
    operator = getOp(list(node)[0])

    valueOn = getValue( node.find("value" ) )
    if operator in ["sqrt", "abs", "-1*", "pow", "log", "log10", "exp"]:
        return parseNextBlock(node, depth, (operator + "(" + valueOn + ")"))
    if operator == "pow10": 
        return parseNextBlock(node, depth, ("pow(10," + valueOn + ")"))

    return parseNextBlock(node, depth, (operator + valueOn))

#math modulo
def mathModulo(node, depth):
    values = [ n for n in node if n.tag == "value" ]
    dividend = getValue( values[0] )
    divisor = getValue( values[1] )

    return parseNextBlock(node, depth, "(int)" + dividend + " % (int)" + divisor)

#math random
def mathRand(node, depth):
    minNum = parseBlocksRecursively(list(list(node)[0])[0], depth)
    maxNum = parseBlocksRecursively(list(list(node)[1])[0], depth)

    return "rand() % (" + maxNum + " - " + minNum + ") + " + minNum

#math random float
def mathRandFloat(node, depth):
    return "(float) rand() / RAND_MAX"

#while loop
def whileUnt(node, depth):
    retString = "while("

    if (len(list(node)) < 3):
        raise BlocklyError("While-loop requires a condition and statements!")

    if (list(node)[0]).text == "UNTIL":
        retString += "!("

    if ((list(node)[1]).attrib.get("name") != None and (list(node)[1]).attrib["name"] == "BOOL"):
        condit = getArgs(list(node)[1])
        retString += condit

    if (list(node)[0]).text == "UNTIL":
        retString += ")"

    retString += ") {\n"

    if (list(node)[2]).attrib.get("name") != None and (list(node)[2]).attrib["name"] == "DO":
        statement = parseBlocksRecursively(list(node)[2], depth + 1)
    else:
        statement = "\n";

    retString += statement + ";\n" + (spaces*depth) + "}"

    return parseNextBlock(node, depth, retString)

#negate
def negate(node, depth):
    retString = "!("

    inner = parseBlocksRecursively(list(list(node)[0])[0], 0)
    return parseNextBlock(node, depth, (retString + inner + ")"))

#repeat for specified num of times
def repeatControl(node, depth):
    retString = ";\n" + (spaces*depth) + "int __i;\n"
    retString += (spaces*depth) + "for(__i = 0; __i < "
    count = parseBlocksRecursively(list(node)[0], 0)
    retString += count + "; __i++) {\n"

    statement = parseBlocksRecursively(list(node)[1], depth+1)

    retString += statement + ";\n" + (spaces*depth) + "}\n"

    return parseNextBlock(node, depth, retString)

#for loop
def forloop(node, depth):
    #from
    val = getField(list(node)[0])
    values = node.findall("value")
    fromVal = getValue( values[0] )

    # Moving this here so that val can be declared outside
    retString = (spaces*(depth-1)) + "for(int "

    retString += val + " = " + fromVal

    #to
    toVal = getValue( values[1] )

    #increment
    incr = getValue( values[2] )

    try: cond = "<=" if float(fromVal) <= float(toVal) else ">="
    except: cond = "<="

    retString += "; " + val + cond + "("+toVal+"); " + val + "+=(" + incr + ")) {\n"

    statement = parseBlocksRecursively(list(node)[4], depth+1)

    retString += statement + ";\n " + (spaces*depth) + "}"

    return parseNextBlock(node, depth, retString)

#delay
def delay(node,depth):
    retString = "delay((int)"
    varValue = getArgs(list(node)[0])
    retString += varValue + ")"
    return parseNextBlock(node, depth, retString)

#delaySeconds
def delaySeconds(node,depth):
    retString = "delay( (int) ( 1000 * ("
    varValue = getArgs(list(node)[0])
    retString += varValue + ")))"
    return parseNextBlock(node, depth, retString)

#millis
def millis(node, depth):
    return parseNextBlock(node, depth, "millis()")

#controls_flow_statements
def flowcontrols(node, depth):
    flow = getOp(list(node)[0])
    return parseNextBlock(node, depth, flow)

#Function creation
def funcCreation(node, depth):
    params = ""
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
        if (child.tag == "comment"):
            comment += child.text + "\n" + (spaces*depth) + "*/\n"
        if (child.tag == "field"):
            funcName = str.replace(child.text, " ", "")
        if (child.tag == "statement"):
            funcBody = parseBlocksRecursively(list(child)[0], depth + 1) + ";\n"
        if (child.tag == "value"):
            retType = getType(list(child)[0])
            funcRet = (spaces*(depth + 1)) + "return " + parseBlocksRecursively(list(child)[0], 0) + ";;\n"

    total = comment + retType + " " + funcName + "(" + params + ") {\n" + funcBody + funcRet + (spaces*depth) + "}\n"

    #paramNum, func
    global declaredFuncs
    global definedFuncs
    if (checkFuncDefs.get(funcName) == None):
        definedFuncs += total.split("\n")
        declaredFuncs.append(retType + " " + funcName + "(" + params + ");")
        checkFuncDefs[funcName] = True

    return parseNextBlock(node, depth, total)

def findDefine(node):
    paramNum = 0;
    funcName = ""
    for child in node:
        if(child.tag == "mutation"):
            for arg in child:
                paramNum += 1
        if(child.tag == "field"):
            funcName = str.replace(child.text, " ", "")

    madeFuncNames[funcName] = paramNum

#call the method with correct arguments as stored by function dictionary
def callMethod(node, depth):
    methodName = str.replace((list(node)[0]).attrib["name"], " ", "")
    arguments = ""
    argNums = 0

    #check dictionary for params to pull
    call = methodName + "("

    #PQ TODO FIX THIS
    if ((madeFuncNames[methodName]) > 0):
        for arg in list(node)[0]:
            argNums += 1

        for child in node:
            if (child.tag == "value"):
                if(arguments != ""):
                    arguments += ", "
                arguments += parseBlocksRecursively(child, 0)
        
        call += arguments

    return parseNextBlock(node, depth, call + ")")

#make an if-return for function creation
def ifRet(node, depth):
    mainStr = ";\n" + (spaces*depth) + "if("

    boolPart = getArgs(list(node)[1])
    funcRet = (spaces*(depth + 1)) + "return " + parseBlocksRecursively(list(list(node)[2])[0], 0) + ";"

    mainStr += boolPart + ") {\n" + funcRet + ";\n" + (spaces*depth) + "}\n"

    return parseNextBlock(node, depth, mainStr)

def funcCheckGet(blockType, node, depth):
    if (len(list(node)) > 0 and (list(node)[0]).tag == "next"):
        return parseNextBlock(node, depth, "")
    
    return funcGet[blockType](node, depth)

madeFuncNames = {
}

checkFuncDefs = {
}
funcGet = {
    "variables_set": setVar,
    "controls_if": ifBlock,
    "logic_compare": compLog,
    "logic_operation": compLog,
    "math_number_property": mathProp,
    "math_arithmetic": mathMetic,
    "math_single": mathSingle,
    "math_modulo": mathModulo,
    "math_random_int": mathRand,
    "math_random_float": mathRandFloat,
    "controls_whileUntil": whileUnt,
    "controls_repeat_ext": repeatControl,
    "controls_for": forloop,
    "delay": delay,
    "delaySeconds": delaySeconds,
    "millis": millis,
    "logic_negate": negate,
    "controls_flow_statements": flowcontrols,
    "procedures_defreturn": funcCreation,
    "procedures_defnoreturn": funcCreation,
    "procedures_ifreturn": ifRet,
    "procedures_callreturn": callMethod,
    "procedures_callnoreturn": callMethod
}

def findFuncDefs(node):
    for child in node:
        if(child.tag == "field"):
            funcName = str.replace(child.text, " ", "")

    if(madeFuncNames[funcName] != None):
        return True
    return False

def run( xml ):
    tree = ET.parse(xml)
    root = tree.getroot()
    madeFuncNames.clear()
    checkFuncDefs.clear()
    try:
        if DEBUG: print("--- RUNNING IN DEBUG MODE ---")
        mainStr = (parseBlocksRecursively(root,0))
        mainStr = "\n".join( [ a for a in getVars() ] ) + "\n" + mainStr 

        # Jinja would be better
        if use_c_lib: mainStr = c_lib + mainStr 
        return mainStr
    except BlocklyError as e:
        print("Error: " + e.value)
        raise
		
#############################################################################
#def stateBlock ( xml ):

#def transitionBlock (xml):

#############################################################################		

def getLoop(): return main_loop
def getVars(): return set(declaredVars)
def getFuncDefs(): return definedFuncs
def getFuncDecs(): return declaredFuncs
def getSetup(): return main_setup

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

