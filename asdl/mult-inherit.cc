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

class word_part_t : public obj_t, public attrs {
};

class expr_t : public obj_t, public attrs {
};

class SingleQuoted : public expr_t, public word_part_t {
 public:
};

// This doesn't work!
class DoubleQuoted : public expr_t, public word_part_t {
};


int main(int argc, char **argv) {
  DoubleQuoted dq;

  // Doesn't work because
  dq.lineno = 1;
  dq.col = 2;

  // This would print 16!!!
  printf("dq = %zu\n", sizeof(dq));
}
