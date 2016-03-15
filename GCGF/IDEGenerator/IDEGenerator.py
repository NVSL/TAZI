__author__ = "Michael Gonzalez"
__email__ = "mmg005@eng.ucsd.edu"

import json
import unicodedata
import xml.etree.ElementTree as ET
from GspecParser import GspecParser
import os
import copy
from StringIO import StringIO
import jinja2


class IDEGenerator:
    # Default constructor
    def __init__(self, DefaultWorkspaceFile="Resources/DefaultRobotWorkspace.xml"):
        self.components = None
        self.JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
        self.jinja_vars = {"blocklist":[]}
	#self.jinja_vars["defaultBlocks"] = open(DefaultWorkspaceFile).read().replace("\n", "").replace('"', '\\"')
	self.jinja_vars["defaultBlocks"] = "{{defaultBlocks}}"
	self.jinja_vars["resDir"] = "/static/"
        
    def setJinjaTemplate(self, template):
        self.template = self.JINJA_ENVIRONMENT.get_template(template)
        
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
        totalNumberOfCategories = 0
        componentIdx = 1.0
        for k in self.components.keys():
            totalNumberOfCategories = totalNumberOfCategories + self.components[k]
        for component in self.components.keys():
            for i in range( 1, self.components[component] + 1 ):
                # Some useful aliases
                name = component + " #" + str(i)
                
                # We want a new colour for this subset
                color = str(int((componentIdx / totalNumberOfCategories) * 360))
                componentIdx = componentIdx + 1
                
                # The blocks for just this component will be called localBlocks
                localBlocks = {}
                
                # Create the categoriesXML node
                categoryNode = ET.SubElement(self.categoriesXML, "category" )
                categoryNode.attrib["name"] = name
                categoryNode.attrib["colour"] = color
                
                # Iterate over each block in our copy so we can make a unique instance
                jsonElem = copy.deepcopy(self.blocks[component])
                uid = 0
                for block in jsonElem:
		    # Set the name that will be displayed on this block
		    # to have the same number as this component instance
		    message0 = block["message0"].split(' ')
		    message0[0] += " #"+str(i)
		    block["message0"] = " ".join(message0)
                    block["id"] = "$" + component.lower() + str(i) + "$" + block["id"]
                    id = block["id"].encode('ascii', 'ignore')
                    block["colour"] = color
                    # Add the new block to its proper category
                    blockNode = ET.SubElement(categoryNode, "block")
                    blockNode.attrib["type"] = id + "$" + str(uid)
                    blockNode.text = " "
                    localBlocks[ block["id"] ] = block
                    self.jinja_vars["blocklist"].append( [ id + "$" + str(uid), str(json.dumps(block)) ] )
                    uid += 1
                self.blockCategories[ name ] = localBlocks
        self.jinja_vars["toolbox"] = str(ET.tostring( self.categoriesXML ))
	#print self.jinja_vars["toolbox"]
    
    def renderIDE(self):
        return self.template.render(self.jinja_vars)
                
if __name__ == "__main__":

    # Default file locations
    jsonFile = "Blocks.json"
    catalog = "Components.xms"
    jinjaFile = "index.jinja"
    blocksXml = "DefaultCategories.xml"
    # Arg parse stuff
    import argparse
    parser = argparse.ArgumentParser(description="IDEGenerator.py creates a Blockly IDE for Gadgetron. It uses Jinja to create the IDE")
    parser.add_argument("-j", "--json", required=False)
    parser.add_argument("-c", "--catalog", required=False)
    parser.add_argument("-g", "--gspec", required=False)
    parser.add_argument("-d", "--default_blocks", required=False)
    parser.add_argument("-w", "--default_workspace", default="Resources/DefaultRobotWorkspace.xml" )
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

    generator = IDEGenerator( args.default_workspace )
    generator.setJinjaTemplate( jinjaFile )
    generator.loadBlockDefinitions( jsonFile )
    generator.loadDefaultBlocks( blocksXml )
    if args.gspec is not None:
        generator.loadGspec( args.gspec, catalog )
        generator.createBlockSubset()
    print generator.renderIDE().encode('ascii','ignore')
