#include <iostream>
#include <cmath>
#include <stdlib.h>
using namespace std;
int main() {
   double item = 1;
  for(int i = 1; i<=(10); i+=(1)) {
    int item = i * 2;
    if(item % 10 == 0) {
      cout << (item) << endl;
    };
   };
   return 0;
}
