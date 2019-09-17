#include <assert.h>
#include <stdio.h>

// This isn't a base type of anything, because otherwise we would have the
// diamond inheritance problem.
class tagged {
 public:
  int tag;
};

// Need reinterpret_cast since we're avoiding multiple inheritance of
// fields (which is apparently solved by virtual inheritance, but I can't
// get it to work.)

#define TAG(node) (reinterpret_cast<tagged*>(node)->tag)

// Empty sum types.  They have to be empty to avoid the diamond inheritance
// problem.
class word_part_t {};
class expr_t {};

// Tag definitions.
namespace expr_e {
  const int DoubleQuoted = 42;
};
namespace word_part_e {
  const int DoubleQuoted = 42;  // Same!
};

class double_quoted : public expr_t, public word_part_t {
 public:
  double_quoted(int payload) : tag(42), payload(payload) {}

  int tag;
  int payload;
};

void f(expr_t* e) {
  printf("f() e.tag = %d\n", TAG(e));

  switch (TAG(e)) {
    case expr_e::DoubleQuoted: {
      double_quoted* dq = static_cast<double_quoted*>(e);
      printf("payload = %d\n", dq->payload);
      break;
    }
    default:
      printf("other\n");
      break;
  }
}

void g(word_part_t* part) {
  printf("g() part.tag = %d\n", TAG(part));

  switch (TAG(part)) {
    case word_part_e::DoubleQuoted: {
      double_quoted* dq = static_cast<double_quoted*>(part);
      printf("payload = %d\n", dq->payload);
      break;
    }
    default:
      printf("other\n");
      break;
  }
}

int main(int argc, char **argv) {
  double_quoted dq(123);
  printf("dq = %zu\n", sizeof(dq));
  printf("dq tag = %d\n", dq.tag);

  printf("---\n");
  f(&dq);

  printf("---\n");
  g(&dq);
}
