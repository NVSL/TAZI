import wsgiref.simple_server
import webapp2
import os

INDEX = "../Blockly/index.html"

class IDERequestHandler(webapp2.RequestHandler):
    def get(self):
        index = open(INDEX).read()
        self.response.write(index)
app = webapp2.WSGIApplication([
    ("/", IDERequestHandler),
], debug=True)

def main ():
    port = 8081
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
