import json
import GspecParser
from StringIO import StringIO



class IDEGenerator:
    def loadBlockDefinitions( self, blockJson ):
        # Type checking
        if type (blockJson) == str:
            stream = StringIO( blockJson )
            jsonObj = json.load(stream)
        # For some reason, it seems like json objects get passed as lists
        elif type (blockJson) == list:
            jsonObj = blockJson
        else:
            print "Unknown type: ", type(blockJson)
            raise "Unknown type passed to loadBlockDefinitions"


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="IDEGenerator.py creates a Blockly IDE for Gadgetron. It uses Jinja to create the IDE")
    parser.add_argument("-j", "--json", required=True)
    generator = IDEGenerator()
    stream = StringIO( '["streaming API"]' )
    jsonObj = json.load(stream)
    generator.loadBlockDefinitions( jsonObj )