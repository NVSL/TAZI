#include <iostream>
#include <cmath>
#include <stdlib.h>
using namespace std;
int main() {
   double item = 1;
  for(int i = 1; i<=(100); i+=(1)) {
    if((int)i % (int)5 == 0) {
      cout << (i) << endl;;
    };
   };
   return 0;
}
