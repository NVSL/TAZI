/** ############################# Robot Name ############################## **\
|** ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~***********~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ **|
|** ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/           \~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ **|
|** ============================{ Gadget Name }============================ **|
|** ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\           /~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ **|
|** ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~***********~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ **|
\** #############################[[[[[^_^]]]]]############################# **/



/** ======================================================================= **\
|** ------------------------------ Libraries ------------------------------ **|
\** ======================================================================= **/

#include "MomentaryButton.h"
#include "PinChangeInt.h"
#include "Motor.h"
#include "Buzzer.h"
#include "GadgetManager.h"
#include "LED.h"
#include "RGBLED.h"


/** ======================================================================= **\
|** ---------------------------- Pin Constants ---------------------------- **|
\** ======================================================================= **/

#define MOTOR1_STBY 4
#define MOTOR1_PWMA 3
#define MOTOR1_AIN1 8
#define MOTOR1_AIN2 11
#define MOTOR1_PWMB 5
#define MOTOR1_BIN1 12
#define MOTOR1_BIN2 13
#define BUZZER1_1 1
#define RGBLED1_LED_R 6
#define RGBLED1_LED_G 9
#define RGBLED1_LED_B 10
#define LED1_CONTROL A0
#define LED2_CONTROL A1
#define LED3_CONTROL A2
#define MOMENTARYBUTTON1_SENSE 0

/** ======================================================================= **\
|** ------------------------- Object Declarations ------------------------- **|
\** ======================================================================= **/

Motor motor1(MOTOR1_STBY, MOTOR1_PWMA, MOTOR1_AIN1, MOTOR1_AIN2, MOTOR1_PWMB, MOTOR1_BIN1, MOTOR1_BIN2);
Buzzer buzzer1(BUZZER1_1);
RGBLED rgbled1(RGBLED1_LED_R, RGBLED1_LED_G, RGBLED1_LED_B);
LED led1(LED1_CONTROL);
LED led2(LED2_CONTROL);
LED led3(LED3_CONTROL);
MomentaryButton momentarybutton1(MOMENTARYBUTTON1_SENSE);

/** ======================================================================= **\
|** --------------------------- Setup Function ---------------------------- **|
|** %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% **|
|** ............................. Description ............................. **|
|** The setup() function runs --ONCE-- when the Arduino boots up. As the    **|
|** name implies, it's useful to add code that 'sets up' your Gadget to     **|
|** run correctly.                                                          **|
|** %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% **|
\** ======================================================================= **/

void setup() {
   motor1.setup();
   buzzer1.setup();
   rgbled1.setup();
   led1.setup();
   led2.setup();
   led3.setup();
   momentarybutton1.setup();
}

/** ======================================================================= **\
|** ---------------------------- Loop Function ---------------------------- **|
|** %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% **|
|** ............................. Description ............................. **|
|** The loop() function runs continuously after the setup() function        **|
|** finishes and while the Arduino is running. In other words, this         **|
|** function is called repeatly over and over again when it reaches the     **|
|** end of the function. This function is where the majority of your        **|
|** program's logic should go.                                              **|
|** %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% **|
\** ======================================================================= **/

void loop() {
     motor1.backward();
     delay( (int) ( 1000 * (5)));
     motor1.spinRight();
     delay( (int) ( 1000 * (5)));
     led1.toggle();
     motor1.forwardAndLeft();
     delay( (int) ( 1000 * (5)));
     led3.toggle();
     led2.turnOn();
     motor1.spinLeft();
     delay( (int) ( 1000 * (5)));
     led2.turnOn();
}
