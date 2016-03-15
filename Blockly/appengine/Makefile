PROG_NAME = SimpleLEDTest
PROG_EXT = cpp
run:
	python main.py -n $(PROG_NAME) -e $(PROG_EXT)
runino:
	python main.py -n $(PROG_NAME) -e ino -t DefaultRobotWorkspace.xml
all:	copy run
copy:
	make -C ../ copy
clean: 
	make -C ../ clean
clean_inner:
	rm -f $(PROG_NAME)
	rm -f $(PROG_NAME).$(PROG_EXT)
	rm -f *.pyc
