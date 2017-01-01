// RootNode.h

#ifndef _ROOTNODE_h
#define _ROOTNODE_h
#include "BehaviorNode.h"
#if defined(ARDUINO) && ARDUINO >= 100
	#include "arduino.h"
#else
	#include "WProgram.h"
#endif

#define MAKE_NODE_LIST(size) new BehaviorNode*[size]

class RootNode : BehaviorNode {
public:
	RootNode(BehaviorNode * child);
	uint8_t tick();
private:
	BehaviorNode * child;
};
#endif

