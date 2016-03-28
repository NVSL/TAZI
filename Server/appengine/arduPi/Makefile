CC = g++
FLAGS = -std=c++11 -lrt -lpthread -lbcm2835
ARDUPI = arduPi.o
PROG = program
OBJS = arduPi.o LED.o MomentaryButton.o Motor.o

default: $(PROG)
$(PROG): $(OBJS)
	$(CC) -o ../$(PROG) $(OBJS) $(PROG).cpp $(FLAGS)
clean:
	rm -f $(PROG)
	rm -f *.o
run: $(PROG)
	sudo ../$(PROG)
%: %.cpp $(ARDUPI)
	$(CC) -o $@ $(ARDUPI) $< $(FLAGS)
%.o: %.cpp
	$(CC) -c -o $@ $< $(FLAGS)
