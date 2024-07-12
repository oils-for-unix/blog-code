Shell vs. Catbrain
==================

Simple Commands:

    # echo hi

    w-line hi

Assignment:

    # a=b

    # doesn't exist yet
    setvar a b
    setvar x { echo hi }  # does this make sense?  It's a block?

I guess variables do not.

Interpolation

    # echo $x

    # doesn't exist
    echo $x

Pipeline:

    # echo hi | wc -l

    pipeline {
      echo hi
      wc -l
    }

Command Sub:

    x=$(echo hi)

    capture { w-line hi }
    set x   # this kinda makes sense

Shelling Out:

    # sh -c 'ls | wc -l'

    sh 'ls | wc -l'

    # Hm I wonder if we also have
    capture-stdout 'ls | wc -l'

    ysh 'ls | wc -l'


## Iteration

    for-line {
      w
    }

    for {
      w
    }

## Conditional

    if empty {
      break
    }

## Functions / Macros

Not done:

    def f {
      w-line foo
      w-line bar
    }

    def f a b c {  # are these the things on the stack?
      w '['
      w $x
      w ']'
    }

So

    f foo

is short for

    const foo
    f

It's like passing args.  Hm.

## YSH

Error handling:

   try {
     sh false
   }
   if failed {
     w-line 'failed'
   }
   # yes this failed!

Hay:

   Package cpython {
     version '3.12'
     url 'https://python.org/'
   }

   # no integer literals, bool litearls, etc.
   Package cpython {
     version '3.12'
     url 'https://python.org/'
   }
