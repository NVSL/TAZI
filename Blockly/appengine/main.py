import wsgiref.simple_server
import webapp2
import os

INDEX = "static/index.html"
STATIC = "static/"
BLOCKLY_C = "blockly_compressed.js"
BLOCKS = "blocks_compressed.js"
CUSTOM_BLOCKS = "custom_blocks.js"
MSGJS = "msg/js/en.js"
BLOCKSIO = "BlocksIO.js"
GTRON_IMAGE = "GtronImage.png"

def openStaticFile( fn ): return open(STATIC+fn).read()

class IDERequestHandler(webapp2.RequestHandler):
    def get(self):
        index = open(INDEX).read()
        self.response.write(index)
class BlocklyCompJSHandler(webapp2.RequestHandler):
    def get(self):
        index = openStaticFile( BLOCKLY_C )
        self.response.write(index)

class BlocksCompJSHandler(webapp2.RequestHandler):
    def get(self):
        index = openStaticFile( BLOCKS )
        self.response.write(index)

class CustomBlocksHandler(webapp2.RequestHandler):
    def get(self):
        index = openStaticFile( CUSTOM_BLOCKS )
        self.response.write(index)

class MsgHandler(webapp2.RequestHandler):
    def get(self):
        index = openStaticFile( MSGJS )
        self.response.write(index)

class BlocksIO(webapp2.RequestHandler):
    def get(self):
        index = openStaticFile( BLOCKSIO )
        self.response.write(index)

class GtronImage(webapp2.RequestHandler):
    def get(self):
        index = openStaticFile( GTRON_IMAGE )
        self.response.write(index)



app = webapp2.WSGIApplication([
    ("/", IDERequestHandler),
    ("/"+MSGJS, MsgHandler),
    ("/"+BLOCKS, BlocksCompJSHandler),
    ("/"+BLOCKSIO, BlocksIO),
    ("/"+BLOCKLY_C, BlocklyCompJSHandler),
    ("/"+GTRON_IMAGE, GtronImage),
    ("/"+CUSTOM_BLOCKS, CustomBlocksHandler),
], debug=True)

def main ():
    port = 80
    httpd = wsgiref.simple_server.make_server('', port, app)
    print "Serving HTTP on port "+str(port)+"..."
    httpd.serve_forever()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--html" )
    args = parser.parse_args()
    if args.html is not None: INDEX = args.html
    main()
