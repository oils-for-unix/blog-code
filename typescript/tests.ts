import { lex } from './lex.ts';
import {
  run,
  TRACE_EVAL,
  TRACE_LEX,
  TRACE_PARSE,
  TRACE_TRANSFORM,
  TRACE_TYPE,
} from './main.ts';

function testLex() {
  if (0) {
    console.log('-----------');
    let t = lex('(+ 42 23 define true)');
    console.log(t);

    console.log('-----------');
    t = lex('# comment\n hello\n #comment');
    console.log(t);
  }

  let trace = TRACE_LEX;
  run('~', trace);
  run('42 ~ bob', trace);

  run('42', trace);
  run('foo 43', trace);
  run('(foo 43)', trace);
}

function testParse() {
  let trace = TRACE_PARSE;
  run('42', trace);

  run('(* 42 (+ 99 1))', trace);

  run('(fib 11', trace);
  run('(fib 22]', trace);

  run('(42)', trace);
}

/*
function runTests() {

  run('define');
  run('(define)');
  run('42');
  run('(+ 5 6)');
  run('(== 11 (+ 5 6))');
  run('(fn [x] (+ x 1))');
  run('(not (> 1 2))');
  run('(if true 42 (+ 99 1))');

  // binary operand mismatch
  run('(+ 42 true)');
  // condition is wrong type
  run('(if 0 true true)');
  // then-else match
  run('(if true false 42)');

  return;

  // Incomplete
  run('(+ 42');

  // Too many
  run('(+ 42) oops');

  run(']');

  // String after (
  run('( ] )');

  // Unbalanced
  run('(fn [x) )');

  run(`
  (define fib [x]
    (+ x 42) ]
  `);
}
*/

/*
testLex();
*/
testParse();
/*
testTransform();
testTypeCheck();
testEval();
*/
