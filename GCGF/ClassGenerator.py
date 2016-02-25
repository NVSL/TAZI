__author__ = "Michael Gonzalez"
__email__ = "mmg005@eng.ucsd.edu"

import xml.etree.ElementTree as ETree
import functools
class Arg:
    def __init__(self, value, name):
        self.value = value
	self.name = name
class CObj:
    def __init__(self, objType):
        self.objType = objType
    def setArgs(self, args):
        self.args = args
class ClassGenerator:
    objects = []
    libraries = []
    objInstances = []

    def getSetupFunction(self):
        def concatLines(acc, line): return acc + "   " + line + ".setup();\n"
	return functools.reduce( concatLines, self.objInstances, "void setup() {\n" ) + "}"
    def getLibraries(self):
        def concatLib( acc, elem): return acc + '#include "' + elem + '"\n'
	return functools.reduce( concatLib, set(self.libraries), "" )
    def getConstants(self):
        retStrings = []
	for obj in self.objects:
	    for arg in obj.args:
	        currStr = "#define " + arg.name + " " + str(arg.value)
	        retStrings.append(currStr)
	return retStrings
    def getObjectDeclarations(self):
        retStrings = []
	countMap = {}
	for obj in self.objects:
	    countMap[ obj.objType ] = 1
	for obj in self.objects:
	    argC = 0
	    instanceName = str.lower(obj.objType) + str(countMap[ obj.objType ])
	    self.objInstances.append(instanceName)
	    currStr = obj.objType + " " + instanceName + "("
	    for arg in obj.args :
		if argC is not 0:
		    currStr = currStr + ", "
	        currStr = currStr + str( arg.name )
		argC = argC + 1
	    currStr = currStr + ");"
	    retStrings.append(currStr)
        return retStrings
    def parseApiGspec(self, root):
        for component in root:
	    if component.tag != "component":
	        continue
	    for node in component:
	        if node.tag != "api":
		    continue
                currentObj = CObj( node.attrib["class"] )
	        args = []
	        for arg in node:
	            currentArg = Arg( arg.attrib["digitalliteral"], arg.attrib["arg"] )
		    args.append( currentArg )
	        currentObj.setArgs( args )
	        self.objects.append( currentObj )
	        self.libraries.append( node.attrib["include"])


if __name__ == "__main__":
    import argparse
    argparser = argparse.ArgumentParser("stuff")
    argparser.add_argument("-g", "--gspec", required=True)
    args = argparser.parse_args()
    api = ETree.parse(args.gspec).getroot()
    generator = ClassGenerator()
    generator.parseApiGspec(api)
    print generator.getLibraries()
    for string in generator.getConstants():
        print string
    for string in generator.getObjectDeclarations():
        print string
    print generator.getSetupFunction()
