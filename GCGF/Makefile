build:
	python BlockGenerator.py -l ComponentsLibrary.xml -j index.jinja -d DefaultCategories.xml > ../Blockly/index.html
testclang:
	python ClangBindings.py clangtest.h 
classbuilder:
	python ClassGenerator.py -g test.api.gspec 
clean:
	rm *.pyc
