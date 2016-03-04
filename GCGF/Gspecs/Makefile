EAGLESERVER = ../../../EagleServer/
MAKEGADGET = python $(EAGLESERVER)make_gadget.py
GSPECS = $(wildcard *.gspec)
PAPIS = $(GSPECS:%.gspec=%.api.gspec)
CLEAN = rm -f *.brd;rm -f *.readme;rm -f *.status;\
	rm -f *.status;rm -f *.api.api.gspec;rm -f *.sch 
all: $(APIS) 
%.api.gspec : %.gspec 
	$(MAKEGADGET) -k $* -n $*
	$(CLEAN)
clean:
	$(CLEAN)
