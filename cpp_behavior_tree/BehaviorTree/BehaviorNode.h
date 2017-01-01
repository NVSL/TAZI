// BehaviorNode.h

#ifndef _BEHAVIORNODE_h
#define _BEHAVIORNODE_h

#define BEHAVIOR_SUCCESS 1
#define BEHAVIOR_FAILED 0
#define BEHAVIOR_RUNNING 2

#if defined(ARDUINO) && ARDUINO >= 100
	#include "arduino.h"
#else
	#include "WProgram.h"
#endif

class BehaviorNode {
public:
	virtual uint8_t tick() = 0;
};
typedef BehaviorNode** NodeList;

#endif

