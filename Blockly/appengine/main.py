import wsgiref.simple_server
import webapp2
import os
from lxml import etree as ET

INDEX = "static/index.html"
STATIC = "static/"

# Real Request Handlers
class IDERequestHandler(webapp2.RequestHandler):
    def get(self):
        index = open(INDEX).read()
        self.response.write(index)

class CompileRequestHandler(webapp2.RequestHandler):
    def post(self):
        request = dict(self.request.POST)
        print "I got a compile request!"
	print request
	self.response.write("hi")
class AspTestHandler(webapp2.RequestHandler):
    def post(self):
        request = dict(self.request.POST)
        print "I got an asp test request!"
	print request

# Auto Generated Static Request Handlers
def openStaticFile( fn ): return open(STATIC+fn).read()

def createHandler( static_file ):
    class Handler(webapp2.RequestHandler):
        def get(self):
	    static_str = openStaticFile( static_file )
	    self.response.write( static_str )
    return Handler

def create_path_pair( static_file ): 
    return ( "/" + static_file, createHandler( static_file ) )

def parseStaticFiles( xml_file ):
    root = ET.parse(xml_file).getroot()
    static_dir = root.attrib["dir"]
    files = [f.attrib["path"] for f in root ]
    return (static_dir, files)
    

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
    STATIC, files = parseStaticFiles( args.static_files )
    app = webapp2.WSGIApplication([ 
        ("/", IDERequestHandler),
	("/compile", CompileRequestHandler),
	("/demo_test.asp", AspTestHandler),
	] + [ create_path_pair(f) for f in files ]  , debug=True)
    main(app)
