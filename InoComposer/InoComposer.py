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
	self.get_cpp()
        generator = ClassGenerator( self.gspec )
	loop_str = Translator.getLoop() 
	generator.appendToLoop( loop_str ) 
	generator.defineFunctions( Translator.getFuncDefs() )
	generator.declareFunctions( Translator.getFuncDecs() )
        ino = generator.getClass() + "\n"
	return ino
    # Returns the translated cpp as a string
    def get_cpp(self):
        return Translator.run( StringIO(self.xml) )

def resolve_robot_name( gspec ):
    generator = ClassGenerator( gspec )
    return generator.name

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
    print
    my_vars = Translator.getVars()
    print type(my_vars), my_vars
