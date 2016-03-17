//Include arduPi library
//#pragma G++ diagnostic ignored "-fpermissive"
#include "arduPi.h"

/*********************************************************
 *  IF YOUR ARDUINO CODE HAS OTHER FUNCTIONS APART FROM  *
 *  setup() AND loop() YOU MUST DECLARE THEM HERE        *
 * *******************************************************/
#include "program.ino"

int main(){
    setup();
    while(1) {
      loop();
    }
    return (0);
}
