#include <iostream>
#include <string>

#include "lib/hello-greet.h"

using namespace std;

int main(int argc, char **argv) {
    string who = "world";
    if(argc > 1) {
        who = argv[1];
    }
    cout << get_greet(who) << endl;
    return 0;
}
