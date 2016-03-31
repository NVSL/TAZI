GSPEC_DIR = Gspecs/
RESOURCES = Resources
OUTPUT = Output/

GSPEC = RaspberryPiTest2
APIGSPEC = SimpleLEDTest
APIGSPECS = $(wildcard Gspecs/*.api.gspec)
INOS = $(APIGSPECS:Gspecs/%.api.gspec=%.ino)
ARDUINO = arduino

GSPEC_FILE = -g $(GSPEC_DIR)$(GSPEC).gspec
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
RESDIR = -r "{{resDir}}"
BLOCKLYDIR = -b "{{blockly}}"
.PRECIOUS: $(GSPEC_DIR)%.api.gspec

packages: ide_package ino_package
ide_package:
	cp IDEGenerator.py IDEGenerator/
	cp GspecParser.py IDEGenerator/
	cp JinjaUtil.py IDEGenerator/
ino_package:
	cp $(INOGENERATOR) InoGenerator/
	cp InoCommenter.py InoGenerator/
ide:
	python IDEGenerator.py -j $(BLOCKSJSON) $(GSPEC_FILE) -c $(CATALOG) -d $(CATEGORIESXML) -x $(JINJAFILE) $(WORKSPACE) > ../Server/index.html
idejinja:
	python IDEGenerator.py -j $(BLOCKSJSON) $(GSPEC_FILE) -c $(CATALOG) -d $(CATEGORIESXML) -x $(JINJAFILE) $(WORKSPACE) $(RESDIR) $(BLOCKLYDIR)> ../Server/jinja_templates/ide.jinja
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
	rm -f *.pyc
	make -C $(OUTPUT) clean
	make -C $(GSPEC_DIR) clean
display:
	google-chrome ../Server/index.html
%.ino : $(GSPEC_DIR)%.api.gspec
	mkdir -p $(OUTPUT)$*
	python $(INOGENERATOR) -g $< > $(OUTPUT)$*/$@
	$(ARDUINO) --verify $(OUTPUT)$*/$@
$(GSPEC_DIR)%.api.gspec : $(GSPEC_DIR)%.gspec
	make -C $(GSPEC_DIR) $*.api.gspec
