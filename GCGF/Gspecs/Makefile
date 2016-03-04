EAGLESERVER = ../../../EagleServer/
MAKEGADGET = python $(EAGLESERVER)make_gadget.py
GSPECS = $(wildcard *.gspec)
APIS = $(GSPECS:%.gspec=%.api.gspec)
all: $(APIS) clean
%.api.gspec : %.gspec 
	$(MAKEGADGET) -k $* -n $*
clean:
	rm -f *.brd
	rm -f *.readme
	rm -f *.status
	rm -f *.sch
	rm -f *.api.api.gspec
