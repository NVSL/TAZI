// 
// 
// 

#include "ActionNode.h"

ActionNode::ActionNode(void(*func)())
{
	this->c_like_func = func;
}

uint8_t ActionNode::tick()
{
	this->c_like_func();
	return BEHAVIOR_SUCCESS;
}
