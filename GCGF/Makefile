GSPEC_DIR = Gspecs/
RESOURCES = Resources
OUTPUT = Output/

GSPEC = HotlineBling
APIGSPEC = Chase
APIGSPECS = $(wildcard Gspecs/*.api.gspec)
INOS = $(APIGSPECS:Gspecs/%.api.gspec=%.ino)
ARDUINO = arduino

GSPEC_FILE = $(GSPEC_DIR)$(GSPEC).gspec
APIGSPEC_FILE = $(GSPEC_DIR)$(APIGSPEC).api.gspec
GADGET_DIR = $(OUTPUT)$(APIGSPEC)
GADGET_INO = $(GADGET_DIR)/$(APIGSPEC).ino

CATALOG = $(GADGETRON_CATALOG)/Components.xml
CATEGORIESXML = $(RESOURCES)/DefaultCategories.xml
WORKSPACE = -w $(RESOURCES)/CppDefault.xml
BLACKLIST = $(RESOURCES)/BlackListedFunctions.xml
BLOCKSJSON = $(RESOURCES)/Blocks.json
JINJAFILE = $(RESOURCES)/index.jinja
INOGENERATOR = InoGenerator.py
.PRECIOUS: $(GSPEC_DIR)%.api.gspec

ide:
	cp IDEGenerator.py IDEGenerator/
	cp GspecParser.py IDEGenerator/
	python IDEGenerator.py -j $(BLOCKSJSON) -g $(GSPEC_FILE) -c $(CATALOG) -d $(CATEGORIESXML) -x $(JINJAFILE) $(WORKSPACE) > ../Blockly/index.html
json:
	python BlockGenerator.py -l ComponentsLibrary.xml -b $(BLACKLIST) > $(BLOCKSJSON)
testclang:
	python ClangBindings.py clangtest.h 
inos: $(INOS)
class:
	mkdir -p $(GADGET_DIR)
	python $(INOGENERATOR) -g $(APIGSPEC_FILE) > $(GADGET_INO)
	$(ARDUINO) --verify $(GADGET_INO)
clean:
	rm *.pyc
	make -C $(OUTPUT) clean
	make -C $(GSPEC_DIR) clean
display:
	google-chrome ../Blockly/index.html
%.ino : $(GSPEC_DIR)%.api.gspec
	mkdir -p $(OUTPUT)$*
	python $(INOGENERATOR) -g $< > $(OUTPUT)$*/$@
	$(ARDUINO) --verify $(OUTPUT)$*/$@
$(GSPEC_DIR)%.api.gspec : $(GSPEC_DIR)%.gspec
	make -C $(GSPEC_DIR) $*.api.gspec
