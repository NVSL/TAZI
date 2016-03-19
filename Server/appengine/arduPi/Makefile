CC = g++
FLAGS = -lrt -lpthread
ARDUPI = arduPi.o
PROG = program

default: $(PROG)
$(PROG):
	$(CC) $(FLAGS) -o ../$(PROG) $(ARDUPI) $(PROG).cpp
clean:
	rm -f $(PROG)
run: $(PROG)
	sudo ../$(PROG)
%: %.cpp arduPi.o
	$(CC) $(FLAGS) -o $@ $(ARDUPI) $<
%.o: %.cpp
	$(CC) $(FLAGS) -c -o $@ $<
