PROG_NAME = blockly_executable
PROG_EXT = ino
COPY = ln -s
DEST = static/
INOCOMPOSER = InoComposer
WORKSPACE_RENDERER = JinjaUtil.py
JINJA_DIR = ../jinja_templates
runino:
	python main.py -n $(PROG_NAME) -e ino -t DefaultRobotWorkspace.xml
run:
	python main.py -n $(PROG_NAME) -e $(PROG_EXT)
all:	copy run
copy:
	make -C ../../$(INOCOMPOSER) copy
	mkdir -p $(DEST)
	$(COPY) ../../views $(DEST)
	$(COPY) ../../controllers $(DEST)
	$(COPY) ../../lib $(DEST)
	$(COPY) ../../media $(DEST)
	$(COPY) ../../$(INOCOMPOSER) $(APPENGINE)
	$(COPY) ../../GCGF/$(WORKSPACE_RENDERER) $(APPENGINE)
	$(COPY) ../../GCGF/Resources/DefaultRobotWorkspace.xml $(APPENGINE)
	$(COPY) ../../GCGF/Resources/CppDefault.xml $(APPENGINE)
	$(COPY) $(JINJA_DIR) $(APPENGINE)
clean: 
	rm -f *.xml
	rm -rf $(DEST)
	rm -f $(INOCOMPOSER)
	rm -f $(WORKSPACE_RENDERER)
	rm -f jinja_templates
	#rm -f $(PROG_NAME)
	rm -f $(PROG_NAME).$(PROG_EXT)
	rm -f *.pyc
	rm -f *.ino
	rm -f *.cpp
