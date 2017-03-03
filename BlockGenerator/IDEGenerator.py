__author__ = "Michael Gonzalez"
__email__ = "mmg005@eng.ucsd.edu"

import json
import unicodedata
import xml.etree.ElementTree as ET
from GspecParser import GspecParser
import os
import copy
from StringIO import StringIO
from JinjaUtil import *

# Open config
json_file = open(os.path.join("..", "config", "config.json"))
config = json.load(json_file)
json_file.close()

gspec = str(os.path.join( "..", config["gspec_file"] ))

resources_dir = "Resources"
extra_categories_file = "extra_categories.jinja.xml"
js_template = "Javascript_Template.jinja.js"
js_definitions = "javascript_block_definitions.js"
output_dir = os.path.join("..", "WebStatic", "jinja_templates" )


class IDEGenerator:
    # Default constructor
    def __init__(self, resDir, defaultWorkspaceFile, blocklyDir):
        self.components = None
        self.jinja_vars = {"blocklist":[]}
        #self.jinja_vars["defaultBlocks"] = open(defaultWorkspaceFile).read().replace("\n", "").replace('"', '\\"')
        self.jinja_vars["defaultBlocks"] = "{{defaultBlocks}}"
        self.jinja_vars["resDir"] = resDir
        self.jinja_vars["lib"] = resDir + "lib/"
        self.jinja_vars["blockly"] = blocklyDir
        
    # Loads default blocks xml to build the Blockly toolbox
    def loadDefaultBlocks( self, blocksXml ):
        self.categoriesXML = ET.Element("xml")
        self.categoriesXML.attrib["id"] = "toolbox"
        self.categoriesXML.attrib["style"] = "display: none"
        # Grab the default categories
        default_block_root = ET.parse(blocksXml)
        if type(blocksXml) is unicode: 
            default_block_root = ET.fromstring(blocksXml)
        #Append each block to our template
        for block in default_block_root.getroot():
            self.categoriesXML.append( block )
        self.jinja_vars["toolbox"] = str(ET.tostring( self.categoriesXML ))
    # Loads the block json into the object
    def loadBlockDefinitions( self, blockJson ):
        # Type checking
        if type (blockJson) == str:
            stream = None
            # Is it a file?
            if os.path.isfile( blockJson):
                stream = open(blockJson)
            # Otherwise, treat it like a string
            else:
                stream = StringIO( blockJson )
            self.blocks = json.load(stream)
        # For some reason, it seems like json objects get passed as lists
        elif type (blockJson) == list:
            self.blocks = blockJson
        else:
            print "Unknown type: ", type(blockJson)
            raise "Unknown type passed to loadBlockDefinitions"

    # Loads the gspec into the object using Priyanka's gspec parser
    # Saves the gspec, doesn't return anything
    def loadGspec( self, gspec, catalog ):
        gspecParser = GspecParser()
        gspecParser.setCatalog(catalog)
        self.components = gspecParser.getComps(gspec)
        
    def createBlockSubset(self):
        self.blockCategories = {}
        extra_categories = []
        totalNumberOfCategories = 0
        componentIdx = 1.0
        for k in self.components.keys():
            totalNumberOfCategories = totalNumberOfCategories + len(self.components[k])
        for key in self.components.keys():
            i = 0
            for instance in self.components[key]:
                i += 1
                # Some useful aliases
                name = key + " #" + str(i)
                
                # We want a new colour for this subset
                color = str(int((componentIdx / totalNumberOfCategories) * 360))
                componentIdx = componentIdx + 1
                
                # The blocks for just this component will be called localBlocks
                localBlocks = {}
                
                # Create the categoriesXML node
                categoryNode = ET.Element("category" )
                categoryNode.attrib["name"] = name
                categoryNode.attrib["colour"] = color
                
                # Iterate over each block in our copy so we can make a unique instance
                jsonElem = copy.deepcopy(self.blocks[key])
                uid = 0
                for block in jsonElem:
                    # Set the name that will be displayed on this block
                    # to have the same number as this component instance
                    message0 = block["message0"].split(' ')
                    message0[0] += " #"+str(i)
                    block["message0"] = " ".join(message0)
                    block["id"] = "$" + instance + "$" + block["id"]
                    id = block["id"].encode('ascii', 'ignore')
                    block["colour"] = color
                    # Add the new block to its proper category
                    blockNode = ET.SubElement(categoryNode, "block")
                    blockNode.attrib["type"] = id + "$" + str(uid)
                    blockNode.text = " "
                    # Add the shadow arguments to the block
                    for arg in block["args0"]:
                        if "name" in arg:
                            valueNode = ET.SubElement( blockNode, "value" )
                            shadowNode = ET.SubElement( valueNode, "shadow")
                            fieldNode = ET.SubElement( valueNode, "field")
                            valueNode.attrib["name"] = arg["name"]
                            if arg["check"] == "Number":
                                shadowNode.attrib["type"] = "math_number"
                                fieldNode.attrib["name"] = "NUM"
                                fieldNode.text = "0"
                    localBlocks[ block["id"] ] = block
                    self.jinja_vars["blocklist"].append( [ id + "$" + str(uid), str(json.dumps(block)) ] )
                    uid += 1
                self.blockCategories[ name ] = localBlocks
                if len(categoryNode): extra_categories.append(ET.tostring(categoryNode))
        #self.jinja_vars["toolbox"] = str(ET.tostring( self.categoriesXML ))
        #print self.jinja_vars["toolbox"]
        # Find the file to place all extra files
        out_file = open(os.path.join( output_dir, extra_categories_file ), "w+")
        out_file.write("\n".join(extra_categories))
        out_file.close()

    
    def renderIDE(self, jinja_file):
        jinja_path = os.path.join(os.path.dirname(__file__), resources_dir)
        JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(jinja_path))
        return render_template(jinja_file, self.jinja_vars, jinja_env=JINJA_ENVIRONMENT)
                
if __name__ == "__main__":

    # Default file locations
    jsonFile = "Blocks.json"
    jsonFile = os.path.join(resources_dir, jsonFile)
    catalog = os.path.join("..", "..", "Components.xml")
    jinjaFile = "index.jinja"
    blocksXml = "DefaultCategories.xml"
    # Arg parse stuff
    import argparse
    parser = argparse.ArgumentParser(description="IDEGenerator.py creates a Blockly IDE for Gadgetron. It uses Jinja to create the IDE")
    parser.add_argument("-j", "--json", required=False)
    parser.add_argument("-c", "--catalog", required=False)
    parser.add_argument("-g", "--gspec", required=False)
    parser.add_argument("-r", "--resdir", required=False, default="")
    parser.add_argument("-b", "--blocklydir", required=False, default="lib/blockly/")
    parser.add_argument("-d", "--default_blocks", required=False)
    parser.add_argument("-w", "--default_workspace", default=os.path.join(resources_dir, "DefaultRobotWorkspace.xml") )
    parser.add_argument("-x", "--jinja", required=False)
    args = parser.parse_args()
    if args.jinja is not None:
        jinjaFile = args.jinja
    if args.json is not None:
        jsonFile = args.json
    if args.default_blocks is not None:
        blocksXml = args.default_blocks
    if args.catalog is not None:
        catalog = args.catalog

    generator = IDEGenerator( args.resdir, args.default_workspace, args.blocklydir )
    generator.loadBlockDefinitions( jsonFile )
    #generator.loadDefaultBlocks( blocksXml )
    generator.loadGspec( gspec, catalog )
    generator.createBlockSubset()
    #print "\n".join([ str(w) for w in generator.jinja_vars["blocklist"]])
    js_output = open(os.path.join( output_dir, js_definitions ), "w+")
    js_output.write( generator.renderIDE(js_template).encode('ascii','ignore'))
    js_output.close()
    #print generator.renderIDE(jinjaFile).encode('ascii','ignore')
