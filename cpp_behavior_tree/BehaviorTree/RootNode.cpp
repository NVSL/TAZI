// 
// 
// 

#include "RootNode.h"
long RootNode::current_time = 0;

RootNode::RootNode(BehaviorNode * child)
{
	this->child = child;
}

uint8_t RootNode::tick()
{
    current_time = millis();
	return this->child->tick();
}
