#include "InverterNode.h"

InverterNode::InverterNode(BehaviorNode * child)
{
	this->child = child;
}

uint8_t InverterNode::tick()
{
	uint8_t rv = child->tick();
	if (rv == BEHAVIOR_SUCCESS)
		rv = BEHAVIOR_FAILED;
	else if(rv == BEHAVIOR_FAILED)
		rv = BEHAVIOR_SUCCESS;
	return rv;
}
