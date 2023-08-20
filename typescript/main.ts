import { Error, Expr, Node, Token, Type, Value } from './header.ts';
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

function printError(prog: string, blame_tok: Token, e: Error) {
  // Extract the right line, and find The LAST newline before the start
  let blame_start = blame_tok.start;

  let [line_start, line_num] = findStartOfLine(prog, blame_start);

  let pos = prog.indexOf('\n', line_start);
  let line_end = (pos === -1) ? prog.length : pos;

  //log(`line_num ${line_num} begin ${line_start} end ${line_end}`);

  // Show snippet
  log(prog.slice(line_start, line_end));

  // Point to token
  let col = blame_start - line_start;
  repeatString(' ', col);

  let n = max(blame_tok.len, 1); // EOF is zero in length
  repeatString('^', n);

  puts('\n');

  // Columns are 1-based like lines
  log(`Error at line ${line_num}, column ${col + 1}: ${e.message}`);
}

export const TRACE_LEX = 1 << 1;
export const TRACE_PARSE = 1 << 2;
export const TRACE_TRANSFORM = 1 << 3;
export const TRACE_TYPE = 1 << 4;
export const TRACE_EVAL = 1 << 5;

export function run(prog: string, trace: number): Value | undefined {
  log('');
  log('===========');
  log(`  PROGRAM ${prog}`);

  let tokens = lex(prog); // failures deferred to parsing

  log('  LEX');
  if (trace & TRACE_LEX) {
    // Could print these more niecly -- they point to the whole program
    log(tokens);
  }

  let tree: Node | null = null;
  try {
    tree = parse(tokens);

    log('');
    log('  PARSE');
    if (trace & TRACE_PARSE) {
      log(tree);
    }
  } catch (e) {
    log('  PARSE ERROR');
    //log(e);

    let blame_tok = tokens[e.loc];
    printError(prog, blame_tok, e);
    return;
  }
  if (tree === null) {
    return;
  }

  let tr_errors: Error[] = [];
  let expr = transform(tree, tr_errors);

  if (tr_errors.length) {
    log('  TRANSFORM ERRORS');
    for (let e of tr_errors) {
      let blame_tok = tokens[e.loc];
      printError(prog, blame_tok, e);
    }
    return;
  }

  log('  TRANSFORM');
  if (trace & TRACE_TRANSFORM) {
    log(expr);
  }

  let types: Map<Expr, Type> = new Map();
  let type_errors: Error[] = [];
  inferAndCheck(expr, types, type_errors);

  if (type_errors.length) {
    log('  TYPE ERRORS');
    for (let e of type_errors) {
      let blame_tok = tokens[e.loc];
      printError(prog, blame_tok, e);
    }
    return;
  }

  log('  TOP LEVEL TYPE');
  if (trace & TRACE_TYPE) {
    log(types.get(expr));
  }

  log('  EVAL');
  let val: Value | null = null;
  try {
    val = evaluate(expr);
  } catch (e) {
    log('  PARSE ERROR');
    //log(e);

    let blame_tok = tokens[e.loc];
    printError(prog, blame_tok, e);
    return;
  }

  if (trace & TRACE_EVAL) {
    log(val);
  }

  return val;
}
