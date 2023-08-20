import { Binary, Error, Expr, ShouldNotGetHere, Type } from './header.ts';

const log = console.log;

function resultType(node: Binary): Type {
  switch (node.op) {
    case '+':
    case '-':
    case '*':
    case '/':
      return 'Num';

    case '==':
    case '!=':
    case '<':
    case '>':
    case 'and':
    case 'or':
      return 'Bool';

    default:
      throw ShouldNotGetHere;
  }
}

export function check(
  expr: Expr,
  types: Map<Expr, Type>,
  errors: Error[],
) {
  let ok = true;
  switch (expr.tag) {
    case 'Bool':
    case 'Num':
    case 'Str':
      types.set(expr, expr.tag);
      break;

    case 'Binary': {
      check(expr.left, types, errors);
      check(expr.right, types, errors);

      let l = types.get(expr.left);
      let r = types.get(expr.right);
      if (l != r) {
        errors.push({
          tag: 'Type',
          message:
            `binary expression operands have different types, got ${l} and ${r}`,
          loc: expr.loc,
        });
        ok = false;
      }

      // TODO: should be invalid
      //   (+ true true) should be invalid
      //   (> true true)
      //   (and 2 3)

      if (ok) {
        types.set(expr, resultType(expr));
      }
      break;
    }

    case 'If': {
      check(expr.cond, types, errors);
      check(expr.then, types, errors);
      check(expr.else, types, errors);

      let c = types.get(expr.cond);
      if (c !== 'Bool') {
        errors.push({
          tag: 'Type',
          message: `if condition should be a Bool, got ${c}`,
          loc: expr.cond.loc,
        });
        ok = false;
      }

      let t = types.get(expr.then);
      let e = types.get(expr.else);
      if (t !== e) {
        errors.push({
          tag: 'Type',
          message: `if branches must have same type: got ${t} and ${e}`,
          loc: expr.loc,
        });
        ok = false;
      }
      if (ok) {
        let t = types.get(expr.then);
        if (t) { // satisfy type system
          types.set(expr, t);
        }
      }
      break;
    }

    case 'Transform': // ignore error
      break;

    default:
      throw ShouldNotGetHere;
  }
}
