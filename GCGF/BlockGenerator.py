__author__ = "Michael Gonzalez"
__email__ = "mmg005@eng.ucsd.edu"

import xml.etree.ElementTree as ET
from lxml import etree as ET2
import argparse
import os
import random
import platform
import json
import jinja2
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
parser = argparse.ArgumentParser(description="BlockGenerator.py creates a Blockly IDE for Gadgetron. It parses our existing C++ clase libraries using Clang to generate block categories and blocks. It then uses Jinja to actually create the IDE")
parser.add_argument("-l", "--library", required=True)
parser.add_argument("-d", "--default_blocks", required=True)
parser.add_argument("-j", "--jinja", required=True)
args = parser.parse_args()

# Prep Jinja Template
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
template = JINJA_ENVIRONMENT.get_template(args.jinja)
# This variable is used later in the script to pass variables to the template
jinja_vars = {"blocklist":[]}

# Prepare lxml 
# This script uses lxml to build the Blockly toolbox
root = ET2.Element("xml")
root.set("id", "toolbox")
root.set("style", "display: none")
# Grab the default categories
default_block_root = ET2.parse(args.default_blocks)
# Append each block to our template
for block in default_block_root.getroot():
    root.append( block )

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
        # Pick a random color to represent this class's category
        currColor = random.randrange(0,360)
	# Start the xml definition for this category's toolbox representation
        newBlock = ET.SubElement(root, "category") 
	# Set the category's name attribute
	newBlock.set("name", aClass.name)
	# Set the category's colour attribute
	newBlock.set("colour", str(currColor))
	# Iterate over all the functions in the current class
	fp = 0

	for func in aClass.functions:
	    # Create a blockly json definition
	    # The arrtibutes passed here should be the same accross all blockly json files
	    funcjson = {
	            "id":"_"+aClass.name+"_"+func.name + str(fp),
	            "message0":aClass.name+" "+func.name + " %1",
                    "colour" : currColor,
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
	    # Create an xml block to represent this function
	    funcxml = ET.SubElement( newBlock, "block")
	    # Set the type to the id
	    funcxml.set("type", funcjson["id"] )
	    # We need to set the text to something so the tag closes properly
	    funcxml.text = " "
	    jinja_vars["blocklist"].append([str(funcjson["id"]), str(json.dumps(funcjson))])
        #hasSetup = printClassFunctions( aClass)
        #if hasSetup is False:
        #    raise Exception( aClass.name + " has no setup() method!")

# Put the toolbox into the jinja variables
jinja_vars["toolbox"] = str(ET2.tostring( root ))
# Print the output!
print template.render(jinja_vars)
