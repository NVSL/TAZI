// SelectorNode.h

#ifndef _SELECTORNODE_h
#define _SELECTORNODE_h
#include "InternalNode.h"

#if defined(ARDUINO) && ARDUINO >= 100
	#include "arduino.h"
#else
	#include "WProgram.h"
#endif
class SelectorNode : public InternalNode {
public: 
	SelectorNode(NodeList children, int numberOfChildren) :
			     InternalNode(children, numberOfChildren) {};
	uint8_t tick();
};

#endif

