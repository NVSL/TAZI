COPY = '-R'
APPENGINE = appengine/
DEST = $(APPENGINE)static/
B2CPP = BlocksToCpp
INOGEN = InoGenerator

all:	copy run
copy:
	cp $(COPY) blocks/ $(DEST)
	cp $(COPY) core/ $(DEST)
	cp $(COPY) demos/ $(DEST)
	cp $(COPY) generators/ $(DEST)
	cp $(COPY) media/ $(DEST)
	cp $(COPY) msg/ $(DEST)
	cp $(COPY) tests/ $(DEST)
	cp $(COPY) blockly_compressed.js $(DEST)
	cp $(COPY) blockly_uncompressed.js $(DEST)
	cp $(COPY) blocks_compressed.js $(DEST)
	cp $(COPY) dart_compressed.js $(DEST)
	cp $(COPY) javascript_compressed.js $(DEST)
	cp $(COPY) jquery-2.2.1.min.js $(DEST)
	cp $(COPY) php_compressed.js $(DEST)
	cp $(COPY) python_compressed.js $(DEST)
	cp $(COPY) custom_blocks.js $(DEST)
	cp $(COPY) BlocksIO.js $(DEST)
	cp $(COPY) GtronImage.png $(DEST)
	cp $(COPY) landing.html $(DEST)
	cp $(COPY) index.html $(DEST)
	cp $(COPY) Requests.js $(DEST)
	cp $(COPY) angular*/ $(DEST)
	cp $(COPY) ../$(B2CPP) $(APPENGINE)
	make -C ../GCGF ino_package
	cp $(COPY) ../GCGF/$(INOGEN) $(APPENGINE)
clean:
	rm -rf $(DEST)
	rm -rf $(APPENGINE)$(B2CPP)
	rm -rf $(APPENGINE)$(INOGEN)
	make -C $(APPENGINE) clean_inner
run:
	make -C $(APPENGINE)
