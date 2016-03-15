import subprocess
import wsgiref.simple_server
import webapp2
import os
from JinjaUtil import *
from BlocksToCpp import blocklyTranslator as Translator
from InoGenerator.InoGenerator import ClassGenerator as InoGenerator
import xml.etree.ElementTree as ET
from StringIO import StringIO

program_name = "testfile"
compiled_name = "COMPILEDPROG"
out_file = program_name + ".cpp"
PROGRAM_PATH = "programs/"
api_gspec = "HotlineBling.api.gspec"
STATIC = "static/"

api = ET.parse(api_gspec).getroot()
generator = InoGenerator(api)

############################# Helper Functions ############################# 

def setupOutput( name="testfile", ext="cpp"):
    global program_name
    program_name = name 
    global out_file
    out_file = program_name + "." + ext 

############################# Request Handlers ############################# 

class LandingHandler(webapp2.RequestHandler):
    def get(self):
        path = PROGRAM_PATH
	progs = [ f for f in os.listdir(path) if os.path.isfile(path+f)]
        progs = [ f.replace(".xml", "") for f in progs] 
        jinja_vars = { "programs" : progs, "name" : generator.name }
	html = render_template( "landing.jinja", jinja_vars )
	self.response.write(html)

class NewProgramHandler(webapp2.RequestHandler):
    def post(self):
        request = dict(self.request.POST)
	print request["name"].encode('ascii', 'ignore')
	self.response.write("1")

class ProgramHandler(webapp2.RequestHandler):
    def get(self, prog_name):
	global program_name
	program_name = prog_name
        xml_file = PROGRAM_PATH + prog_name + ".xml"
        if not os.path.exists( xml_file):
	    xml_file = "CppDefault.xml" 
	workspace = render_workspace( xml_file, "index.jinja" )
        self.response.write( workspace ) 
	
class StaticFileHandler(webapp2.RequestHandler):
    def get(self, file_name):
        self.response.write( openStaticFile( file_name) )

class SaveHandler(webapp2.RequestHandler):
    def saveProgram(self):
        request = dict(self.request.POST)
	self.xml = request["xml"]
        xml_file_path = PROGRAM_PATH + program_name + ".xml"
	xml_file = open(xml_file_path, "w")
	xml_file.write(self.xml)
	xml_file.close()
	
class CompileHandler(SaveHandler):
    def translateRequest(self):
        self.saveProgram()
	self.compiled = Translator.run( StringIO(self.xml) )
    def writeToOutfile( self ):
        f = open(out_file, "w")
        f.write(self.compiled)

class CompileCPPHandler(CompileHandler):
    def post(self):
        self.translateRequest()
	self.writeToOutfile()
	subprocess.check_call(["g++", "-o",  compiled_name, out_file])
	proc = subprocess.Popen([ "./"+compiled_name], shell=True, stdout=subprocess.PIPE)
	self.response.write( proc.stdout.read() )

class CompileInoHandler(CompileHandler):
    def post(self):
        self.translateRequest()
	generator.appendToLoop( Translator.getLoop() )
	self.compiled = generator.getClass()
	self.writeToOutfile()
	print self.compiled
	self.response.write(self.compiled)

######################## Static Handler Functions  ######################## 

def openStaticFile( fn ): return open(STATIC+fn).read()

def createStaticHandler( static_file ):
    class Handler(webapp2.RequestHandler):
        def get(self):
	    static_str = openStaticFile( static_file )
	    self.response.write( static_str )
    return Handler


