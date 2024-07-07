#!/usr/bin/env nodejs

// Rough idea to explain semantics of:
//
// $ seq 3
// 0
// 1
// 2

// $ seq 3 | jq 'def inc(n): . + n; inc(3) | inc(-1)'
// 3
// 4
// 5

function inc(n) {
  return function (dot) {
    return dot + n;
  }
}

// function composition operator
//
// (f o g)(x) = f(g(x))
//
// This doesn't take into account that | is "cartesian product" in jq.

function pipe(f, g) {
  return function(dot) {
    return f(g(dot))
  }
}

console.log(42);

var inc3 = inc(3);

console.log("inc3", inc3(42));

var dec = inc(-1);

console.log("dec(inc3( ))", dec(inc3(42)));

var composed = pipe(inc3, dec);

console.log("composed", composed(42));

var composed2 = pipe(composed, dec);

console.log("composed2", composed2(42));

