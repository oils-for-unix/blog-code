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

var log = console.log;

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

Deno.test(function testParse() {
  let trace = TRACE_PARSE;

  // Unexpected EOF
  run('', trace);

  // Unexpected )
  run('[ foo )', trace);

  // Unexpected ]
  run(']', trace);

  // Expected string after )
  run('( 42 )', trace);

  // Extra tokens
  run('42 43', trace);

  let actual = run('(* 3 (+ 1 2))', trace);
  assert(actual !== undefined);
  assertEquals(9, actual.value);
});

Deno.test(function testTransform() {
  let trace = TRACE_TRANSFORM;

  // Invalid node
  run('(zz true 1 2)', trace);

  // If arity 3
  run('(if true 1)', trace);

  // + arity 2
  run('(+ 3)', trace);

  // Success
  run('(if (== 1 1) 42 43)', trace);

  let actual = run('(+ 2 3)', trace);
  assert(actual !== undefined);
  assertEquals(5, actual.value);
});

Deno.test(function testTypeCheck() {
  let trace = TRACE_TYPE;

  // If condition not boolean
  run('(if 0 42 43)', trace);

  // If branches don't match
  run('(if true 42 false)', trace);

  // operands don't match
  run('(== 3 true)', trace);

  // TODO: this is a bug
  run('(+ true true)', trace);

  let actual = run('(if true true false)', trace);
  assert(actual !== undefined);
  assertEquals(true, actual.value);
});

Deno.test(function testEval() {
  let trace = TRACE_EVAL;

  // divide by zero
  run('(/ 42 0)', trace);

  // Bug
  let actual = run('(== 5 (+ 2 3))', trace);
  assert(actual !== undefined);
  assertEquals(true, actual.value);

  actual = run('(or (== 3 4) (== 5 5))', trace);
  assert(actual !== undefined);
  assertEquals(true, actual.value);

  return;

  run('(if true 47 48)', trace);
  run('(== 3 4)', trace);

  run('(and true true)', trace);
  run('(and false true)', trace);

  run('(or false false)', trace);
  run('(or false true)', trace);

  run('(if 0 42 43)', trace);
});
