COPY = '-R'
APPENGINE = appengine/
DEST = $(APPENGINE)static/
B2CPP = BlocksToCpp
INOGEN = InoGenerator
WORKSPACE_RENDERER = JinjaUtil.py
JINJA_DIR = jinja_templates/

all:	copy run
copy:
	make -C ../GCGF ino_package
	cp $(COPY) $(JINJA_DIR) $(APPENGINE)
	mkdir -p $(DEST)
	cp $(COPY) views/ $(DEST)
	cp $(COPY) lib/ $(DEST)
	cp $(COPY) media/ $(DEST)
	cp $(COPY) ../$(B2CPP) $(APPENGINE)
	cp $(COPY) ../GCGF/$(INOGEN) $(APPENGINE)
	cp $(COPY) ../GCGF/$(WORKSPACE_RENDERER) $(APPENGINE)
	cp $(COPY) ../GCGF/Resources/DefaultRobotWorkspace.xml $(APPENGINE)
	cp $(COPY) ../GCGF/Resources/CppDefault.xml $(APPENGINE)
clean:
	rm -rf $(DEST)
	rm -rf $(APPENGINE)$(B2CPP)
	rm -rf $(APPENGINE)$(INOGEN)
	rm -f $(APPENGINE)$(WORKSPACE_RENDERER)
	rm -rf $(APPENGINE)$(JINJA_DIR)
	rm -f $(APPENGINE)*.xml
	rm index.html
	make -C $(APPENGINE) clean_inner
run:
	make -C $(APPENGINE)
