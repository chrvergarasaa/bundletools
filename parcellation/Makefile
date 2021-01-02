CC = g++ -std=c++11 -fopenmp

CFLAGS = -c -Wall -O3

all: felipe

felipe: main.o intersection.o alignment.o regions.o
	$(CC) main.o intersection.o alignment.o regions.o -o felipe

main.o: main.cpp
	$(CC) $(CFLAGS) main.cpp

intersection.o: intersection.cpp
	$(CC) $(CFLAGS) intersection.cpp

alignment.o: alignment.cpp
	$(CC) $(CFLAGS) alignment.cpp

regions.o: regions.cpp
	$(CC) $(CFLAGS) regions.cpp

clean:
	rm -rf *o felipe
