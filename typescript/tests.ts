// Run with ./run.sh tests --filter Lex ,etc.
import { lex } from './lex.ts';
import {
  run,
  TRACE_EVAL,
  TRACE_LEX,
  TRACE_PARSE,
  TRACE_TRANSFORM,
  TRACE_TYPE,
} from './main.ts';

// I kinda don't like this, but it's just for testing
import {
  assert,
  assertEquals,
} from 'https://deno.land/std@0.198.0/assert/mod.ts';

let log = console.log;

// No errors in lexing, but BAD token causes Parse error
Deno.test(function testLex() {
  let trace = TRACE_LEX;

  // Bad characters
  run('~', trace);
  run('42 ! bob', trace);

  // Success
  let actual = run('42', trace);

  assert(actual !== undefined);
  assertEquals(42, actual.value);
});

// 5 different parse errors
Deno.test(function testParse() {
  let trace = TRACE_PARSE;

  // Unexpected EOF
  run('', trace);

  // Unexpected )
  run('[ foo )', trace);

  // Unexpected ]
  run(']', trace);

  // Expected Symbol after )
  run('( 42 )', trace);

  // Extra tokens
  run('42 43', trace);

  let actual = run('(* 3 (+ 1 2))', trace);
  assert(actual !== undefined);
  assertEquals(9, actual.value);
});

// 3 possible transform errors
Deno.test(function testTransform() {
  let trace = TRACE_TRANSFORM;

  // Invalid node
  run('(zz true 1 2)', trace);

  // If arity 3
  run('(if true 1)', trace);

  // + arity 2
  run('(+ 3)', trace);

  // This transforms, but doesn't type check
  run('(+ 3 a)', trace);

  // MULTIPLE transform errors
  run('(+ (foo x) (if x))', trace);

  // Success
  run('(if (== 1 1) 42 43)', trace);

  let actual = run('(+ 2 3)', trace);
  assert(actual !== undefined);
  assertEquals(5, actual.value);
});

// 4 possible type errors
Deno.test(function testTypeCheck() {
  let trace = TRACE_TYPE;

  // If condition not boolean
  run('(if 0 42 43)', trace);

  // If branches don't match
  run('(if true 42 false)', trace);

  // operands don't match
  run('(== 3 (== 1 1))', trace);

  // MULTIPLE type errors
  run('(if 0 42 false)', trace);

  // TODO: this is a bug
  run('(+ true true)', trace);

  let actual = run('(if true true false)', trace);
  assert(actual !== undefined);
  assertEquals(true, actual.value);
});

// 1 runtime error
Deno.test(function testEval() {
  let trace = TRACE_EVAL;

  // divide by zero
  let actual = run('(/ 42 0)', trace);
  assertEquals(undefined, actual);

  // Bug
  actual = run('(== 5 (+ 2 3))', trace);
  assert(actual !== undefined);
  assertEquals(true, actual.value);

  actual = run('(or (== 3 4) (== 5 5))', trace);
  assert(actual !== undefined);
  assertEquals(true, actual.value);
});
