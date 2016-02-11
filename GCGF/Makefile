GSPEC = Gspecs/PessimistPrime.gspec
RESOURCES = Resources
CATALOG = $(GADGETRON_CATALOG)/Components.cat
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
classbuilder:
	python ClassGenerator.py -g test.api.gspec 
clean:
	rm *.pyc
display:
	google-chrome ../Blockly/index.html
