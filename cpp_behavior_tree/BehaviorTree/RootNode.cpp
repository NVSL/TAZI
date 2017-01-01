// 
// 
// 

#include "RootNode.h"

RootNode::RootNode(BehaviorNode * child)
{
	this->child = child;
}

uint8_t RootNode::tick()
{
	return this->child->tick();
}
