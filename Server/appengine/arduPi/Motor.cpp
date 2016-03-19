#include "Motor.h"

const int MAX_SPEED = 255;

Motor::Motor( int STBY, int PWMA, int AIN1, int AIN2,
              int PWMB, int BIN1, int BIN2) {
  this->STBY = STBY;
  this->PWMA = PWMA;
  this->AIN1 = AIN1;
  this->AIN2 = AIN2;
  this->PWMB = PWMB;
  this->BIN1 = BIN1;
  this->BIN2 = BIN2;
  _isMoving = false;
  polarity = 0;
}

void Motor::setup() {
  if(_disable)
    return;
  pinMode(this->STBY, OUTPUT);
  pinMode(this->PWMA, OUTPUT);
  pinMode(this->AIN1, OUTPUT);
  pinMode(this->AIN2, OUTPUT);
  pinMode(this->PWMB, OUTPUT);
  pinMode(this->BIN1, OUTPUT);
  pinMode(this->BIN2, OUTPUT);
}

void Motor::changePolarity()
{
 if(polarity == 0)
    polarity = 1;
 else
    polarity = 0;
}

void Motor::move(int motor, int speed=255, int direction=0) {
  if(_disable)
    return;
  
  digitalWrite(STBY, HIGH);
  bool inPin1 = LOW;
  bool inPin2 = HIGH;
  _isMoving = true;
  if(direction == 1) {
    inPin1 = HIGH;
    inPin2 = LOW;
  }
  if( motor == A ) {
    digitalWrite(AIN1, inPin1);
    digitalWrite(AIN2, inPin2);
    analogWrite(PWMA, speed);
  }
  else {
    digitalWrite(BIN1, inPin1);
    digitalWrite(BIN2, inPin2);
    analogWrite(PWMB, speed);
  }
}

void Motor::brake() {
  if(_disable)
    return;
  // stop();
  _isMoving = false;
  digitalWrite(AIN1, LOW);
  digitalWrite(AIN2, LOW);
  digitalWrite(BIN1, LOW);
  digitalWrite(BIN2, LOW);
}


void Motor::swapDirections() {
  int swap = A;
  A = B;
  B = swap;
}
void Motor::stop() {
  if(_disable)
    return;
  _isMoving = false;
  digitalWrite(STBY,LOW);
  move( A, 0, polarity);
  move( B, 0, polarity);
}

void Motor::forward()
{
  forward(MAX_SPEED);
}

void Motor::forward(int speed) {
  move( A, speed, polarity);
  move( B, speed, polarity);
}

void Motor::backward()
{
  backward(MAX_SPEED);
}

void Motor::backward(int speed) {
  if(polarity == 1) {
    move( A, speed, 0);
    move( B, speed, 0);
  }
  else {
    move( A, speed, 1);
    move( B, speed, 1);
  }
}

void Motor::spinRight()
{
   spinRight(MAX_SPEED);
}

void Motor::spinRight(int speed) {
  if(polarity == 0) {
    move( A, speed, _motorsSwapped ? 0 : 1);
    move( B, speed, _motorsSwapped ? 1 : 0);
  }
  else {
    move( A, speed, _motorsSwapped ? 1 : 0);
    move( B, speed, _motorsSwapped ? 0 : 1);
  }
}

void Motor::spinLeft()
{
     spinLeft(MAX_SPEED);
}

void Motor::spinLeft(int speed) {
  if(polarity == 1) {
    move( A, speed, _motorsSwapped ? 0 : 1);
    move( B, speed, _motorsSwapped ? 1 : 0);
  }
  else {
    move( A, speed, _motorsSwapped ? 1 : 0);
    move( B, speed, _motorsSwapped ? 0 : 1);
  }
}

void Motor::forwardAndRight() {
  forwardAndRight(MAX_SPEED);
}

void Motor::forwardAndRight( int speed ) {
  move( A, speed, polarity);
  move( B, speed/2, polarity);
}

void Motor::forwardAndLeft() {
  forwardAndLeft(MAX_SPEED);
}

void Motor::forwardAndLeft( int speed=MAX_SPEED ) {
  move( A, speed/2, polarity);
  move( B, speed, polarity);
}

bool Motor::isMoving() { return _isMoving; }

void Motor::disable(){
  _disable = true;
}


