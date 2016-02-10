import xml.etree.ElementTree

class GspecParser: 

   def initializeList(self):
      base = xml.etree.ElementTree.parse('Components.cat').getroot()
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
	                        print 'API FOUND FOR ABOVE ELEMENT ', n.attrib["name"]
      return componentsDict

   def getComps(self, compFile, componentsDict): 
      gspec = xml.etree.ElementTree.parse(compFile).getroot()
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
                    print "Increased count ", attribStr
                else:
	                finalDict[instanceName] = 1
	                print "ADDED ", attribStr
	                finallist.append(attribStr)
                print 'FOUND IN BOTH ', instanceName 
      return finalDict

    
if __name__ == "__main__":
    gp = GspecParser()
    dict = gp.getComps("gspec.xml", gp.initializeList())  
    for key in dict.keys():
        print key, dict[key]
