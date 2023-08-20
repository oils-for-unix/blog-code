import { Binary, Error, Expr, ShouldNotGetHere, Value } from './header.ts';

const log = console.log;

export function evaluate(expr: Expr): Value {
  switch (expr.tag) {
    case 'Bool':
    case 'Num':
    case 'Str':
      return expr;

    case 'Binary':
      {
        let left = evaluate(expr.left);
        let right = evaluate(expr.left);

        switch (expr.op) {
          case '+': {
            // type checking ensures this
            let value = (left.value as number) + (right.value as number);
            return { tag: 'Num', value, loc: expr.loc };
          }
          case '-': {
            let value = (left.value as number) - (right.value as number);
            return { tag: 'Num', value, loc: expr.loc };
          }
        }
        return { tag: 'Num', value: 42, loc: expr.loc };
      }
      break;

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
