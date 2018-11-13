#include <assert.h>
#include <stdio.h>

#include <string>

// NOTE: This has a copy of stringpiece.h too.
#include "re2/re2.h"

using std::string;

int main() {
  // Successful parsing.
  int i;
  string s;
  assert(RE2::FullMatch("ruby:1234", "(\\w+):(\\d+)", &s, &i));
  assert(s == "ruby");
  assert(i == 1234);

  printf("Matches: %s %d\n", s.c_str(), i);
}
