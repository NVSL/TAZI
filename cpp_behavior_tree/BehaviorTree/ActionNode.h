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
	ActionNode(void(*func)());
	uint8_t tick();
private:
	void (*c_like_func)();
};


#endif

