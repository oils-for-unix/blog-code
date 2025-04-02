
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

### 2024 Notes

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
