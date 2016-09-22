APPENGINE = appengine/
DEST = $(APPENGINE)static/

all:	run
copy:
	make -C $(APPENGINE) copy 
clean:
	rm -f index.html
	make -C $(APPENGINE) clean
run:
	make -C $(APPENGINE)
