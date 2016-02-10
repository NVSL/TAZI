__author__ = "Michael Gonzalez"
__email__ = "mmg005@eng.ucsd.edu"

import xml.etree.ElementTree as ET
from lxml import etree as ET2
import argparse
import os
import platform
import json
from ClangBindings import *

# Function Name: determineParamType()
# Arguments: param - A string representation of a function's parameter
# Returns: The string which blockly uses to constrain block input types
# Error Handling: If the parameter passed to this function does not match any
#                 of the handled types, then this function will raise an 
#                 exception. THIS FUNCTION IS NOT EXHAUSTIVE
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

# Setup argument parsing
parser = argparse.ArgumentParser(description="BlockGenerator.py creates a Blockly IDE for Gadgetron. It parses our existing C++ class libraries using Clang to generate block categories and blocks. It then uses Jinja to actually create the IDE")
parser.add_argument("-l", "--library", required=True)
parser.add_argument("-d", "--default_blocks", required=True)
args = parser.parse_args()


# Prepare Clang
# This step has only been tested on the iMac in the NVSL and Michael's
# laptop. 
# This line should be the path of the clang library on Ubuntu
clang.cindex.Config.set_library_path('/usr/lib/x86_64-linux-gnu')
# This line should be the path of the clang library on Darwin 
if(platform.platform().split('-')[0].lower() == "darwin"):
    clang.cindex.Config.set_library_path('/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib')
index = clang.cindex.Index.create()

# The library argument passed to this script contains the locations of each of
# the C++ class files. This grabs the root of that xml file
libxml = ET.parse( args.library )
library = libxml.getroot()

# The JSON repsentation of the blocks we're going to dump
blocksJSON = {}

# Then iterate over each component in library
for component in library:
    # Grab the real class file's location
    path = component.attrib["path"]
    path = os.path.expandvars( path )
    # Create a clang translation unit to traverse the class
    translation_unit = index.parse(path, ['-x', 'c++', '-std=c++11', '-D__CODE_GENERATOR__'])
    classes = build_classes(translation_unit.cursor, path)

    # Iterate over all classes
    for aClass in classes:
        
	# Iterate over all the functions in the current class
	fp = 0
        blocksJSON[aClass.name] = []

	for func in aClass.functions:
	    skippedFunctions = [ "setup", "update", "loop" ]
	    if func.name in skippedFunctions:
	        continue
	    # Create a blockly json definition
	    # The attributes passed here should be the same across all blockly json files
	    funcjson = {
	            "id":func.name,
	            "message0":aClass.name+" "+func.name + " %1",
	            "tooltip" : "",
	            "helpUrl": "gadgetron.build" }
            args = [{"type":"input_dummy"}]
	    # We want to keep an index to update our message0 attribute later
	    i = 2
            fp += 1
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
	    
            blocksJSON[aClass.name].append(funcjson)

        #hasSetup = printClassFunctions( aClass)
        #if hasSetup is False:
        #    raise Exception( aClass.name + " has no setup() method!")


print json.dumps(blocksJSON, indent = 4 )

