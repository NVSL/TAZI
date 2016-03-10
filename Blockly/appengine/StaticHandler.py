from lxml import etree as ET
import webapp2
import os
STATIC = "static/"

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
    

