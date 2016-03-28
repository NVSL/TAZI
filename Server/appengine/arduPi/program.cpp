//Include arduPi library
//#pragma G++ diagnostic ignored "-fpermissive"
#include "arduPi.h"

/*********************************************************
 *  IF YOUR ARDUINO CODE HAS OTHER FUNCTIONS APART FROM  *
 *  setup() AND loop() YOU MUST DECLARE THEM HERE        *
 * *******************************************************/
#include "program.ino"
#include <bcm2835.h>

int main(){
    bcm2835_init();
    // Setup PWM
    bcm2835_pwm_set_clock(BCM2835_PWM_CLOCK_DIVIDER_16);
    bcm2835_pwm_set_mode(0,1,1);
    bcm2835_pwm_set_range(0,255);
    setup();
    while(1) {
      loop();
    }
    return (0);
}
