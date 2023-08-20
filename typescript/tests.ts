import { lex } from './lex.ts';
import { run } from './main.ts';

function runTests() {
  console.log('-----------');
  let t = lex('(+ 42 23 define true)');
  console.log(t);

  console.log('-----------');
  t = lex('# comment\n hello\n #comment');
  console.log(t);

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

runTests();
