GSPEC = Gspecs/Wall-E.gspec
APIGSPEC = Gspecs/HotlineBling.api.gspec
RESOURCES = Resources
CATALOG = $(GADGETRON_CATALOG)/Components.xml
CATEGORIESXML = $(RESOURCES)/DefaultCategories.xml
BLOCKSJSON = $(RESOURCES)/Blocks.json
JINJAFILE = $(RESOURCES)/index.jinja

ide:
	cp IDEGenerator.py IDEGenerator/
	cp GspecParser.py IDEGenerator/
	python IDEGenerator.py -j $(BLOCKSJSON) -g $(GSPEC) -c $(CATALOG) -d $(CATEGORIESXML) -x $(JINJAFILE) > ../Blockly/index.html
json:
	python BlockGenerator.py -l ComponentsLibrary.xml > $(BLOCKSJSON)
testclang:
	python ClangBindings.py clangtest.h 
class:
	python ClassGenerator.py -g $(APIGSPEC) 
clean:
	rm *.pyc
display:
	google-chrome ../Blockly/index.html
