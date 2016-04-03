from BlocksToCpp import blocklyTranslator as Translator
from InoGenerator.InoGenerator import *
from StringIO import StringIO
import xml.etree.ElementTree as ETree

class InoComposer:
    # An InoComposer object expects the api_gspec to be an ET element
    # It expects the xml to be a string
    def __init__(self, api_gspec, xml):
        self.gspec = api_gspec
	self.xml = xml
    # Returns the ino as a string
    def get_ino(self):
        generator = ClassGenerator( self.gspec )
        Translator.run( StringIO(self.xml) )
	loop_str = Translator.getLoop() 
	generator.appendToLoop( loop_str ) 
        return generator.getClass()

if __name__ == "__main__":
    # Setting up argparse
    import argparse
    argparser = argparse.ArgumentParser("stuff")
    argparser.add_argument("-g", "--gspec", required=True)
    argparser.add_argument("-x", "--xml", required=True)
    args = argparser.parse_args()
    api_gspec = ETree.parse(args.gspec).getroot()
    # We need the xml as a string
    xml = open(args.xml).read()
    # Make a composer object
    composer = InoComposer(api_gspec, xml)
    # Print the string representation of the ino
    print composer.get_ino()
