import sys
import asciitree
import clang.cindex
import platform
class Function(object):
    def __init__(self, cursor):
        self.name = cursor.spelling
        self.params = []
        self.get_params(cursor)
	self.returnType = cursor.type.spelling.split(' ')[0]

    def __str__(self):
        return self.returnType + " " + self.name + str(self.params)

    def get_params(self, cursor):
        i = 0
        for node in cursor.get_children():
	    if( node.spelling != None ):
	        currentParam = [node.spelling, node.type.spelling]
	        self.params.append(currentParam) 
        for t in cursor.type.argument_types():
	    #print t.spelling()
            canonical = t.get_canonical()
	    #print canonical
            # print 'Parameter type: ' + canonical.kind.name
            type_kind_name = canonical.kind.name

            if canonical.kind == clang.cindex.TypeKind.POINTER:
                pointee = canonical.get_pointee()
                type_displayname = pointee.get_declaration().displayname
                # print pointee.get_declaration().displayname

            elif canonical.kind == clang.cindex.TypeKind.RECORD:
                # print canonical.get_declaration().displayname
                type_displayname = canonical.get_declaration().displayname
                
            else:
                # print canonical.kind.spelling
                type_displayname = canonical.kind.spelling

            #self.params[i].append( type_displayname )
	    #i = i + 1

class Class(object):
    def __init__(self, cursor):
        self.name = cursor.spelling
        self.functions = []

        for c in cursor.get_children():
            if (c.kind == clang.cindex.CursorKind.CXX_METHOD and
                c.access_specifier == clang.cindex.AccessSpecifier.PUBLIC):
                f = Function(c)
                self.functions.append(f)
def build_classes(cursor, file_name):
    """
    This function must be called first since it sets the global variable FILE_NAME.
    This is ugly but I haven't figured out a way to make it nicer.
    :param cursor: The cursor object
    :param file_name: The path to the source file being parsed
    :return: A list of Class objects
    """

    #print "Building classes"

    global FILE_NAME
    FILE_NAME = file_name
    result = []

    for c in cursor.get_children():
	#print c
        #print "file name = " + c.location.file.name
        if (c.kind == clang.cindex.CursorKind.CLASS_DECL and
            c.location.file.name == FILE_NAME):
            a_class = Class(c)
            result.append(a_class)
    return result

if __name__ == "__main__":
    clang.cindex.Config.set_library_path('/usr/lib/x86_64-linux-gnu')
    if(platform.platform().split('-')[0].lower() == "darwin"):
        clang.cindex.Config.set_library_path('/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib')
    index = clang.cindex.Index.create()
    translation_unit = index.parse(sys.argv[1], ['-x', 'c++', '-std=c++11', '-D__CODE_GENERATOR__'])
    classes = build_classes(translation_unit.cursor, sys.argv[1])
    for aClass in classes:
        print 'For class ' + aClass.name + ', public methods:'
        for aFunction in aClass.functions:
            print aFunction
    exit()
