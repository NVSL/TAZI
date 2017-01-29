/** ############################# Robot Name ############################## **\
|** ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*****~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ **|
|** ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~/     \~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ **|
|** ==============================={ Chase }=============================== **|
|** ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\     /~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ **|
|** ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*****~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ **|
\** ################################[[^_^]]################################ **/



/** ======================================================================= **\
|** ------------------------------ Libraries ------------------------------ **|
\** ======================================================================= **/

#include "PinChangeInt.h"
#include "DistanceSensor.h"
#include "Motor.h"
#include "LED.h"
#include "MomentaryButton.h"


/** ======================================================================= **\
|** ---------------------------- Pin Constants ---------------------------- **|
\** ======================================================================= **/

#define MOTOR1_STBY 4
#define MOTOR1_PWMA 3
#define MOTOR1_AIN1 6
#define MOTOR1_AIN2 8
#define MOTOR1_PWMB 5
#define MOTOR1_BIN1 9
#define MOTOR1_BIN2 10
#define DISTANCESENSOR1_A A2
#define DISTANCESENSOR2_A A3
#define LED1_CONTROL 11
#define LED2_CONTROL 12
#define LED3_CONTROL 13
#define MOMENTARYBUTTON1_SENSE A0
#define MOMENTARYBUTTON2_SENSE A1

/** ======================================================================= **\
|** ------------------------- Object Declarations ------------------------- **|
\** ======================================================================= **/

Motor motor1(MOTOR1_STBY, MOTOR1_PWMA, MOTOR1_AIN1, MOTOR1_AIN2, MOTOR1_PWMB, MOTOR1_BIN1, MOTOR1_BIN2);
DistanceSensor distancesensor1(DISTANCESENSOR1_A);
DistanceSensor distancesensor2(DISTANCESENSOR2_A);
LED led1(LED1_CONTROL);
LED led2(LED2_CONTROL);
LED led3(LED3_CONTROL);
MomentaryButton momentarybutton1(MOMENTARYBUTTON1_SENSE);
MomentaryButton momentarybutton2(MOMENTARYBUTTON2_SENSE);

/** ======================================================================= **\
|** --------------------- User Functions Declarations --------------------- **|
\** ======================================================================= **/
void toggleMotors();
void accelerate();


/** ======================================================================= **\
|** --------------------- User Functions Definitions ---------------------- **|
\** ======================================================================= **/
/* Describe this function...
*/
void toggleMotors() {
  if(motor1.isMoving()) {
    motor1.stop();
  }
  else {
    accelerate();
  };
}

/* Describe this function...
*/
void accelerate() {
  for(int i = 0; i<=(255); i+=(1)) {
    motor1.forward(i);
    delay((int)50);
   };
}



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
   distancesensor1.setup();
   distancesensor2.setup();
   led1.setup();
   led2.setup();
   led3.setup();
   momentarybutton1.setup();
   momentarybutton2.setup();
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
     if(momentarybutton1.isPressed()) {
       toggleMotors();
     };
}
