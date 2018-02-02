#!/usr/bin/perl -w

# https://www.reddit.com/r/oilshell/comments/7tqs0a/why_create_a_new_unix_shell/dtml31j/

use strict;
use English;
use autodie;

sub f {
  print "--\n";
  open(my $h,"ls / |");
  print (<$h>);
  print "--\n";
}

open(my $o,">out.txt");
select $o;
f();

open($o,"| wc -l ");
select $o;
f();
