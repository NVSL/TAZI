#ifndef GRABBER_SENSOR_3_H 
#define GRABBER_SENSOR_3_H

/** ======================================================================= **\
|** ------------------------------ Libraries ------------------------------ **|
\** ======================================================================= **/
#include "Gadgetron.h"

/** ======================================================================= **\
|** ---------------------------- Pin Constants ---------------------------- **|
\** ======================================================================= **/
#define PINCER_DATA 3        
#define SERVO_DATA 4        
#define DISTANCESENSOR_A A0        
#define BUMP_SENSE 8        
#define BUMP_2_SENSE 9        
#define BUTTON_SENSE 10        
#define DRIVE_STBY 11        
#define DRIVE_PWMA 5        
#define DRIVE_AIN1 12        
#define DRIVE_AIN2 13        
#define DRIVE_PWMB 6        
#define DRIVE_BIN1 A1        
#define DRIVE_BIN2 A2

/** ======================================================================= **\
|** ------------------------- Object Declarations ------------------------- **|
\** ======================================================================= **/
ServoMotor Servo(SERVO_DATA); 
DistanceSensor distanceSensor(DISTANCESENSOR_A);
MomentaryButton bump(BUMP_SENSE);
MomentaryButton bump_2(BUMP_2_SENSE);
MomentaryButton button(BUTTON_SENSE);      
Pincer pincer(PINCER_DATA);
Motor drive(DRIVE_STBY,DRIVE_PWMA,DRIVE_AIN1,DRIVE_AIN2,DRIVE_PWMB,DRIVE_BIN1,DRIVE_BIN2);


#endif
