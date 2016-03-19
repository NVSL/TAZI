CC = g++
FLAGS = -std=c++11 -lrt -lpthread
ARDUPI = arduPi.o
PROG = program
OBJS = arduPi.o LED.o MomentaryButton.o Motor.o

default: $(PROG)
$(PROG): $(OBJS)
	$(CC) $(FLAGS) -o ../$(PROG) $(OBJS) $(PROG).cpp
clean:
	rm -f $(PROG)
	rm -f *.o
run: $(PROG)
	sudo ../$(PROG)
%: %.cpp $(ARDUPI)
	$(CC) $(FLAGS) -o $@ $(ARDUPI) $<
%.o: %.cpp
	$(CC) $(FLAGS) -c -o $@ $<
