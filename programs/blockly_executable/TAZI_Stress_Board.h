#ifndef TAZI_STRESS_BOARD_H
#define TAZI_STRESS_BOARD_H

#include "Gadgetron.h"


LEDArray display;

#define DRIVE_STBY 8        
#define DRIVE_PWMA 5        
#define DRIVE_AIN1 9        
#define DRIVE_AIN2 10        
#define DRIVE_PWMB 6        
#define DRIVE_BIN1 11        
#define DRIVE_BIN2 12        
Motor drive(DRIVE_STBY,DRIVE_PWMA,DRIVE_AIN1,DRIVE_AIN2,DRIVE_PWMB,DRIVE_BIN1,DRIVE_BIN2);

#define BUTTON_SENSE 13        
MomentaryButton button(BUTTON_SENSE);

#define LED_CONTROL A0        
LED led(LED_CONTROL);

#define LED_2_CONTROL A1        
LED led_2(LED_2_CONTROL);

#define SERVO_DATA 3        
ServoMotor Servo(SERVO_DATA);

#define BUZZER_1 4        
Buzzer buzzer(BUZZER_1);


#endif