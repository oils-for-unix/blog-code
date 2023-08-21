import { Context, Error, Expr, Node, Token, Type, Value } from './header.ts';
import { lex } from './lex.ts';
import { parse } from './parse.ts';
import { transform } from './transform.ts';
import { check } from './check.ts';
import { evaluate } from './eval.ts';

function max(x: number, y: number): number {
  return x > y ? x : y;
}

function repeatString(ctx: Context, s: string, n: number) {
  let out = Array(n + 1).join(s);
  ctx.write(out);
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

function printError(
  ctx: Context,
  prog: string,
  tokens: Token[],
  kind: string,
  e: Error,
) {
  let blame_tok = tokens[e.loc];
  let blame_start = blame_tok.start;

  // Extract the right line, and find The LAST newline before the start
  let [line_start, line_num] = findStartOfLine(prog, blame_start);

  let pos = prog.indexOf('\n', line_start);
  let line_end = (pos === -1) ? prog.length : pos;

  //log(`line_num ${line_num} begin ${line_start} end ${line_end}`);

  // Show snippet
  ctx.write(prog.slice(line_start, line_end));
  ctx.write('\n');

  // Point to token
  let col = blame_start - line_start;
  repeatString(ctx, ' ', col);

  let n = max(blame_tok.len, 1); // EOF is zero in length
  repeatString(ctx, '^', n);
  ctx.write('\n');

  // Columns are 1-based like lines
  ctx.write(
    `yaks:${line_num}:${col + 1}: ${kind} error: ${e.message}`,
  );
  ctx.write('\n\n');
}

// Control printing
export const TRACE_LEX = 1 << 1;
export const TRACE_PARSE = 1 << 2;
export const TRACE_TRANSFORM = 1 << 3;
export const TRACE_TYPE = 1 << 4;
export const TRACE_EVAL = 1 << 5;

export const DYNAMIC = 1 << 6;

export function interpret(
  ctx: Context,
  prog: string,
  trace: number,
): Value | undefined {
  let log = ctx.log;
  let write = ctx.write;

  log('');
  log(`    PROGRAM ${prog}`);

  let tokens = lex(prog); // failures deferred to parsing

  if (trace & TRACE_LEX) {
    log('    LEX');
    // TODO: print these more nicely -- they point to the whole program
    log(tokens);
  }

  let tree: Node | null = null;
  try {
    tree = parse(tokens);

    if (trace & TRACE_PARSE) {
      log('    PARSE');
      log(tree);
    }
  } catch (e) {
    log('    PARSE ERROR');
    printError(ctx, prog, tokens, 'Parse', e);
    return;
  }
  if (tree === null) {
    return;
  }

  let tr_errors: Error[] = [];
  let expr = transform(tree, tr_errors);

  if (tr_errors.length) {
    log('    TRANSFORM ERRORS');
    for (let e of tr_errors) {
      printError(ctx, prog, tokens, 'Transform', e);
    }
    return;
  }
  if (trace & TRACE_TRANSFORM) {
    log('    TRANSFORM');
    log(expr);
  }

  if (!(trace & DYNAMIC)) {
    let types: Map<Expr, Type> = new Map();
    let type_errors: Error[] = [];
    let typ = check(expr, types, type_errors);

    if (type_errors.length) {
      log('    TYPE ERRORS');
      for (let e of type_errors) {
        printError(ctx, prog, tokens, 'Type', e);
      }
      return;
    }
    if (trace & TRACE_TYPE) {
      log('    TOP LEVEL TYPE');
      log(`    --> ${typ}`);
    }
  }

  let val: Value | null = null;
  try {
    val = evaluate(expr);
  } catch (e) {
    log('    EVAL ERROR');
    printError(ctx, prog, tokens, 'Runtime', e);
    return;
  }

  if (trace & TRACE_EVAL) {
    log('    EVAL');
    write('    --> ');
    log(val);
  }

  return val;
}

function write(s: string) {
  let bytes = new TextEncoder().encode(s);
  Deno.writeAllSync(Deno.stdout, bytes);
}

export function run(prog: string, trace: number): Value | undefined {
  let ctx = { log: console.log, write: write };
  return interpret(ctx, prog, trace);
}
