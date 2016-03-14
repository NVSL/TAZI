import subprocess
import wsgiref.simple_server
import webapp2
from BlocksToCpp import blocklyTranslator as Translator
from InoGenerator.InoGenerator import ClassGenerator as InoGenerator
import xml.etree.ElementTree as ET
from StringIO import StringIO

program_name = "testfile"
out_file = program_name + ".cpp"
api_gspec = "HotlineBling.api.gspec"
STATIC = "static/"

############################# Helper Functions ############################# 

def setupOutput( name="testfile", ext="cpp"):
    global program_name
    program_name = name 
    global out_file
    out_file = program_name + "." + ext 

############################# Request Handlers ############################# 

class NewProgramHandler(webapp2.RequestHandler):
    def post(self):
        request = dict(self.request.POST)
	print request["name"].encode('ascii', 'ignore')
	self.response.write("1")
	
class StaticFileHandler(webapp2.RequestHandler):
    def get(self, file_name):
        self.response.write( openStaticFile( file_name) )

class CompileHandler(webapp2.RequestHandler):
    def translateRequest(self):
        request = dict(self.request.POST)
	xml = request["xml"]
	self.compiled = Translator.run( StringIO(xml) )
    def writeToOutfile( self ):
        f = open(out_file, "w")
        f.write(self.compiled)

class CompileCPPHandler(CompileHandler):
    def post(self):
        self.translateRequest()
	self.writeToOutfile()
	subprocess.check_call(["g++", "-o",  program_name, out_file])
	proc = subprocess.Popen([ "./"+program_name], shell=True, stdout=subprocess.PIPE)
	self.response.write( proc.stdout.read() )

class CompileInoHandler(CompileHandler):
    def post(self):
        self.translateRequest()
	api = ET.parse(api_gspec).getroot()
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


