GSPEC_DIR = Gspecs/
RESOURCES = Resources
OUTPUT = Output/

GSPEC = Chase
APIGSPEC = RotorBuzzer

GSPEC_FILE = $(GSPEC_DIR)$(GSPEC).gspec
APIGSPEC_FILE = $(GSPEC_DIR)$(APIGSPEC).api.gspec

CATALOG = $(GADGETRON_CATALOG)/Components.xml
CATEGORIESXML = $(RESOURCES)/DefaultCategories.xml
BLACKLIST = $(RESOURCES)/BlackListedFunctions.xml
BLOCKSJSON = $(RESOURCES)/Blocks.json
JINJAFILE = $(RESOURCES)/index.jinja

ide:
	cp IDEGenerator.py IDEGenerator/
	cp GspecParser.py IDEGenerator/
	python IDEGenerator.py -j $(BLOCKSJSON) -g $(GSPEC_FILE) -c $(CATALOG) -d $(CATEGORIESXML) -x $(JINJAFILE) > ../Blockly/index.html
json:
	python BlockGenerator.py -l ComponentsLibrary.xml -b $(BLACKLIST) > $(BLOCKSJSON)
testclang:
	python ClangBindings.py clangtest.h 
class:
	python ClassGenerator.py -g $(APIGSPEC_FILE) > $(OUTPUT)$(APIGSPEC).cpp  
clean:
	rm *.pyc
display:
	google-chrome ../Blockly/index.html
