import json
from GspecParser import GspecParser
import os
from StringIO import StringIO



class IDEGenerator:
    def __init__(self):
        self.components = None
    def loadBlockDefinitions( self, blockJson ):
        # Type checking
        if type (blockJson) == str:
            stream = None
            # Is it a file?
            if os.path.isfile( blockJson):
                stream = open(blockJson)
            else:
                stream = StringIO( blockJson )
            self.blocks = json.load(stream)
        # For some reason, it seems like json objects get passed as lists
        elif type (blockJson) == list:
            self.blocks = blockJson
        else:
            print "Unknown type: ", type(blockJson)
            raise "Unknown type passed to loadBlockDefinitions"

    def loadGspec( self, gspec, catalog ):
        gspecParser = GspecParser()
        gspecParser.setCatalog(catalog)
        self.components = gspecParser.getComps(gspec)
    def createBlockSubset(self):
        for component in self.components.keys():
            for i in range( 0, self.components[component] ):
                jsonElem = self.blocks[component]
                print json.dumps( jsonElem, indent=4)
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