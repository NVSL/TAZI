import wsgiref.simple_server
import webapp2
import os
from lxml import etree as ET

INDEX = "static/index.html"
STATIC = "static/"
BLOCKLY_C = "blockly_compressed.js"
BLOCKS = "blocks_compressed.js"
CUSTOM_BLOCKS = "custom_blocks.js"
MSGJS = "msg/js/en.js"
BLOCKSIO = "BlocksIO.js"
GTRON_IMAGE = "GtronImage.png"

def openStaticFile( fn ): return open(STATIC+fn).read()

def createHandler( static_file ):
    class Handler(webapp2.RequestHandler):
        def get(self):
	    static_str = openStaticFile( static_file )
	    self.response.write( static_str )
    return Handler

def create_path_pair( static_file ): 
    return ( "/" + static_file, createHandler( static_file ) )

class IDERequestHandler(webapp2.RequestHandler):
    def get(self):
        index = open(INDEX).read()
        self.response.write(index)

app = webapp2.WSGIApplication([
    ("/", IDERequestHandler),
    create_path_pair(MSGJS),
    create_path_pair(BLOCKS),
    create_path_pair(BLOCKSIO),
    create_path_pair(BLOCKLY_C),
    create_path_pair(GTRON_IMAGE),
    create_path_pair(CUSTOM_BLOCKS),
], debug=True)

def main ():
    port = 80
    httpd = wsgiref.simple_server.make_server('', port, app)
    print "Serving HTTP on port "+str(port)+"..."
    httpd.serve_forever()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="From a gspec and a component library, compiles a schematic and semi-placed board.")
    parser.add_argument("-s", metavar="static_files", type=str, nargs="*", default=["static_files.xml"], help="the complete list of static files that will be served by the server")
    args = parser.parse_args()
    main()
