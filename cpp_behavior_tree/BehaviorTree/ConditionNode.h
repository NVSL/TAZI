// ConditionNode.h

#ifndef _CONDITIONNODE_h
#define _CONDITIONNODE_h
#include "BehaviorNode.h"



#if defined(ARDUINO) && ARDUINO >= 100
	#include "arduino.h"
#else
	#include "WProgram.h"
#endif
class ConditionNode : public BehaviorNode {
public:
	ConditionNode(bool(*func)());
	uint8_t tick(); 
private:
	bool(*c_like_func)();
};
uint8_t ConditionNode::tick()
{
	return c_like_func();
}
ConditionNode::ConditionNode(bool(*func)())
{
	this->c_like_func = func;
};


#endif
