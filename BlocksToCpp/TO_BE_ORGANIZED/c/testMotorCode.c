#include <iostream>
#include <cmath>
#include <stdlib.h>
using namespace std;

#include "Motor.h"

 Motor motor1(1,2,3,4,5,6,7);

void loop () {
  motor1.forward();
};

