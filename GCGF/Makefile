GSPEC_DIR = Gspecs/
RESOURCES = Resources
OUTPUT = Output/

GSPEC = HotlineBling
APIGSPEC = Chase
APIGSPECS = $(wildcard Gspecs/*.api.gspec)
INOS = $(APIGSPECS:Gspecs/%.api.gspec=%.ino)
ARDUINO = /home/michael/Downloads/arduino-1.6.4/arduino

GSPEC_FILE = $(GSPEC_DIR)$(GSPEC).gspec
APIGSPEC_FILE = $(GSPEC_DIR)$(APIGSPEC).api.gspec
GADGET_DIR = $(OUTPUT)$(APIGSPEC)
GADGET_INO = $(GADGET_DIR)/$(APIGSPEC).ino

CATALOG = $(GADGETRON_CATALOG)/Components.xml
CATEGORIESXML = $(RESOURCES)/DefaultCategories.xml
BLACKLIST = $(RESOURCES)/BlackListedFunctions.xml
BLOCKSJSON = $(RESOURCES)/Blocks.json
JINJAFILE = $(RESOURCES)/index.jinja
.PRECIOUS: $(GSPEC_DIR)%.api.gspec

ide:
	cp IDEGenerator.py IDEGenerator/
	cp GspecParser.py IDEGenerator/
	python IDEGenerator.py -j $(BLOCKSJSON) -g $(GSPEC_FILE) -c $(CATALOG) -d $(CATEGORIESXML) -x $(JINJAFILE) > ../Blockly/index.html
json:
	python BlockGenerator.py -l ComponentsLibrary.xml -b $(BLACKLIST) > $(BLOCKSJSON)
testclang:
	python ClangBindings.py clangtest.h 
inos: $(INOS)
class:
	mkdir -p $(GADGET_DIR)
	python ClassGenerator.py -g $(APIGSPEC_FILE) > $(GADGET_INO)
	$(ARDUINO) --verify $(GADGET_INO)
clean:
	rm *.pyc
display:
	google-chrome ../Blockly/index.html
%.ino : $(GSPEC_DIR)%.api.gspec
	mkdir -p $(OUTPUT)$*
	python ClassGenerator.py -g $< > $(OUTPUT)$*/$@
	$(ARDUINO) --verify $(OUTPUT)$*/$@
$(GSPEC_DIR)%.api.gspec : $(GSPEC_DIR)%.gspec
	make -C $(GSPEC_DIR) $*.api.gspec
