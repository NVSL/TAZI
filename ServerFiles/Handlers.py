import subprocess
import wsgiref.simple_server
import webapp2
import os
import __main__
from BlockGenerator.JinjaUtil import *
from ProgramManager import *
from InoComposer.InoComposer import *
import xml.etree.ElementTree as ET
from StringIO import StringIO

slashes = os.path 
block_generator = "BlockGenerator"
compiled_name = "blockly_executable"
out_file = compiled_name + ".ino"
program_path = slashes.join( "programs") 
static_file_dir = os.path.join( "WebStatic" )
api_gspec = slashes.join(block_generator, "Gspecs","Swag.api.gspec")
default_workspace = os.path.join( block_generator, "Resources" )
static_dir = "WebStatic"
landing_file = "landing.jinja"
arduPi = "arduPi/" 

program_status = ProgramManager()
api = ET.parse(api_gspec).getroot()

# Jinja Variables
global_jinja_vars = { "resDir" : "/static/", } 
global_jinja_vars["lib"] = global_jinja_vars["resDir"] + "lib/"  
global_jinja_vars["blockly"] = global_jinja_vars["resDir"] + "lib/blockly/"  
templates_dir = slashes.join( static_dir, "jinja_templates")

run_as_arduino = True 
arduino_flags = "--upload"
arduino_args = ["cmd", "/C" "arduino.exe"] if os.name == "nt" else ["arduino"]

############################# Helper Functions ############################# 

def setupOutput( name="testfile", ext="ino", workspace="CppDefault.xml"):
    global out_file
    out_file = name 
    if run_as_arduino: 
        out_file = ("\\" if os.name =="nt" else "/").join( [ program_path, out_file, out_file ] )
    out_file += "." + "ino" 
    global default_workspace
    default_workspace = os.path.join(default_workspace, workspace)

############################# Request Handlers ############################# 

class LandingHandler(webapp2.RequestHandler):
    def get(self):
        path = program_path
        progs = [ f for f in os.listdir(path) if os.path.isfile(path+f)]
        progs = [ f.replace(".xml", "") for f in progs] 
        jinja_vars = { "programs" : progs,
                       "name" : resolve_robot_name(api),
                       "loadedProgram" : program_status.name,
                       "programStatus" : program_status.status,
                       "lib" : "static/"
                       }
        jinja_vars.update(global_jinja_vars)
        template = get_jina_env().get_template(landing_file)
        html = template.render(jinja_vars).encode('ascii', 'ignore')
        self.response.write(html)

class NewProgramHandler(webapp2.RequestHandler):
    def post(self):
        request = dict(self.request.POST)
        self.response.write("1")

class ProgramHandler(webapp2.RequestHandler):
    def get(self, prog_name):
        # We only want to save the program
        # Return if we're trying to access anything else
        if len(prog_name.split("/")) > 1: return
        global program_status
        program_status = ProgramManager( name=prog_name, program="./"+compiled_name )
        xml_file = program_path + prog_name + ".xml"
        if not os.path.exists( xml_file): xml_file = default_workspace
        file_path =  "ide.jinja"
        env = get_jina_env()
        workspace = render_workspace( xml_file, file_path, additional_args=global_jinja_vars, jinja_env=env )
        self.response.write( workspace ) 
        
class StaticFileHandler(webapp2.RequestHandler):
    def get(self, file_name):
        self.response.write( openStaticFile( file_name) )

class RunProgramHandler(webapp2.RequestHandler):
    def post(self): 
        if not run_as_arduino: program_status.run()
class KillProgramHandler(webapp2.RequestHandler):
    def post(self): 
        if not run_as_arduino: program_status.kill()

class SaveHandler(webapp2.RequestHandler):
    result_cached = False
    cached_xml = ""
    def post(self):
        self.saveProgram()
    def __init__( self, *args, **kwargs):
        webapp2.RequestHandler.__init__( self, *args, **kwargs)
    def saveProgram(self):
        request = dict(self.request.POST)
        xml = request["xml"]
        if xml != SaveHandler.cached_xml or run_as_arduino:
            self.xml = xml
            SaveHandler.result_cached = False
            xml_file_path = program_path + program_status.name + ".xml"
            xml_file = open(xml_file_path, "w")
            xml_file.write(self.xml)
            xml_file.close()
        else: SaveHandler.result_cached = True
        SaveHandler.cached_xml = self.xml = xml
        
class CompileHandler(SaveHandler):
    def translateRequest(self):
        self.saveProgram()
        self.composer = InoComposer( api, self.xml)
    def writeToOutfile( self ):
        print out_file
        f = open(out_file, "w+")
        f.write(self.compiled)

class CompileCPPHandler(CompileHandler):
    def post(self):
        self.translateRequest()
        self.compiled = self.composer.get_cpp()
        self.writeToOutfile()
        subprocess.check_call(["g++", "-o",  compiled_name, out_file])
        program_status.run()
        self.response.write( "Running program!" )
        #self.response.write( program_status.read_stdout() )

class CompileInoHandler(CompileHandler):
    def post(self):
        self.translateRequest()
        if not SaveHandler.result_cached: self.compile()
        program_status.run()
        self.response.write( "Running program!" )
    def compile(self):
        print "I'm really compiling!"
        self.compiled = self.composer.get_ino()
        print self.compiled
        self.writeToOutfile()
        abs_path = os.path.abspath(out_file)
        if run_as_arduino:
            flags = [ arduino_flags , abs_path]
            subprocess.call(arduino_args + flags, shell=True)
        else:
            subprocess.check_call(["mv",abs_path, arduPi])
            subprocess.check_call(["make","-C", arduPi])

######################## Static Handler Functions  ######################## 

def openStaticFile( fn ): return open(slashes.join(static_file_dir,fn)).read()

def createStaticHandler( static_file ):
    class Handler(webapp2.RequestHandler):
        def get(self):
            static_str = openStaticFile( static_file )
            self.response.write( static_str )
    return Handler

def get_jina_env():
    # Get the exact directory where we'll be working
    dirr = os.path.join(os.path.dirname(__main__.__file__), templates_dir )
    JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(dirr))
    return JINJA_ENVIRONMENT
