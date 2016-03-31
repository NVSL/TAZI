#include <iostream>
#include <cmath>
#include <stdlib.h>
using namespace std;
int main() {
   double item = 0;
  while((int)item % (int)10 != 0) {
    int item = item + 4;
  };
  cout << (item) << endl;;
   return 0;
}
