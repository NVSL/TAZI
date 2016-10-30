//Include arduPi library
//#pragma G++ diagnostic ignored "-fpermissive"
#include "arduPi.h"

/*********************************************************
 *  IF YOUR ARDUINO CODE HAS OTHER FUNCTIONS APART FROM  *
 *  setup() AND loop() YOU MUST DECLARE THEM HERE        *
 * *******************************************************/
#include "blockly_executable.ino"
#include <bcm2835.h>

#define PWM_RANGE 255

int main(){
    bcm2835_init();
    // Setup PWM
    bcm2835_pwm_set_clock(BCM2835_PWM_CLOCK_DIVIDER_16);
    bcm2835_pwm_set_mode(PWM_CHANNEL_0,1,1);
    bcm2835_pwm_set_mode(PWM_CHANNEL_1,1,1);
    bcm2835_pwm_set_range(PWM_CHANNEL_0, PWM_RANGE);
    bcm2835_pwm_set_range(PWM_CHANNEL_1, PWM_RANGE);
    setup();
    while(1) {
      loop();
    }
    return (0);
}
