import xml.etree.ElementTree as ET
#import sys

def findblock(depth, node):
    for nod in node.findall('block'):
        print depth
        print nod.attrib
        findblock(depth + 1, nod) #return?


treeR = raw_input("Which file would you like to read? ").lower()

tree = ET.parse(treeR)
root = tree.getroot()

#root = ET.fromstring(country_data_as_string)

print "top level: "
print root.findall(".")

print "findblock: "
findblock(0, root)

print "Printing out child xml attributes"

for child in root:
    print child.tag, child.attrib

print "from 'root' the tag at [1][0] " + root[1][0].text

print "findall block: "
for boop in root.findall('block'): #just iter() works
    print boop.tag, boop.attrib

tester = raw_input("Please put in tag: ").lower()

#only elements with a tag with elements as a direct child of curr elem
for tagg in root.iterfind(tester):
    search = raw_input("find sub_tag: ").lower()
    print "tag: " + tagg.tag
    print tagg.atrrib
    print "text: " + tagg.text
    rank = country.find(search).text    #find = first child w/ that tag
    name = country.attrib
    #name = country.get('name')          #get = element's attribs
    print name, rank

cont = 1;

while(cont == 1):
    readIn = raw_input("Please put in the tag you would like to search for: ").lower()
    if readIn == "quit" or readIn == "q":
        print "quit now"
        cont = 0
    #country
else:
    print "searching for " + readIn
    for search in root.iter(readIn): #findall
        print search.find('rank').text
        print search.get('name')
