CC = g++
FLAGS = -lrt -lpthread
ARDUPI = arduPi.cpp
PROG = test

default: $(PROG)
$(PROG):
	$(CC) $(FLAGS) -o $(PROG) $(ARDUPI) $(PROG).cpp
clean:
	rm -f $(PROG)
run: $(PROG)
	sudo ./$(PROG)
%: %.cpp
	$(CC) $(FLAGS) -o $@ $(ARDUPI) $<
