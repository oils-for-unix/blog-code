import {
  Error,
  Expr,
  OP_SIGNATURES,
  ShouldNotGetHere,
  Type,
} from './header.ts';

const log = console.log;

function add(errors: Error[], message: string, loc: number) {
  errors.push({ tag: 'Error', message, loc });
}

// We use a Map<Expr, Type> to store computed types.
// Expr<void> vs. Expr<T> (which matklad used) is another solution to the "AST
// Typing Problem": https://news.ycombinator.com/item?id=37114976
// That has more type safety, but involves more indirection.

export function check(
  expr: Expr,
  types: Map<Expr, Type>,
  errors: Error[],
): Type | null {
  let ok = true;
  let result: Type | null = null; // return type of this Expr

  switch (expr.tag) {
    case 'Name': // filtered out by transform()
      throw ShouldNotGetHere;

    case 'Bool':
    case 'Num':
      result = expr.tag;
      break;

    case 'Binary': {
      let l = check(expr.left, types, errors);
      let r = check(expr.right, types, errors);
      let [l_expect, r_expect, op_result] = OP_SIGNATURES[expr.op];

      if (l !== l_expect) {
        let message = `Left operand has type ${l}, expected ${l_expect}`;
        add(errors, message, expr.left.loc);
        ok = false;
      }
      if (r !== r_expect) {
        let message = `Right operand has type ${r}, expected ${r_expect}`;
        add(errors, message, expr.right.loc);
        ok = false;
      }

      if (ok) {
        result = op_result;
      }
      break;
    }

    case 'If': {
      let c = check(expr.cond, types, errors);
      let t = check(expr.then, types, errors);
      let e = check(expr.else, types, errors);

      if (c !== 'Bool') {
        let message = `if condition should be a Bool, got ${c}`;
        add(errors, message, expr.cond.loc);
        ok = false;
      }
      if (t !== e) {
        let message = `if branches must have same type: got ${t} and ${e}`;
        add(errors, message, expr.loc);
        ok = false;
      }
      if (ok && t !== null) {
        result = t;
      }
      break;
    }

    case 'Error': // ignore error
      break;

    default:
      throw ShouldNotGetHere;
  }

  // Relate this node and the type, and ALSO return it.
  if (result !== null) {
    types.set(expr, result);
  }
  return result;
}
