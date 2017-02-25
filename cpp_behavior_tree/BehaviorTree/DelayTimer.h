// DelayTimer.h

#ifndef _DELAYTIMER_h
#define _DELAYTIMER_h

#if defined(ARDUINO) && ARDUINO >= 100
	#include "arduino.h"
#else
	#include "WProgram.h"
#endif

#include "RootNode.h"
class DelayTimer {
public:
	DelayTimer(long delay_time);
	bool delay();
private:
	long delay_time, start_time;
};


#endif

