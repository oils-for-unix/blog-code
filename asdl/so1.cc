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
    Down() : Base(42), Left(), Right()
    {}
};

int main(int argc, char **argv) {
  Down d;

  // This would print 16!!!
  printf("d = %zu\n", sizeof(d));
  printf("d tag = %d\n", d.x);
}
