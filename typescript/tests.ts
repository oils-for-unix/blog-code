// Run with ./run.sh tests --filter Lex ,etc.
import {
  DYNAMIC,
  TRACE_EVAL,
  TRACE_LEX,
  TRACE_PARSE,
  TRACE_TRANSFORM,
  TRACE_TYPE,
} from './yaks.ts';

import { run } from './main.ts';

// I kinda don't like this, but it's just for testing
import {
  assert,
  assertEquals,
} from 'https://deno.land/std@0.198.0/assert/mod.ts';

let log = console.log;

// No errors in lexing, but BAD token causes Parse error
Deno.test(function testLex() {
  let flags = TRACE_LEX;

  // Bad characters
  run('~', flags);
  run('42 ! bob', flags);

  // Success
  let actual = run(
    `
  ( +    # operator
    40   # 2 operatns
    2
  )`,
    flags,
  );

  assert(actual !== undefined);
  assertEquals(42, actual.value);
});

// 5 different parse errors
Deno.test(function testParse() {
  let flags = TRACE_PARSE;

  // Unexpected EOF
  run('', flags);

  // Unexpected )
  run('[ foo )', flags);

  // Unexpected ]
  run(']', flags);

  // Expected Symbol after )
  run('( 42 )', flags);

  // Extra tokens
  run('42 43', flags);

  let actual = run('(* 3 (+ 1 2))', flags);
  assert(actual !== undefined);
  assertEquals(9, actual.value);
});

// 3 possible transform errors
Deno.test(function testTransform() {
  let flags = TRACE_TRANSFORM;

  // Invalid node
  run('(zz true 1 2)', flags);

  // If arity 3
  run('(if true 1)', flags);

  // + arity 2
  run('(+ 3)', flags);

  run('(+ 3 a)', flags);

  // MULTIPLE transform errors
  run('(+ (foo x) (if x))', flags);

  // Success
  run('(if (== 1 1) 42 43)', flags);

  let actual = run('(+ 2 3)', flags);
  assert(actual !== undefined);
  assertEquals(5, actual.value);
});

// 4 possible type errors
Deno.test(function testTypeCheck() {
  let flags = TRACE_TYPE;

  // If condition not boolean
  run('(if 0 42 43)', flags);

  // If branches don't match
  run('(if true 42 false)', flags);

  // operands don't match
  run('(== 3 (== 1 1))', flags);

  // MULTIPLE type errors
  run('(if 0 42 false)', flags);

  let actual = run('(+ true true)', flags);
  assert(actual === undefined);

  actual = run('(+ 10 true)', flags);
  assert(actual === undefined);

  actual = run('(if true true false)', flags);
  assert(actual !== undefined);
  assert(actual !== null);
  assertEquals(true, actual.value);
});

// 1 runtime error
Deno.test(function testEval() {
  let flags = TRACE_EVAL;

  // BAD!!  Dynamic typing lets this through
  // Need to add argument checking.  'a' is type 'symbol' for now, not string
  let actual = run('(+ a b)', flags | TRACE_PARSE | TRACE_TRANSFORM);
  assertEquals(undefined, actual);

  // divide by zero
  actual = run('(/ 42 0)', flags);
  assertEquals(undefined, actual);

  // Bug
  actual = run('(== 5 (+ 2 3))', flags);
  assert(actual !== undefined);
  assertEquals(true, actual.value);

  actual = run('(or (== 3 4) (== 5 5))', flags);
  assert(actual !== undefined);
  assertEquals(true, actual.value);
});

// TODO: Disable type checking and hit dynamic errors
Deno.test(function testDynamic() {
  let flags = DYNAMIC;
  run('(+ true true)', flags);
  run('(+ 42 (== 1 1))', flags);

  run('(== true 42)', flags);
  run(
    `
    (and
       (== 3 3)
       42
    )
  `,
    flags,
  );
});
