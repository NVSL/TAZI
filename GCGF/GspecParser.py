import xml.etree.ElementTree as ET
import os

class GspecParser: 

   def __init__(self):
       self.catalogTree = None
   def setCatalog(self, catalog):
       if type( catalog ) is str:
           if os.path.isfile( catalog ):
               self.catalogTree = ET.parse(catalog).getroot()
           else:
               self.catalogTree = ET.fromstring( catalog ).getroot()
   def initializeList(self):
      if self.catalogTree is None:
          raise BaseException("Catalog root was never set!")
      base = self.catalogTree
      
      componentsDict = {}
      #Parsing the components file from Gadgetron
      for component in base.findall('component'):
         compStr = component.get('keyname')
         instanceName = None
         for child in component:
         # Check if the component has an API tag
            if child.tag == 'API':
	        for node in child:
		    if node.tag.lower() == 'arduino':
		        for n in node:
			    if n.tag.lower() == 'class':
	                        componentsDict[compStr] = n.attrib["name"]
	                        #print 'API FOUND FOR ABOVE ELEMENT ', n.attrib["name"]
      return componentsDict

   def getComps(self, compFile):
      componentsDict = self.initializeList()
      gspec = None
      if type( compFile) is str:
          if os.path.isfile( compFile):
              gspec = ET.parse(compFile).getroot()
          else:
              gspec = ET.fromstring(compFile).getroot()
      finallist =[]
      finalDict = dict()
      #Parsing the gspec (made in Jet)
      for node in gspec:
         if node.tag == "component":
            attribStr = node.attrib["type"]
            if attribStr in componentsDict.keys():
                instanceName = componentsDict[ attribStr]
                if instanceName in finalDict:
                    finalDict[instanceName] = finalDict[instanceName] + 1
                    #print "Increased count ", attribStr
                else:
	                finalDict[instanceName] = 1
	                #print "ADDED ", attribStr
	                finallist.append(attribStr)
                #print 'FOUND IN BOTH ', instanceName 
      return finalDict

    
if __name__ == "__main__":
    gp = GspecParser()
    gp.setCatalog( "Components.cat" )
    dict = gp.getComps("gspec.xml") 
    for key in dict.keys():
        print key, dict[key]
