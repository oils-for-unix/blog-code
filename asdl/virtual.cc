#include <assert.h>
#include <stdio.h>

// Base type
class obj_t {
 public:
  int type_id;
};

// Common attributes
class attrs {
 public:
  int lineno;
  int col;
};

class word_part_t : virtual obj_t, virtual  attrs {
};

class expr_t : virtual obj_t, virtual attrs {
};

class SingleQuoted : virtual expr_t, virtual word_part_t {
};

// This doesn't work!
class DoubleQuoted : virtual expr_t, virtual word_part_t {
};


int main(int argc, char **argv) {
  DoubleQuoted dq;

  // This doesn't even work
  dq.type_id = 42;

  // Doesn't work because
  //dq.lineno = 1;
  //dq.col = 2;

  // This would print 16!!!
  printf("dq = %zu\n", sizeof(dq));
}
