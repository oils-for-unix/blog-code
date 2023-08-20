// @ts-nocheck
// This file uses dynamic typing

import { Binary, Error, Expr, ShouldNotGetHere, Value } from './header.ts';

const log = console.log;

export function evaluate(expr: Expr): Value {
  let result;

  switch (expr.tag) {
    case 'Bool':
    case 'Num':
    case 'Str':
      return expr;

    case 'Binary': {
      let left = evaluate(expr.left);
      let right = evaluate(expr.right);

      // Uses DYNAMIC typing

      // deno-fmt-ignore
      switch (expr.op) {
        // Int -> Int
        case '+': result = left.value + right.value; break;
        case '-': result = left.value - right.value; break;
        case '*': result = left.value * right.value; break;
        case '/': result = left.value / right.value; break;

        // Exact equality
        case '==': result = left.value === right.value; break;
        case '!=': result = left.value !== right.value; break;
        case '<': result = left.value < right.value; break;
        case '>': result = left.value > right.value; break;

        case 'and': result = left.value && right.value; break;
        case 'or': result = left.value || right.value; break;

        default: throw ShouldNotGetHere;
      }

      // Make result statically typed
      switch (expr.op) {
        // Int -> Int
        case '+':
        case '-':
        case '*':
        case '/':
          return { tag: 'Num', value: result, loc: expr.loc };

        case '==':
        case '!=':
        case '<':
        case '>':
        case 'and':
        case 'or':
          return { tag: 'Bool', value: result, loc: expr.loc };

        default:
          throw ShouldNotGetHere;
      }
    }

    case 'If': {
      if (evaluate(expr.cond)) {
        return evaluate(expr.then);
      } else {
        return evaluate(expr.else);
      }
    }

    default:
      throw ShouldNotGetHere;
  }
}
