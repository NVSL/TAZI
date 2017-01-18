from BlocksToCpp.blocklyTranslator import *
from InoGenerator import *
from StringIO import StringIO
import xml.etree.ElementTree as ETree

class InoComposer:
    # An InoComposer object expects the api_gspec to be an ET element
    # It expects the xml to be a string
    def __init__(self, api_gspec, xml, program_name):
        self.gspec = api_gspec
        self.xml = xml
        self.program_name = program_name
        self.translator = BlocklyTranslator()

    # Returns the ino as a string
    def get_ino(self):
        self.get_cpp()
        generator = ClassGenerator( self.gspec )
        translator = self.translator
        setup_str = translator.get_setup()
        loop_str = self.translator.get_loop() 
        generator.define_functions(  translator.get_func_defs() )
        generator.declare_functions( translator.get_func_decs() )
        generator.declare_variables( translator.get_variables() )
        generator.declare_objects( [ v for v in translator.declaredObjs ])
        generator.appendToSetup( setup_str ) 
        generator.appendToLoop( loop_str ) 
        ino = generator.getClass() + "\n"
        return ino
    # Returns the translated cpp as a string
    def get_cpp(self):
        self.translator.program_name = self.program_name.replace(" ", "_")
        return self.translator.run( StringIO(self.xml) )

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
    composer = InoComposer(api_gspec, xml, "foobar")
    # Print the string representation of the ino
    print composer.get_ino()
    #composer.get_ino()
    #print
