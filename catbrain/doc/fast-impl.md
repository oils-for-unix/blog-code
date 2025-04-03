
## Fast C Implementation

### 2025

I think it should be 

- Cheney collector
- not sure about integers as pointers
  - because that reduces the small strings to 4 bytes, instead of 8
    - 1 byte for header
    - so is that 2 or 3 bytes for payload?
    - leave off NUL terminator in small case?  Because C APIs can just copy it trivially?
      - although then it's not GC-managed, hm, ownership becomes an issue
    - would be nicer to have 6 bytes
  - and I think to send to untrusted processes, you need a validation step
  - you can't just memcpy()

- BUT WINDOWS processes are trusted
  - so in that case you can memcpy
  - and maybe you can cache on disk, not sure if that's safe

### Does catbrain have an AST?

- In addition to the CST / "token tree"
  - Rhombus language has it

- this would reduce work at runtime

- Rhombus also says there is a  "Macro loop" from AST to CST
  - it's not just CST rewriting, or AST rewriting

Example:

    if test -f / { 
        echo file
    } elif test -f z {
        echo fo
    } else {
        echo hi
    }

and then

    case %x {
      glob '*.py' {
        echo python
      }
    }

the problem is that you don't want to spend time at runtime parsing this

It's the CST/reader layer

### Could have bytecode like tinypy

Tnen it would need an AST, for all the control flow:

- for while
  - break continue
- if case
- try error
- fn

Although then it wouldn't be as extensible/programmable?

## 2024 Notes

- Hm should have immediate string / small string optimization
  - everything is either Str or List[str] - following shell

- if you really wanted to be ambitious, you could do a Cheney collector
  - revive the old one
  - however I think it's better to start with the global vars

Notes:

    struct VM {
      Pair* stack;
      Pair* top;
      int counter;
      bool eof;
    };

    struct Str {
      int len;
      char* data;
    };

    struct Pair {
      // remember in Yaks this wasn't a string?  You could could have ((f 42) 43)
      Str* head;
      Pair* next;
    };

### ERRORS in C implementation

- Out of stack space - well this is realy a heap
  - make it as long as argv?
- Code is too big - maybe make it 4096 bytes or something?

## Benchmarks

- TODO: Benchmark vs. Femtolisp
  - which uses tagged values
  - and Cheney GC

(unlike CPython or Lua -- both of them use pointers, and non-moving GC)
