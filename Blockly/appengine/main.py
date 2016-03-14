import wsgiref.simple_server
import webapp2
import StaticHandler
import subprocess
from StringIO import StringIO
from BlocksToCpp.blocklyTranslator import run as compile
from BlocksToCpp.blocklyTranslator import getLoop as getLoop
from InoGenerator import ClassGenerator as InoGenerator
import xml.etree.ElementTree as ET

INDEX = "static/index.html"
api_gspec = "HotlineBling.api.gspec"
#out_file = "HotlineBling/HotlineBling.ino"
program_name = "testfile"
out_file = program_name + ".cpp"
STATIC = StaticHandler.STATIC

def compileRequest( request, DebugMessage="I got a compile request!" ):
    print DebugMessage
    xml = request["xml"]
    return compile(StringIO(xml))
def writeToOutfile( contents ):
    f = open(out_file, "w")
    f.write(contents)
# Real Request Handlers
class NewProgramHandler(webapp2.RequestHandler):
    def post(self):
        request = dict(self.request.POST)
	print request["name"].encode('ascii', 'ignore')
	self.response.write("1")
	
class StaticFileHandler(webapp2.RequestHandler):
    def get(self, file_name):
        self.response.write( StaticHandler.openStaticFile( file_name) )

class CompileCPPHandler(webapp2.RequestHandler):
    def post(self):
        request = dict(self.request.POST)
	cpp = compileRequest( request, DebugMessage="I got a compile request!" )
	writeToOutfile( cpp )
	subprocess.check_call(["g++", "-o",  program_name, out_file])
	proc = subprocess.Popen([ "./"+program_name], shell=True, stdout=subprocess.PIPE)
	self.response.write( proc.stdout.read() )
class CompileRequestHandler(webapp2.RequestHandler):
    def post(self):
        request = dict(self.request.POST)
	compileRequest( request )
	api = ET.parse(api_gspec).getroot()
	generator = InoGenerator(api)
	generator.appendToLoop( getLoop() )
	cpp = generator.getClass()
	writeToOutfile( cpp )
	print cpp
	self.response.write(cpp)

def removeNSHack( xml ):
    xIdx = xCnt = qIdx = qCnt = i = 0
    for c in xml:
        if c == "x": xCnt += 1
        if c == '"': qCnt += 1
	if c == "x" and xCnt == 2: xIdx = i 
	if c == '"' and qCnt == 2: qIdx = i 
	if qCnt >= 2 and xCnt >= 2: return xml[:xIdx] + xml[qIdx+1:]
	#print c, xCnt, qCnt, i
	i += 1

def main (app):
    port = 8080
    httpd = wsgiref.simple_server.make_server('', port, app)
    print "Serving HTTP on port "+str(port)+"..."
    httpd.serve_forever()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="From a gspec and a component library, compiles a schematic and semi-placed board.")
    parser.add_argument("-s", "--static_files", type=str, nargs="*", default="static_files.xml", help="the complete list of static files that will be served by the server")
    args = parser.parse_args()
    STATIC, files = StaticHandler.parseStaticFiles( args.static_files )
    app = webapp2.WSGIApplication([ 
	("/compile", CompileCPPHandler),
	("/newprogram", NewProgramHandler),
	("/", StaticHandler.createHandler("landing.html")),
	("/ide", StaticHandler.createHandler("index.html")),
	(r'/static/(.+)', StaticFileHandler),
	]    , debug=True)
    main(app)
