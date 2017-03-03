__author__ = "Michael Gonzalez"
__email__ = "mmg005@eng.ucsd.edu"

import xml.etree.ElementTree as ET
import argparse
import os
import platform
import json
from ClangBindings import *

jet_components_dir = os.path.join( "..", "..", "JetComponents" )
release_lib_file = os.path.join( jet_components_dir, "ArduinoReleaseLibs.txt" )
resources_dir = os.path.join(".", "Resources")
black_listed_classes_file = os.path.join( resources_dir, "IgnoredClasses.txt" )
output_file = os.path.join( resources_dir, "Blocks.json" )
black_listed_functions_file = os.path.join(resources_dir, "BlackListedFunctions.xml" )


black_listed_classes_fd = open(black_listed_classes_file)
black_listed_classes = black_listed_classes_fd.read().split("\n")
black_listed_classes_fd.close()

def cleanFunctionName( func ):
    acc = [] 
    expandWords = { "pos" : "position", "max" : "maximum", "rec" : "rectangle", "pix" : "pixel" }
    for w in func.split("_"):
        s0 = 0
        idxs = [ i for i, c in enumerate(w) if c.isupper() ]
        for i in idxs + [ len(w) ]:
            acc.append( w[s0:i].lower() )
            s0 = i
    for i in xrange(len(acc)): 
        if acc[i] in expandWords: acc[i] = expandWords[acc[i]] 
    return " ".join(acc)

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



# Prepare Clang
# This step has only been tested on the iMac in the NVSL and Michael's
# laptop. 
# This line should be the path of the clang library on Ubuntu
clang.cindex.Config.set_library_path('/usr/lib/x86_64-linux-gnu')
# This line should be the path of the clang library on Darwin 
if(platform.platform().split('-')[0].lower() == "darwin"):
    clang.cindex.Config.set_library_path('/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib')
index = clang.cindex.Index.create()

release_lib_fd = open( release_lib_file )
libs = release_lib_fd.read().split("\r\n")
libs = [ lib for lib in libs if lib != "" ]
lib_paths = [ os.path.join(jet_components_dir, lib) for lib in libs ]
print libs
print lib_paths 

# The black list contains functions we don't want to show the Blockly users
blxml = ET.parse( black_listed_functions_file )
blroot = blxml.getroot()
blackList = set()
for f in blroot:
    key = f.attrib["name"]
    if "class" in f.attrib.keys(): key = f.attrib["class"] + key
    blackList.add(key)

# The JSON repsentation of the blocks we're going to dump
blocksJSON = {}

# Then iterate over each component in library
for lib, gcom_dir in zip(libs, lib_paths):
    # Grab the real class file's location
    if not os.path.exists( gcom_dir ): continue
    files = os.listdir( gcom_dir )
    gcom_file = [ f for f in files if "gcom" in f and ".swp" not in f ][0]
    gcom_file = os.path.join( gcom_dir, gcom_file )
    try:
        print "Trying to locate the gcom for", lib
        gcom = ET.parse( gcom_file ).getroot()
        libinfo = [ elem for elem in gcom.iter('libdirectory') ][0]
    except BaseException as e:
        print "ERROR PARSING", lib
        raise e
    path = os.path.join( gcom_dir, libinfo.attrib["path"], libinfo.attrib["link-as"]+".h") 
    print "Parsed path:", path, "for", lib
    # Create a clang translation unit to traverse the class
    try:
        translation_unit = index.parse(path, ['-x', 'c++', '-std=c++11', '-D__CODE_GENERATOR__'])
        classes = build_classes(translation_unit.cursor, path)
    except BaseException as e:
        print "ERROR PARSING", lib 
        print "Parsing path:", path
        raise e

    # Iterate over all classes
    for aClass in classes:
        for f in aClass.functions:
            print f
        #raw_input()
	# Iterate over all the functions in the current class
        fp = 0
        if aClass.name in black_listed_classes :
            print "Skipping", aClass.name
            continue
        else: 
            print "Parsing:", aClass.name
        blocksJSON[aClass.name] = []


	    # We want to verify that all our classes have a setup function
        hasSetup = False
        for func in aClass.functions:
            if func.name in blackList or aClass.name+func.name in blackList:
                if func.name == "setup": hasSetup = True
                continue
	        # Create a blockly json definition
	        # The attributes passed here should be the same across all blockly json files
            funcjson = {
	                "id":func.name,
	                "message0":aClass.name+" "+ cleanFunctionName(func.name) + " %1",
	                "tooltip" : "",
	                "helpUrl": "gadgetron.build" }
            args = [{"type":"input_dummy"}]
	        # We want to keep an index to update our message0 attribute later
            i = 2
            fp += 1
	        # Iterate over all the arguments for the current function
            skip_func = False
            for arg in func.params:
                if arg[0] == "": continue
                argType = determineParamType(arg[1])
                preposition = { "String" : "as", "Number":"at","Boolean":"being" } 
                argJson = {"type":"input_value",
	                       "name":arg[0],
                           "check":argType}
                funcjson["message0"] += " with " + arg[0] + " " + preposition[argType] + " %" + str(i)
                i += 1
                args.append(argJson)
            if skip_func: continue
            funcjson["args0"] = args
	        # Determine the return type of the block
            if func.returnType == "void":
                funcjson["previousStatement"] = None
                funcjson["nextStatement"] = None
            else:
                funcjson["output"] = None
            blocksJSON[aClass.name].append(funcjson)
            
        if hasSetup is False: raise Exception( aClass.name + " has no setup() method!")

out_file_fd = open( output_file, "w+" )
json.dump( blocksJSON, out_file_fd ) 

