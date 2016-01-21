build:
	python BlockGenerator.py -l ComponentsLibrary.xml -j index.jinja > ../Blockly/index.html
testclang:
	python ClangBindings.py clangtest.h 
classbuilder:
	python ClassGenerator.py -g test.api.gspec 
clean:
	rm *.pyc
