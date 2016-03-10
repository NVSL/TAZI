/** ############################# Robot Name ############################## **\
|** ~~~~~~~~~~~~~~~~~~~~~~~~~~*******************~~~~~~~~~~~~~~~~~~~~~~~~~~ **|
|** ~~~~~~~~~~~~~~~~~~~~~~~~~/                   \~~~~~~~~~~~~~~~~~~~~~~~~~ **|
|** ========================{ 1-800 Hotline Bling }======================== **|
|** ~~~~~~~~~~~~~~~~~~~~~~~~~\                   /~~~~~~~~~~~~~~~~~~~~~~~~~ **|
|** ~~~~~~~~~~~~~~~~~~~~~~~~~~*******************~~~~~~~~~~~~~~~~~~~~~~~~~~ **|
\** #########################[[[[[[[[[^_^]]]]]]]]]######################### **/



/** ======================================================================= **\
|** ------------------------------ Libraries ------------------------------ **|
\** ======================================================================= **/

#include <Adafruit_LEDBackpack.h>
#include <MomentaryButton.h>
#include <PinChangeInt.h>
#include <Motor.h>
#include <Adafruit_GFX.h>
#include <Buzzer.h>
#include <LEDArray.h>
#include <LED.h>
#include <Wire.h>


/** ======================================================================= **\
|** ---------------------------- Pin Constants ---------------------------- **|
\** ======================================================================= **/

#define MOTOR1_PWMA 3
#define MOTOR1_PWMB 5
#define MOTOR1_STBY 4
#define MOTOR1_AIN1 6
#define MOTOR1_AIN2 8
#define MOTOR1_BIN1 9
#define MOTOR1_BIN2 10
#define BUZZER1_1 11
#define LEDARRAY1_SDA A4
#define LEDARRAY1_SCL A5
#define MOMENTARYBUTTON1_SENSE 12
#define LED1_CONTROL 13
#define LED2_CONTROL A0
#define LED3_CONTROL A1
#define LED4_CONTROL A2

/** ======================================================================= **\
|** ------------------------- Object Declarations ------------------------- **|
\** ======================================================================= **/

Motor motor1(MOTOR1_PWMA, MOTOR1_PWMB, MOTOR1_STBY, MOTOR1_AIN1, MOTOR1_AIN2, MOTOR1_BIN1, MOTOR1_BIN2);
Buzzer buzzer1(BUZZER1_1);
LEDArray ledarray1(LEDARRAY1_SDA, LEDARRAY1_SCL);
MomentaryButton momentarybutton1(MOMENTARYBUTTON1_SENSE);
LED led1(LED1_CONTROL);
LED led2(LED2_CONTROL);
LED led3(LED3_CONTROL);
LED led4(LED4_CONTROL);

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
   ledarray1.setup();
   momentarybutton1.setup();
   led1.setup();
   led2.setup();
   led3.setup();
   led4.setup();
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
     led2.turnOn();
}