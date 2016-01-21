import xml.etree.ElementTree as ET
from lxml import etree as ET2
import argparse
import os
import random
import platform
import json
from clangTest import *
def createBlockName( func ):
    name = func.name
    name[0].title()
    i = 0
    for param in func.params:
        if( i is 0):
	    name = name + " with "
	else:
	    name = name + " and "
        name = name + param[0] + " as "
	name = name + " %'" + param[0] + "'"
	i = i + 1
    return name
def determineBlockType( func ):
    type = func.returnType.lower()
    if( type == "int" or type == "float" or type == "double"):
        return "reporter"
    if( type == "bool" or type == "boolean" ):
        return "predicate"
    else:
        return "command"
def determineParamType( param ):
    cleaned = param.lower()
    if( cleaned == "int" or cleaned == "float" or cleaned == "double"):
        return "Number"
    if( cleaned == "std::string" or "string" ):
        return "String"
    if( cleaned == "bool" or "boolean" ):
        return "Boolean"
    else:
        print "FunctionParam Error: Could not determine parameter type in determineParamType in BlockGenerator.py"
	raise
# Arg parse stuff
parser = argparse.ArgumentParser(description="Generates XML objects that represent each function in our arduino libraries")
parser.add_argument("-l", "--library", required=True)
args = parser.parse_args()
# Xml stuff
libxml = ET.parse( args.library )
library = libxml.getroot()
# Clang stuff
clang.cindex.Config.set_library_path('/usr/lib/x86_64-linux-gnu')
if(platform.platform().split('-')[0].lower() == "darwin"):
    clang.cindex.Config.set_library_path('/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib')
index = clang.cindex.Index.create()
# lxml generator stuff
root = ET2.Element("blocks")
root.set("app", "Snap! 4.0, http://snap.berkeley.edu") 
root.set("version", "1") 
def printClassFunctions( aClass ):
    for aFunction in aClass.functions:
    #print aFunction
        hasSetup = False
        newBlock = ET.SubElement( root, "block-definition" )
        newBlock.set("s", createBlockName(aFunction) )
        newBlock.set("type", determineBlockType(aFunction))
        ET.SubElement( newBlock, "header" )
        ET.SubElement( newBlock, "code" )
        inputs = ET.SubElement( newBlock, "inputs" )
        for param in aFunction.params:
            input = ET.SubElement( inputs, "input" )
	    input.set("type", determineParamType( param[1] ))
	    if( param[0] is "setup" ):
	        hasSetup = True
	return hasSetup
for component in library:
    path = component.attrib["path"]
    path = os.path.expandvars( path )
    #print path
    translation_unit = index.parse(path, ['-x', 'c++', '-std=c++11', '-D__CODE_GENERATOR__'])
    classes = build_classes(translation_unit.cursor, path)
    # Iterate over all classes
    for aClass in classes:
        # Pick a random color to represent this category
        currColor = random.randrange(0,360)
	# Start the xml definition for this category
        newBlock = ET.SubElement(root, "Category") 
	ET.SubElement(newBlock, "empty")
	# Set the name attribute
	newBlock.set("name", aClass.name)
	# Set the colour attribute
	newBlock.set("colour", str(currColor))
	
	# Iterate over all the functions in the current class
	for func in aClass.functions:
	    # Create the standard json definition
	    funcjson = {
	            "id":aClass.name+"_"+func.name,
	            "message0":aClass.name+" "+func.name + " %1",
                    "colour" : currColor,
	            "tooltip" : "",
	            "helpUrl": "gadgetron.build" }
            args = [{"type":"input_dummy"}]
	    i = 2 # We want to keep an index to update our message0 attribute later
	    # Iterate over all the arguments for the current function
	    for arg in func.params:
	        argJson = {"type":"input_value",
		           "name":arg[0],
			   "check":determineParamType(arg[1])}
	        funcjson["message0"] = funcjson["message0"] + " with " + arg[0] + " %" + str(i)
		i = i + 1
		args.append(argJson)
	    funcjson["args0"] = args
	    # Determine the return type of the block
	    if func.returnType == "void":
	        funcjson["previousStatement"] = None
	        funcjson["nextStatement"] = None
            else:
	        funcjson["output"] = None
	    # Create an xml block to represent this function
	    funcxml = ET.SubElement( newBlock, "block")
	    # Set the type to the id
	    funcxml.set("type", funcjson["id"] )
            #print json.dumps(funcjson)
        #hasSetup = printClassFunctions( aClass)
        #if hasSetup is False:
        #    raise Exception( aClass.name + " has no setup() method!")

print ET2.tostring( root, pretty_print=True )
#tree = ET2.ElementTree( root )
