#include <iostream>
#include <cmath>
#include <stdlib.h>
using namespace std;
int main() {
   for(int i = 1; i<=(10); i+=(1)) {
    cout << (rand() % (100 - 1) + 1) << endl;
   };
   return 0;
}
