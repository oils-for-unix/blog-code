// fib.c
#include "fib.h"

unsigned long long compute_fib(int n) {
    if (n <= 1) return n;
    
    unsigned long long prev = 0;
    unsigned long long curr = 1;
    
    for(int i = 2; i <= n; i++) {
        unsigned long long next = prev + curr;
        prev = curr;
        curr = next;
    }
    
    return curr;
}

