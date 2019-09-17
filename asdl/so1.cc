#include <assert.h>
#include <stdio.h>

struct Base
{
    Base(int x) 
        : x(x)
    {}
    virtual ~Base() = default;
    int x;
};

struct Left : virtual Base
{
    Left() : Base(1)
    {}
};

struct Right : virtual Base
{
    Right() : Base(2)
    {}
};

/*
// This does not compile.
struct Down : Left, Right
{
    Down() : Left(), Right()
    {}
};
*/

// Hooray, this version compiles.
struct Down : Left, Right
{
    Down() : Base(123), Left(), Right()
    {}
};

int main(int argc, char **argv) {
  Down d;

  printf("d tag = %d\n", d.x);

  // 32 bytes!!!  Not OK.  Also requires the C++ runtime library with
  // -lstdc++.
  printf("sizeof(d) = %d\n", sizeof(d));
}
