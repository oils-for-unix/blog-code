import {
  Error,
  Expr,
  OP_SIGNATURES,
  ShouldNotGetHere,
  Sig,
  Type,
} from './header.ts';

const log = console.log;

export function check(
  expr: Expr,
  types: Map<Expr, Type>,
  errors: Error[],
) {
  let ok = true;
  switch (expr.tag) {
    case 'Name': // filtered out by transform()
      throw ShouldNotGetHere;

    case 'Bool':
    case 'Num':
      types.set(expr, expr.tag);
      break;

    case 'Binary': {
      check(expr.left, types, errors);
      check(expr.right, types, errors);

      let l = types.get(expr.left);
      let r = types.get(expr.right);

      let sig = OP_SIGNATURES[expr.op];
      let expected_left = sig[0];
      let expected_right = sig[1];

      //log(`left ${l}`)
      //log(`ex ${expected_left}`)

      if (l !== expected_left) {
        errors.push({
          tag: 'Error',
          message: `Left operand has type ${l}, expected ${expected_left}`,
          loc: expr.left.loc,
        });
        ok = false;
      }
      if (r !== expected_right) {
        errors.push({
          tag: 'Error',
          message: `Right operand has type ${r}, expected ${expected_right}`,
          loc: expr.right.loc,
        });
        ok = false;
      }

      if (ok) {
        let result_type: Type = sig[2];
        types.set(expr, result_type);
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
          tag: 'Error',
          message: `if condition should be a Bool, got ${c}`,
          loc: expr.cond.loc,
        });
        ok = false;
      }

      let t = types.get(expr.then);
      let e = types.get(expr.else);
      if (t !== e) {
        errors.push({
          tag: 'Error',
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

    case 'Error': // ignore error
      break;

    default:
      throw ShouldNotGetHere;
  }
}
