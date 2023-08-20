import { Error, Expr, Node, Type, Value } from './header.ts';
import { lex } from './lex.ts';
import { parse } from './parse.ts';
import { transform } from './transform.ts';
import { inferAndCheck } from './check.ts';
import { evaluate } from './eval.ts';

const log = console.log;

function max(x: number, y: number): number {
  return x > y ? x : y;
}

function puts(s: string) {
  let bytes = new TextEncoder().encode(s);
  Deno.writeAllSync(Deno.stdout, bytes);
}

function repeatString(s: string, n: number) {
  let out = Array(n + 1).join(s);
  puts(out);
}

// Returns the position of the newline, or -1
function findStartOfLine(s: string, blame_pos: number): [number, number] {
  let pos = -1;
  let line_num = 1;

  while (true) {
    let new_pos = s.indexOf('\n', pos + 1);

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

export function run(s: string): Value | undefined {
  log('');
  log('===========');
  log('PROGRAM ' + s);
  let tokens = lex(s);
  // TODO:
  // support \n \\ and maybe \u{123456}
  // error like \z should be fatal

  log('  LEX');
  //log(tokens);

  let tree: Node | null = null;
  try {
    tree = parse(tokens);

    log('');
    log('  PARSE');
    log(tree);
  } catch (e) {
    log('  PARSE ERROR');
    log(e);

    let blame_tok = tokens[e.pos];
    //log(`blame ${JSON.stringify(blame_tok)}`);
    //log(`blame ${blame_tok.start} ${blame_tok.len}`);

    // Extract the right line, and find The LAST newline before the start

    let blame_start = blame_tok.start;

    let [line_begin, line_num] = findStartOfLine(s, blame_start);

    let pos = s.indexOf('\n', line_begin);
    let line_end = (pos === -1) ? s.length : pos;

    log(`line_num ${line_num} begin ${line_begin} end ${line_end}`);

    log(s.slice(line_begin, line_end));

    // Quote line
    let col = blame_start - line_begin;
    repeatString(' ', col);

    // Point to column
    let n = max(blame_tok.len, 1); // EOF is zero in length
    repeatString('^', n);

    puts('\n');

    // columns are 1-based like lines
    log(`Parse error at line ${line_num}, column ${col + 1}: ${e.message}`);
  }

  if (tree === null) {
    return;
  }

  let tr_errors: Error[] = [];
  let expr = transform(tree, tr_errors);

  // TODO: print locations
  for (let err of tr_errors) {
    log(err);
  }

  // TODO: Don't type check if there are any transform errors

  log('  EXPR');
  log(expr);

  let types: Map<Expr, Type> = new Map();
  let type_errors: Error[] = [];
  inferAndCheck(expr, types, type_errors);

  // TODO: print locations
  for (let err of type_errors) {
    log(err);
  }

  log('  EXPR with TYPE: TOP');
  log(types.get(expr));

  // TODO: Don't eval if there are any type errors
  log('  EVAL');
  let val = evaluate(expr);
  log(val);
}
