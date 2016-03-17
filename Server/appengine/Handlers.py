import subprocess
import wsgiref.simple_server
import webapp2
import os
from JinjaUtil import *
from ProgramStatus import *
from BlocksToCpp import blocklyTranslator as Translator
from InoGenerator.InoGenerator import ClassGenerator as InoGenerator
import xml.etree.ElementTree as ET
from StringIO import StringIO

compiled_name = "program"
out_file = compiled_name + ".cpp"
PROGRAM_PATH = "programs/"
api_gspec = "SimpleLEDTest.api.gspec"
STATIC = "static/"
program_status = ProgramStatus()

default_workspace = ""
api = ET.parse(api_gspec).getroot()
generator = InoGenerator(api)

global_jinja_vars = { "resDir" : "/static/", } 
global_jinja_vars["lib"] = global_jinja_vars["resDir"] + "lib/"  
global_jinja_vars["blockly"] = global_jinja_vars["resDir"] + "lib/blockly/"  
templates_dir = "jinja_templates/"

############################# Helper Functions ############################# 

def setupOutput( name="testfile", ext="cpp", workspace="CppDefault.xml"):
    global out_file
    out_file = compiled_name + "." + ext 
    global default_workspace
    default_workspace = workspace

############################# Request Handlers ############################# 

class LandingHandler(webapp2.RequestHandler):
    def get(self):
        path = PROGRAM_PATH
	progs = [ f for f in os.listdir(path) if os.path.isfile(path+f)]
        progs = [ f.replace(".xml", "") for f in progs] 
        jinja_vars = { "programs" : progs, "name" : generator.name }
	file_path = templates_dir + "landing.jinja"
	html = render_template( file_path, jinja_vars, additional_args=global_jinja_vars )
	self.response.write(html)

class NewProgramHandler(webapp2.RequestHandler):
    def post(self):
        request = dict(self.request.POST)
	print request["name"].encode('ascii', 'ignore')
	self.response.write("1")

class ProgramHandler(webapp2.RequestHandler):
    def get(self, prog_name):
	global program_status
	program_status = ProgramStatus( name=prog_name, program="./"+compiled_name )
        xml_file = PROGRAM_PATH + prog_name + ".xml"
        if not os.path.exists( xml_file):
	    xml_file = default_workspace
	file_path = templates_dir + "ide.jinja"
	workspace = render_workspace( xml_file, file_path, additional_args=global_jinja_vars )
        self.response.write( workspace ) 
	
class StaticFileHandler(webapp2.RequestHandler):
    def get(self, file_name):
        self.response.write( openStaticFile( file_name) )

class KillProgramHandler(webapp2.RequestHandler):
    def post(self): program_status.kill()

class SaveHandler(webapp2.RequestHandler):
    def saveProgram(self):
        request = dict(self.request.POST)
	self.xml = request["xml"]
        xml_file_path = PROGRAM_PATH + program_status.name + ".xml"
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
	program_status.run()
	#self.response.write( program_status.read_stdout() )

class CompileInoHandler(CompileHandler):
    def post(self):
        self.translateRequest()
        generator = InoGenerator(api)
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


