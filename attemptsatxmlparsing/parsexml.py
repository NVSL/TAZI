import xml.etree.ElementTree as ET
#import sys

treeR = raw_input("Which file would you like to read? ").lower()

tree = ET.parse(treeR)

#tree = ET.parse('blah.xml')
root = tree.getroot()

#root = ET.fromstring(country_data_as_string)

print root.tag
print root.attrib

print "tree: "
print tree.findall(".")

print "Printing out child xml attributes"

for child in root:
    print child.tag, child.attrib

print "from 'root' the tag at [1][1] " + root[1][1].text

print "iterate recursively through a subtree: "
for tagg in root.iter('country'):
    print "tag: " + tagg.tag
    print tagg.attrib
    print "text: " + tagg.text

print "find required: "
tester = raw_input("Please put in tag: ").lower()

#only elements with a tag with elements as a direct child of curr elem
for country in root.iter(tester):
    print country.tag
    search = raw_input("find sub_tag: ").lower()
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
        #readIn = '//' + readIn
        print "searching for " + readIn
        for search in root.iter(readIn): #findall
            print search.find('rank').text
            print search.get('name')

while(cont == 1):
    readIn = raw_input("Please put in the tag you would like to search for: ").lower()
    if readIn == "quit" or readIn == "q":
        print "quit now"
        cont = 0
    #country
    else:
        readIn = "//" + readIn
        print "searching for " + readIn

        print tree.find(readIn).text
        for search in root.find(readIn): #findall
            print search.text
            #print search.find('rank').text
            #print search.get('name')


'''try:
  # open file stream
  file = open(file_name, "w")
except IOError:
  print "There was an error writing to", file_name
  sys.exit()
print "Enter '", file_finish,
print "' When finished"
while file_text != file_finish:
  file_text = raw_input("Enter text: ")
  if file_text == file_finish:
    # close the file
    file.close
    break
  file.write(file_text)
  file.write("\n")
file.close()
file_name = raw_input("Enter filename: ")
if len(file_name) == 0:
  print "Next time please enter something"
  sys.exit()
try:
  file = open(file_name, "r")
except IOError:
  print "There was an error reading file"
  sys.exit()
file_text = file.read()
file.close()
print file_text'''

