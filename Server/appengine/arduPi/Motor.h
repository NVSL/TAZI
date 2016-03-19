#ifndef MOTOR_H
#define MOTOR_H

#ifdef ARDUINO
#include <Arduino.h>
#else
#include "arduPi.h"
#endif
/**
 * Filename: Motor.h 
 *Author: Michael Gonzalez 
 * Description: This class controls the Sparkfun Motor Driver TB6612FNG. It\n
 * provides methods to move the motors forward and backwards, to spin left\n
 * and right, to stop the motors, and to provide information about the motor\n
 * driver's state.
 */
class Motor
{
   public:
      /**
	   * This is the constructor to make your motor.
	   * The arguments are the various pins that your motor connects to on its 
	   * board.
	   */
      Motor( int STBY, int PWMA, int AIN1, int AIN2, 
             int PWMB, int BIN1, int BIN2); 
	  /**
	   * Move the motors forward at full speed
	   */
      void forward();
	  /**
	   * Move the motors forward at a definable speed. \n
	   * Valid input range is 0 (Slowest Speed/Stopped) to 255 (Fastest Speed)
	   */
      void forward(int speed);
	  /**
	   * Move the motors backwards at full speed
	   */
      void backward();
	  /**
	   * Move the motors backwards at a definable speed.\n
	   * Valid input ranges 0 (Slowest Speed/Stopped) to 255 (Fastest Speed)
	   */
      void backward(int speed);
	  /**
	   * Move the motors to spin a gadget full speed to the left
	   */
      void spinLeft();
	  /**
	   * Move the motors to spin a gadget at a definable speed to the left.\n
	   * Valid input ranges from 0 (Slowest Speed/Stopped) to 255 (Fastest Speed)
	   */
      void spinLeft(int speed);
	   /**
	   * Move the motors to spin a gadget full speed to the right
	   */
      void spinRight();
	  /**
	   * Move the motors to spin a gadget at a definable speed to the right.\n
	   * Valid input ranges from 0 (Slowest Speed/Stopped) to 255 (Fastest Speed)
	   */
      void spinRight(int speed);
	  /**
	   * Move the motors forward while drifting to the right at top speed.\n
	   * WARNING: This function is still in testing and is not guaranteed 
	   * to work
	   */
      void forwardAndRight();
	  /**
	   * Move the motors forward while drifting to the right at a definable 
	   * speed.\n
	   * WARNING: This function is still in testing and is not guaranteed 
	   * to work
	   */
      void forwardAndRight(int speed);
	  /**
	   * Move the motors forward while drifting to the left at top speed.\n
	   * WARNING: This function is still in testing and is not guaranteed 
	   * to work
	   */
      void forwardAndLeft();
	  /**
	   * Move the motors forward while drifting to the left at a definable 
	   * speed.\n
	   * WARNING: This function is still in testing and is not guaranteed 
	   * to work
	   */
      void forwardAndLeft(int speed);
	  /**
	   * Sets the motors up to run. This method must be called before use!
	   */
      void setup();
	  /**
	   * Sends the stop signal to the motors
	   */
      void stop();
	  /**
	   * Sends the stop signal to the motors and lowers movement pins
	   */
      void brake();
	  /**
	   * Returns true if the motors are running, else false
	   */
      bool isMoving();
	  /**
	   * Changes spinLeft to spinRight and spinRight to spinLeft
	   */
      void swapDirections();
      int STBY, PWMA, AIN1, AIN2, PWMB, BIN1, BIN2;
	  /**
	   * Changes forward to backward and backward to forward
	   */
      void changePolarity();
      

      //Prevent the motor pins from doing anything
      //Call before setup()
      void disable();   
  private:
      void move(int motor, int speed, int direction);
      int A = 1;
      int B = 0;
      int polarity;
      bool _isMoving;
      bool _motorsSwapped = false;


      //Deactivates all pins associated with the motor
      //No pinMode, no digitalWrites, no analogWrites
      //For serial debugging when there are pin conflicts
      bool _disable = false;

};
#endif
