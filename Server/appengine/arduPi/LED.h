#ifndef LED_INCLUDED
#define LED_INCLUDED

#ifdef ARDUINO
#include "Arduino.h"
#endif

class LED {
    enum {ON, OFF};    //For state stuff

    int pin;   //The pin the LED is connected to
    int onTime;    //The time for the LED to be on during blinking
    int offTime;   //The time for the LED to be off during blinking
    int state;     //The LED's current state (on or off)
    bool blinking; //Whether the LED is 
    unsigned long nextTransition;  //when the next transition time should be when blinking

    public:

    //Constructor that assigns LED pin, etc.
    LED(int pin): 
        pin(pin), 
        onTime(onTime), 
        offTime(offTime) {
            pinMode(pin, OUTPUT);
            digitalWrite(pin, LOW);
            state = OFF;
            blinking = false;
        }

    /** update() checks whether the LED should change states or not depending *
     * on whether it is blinking                                              *
     */
    void update() {
        if (blinking == true) {
            if (millis() > nextTransition) {
                toggle();
                if (state == OFF)
                {
                    nextTransition = millis() + offTime;
                }
                else if (state == ON)
                {
                    nextTransition = millis() + onTime;
                }
            }
        }
    }

    // blink turns the LED on and off in specified intervals
    void blink(int on, int off) {
        onTime = on;
        offTime = off;
        blink();
    }

    // Default blink causes the blink method to occur consistently
    void blink() {
        blinking = true;
        nextTransition = millis() + onTime;
    }

    //Returns whether the LED is in a blinking state or not
    bool isBlinking() {
        return blinking;
    }

    //Turns the LED to the state opposite of what it currently is
    void toggle() {
        if (state == ON) {
            turnOff();
        } else if (state == OFF) {
            turnOn();
        }
    }

    //Turns on the LED
    void turnOn() {
        state = ON;
        digitalWrite(pin, HIGH);
    }

    //Turns off the LED
    void turnOff() {
        state = OFF;
        digitalWrite(pin, LOW);
    }

    //Basic setup causes the LED to blink in 500 ms intervals
    void setup() {
        blink(500, 500);
    }

    //Default loop continues the blinking from default setup
    void loop() {
        update();
    }
};
#endif
