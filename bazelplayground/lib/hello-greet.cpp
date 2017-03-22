/*************************************************************************
	> File Name: hello-greet.cpp
	> Author: 
	> Mail: 
	> Created Time: 2017年03月22日 星期三 20时29分58秒
 ************************************************************************/

#include <iostream>
#include <string>
#include "lib/hello-greet.h"

using namespace std;

string get_greet(const string &thing) {
    return "Hello " + thing;
}
