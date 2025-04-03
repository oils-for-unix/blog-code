Forth-Style
==================

Is forth-style useful / nice?

This is arguably nice / interesting:

    #.ysh
    for x in *.py {
      echo $x
    }

vs

    #.catbrain
    glob '*.py'  # push an array on the stack
    foreach {    # make each element on array top of stack
      echo       # print it
    }


Destructuring assignment

    #.ysh
    yblocks capture (&r) {
      echo hi
    }
    echo $[r.status] $[r.stderr]

vs. 

    #.catbrain
    yblocks capture {
      echo hi
    }
    assign status stderr
    echo $status $stderr

The code isn't strictly shorter, but it is kinda easy to type and
"concatenative" / "ordered".
