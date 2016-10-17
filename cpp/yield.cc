#include <boost/asio/yield.hpp>
#include <boost/asio/coroutine.hpp>
#include <iostream>

boost::asio::coroutine c;

void foo(int i)
{
    reenter(c)
    {
        yield std::cout<<"foo1 "<<i<<std::endl;
        fork foo(100);
        yield std::cout<<"foo2 "<< i+1<<std::endl;
    }
}
int main()
{
    foo(1);
    foo(2);
    foo(3);
    return 0;
}
