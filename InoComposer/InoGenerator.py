__author__ = "Michael Gonzalez"
__email__ = "mmg005@eng.ucsd.edu"

import xml.etree.ElementTree as ETree
import functools
import jinja2
import os
from InoCommenter import *
class ClassGenerator:
    libraries = []
    gadgetron_components = []
    loopBody = []
    name = "" 
    funcs = ""
    functionDeclarations = ""
 
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader( os.path.dirname( __file__ ) ))
    jinja_env.line_comment_prefix = "#//"
    jinja_env.line_statement_prefix = "%"
    variableDeclarations = ""
    jinja_file = "ino_template.jinja.ino"

    def declare_objects(self, objs):
        self.gadgetron_components = objs

    def __init__( self, api, include_str="<>"):
        self.gadgetron_components = []
        self.objInstances = []
        self.setupBody = []
        self.variableDeclarations = []
        self.functionDeclarations = []
        self.loopBody = []
        self.find_name(api)
        self.include_str = include_str

    def appendToSetup(self, lines):
        self.setupBody += lines

    def appendToLoop(self, lines):
        self.loopBody += lines

    def define_functions(self, funcs):
        self.function_definitions = funcs 

    def declare_functions(self, funcs):
        self.functionDeclarations = funcs

    def declare_variables(self, vars):
        self.variableDeclarations = vars 


    def find_name(self, root):
        for component in root:
            if component.tag == "name": self.name = component.text

    def getClass(self):
        jinja_vars = {
            "gadgetron_objs"        : self.gadgetron_components,
            "variable_declarations" : self.variableDeclarations,
            "function_declarations" : self.functionDeclarations,
            "function_definitions"  : self.function_definitions,
            "setup_body"            : self.setupBody,
            "loop_body"             : self.loopBody,
            "name"                  : self.name,
            "custom_header_file"    : self.name.replace(" ", "-") + '.h',
            "header" : createRobotHeader( self.name ),
        }

        template = self.jinja_env.get_template(self.jinja_file)
        code = template.render( jinja_vars )
        return code

if __name__ == "__main__":
    import argparse
    argparser = argparse.ArgumentParser("stuff")
    argparser.add_argument("-g", "--gspec", required=True)
    args = argparser.parse_args()
    api = ETree.parse(args.gspec).getroot()
    generator = ClassGenerator(api)
    generator.getClass()

    
