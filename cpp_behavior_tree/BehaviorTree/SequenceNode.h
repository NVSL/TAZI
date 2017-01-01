// SequenceNode.h

#ifndef _SEQUENCENODE_h
#define _SEQUENCENODE_h

#if defined(ARDUINO) && ARDUINO >= 100
	#include "arduino.h"
#else
	#include "WProgram.h"
#endif

#include "InternalNode.h"
class SequenceNode: public InternalNode {
public: 
	SequenceNode(NodeList children, int numberOfChildren) :
			     InternalNode(children, numberOfChildren) {};
	uint8_t tick();
};

#endif

