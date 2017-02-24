// 
// 
// 

#include "ActionNode.h"

ActionNode::ActionNode(uint8_t(*func)(uint8_t state))
{
	this->c_like_func = func;
	this->state = 0;
}

uint8_t ActionNode::tick()
{
	this->state = this->c_like_func(this->state);
	return ( this->state == 0 ? BEHAVIOR_SUCCESS : BEHAVIOR_RUNNING );
}
