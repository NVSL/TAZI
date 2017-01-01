// ParallelNode.h

#ifndef _PARALLELNODE_h
#define _PARALLELNODE_h

#if defined(ARDUINO) && ARDUINO >= 100
	#include "arduino.h"
#else
	#include "WProgram.h"
#endif

#include "InternalNode.h"
class ParallelNode: public InternalNode {
public: 
	ParallelNode(NodeList children, int numberOfChildren) :
			     InternalNode(children, numberOfChildren) {};
	uint8_t tick();
};



#endif

