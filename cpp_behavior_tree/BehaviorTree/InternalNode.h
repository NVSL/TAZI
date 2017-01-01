// InternalNode.h

#ifndef _INTERNALNODE_h
#define _INTERNALNODE_h

#include "BehaviorNode.h"
#if defined(ARDUINO) && ARDUINO >= 100
	#include "arduino.h"
#else
	#include "WProgram.h"
#endif

class InternalNode : public BehaviorNode {
public:
	InternalNode(NodeList children, int numberOfChildren);
	
protected:
	NodeList children;
	int numberOfChildren;
};
#endif

