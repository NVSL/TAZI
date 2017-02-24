// 
// 
// 

#include "DelayTimer.h"

DelayTimer::DelayTimer(long delay_time)
{
	this->delay_time = delay_time;
	this->start_time = -1;
}

bool DelayTimer::delay()
{
	if (start_time < 0) {
		start_time = millis();
		return false;
	}
	if (millis() - start_time > delay_time) {
		start_time = -1;
		return true;
	}
	return false;
}
