COPY = '-R'
APPENGINE = appengine/
DEST = $(APPENGINE)static/
INOCOMPOSER = InoComposer
WORKSPACE_RENDERER = JinjaUtil.py
JINJA_DIR = jinja_templates/

all:	copy run
copy:
	make -C ../$(INOCOMPOSER) copy
	cp $(COPY) $(JINJA_DIR) $(APPENGINE)
	mkdir -p $(DEST)
	cp $(COPY) views/ $(DEST)
	cp $(COPY) controllers/ $(DEST)
	cp $(COPY) lib/ $(DEST)
	cp $(COPY) media/ $(DEST)
	cp $(COPY) ../$(INOCOMPOSER) $(APPENGINE)
	cp $(COPY) ../GCGF/$(WORKSPACE_RENDERER) $(APPENGINE)
	cp $(COPY) ../GCGF/Resources/DefaultRobotWorkspace.xml $(APPENGINE)
	cp $(COPY) ../GCGF/Resources/CppDefault.xml $(APPENGINE)
clean:
	rm -rf $(DEST)
	rm -rf $(APPENGINE)$(INOCOMPOSER)
	rm -f $(APPENGINE)$(WORKSPACE_RENDERER)
	rm -rf $(APPENGINE)$(JINJA_DIR)
	rm -f $(APPENGINE)*.xml
	rm -f index.html
	make -C $(APPENGINE) clean_inner
run:
	make -C $(APPENGINE)
