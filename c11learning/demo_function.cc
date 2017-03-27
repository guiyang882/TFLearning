#include <iostream>
#include <functional>
#include <map>

using namespace std;

int add(int a, int b) {
	return a+b;
}

auto mod=[](int a, int b) {
	return a%b;
};

struct divide {
	int operator()(int m, int n) {
		return m / n;
	}
};

// a wrapper about the some different funs
map<string, function<int(int, int)>> funs = {
	{"+", add},
	{"-", std::minus<int>()},
	{"/", divide()},
	{"*", [](int i, int j) {
		return i*j;
	}},
	{"%", mod},
};

//使用function的引用来保存函数对象
class CAdd {
public:
	CAdd():m_nSum(0) { };

	// CAdd(const CAdd &) = delete;
	CAdd & operator=(const CAdd &) = delete;

	int operator()(int i) {
		m_nSum += i;
		return m_nSum;
	}

	int Sum() const {
		return m_nSum;
	}

private:
	int m_nSum;
};

int main() {

	function<int(int, int)> func1 = add;
	function<int(int, int)> func2 = divide();
	function<int(int, int)> func3 = mod;

	cout << func1(5,6) << endl;
	cout << func2(5,6) << endl;
	cout << func3(5,6) << endl;
	cout << funs["+"](4, 6) << endl;

	CAdd cAdd;
	function<int(int)> funcAdd1 = cAdd;
	function<int(int)> funcAdd2 = cAdd;
	cout << funcAdd1(10) << endl; // 10
	cout << funcAdd2(10) << endl; // 10
	cout << cAdd.Sum() << endl; // 0

	//将同一个函数对象赋值给了两个function，然后分别调用这两个function，但函数中的成员变量的值没有保存，问题在哪里？
	//因为function的缺省行为是拷贝一份传递给它的函数对象，于是f1,f2中保存的都是cAdd对象的拷贝。
	function<int(int)> funcAdd3 = ref(cAdd);
	function<int(int)> funcAdd4 = ref(cAdd);
	cout << funcAdd3(10) << endl; // 10
	cout << funcAdd4(10) << endl; // 20
	cout << cAdd.Sum() << endl; // 20

	return 0;
}