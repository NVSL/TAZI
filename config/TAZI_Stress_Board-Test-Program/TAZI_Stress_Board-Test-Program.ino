#include <Servo.h>
#include "TAZI_Stress_Board.h"

void setup()
{
  Serial.begin(9600);
  display.setup();
  drive.setup();
  button.setup();
  led.setup();
  led_2.setup();
  Servo.setup();
  buzzer.setup();
  
}

void loop()
{
  Serial.println("Testing display...");
  
  	display.clear();
  	display.drawCircle(3,3, 3);
        Serial.println("Testing drive...");
  
  drive.spinLeft();
  delay(1000);
  drive.spinRight();
  delay(1000);
        Serial.println("Testing button...");
  
  
  	for (int c = 0; c < 500; c++) {
  	     char str[50];
  	     sprintf(str, "button: pressed = %s", button.isPressed() ? "yes" : "no");
  	     Serial.println(str);
  	     delay(1);
  	}
        Serial.println("Testing led...");
  
  led.turnOn();
  delay(1000);
  led.turnOff();
  delay(1000);
          Serial.println("Testing led_2...");
  
  led_2.turnOn();
  delay(1000);
  led_2.turnOff();
  delay(1000);
          Serial.println("Testing buzzer...");
  
  	buzzer.playNote(NOTE_A4,300);
  	delay(300);
  	buzzer.playNote(NOTE_B4,300);
  	delay(300);
  	buzzer.playNote(NOTE_C4,300);
  	delay(300);
        
}