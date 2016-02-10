import json
from GspecParser import GspecParser
import os
import copy
from StringIO import StringIO
import jinja2




class IDEGenerator:
    # Default constructor
    def __init__(self):
        self.components = None
        self.JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
        self.jinja_vars = {"blocklist":[]}
        
    def setJinjaTemplate(self, template):
        self.JINJA_ENVIRONMENT.get_template(template)
        
    # Loads default blocks xml to build the Blockly toolbox
    def loadDefaultBlocks( self, blocksXml ):
        self.categoriesXML = ET.Element("xml")
        self.categoriesXML.attrib["id"] = "toolbox"
        self.categoriesXML.attrib["style"] = "display: none"
        # Grab the default categories
        default_block_root = ET.parse(blocksXml)
        #Append each block to our template
        for block in default_block_root.getroot():
            self.categoriesXML.append( block )
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
        for component in self.components.keys():
            for i in range( 1, self.components[component] + 1 ):
                # The blocks for just this component will be called localBlocks
                localBlocks = {}
                jsonElem = copy.deepcopy(self.blocks[component])
                for block in jsonElem:
                    block["id"] = "_" + component.lower() + str(i) + "_" + block["id"]
                    localBlocks[ block["id"] ] = block
                self.blockCategories[ component + " " + str(i) ] = localBlocks
                
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="IDEGenerator.py creates a Blockly IDE for Gadgetron. It uses Jinja to create the IDE")
    parser.add_argument("-j", "--json", required=True)
    parser.add_argument("-c", "--catalog", required=True)
    parser.add_argument("-g", "--gspec", required=True)
    args = parser.parse_args()
    generator = IDEGenerator()
    generator.loadBlockDefinitions( args.json )
    generator.loadGspec( args.gspec, args.catalog )
    generator.createBlockSubset()
    for key in generator.blockCategories.keys():
        print key, json.dumps(generator.blockCategories[key], indent=4)