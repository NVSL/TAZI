import xml.etree.ElementTree as ET
import webapp2
import os
STATIC = "static/"
custom_routes = {}

# Auto Generated Static Request Handlers
def openStaticFile( fn ): return open(STATIC+fn).read()

def createHandler( static_file ):
    class Handler(webapp2.RequestHandler):
        def get(self):
	    static_str = openStaticFile( static_file )
	    self.response.write( static_str )
    return Handler

def create_path_pair( static_file ): 
    route = "/" + static_file
    if static_file in custom_routes: route = "/" + custom_routes[ static_file ]
    return ( route, createHandler( static_file ) )

def parseStaticFiles( xml_file ):
    root = ET.parse(xml_file).getroot()
    static_dir = root.attrib["dir"]
    #files = [f.attrib["path"] for f in root ]
    files = []
    for f in root:
        files.append( f.attrib["path"])
	if "route" in f.attrib: 
	    custom_routes[ f.attrib["path"] ] = f.attrib["route"]
    return (static_dir, files)
    

