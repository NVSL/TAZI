#ifndef MOMENTARY_BUTTON_INCLUDED
#define MOMENTARY_BUTTON_INCLUDED

#ifdef ARDUINO
#include "Arduino.h"
#include <PinChangeInt.h>   //Still need to #include in the main .ino code too
int8_t (*aInterrupt)(uint8_t, PCIntvoidFuncPtr, int) = PCintPort::attachInterrupt;
#else
void (*aInterrupt)(int, void (*f)(), Digivalue) = attachInterrupt;
#define CHANGE BOTH
#include "arduPi.h"
#endif

/**
 * Filename: MomentaryButton.h \n
 * Authors: Somebody at Arduino, Steve Swanson, Wei-Ping Liao, Paula Quach \n
 * Description: This button library keeps track of the current button state,
 * like whether it is pressed or not pressed and whether it had been so
 * previously. It allows the user to "read" the button's state for themself, but
 * provides easier interface with functions that inform the user directly
 * whether the button had been or is pressed or released. It also deals with
 * "bouncing" and making sure that what is read is not read multiple times.
 */

#define ACTIVE_PINS 20


class MomentaryButton {

    int isDown;
    int pin;

    static MomentaryButton *ptr[ACTIVE_PINS];

    private:
    uint8_t _pin;           //arduino pin number
    uint8_t _puEnable;      //internal pullup resistor enabled
    uint8_t _invert;        //if 0, interpret high state as pressed, else interpret low state as pressed
    uint8_t _state;         //current button state
    uint8_t _lastState;     //previous button state
    uint8_t _changed;       //state changed since last read
    uint8_t _wasPress;       //keeps track if button has been pressed since last check
    uint8_t _wasRelease;     //keeps track if button has been released since last check
    uint32_t _time;         //time of current state (all times are in ms)
    uint32_t _lastChange;   //time of last state change
    uint32_t _dbTime;       //debounce time

    public:
    MomentaryButton(int pin, int debounce_time = 200): pin(pin) {
        _pin = pin;
        _puEnable = 1;
        _invert = 1;
        _dbTime = debounce_time;
        pinMode(_pin, INPUT);
        if (_puEnable != 0)
            digitalWrite(_pin, HIGH);       //enable pullup resistor
        _state = digitalRead(_pin);
        if (_invert != 0) _state = !_state;
        _time = millis();
        _lastState = _state;
        _changed = 0;
        _lastChange = _time;

        if(pin >= 0 && pin < ACTIVE_PINS)
            ptr[pin] = this;
    }
    
   /**
     * waitForPress() blocks until button is pressed.
     */
    void waitUntilPressed ()
    {
        while (read() != 1);
    }

   /**
     * read() returns the state of the button, 1==pressed, 0==released,     
     * does debouncing, captures and maintains times, previous states, etc. 
     */
    uint8_t read()
    {
        static uint32_t ms;
        static uint8_t pinVal;

        ms = millis();
        pinVal = digitalRead(_pin);
        if (_invert != 0) pinVal = !pinVal;
        if (ms - _lastChange < _dbTime) {
            _time = ms;
            _changed = 0;
            return _state;
        }
        else {
            _lastState = _state;
            _state = pinVal;
            _time = ms;
            if (_state != _lastState)   {
                _lastChange = ms;
                _changed = 1;
            }
            else {
                _changed = 0;
            }
            return _state;
        }
    }

   /**
     * isPressed() checks the button state at the moment this method is     
     * called, and returns false (0) or true (!=0) if it is not or is       
     * pressed, respectively.                                               
     */
    uint8_t isPressed()
    {
        read();
        _wasPress = 0; //resets counter for if the button was pressed
        return _state == 0 ? 0 : 1;
    }


   /**
     * isReleased() checks the button state at the moment this method is    
     * called and depending on the state returns false (0) or true (!=0)    
     * accordingly.                                                         
     */
    uint8_t isReleased()
    {
        read();
        _wasRelease = 0; //resets counter for if the button was released
        return _state == 0 ? 1 : 0;
    }

   /**
     * wasPressed() checks the button state to see if it had been pressed   *
     * since the last time a press was checked for or since the last read   *
     * and returns false (0) or true (!=0) accordingly.                     *
     * This function does not cause the button to be read.                  *
     */
    uint8_t wasPressed()
    {
        int press = _wasPress;
        _wasPress = 0;  //reset counter
        return press;
    }

   /**
     * wasReleased() checks the button state to see if it had been released *
     * since the last time a press was checked for or since the last read   *
     * and returns false (0) or true (!=0) accordingly.                     *
     * This function does not cause the button to be read.                  *
     */
    uint8_t wasReleased()
    {
        int rel = _wasRelease;
        _wasRelease = 0;    //reset counter
        return rel;
    }

   /**
     * pressedFor(ms) checks to see if the button is pressed and how long   *
     * it has been in that state. Should it match the specified  time in    *
     * milliseconds, it returns false (0) or true (1) accordingly.          *
     */
    uint8_t pressedFor(uint32_t ms)
    {
        read();
        return (_state == 1 && _time - _lastChange >= ms) ? 1 : 0;
    }

   /**
     * releasedFor(ms) checks to see if the button is released and how long *
     * it has been in that state. Should it match the specified time in     *
     * milliseconds, it returns false (0) or true (1) accordingly.          *
     */
    uint8_t releasedFor(uint32_t ms)
    {
        read();
        return (_state == 0 && _time - _lastChange >= ms) ? 1 : 0;
    }

   /**
     * lastChange() returns the time the button last changed state,         *
     * in milliseconds.                                                     *
     */
    uint32_t lastChange()
    {
        return _lastChange;
    }

    /** Sets the debounce time for when reading the button */
    void setDB(uint32_t ms)
    {
        _dbTime = ms;
    }

   /**
     * Setup takes the calling button's pin and assigns an interrupt to     *
     * that pin to keep a watch on its changes (pressed or released).       *
     */
    void setup() {
        switch (_pin)
        {
            case 3:
                aInterrupt(_pin, pin3rupt, CHANGE); break;
            case 4:
                aInterrupt(_pin, pin4rupt, CHANGE); break;
            case 5:
                aInterrupt(_pin, pin5rupt, CHANGE); break;
            case 6:
                aInterrupt(_pin, pin6rupt, CHANGE); break;
            case 8:
                aInterrupt(_pin, pin8rupt, CHANGE); break;
            case 9:
                aInterrupt(_pin, pin9rupt, CHANGE); break;
            case 10:
                aInterrupt(_pin, pin10rupt, CHANGE); break;
            case 11:
                aInterrupt(_pin, pin11rupt, CHANGE); break;
            case 12:
                aInterrupt(_pin, pin12rupt, CHANGE); break;
            case 13:
                aInterrupt(_pin, pin13rupt, CHANGE); break;
            #ifdef ARDUINO
            case A0:
                aInterrupt(_pin, pinA0rupt, CHANGE); break;
            case A1:
                aInterrupt(_pin, pinA1rupt, CHANGE); break;
            case A2:
                aInterrupt(_pin, pinA2rupt, CHANGE); break;
            case A3:
                aInterrupt(_pin, pinA3rupt, CHANGE); break;
            case A4:
                aInterrupt(_pin, pinA4rupt, CHANGE); break;
            case A5:
                aInterrupt(_pin, pinA5rupt, CHANGE); break;
            #endif
            default:
                break;
        }
    }

    /** Default loop method tells whether the button was pressed */
    void loop() {
        if (wasPressed()) {
            Serial.println("button pressed");
        }
    }

    private:
    //Called when there is an interrupt, the button makes a note whether it
    //was pressed or released.
    void myrupt()
    {
        if (millis() - _lastChange > _dbTime) {
            read();

            if(_state == 0)
            {
                _wasRelease = 1;
            }
            else
            {
                _wasPress = 1;
            }
        }
    }

    /*----------------------------------------------------------------------*
     * pin<number>rupt calls the corresponding pin's interrupt method       *
     *----------------------------------------------------------------------*/
    static void pin3rupt()
    {
        ptr[3]->myrupt();
    }

    static void pin4rupt()
    {
        ptr[4]->myrupt();
    }

    static void pin5rupt()
    {
        ptr[5]->myrupt();
    }

    static void pin6rupt()
    {
        ptr[6]->myrupt();
    }

    static void pin8rupt()
    {
        ptr[8]->myrupt();
    }

    static void pin9rupt()
    {
        ptr[9]->myrupt();
    }

    static void pin10rupt()
    {
        ptr[10]->myrupt();
    }

    static void pin11rupt()
    {
        ptr[11]->myrupt();
    }

    static void pin12rupt()
    {
        ptr[12]->myrupt();
    }

    static void pin13rupt()
    {
        ptr[13]->myrupt();
    }

    #ifdef ARDUINO
    static void pinA0rupt()
    {
        ptr[A0]->myrupt();
    }

    static void pinA1rupt()
    {
        ptr[A1]->myrupt();
    }

    static void pinA2rupt()
    {
        ptr[A2]->myrupt();
    }

    static void pinA3rupt()
    {
        ptr[A3]->myrupt();
    }

    static void pinA4rupt()
    {
        ptr[A4]->myrupt();
    }

    static void pinA5rupt()
    {
        ptr[A5]->myrupt();
    }
    #endif
};
MomentaryButton *MomentaryButton::ptr[ACTIVE_PINS];  //Outside declaration needed for ptr array to work
#endif


