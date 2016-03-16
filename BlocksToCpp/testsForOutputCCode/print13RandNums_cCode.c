#include <iostream>
#include <cmath>
#include <stdlib.h>
using namespace std;
int main() {
   double item = 0;
  while(item != 13) {
    int item = item + 1;
    cout << (rand() % (100 - 1) + 1) << endl;
  };
   return 0;
}
