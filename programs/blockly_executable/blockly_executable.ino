/** ############################# Robot Name ############################## **\
|** ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~***********~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ **|
|** ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/           \~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ **|
|** ============================{ Swag Mobile }============================ **|
|** ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\           /~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ **|
|** ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~***********~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ **|
\** #############################[[[[[^_^]]]]]############################# **/



/** ======================================================================= **\
|** ------------------------------ Libraries ------------------------------ **|
\** ======================================================================= **/

#include "GadgetManager.h"
#include "PinChangeInt.h"
#include "Motor.h"
#include "MomentaryButton.h"
#include "RGBLED.h"


/** ======================================================================= **\
|** ---------------------------- Pin Constants ---------------------------- **|
\** ======================================================================= **/

#define MOTOR1_PWMA 3
#define MOTOR1_PWMB 5
#define MOTOR1_STBY 4
#define MOTOR1_AIN1 8
#define MOTOR1_AIN2 11
#define MOTOR1_BIN1 12
#define MOTOR1_BIN2 13
#define MOMENTARYBUTTON1_SENSE A0
#define MOMENTARYBUTTON2_SENSE A1
#define RGBLED1_CONTROL_RED 6
#define RGBLED1_CONTROL_GREEN 9
#define RGBLED1_CONTROL_BLUE 10

/** ======================================================================= **\
|** ------------------------- Object Declarations ------------------------- **|
\** ======================================================================= **/

Motor motor1(MOTOR1_PWMA, MOTOR1_PWMB, MOTOR1_STBY, MOTOR1_AIN1, MOTOR1_AIN2, MOTOR1_BIN1, MOTOR1_BIN2);
MomentaryButton momentarybutton1(MOMENTARYBUTTON1_SENSE);
MomentaryButton momentarybutton2(MOMENTARYBUTTON2_SENSE);
RGBLED rgbled1(RGBLED1_CONTROL_RED, RGBLED1_CONTROL_GREEN, RGBLED1_CONTROL_BLUE);

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
   momentarybutton1.setup();
   momentarybutton2.setup();
   rgbled1.setup();
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
   ;
}
