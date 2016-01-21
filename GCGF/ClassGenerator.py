import xml.etree.ElementTree as ETree
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
    def getConstants(self):
        retStrings = []
	for obj in self.objects:
	    for arg in obj.args:
	        currStr = "#define " + arg.name + " " + str(arg.value)
	        retStrings.append(currStr)
	return retStrings
    def getObjects(self):
        retStrings = []
	countMap = {}
	for obj in self.objects:
	    countMap[ obj.objType ] = 1
	for obj in self.objects:
	    argC = 0
	    currStr = obj.objType + " " + str.lower( obj.objType )
	    currStr = currStr + str( countMap[ obj.objType ] ) + "("
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
    strings = generator.getObjects()
    for string in strings:
        print string
