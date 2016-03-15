PROG_NAME = COMPILEDPROG
PROG_EXT = cpp
run:
	python main.py -n $(PROG_NAME) -e $(PROG_EXT)
all:	copy run
copy:
	make -C ../ copy
clean: 
	make -C ../ clean
clean_inner:
	rm -f $(PROG_NAME)
	rm -f $(PROG_NAME).$(PROG_EXT)
	rm -f *.pyc
