/*************************************************************************
	> File Name: hello-time.cpp
	> Author: 
	> Mail: 
	> Created Time: 2017年03月22日 星期三 20时27分20秒
 ************************************************************************/

#include <iostream>
#include "source/hello-time.h"
#include <ctime>

using namespace std;


void print_localtime() {
    time_t res = time(nullptr);
    cout << asctime(localtime(&res));
}
