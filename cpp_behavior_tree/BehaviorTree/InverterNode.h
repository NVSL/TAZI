// InverterNode.h

#ifndef _INVERTERNODE_h
#define _INVERTERNODE_h
#include "BehaviorNode.h"

#if defined(ARDUINO) && ARDUINO >= 100
	#include "arduino.h"
#else
	#include "WProgram.h"
#endif


class InverterNode : public BehaviorNode {
public:
	InverterNode(BehaviorNode * child);
	uint8_t tick();
private:
	BehaviorNode * child;

};


#endif

