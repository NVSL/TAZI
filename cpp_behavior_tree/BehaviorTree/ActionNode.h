// ActionNode.h

#ifndef _ACTIONNODE_h
#define _ACTIONNODE_h
#include "BehaviorNode.h"

#if defined(ARDUINO) && ARDUINO >= 100
	#include "arduino.h"
#else
	#include "WProgram.h"
#endif

class ActionNode : public BehaviorNode {
public:
	ActionNode(uint8_t(*func)(uint8_t state));
	uint8_t tick();
private:
	uint8_t (*c_like_func)(uint8_t);
	uint8_t state;
};


#endif

