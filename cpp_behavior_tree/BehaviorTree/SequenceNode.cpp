// 
// 
// 

#include "SequenceNode.h"

uint8_t SequenceNode::tick()
{
	uint8_t state;
	// TODO: Implement state within tick
	for (int i = 0; i < numberOfChildren; i++) {
		state = children[i]->tick();
		if (state == BEHAVIOR_FAILED || state == BEHAVIOR_RUNNING)
			return state;
	}
	return BEHAVIOR_SUCCESS;
}
