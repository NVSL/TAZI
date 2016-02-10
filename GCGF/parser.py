import xml.etree.ElementTree

class GspecParser: 

   def initializeList(self):
      base = xml.etree.ElementTree.parse('Components.cat').getroot()
      compList = []
      #Parsing the components file from Gadgetron
      for component in base.findall('component'):
         compStr = component.get('keyname');
         for child in component:
            if child.tag == 'API':
	       compList.append(compStr)
	       print 'API FOUND FOR ABOVE ELEMENT ', compStr
      return compList

   def getComps(self, compFile, compList): 
      gspec = xml.etree.ElementTree.parse(compFile).getroot()
      finallist =[]
      finalDict = dict()
      #Parsing the gspec (made in Jet)
      for node in gspec:
         if node.tag == "component":
            attribStr = node.attrib["type"]
            if attribStr in compList:
	       if attribStr in finalDict:
	          finalDict[attribStr] = finalDict[attribStr] + 1
		  print "Increased count ", attribStr
	       else:
	          finalDict[attribStr] = 0
	          print "ADDED ", attribStr
               finallist.append(attribStr)
	       print 'FOUND IN BOTH ', node.attrib["type"]

    
if __name__ == "__main__":
    gp = GspecParser()
    gp.getComps("gspec.xml", gp.initializeList())  
