import { lex } from './lex.ts';
import { parse } from './parse.ts';
import { transform } from './transform.ts';

const log = console.log;

function max(x: number, y: number): number {
  return x > y ? x : y;
}

function puts(s: string) {
  var bytes = new TextEncoder().encode(s);
  Deno.writeAllSync(Deno.stdout, bytes);
}

function repeatString(s: string, n: number) {
  var out = Array(n + 1).join(s);
  puts(out);
}

// Returns the position of the newline, or -1
function findStartOfLine(s: string, blame_pos: number): [number, number] {
  var pos = -1;
  var line_num = 1;

  while (true) {
    var new_pos = s.indexOf('\n', pos + 1);

    if (new_pos == -1) {
      return [pos + 1, line_num];
    }

    if (new_pos > blame_pos) {
      return [pos + 1, line_num];
    }

    pos = new_pos;
    line_num += 1;
  }
}

function parseDemo(s: string) {
  log('');
  log('===========');
  log('PROGRAM ' + s);
  var tokens = lex(s);

  log('  LEX');
  //log(tokens);

  try {
    var tree = parse(tokens);
  } catch (e) {
    log('  PARSE ERROR');
    log(e);

    var blame_tok = tokens[e.pos];
    //log(`blame ${JSON.stringify(blame_tok)}`);
    //log(`blame ${blame_tok.start} ${blame_tok.len}`);

    // Extract the right line, and find The LAST newline before the start

    var blame_start = blame_tok.start;

    var [line_begin, line_num] = findStartOfLine(s, blame_start);

    var pos = s.indexOf('\n', line_begin);
    var line_end = (pos === -1) ? s.length : pos;

    log(`line_num ${line_num} begin ${line_begin} end ${line_end}`);

    log(s.slice(line_begin, line_end));

    // Quote line
    var col = blame_start - line_begin;
    repeatString(' ', col);

    // Point to column
    var n = max(blame_tok.len, 1); // EOF is zero in length
    repeatString('^', n);

    puts('\n');

    // columns are 1-based like lines
    log(`Parse error at line ${line_num}, column ${col + 1}: ${e.message}`);

    return;
  }

  log('');
  log('  READ');
  log(tree);
}

function runTests() {
  parseDemo('define');
  parseDemo('(define)');
  parseDemo('42');
  parseDemo('(+ 5 6)');
  parseDemo('(== 11 (+ 5 6))');
  parseDemo('(fn [x] (+ x 1))');

  // Incomplete
  parseDemo('(+ 42');

  // Too many
  parseDemo('(+ 42) oops');

  parseDemo(']');

  // String after (
  parseDemo('( ] )');

  // Unbalanced
  parseDemo('(fn [x) )');

  parseDemo(`
  (define fib [x]
    (+ x 42) ]
  `);

  return;
  console.log('-----------');
  var t = lex('(+ 42 23 define true)');
  console.log(t);

  console.log('-----------');
  var t = lex('# comment\n hello\n #comment');
  console.log(t);
}

runTests();
