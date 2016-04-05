# Dependencies
INOGEN = InoGenerator
B2CPP = BlocksToCpp
# Shell commands
CP = cp -R
RM = rm -rf
# Program Files
TESTDIR = RobotTests/
GSPECNAME = Chase
PROG = LedOnOff

# Program flags
GSPEC_FLAG = -g $(TESTDIR)$(GSPECNAME)/$(GSPECNAME).api.gspec
XML_FLAG = -x $(TESTDIR)$(GSPECNAME)/xml/$(PROG).xml
INO_PATH = $(TESTDIR)$(GSPECNAME)/$(GSPECNAME).ino
test: $(INOGEN)/ $(B2CPP)/
	python runAll.py
run: $(INOGEN)/ $(B2CPP)/
	python InoComposer.py $(GSPEC_FLAG) $(XML_FLAG) 
$(INO_PATH): run
verify: $(INO_PATH)
	arduino --verify $(INO_PATH)
$(INOGEN)/: copy
$(B2CPP)/: copy
copy:
	make -C ../GCGF ino_package
	$(CP) ../GCGF/$(INOGEN) .
	$(CP) ../$(B2CPP) .
clean:
	$(RM) $(INOGEN)
	$(RM) $(B2CPP)
	$(RM) $(INO_PATH)
