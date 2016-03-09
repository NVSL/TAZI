import wsgiref.simple_server
import webapp2
import StaticHandler

INDEX = "static/index.html"

# Real Request Handlers
class IDERequestHandler(webapp2.RequestHandler):
    def get(self):
        index = open(INDEX).read()
        self.response.write(index)

class TestRequestHandler(webapp2.RequestHandler):
    def post(self):
        request = dict(self.request.POST)
        print "I got a test request!"
	print request
	self.response.write("hi")
class AspTestHandler(webapp2.RequestHandler):
    def post(self):
        request = dict(self.request.POST)
        print "I got an asp test request!"
	print request

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
	("/swag", TestRequestHandler),
	("/demo_test.asp", AspTestHandler),
	] + [ StaticHandler.create_path_pair(f) for f in files ]  , debug=True)
    main(app)
