#include <assert.h>
#include <stdio.h>
#include <unistd.h>  // write()

// NOTE: This has a copy of stringpiece.h too.
#include "re2/re2.h"

int main(int argc, char **argv) {
  if (argc != 3) {
    printf("Expected pattern and filename\n");
    return 1;
  }

  char* pat = argv[1];

  FILE *f = fopen(argv[2], "rb");
  if (!f) {
    printf("Error opening %s\n", argv[1]);
    return 1;
  }

  fseek(f, 0, SEEK_END);
  size_t num_bytes = ftell(f);
  fseek(f, 0, SEEK_SET);  //same as rewind(f);

  int fd = fileno(f);

  char* buf = (char*)malloc(num_bytes);
  size_t num_read = read(fd, buf, num_bytes);
  assert(num_read == num_bytes);

  //fprintf(stderr, "pat = %s\n", pat);

  re2::StringPiece input(buf, num_bytes);
  re2::RE2 re(pat);
  assert(re.ok());

  // This loop modifies the input.
  // Have to read the header.
  // https://github.com/google/re2/wiki/CplusplusAPI
  int num_matches = 0;
  while (re2::RE2::FindAndConsume(&input, re)){
    num_matches++;
  }

  fprintf(stderr, "num_matches = %d\n", num_matches);
  fprintf(stderr, "num_bytes = %zu\n", num_bytes);
  free(buf);

  return num_matches ? 0 : 1;
}
