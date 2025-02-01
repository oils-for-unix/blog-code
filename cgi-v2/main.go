// main.go
package main

/*
#include "fib.h"
import "C"
*/

import "fmt"

// Note: NO cgo import "C" here!
func compute_fib(n int32) uint64 // This declares the C function

func main() {
    // Test different Fibonacci numbers
    numbers := []int{0, 1, 10, 20, 30, 40, 50}
    
    for _, n := range numbers {
        // result := C.compute_fib(C.int(n))
        result := compute_fib(int32(n))
        fmt.Printf("Fibonacci(%d) = %d\n", n, uint64(result))
    }
}

