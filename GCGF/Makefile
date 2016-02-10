GSPEC = gspec.xml

ide:
    python IDEGenerator.py -j Blocks.json -g $(GSPEC) -c Components.cat -d DefaultCategories.xml -x index.jina > ../Blockly/index.html
json:
	python BlockGenerator.py -l ComponentsLibrary.xml -d DefaultCategories.xml > Blocks.json
build:
	python BlockGenerator.py -l ComponentsLibrary.xml -j index.jinja -d DefaultCategories.xml > ../Blockly/index.html
testclang:
	python ClangBindings.py clangtest.h 
classbuilder:
	python ClassGenerator.py -g test.api.gspec 
clean:
	rm *.pyc
display:
	google-chrome ../Blockly/index.html
