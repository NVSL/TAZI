PROG_NAME = blockly_executable
PROG_EXT = cpp
runino:
	python main.py -n $(PROG_NAME) -e ino -t DefaultRobotWorkspace.xml
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
	rm -f *.ino
	rm -f *.cpp
