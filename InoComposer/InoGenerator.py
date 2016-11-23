__author__ = "Michael Gonzalez"
__email__ = "mmg005@eng.ucsd.edu"

import xml.etree.ElementTree as ETree
import functools
from InoCommenter import *
class ClassGenerator:
    libraries = []
    objects = []
    loopBody = []
    name = "" 
    funcs = ""
    functionDeclarations = ""
    variableDeclarations = ""

    def declare_objects(self, objs):
        self.objects = objs

    def __init__( self, api, include_str="<>"):
        self.objects = []
        self.objInstances = []
        self.setupBody = []
        self.loopBody = []
        self.find_name(api)
        self.include_str = include_str

    def getSetupFunction(self):
        setup_str = "void setup() {\n" 
        tail_str = ".setup();\n"
        def concatLines(acc, line): return acc + "   " + line + tail_str
        setup_str += functools.reduce( concatLines, self.objects, "" ) 
        tail_str = "\n"
        setup_str += functools.reduce( concatLines, self.setupBody, "")  
        return setup_str + "}" 

    def getLoopFunction(self):
        def concatLines(acc, line): return acc + "   " + line + "\n"
        return functools.reduce( concatLines, self.loopBody, "void loop() {\n" ) + "}"

    def getLibraries(self):
        l = self.include_str[0]
        r = self.include_str[1]
        def concatLib( acc, elem): return acc + '#include "' + elem + '"\n'
        return functools.reduce( concatLib, set(self.libraries), "" )

    def appendToSetup(self, lines):
        self.setupBody += lines

    def appendToLoop(self, lines):
        self.loopBody += lines

    def define_functions(self, funcs):
        for f in funcs: self.funcs += f + "\n"

    def declare_functions(self, funcs):
        for f in funcs: self.functionDeclarations += f + "\n"

    def declare_variables(self, vars):
        for v in vars: self.variableDeclarations += v + "\n"


    def find_name(self, root):
        for component in root:
            if component.tag == "name": self.name = component.text
    """
    TODO: Make this into a jinjna file"
    """
    def getClass(self):
        rv = createRobotHeader( self.name )
        rv += nl * 2
        self.libraries = [self.name.replace(" ", "-") + '.h']
        rv += a(createSectionHeader("Libraries"))
        rv += a(self.getLibraries())
        if self.variableDeclarations != "":
            rv += a(createSectionHeader("User VariableDeclarations"))
            rv += self.variableDeclarations
        if self.funcs != "":
            rv += a(createSectionHeader("User Functions Declarations"))
            rv += self.functionDeclarations
            rv += a(createSectionHeader("User Functions Definitions"))
            rv += self.funcs
        rv += a(createSectionHeader("Setup Function", description="The setup() function runs --ONCE-- when the Arduino boots up. As the name implies, it's useful to add code that 'sets up' your Gadget to run correctly."))
        rv += a(self.getSetupFunction())
        rv += a(createSectionHeader("Loop Function", description="The loop() function runs continuously after the setup() function finishes and while the Arduino is running. In other words, this function is called repeatly over and over again when it reaches the end of the function. This function is where the majority of your program's logic should go."  ))
        rv += a(self.getLoopFunction())
        return rv

if __name__ == "__main__":
    import argparse
    argparser = argparse.ArgumentParser("stuff")
    argparser.add_argument("-g", "--gspec", required=True)
    args = argparser.parse_args()
    api = ETree.parse(args.gspec).getroot()
    generator = ClassGenerator(api)
    print generator.getClass()

    
