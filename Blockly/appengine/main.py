import wsgiref.simple_server
import webapp2
import StaticHandler
from StringIO import StringIO
from BlocksToCpp.blocklyTranslator import run as compile
import xml.etree.ElementTree as ET

INDEX = "static/index.html"

# Real Request Handlers
class IDERequestHandler(webapp2.RequestHandler):
    def get(self):
        index = open(INDEX).read()
        self.response.write(index)

class CompileRequestHandler(webapp2.RequestHandler):
    def post(self):
        request = dict(self.request.POST)
	xml = removeNSHack(request["xml"])
        print "I got a compile request!"
	cpp = compile(StringIO(xml))
	print cpp
	#strs = (cpp[1].split("\n"))
	#print 
	#print (cpp[1]) 
	#for i in range(2, len(strs)-1): print strs[i]
	self.response.write(cpp)
class AspTestHandler(webapp2.RequestHandler):
    def post(self):
        request = dict(self.request.POST)
        print "I got an asp test request!"
	print request

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
        ("/", IDERequestHandler),
	("/compile", CompileRequestHandler),
	("/demo_test.asp", AspTestHandler),
	] + [ StaticHandler.create_path_pair(f) for f in files ]  , debug=True)
    main(app)
