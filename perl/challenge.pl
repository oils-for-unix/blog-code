#!/usr/bin/perl -w

# https://www.reddit.com/r/oilshell/comments/7tqs0a/why_create_a_new_unix_shell/dtml31j/

use strict;
use English;
use autodie;

sub f { open(my $h,"/bin/ls $_[0]|") ; print "--\n",(<$h>),"--\n";}

open(my $o,">/tmp/out.txt") ; select $o ; f("/tmp") ;
open($o,"| wc -l ")         ; select $o ; f("/tmp") ;
