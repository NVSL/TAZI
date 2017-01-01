// 
// 
// 

#include "ParallelNode.h"

uint8_t ParallelNode::tick()
{
	// TODO: Implement state within tick
	for (int i = 0; i < numberOfChildren; i++) {
		children[i]->tick();
	}
	return BEHAVIOR_SUCCESS;
}
