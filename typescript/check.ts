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

// Need 'undefined' because of Map.get()
function typesEqual(lhs: Type | undefined, rhs: Type | undefined): boolean {
  return lhs === rhs;
}

export function inferAndCheck(
  expr: Expr,
  types: Map<Expr, Type>,
  errors: Error[],
) {
  var ok = true;
  switch (expr.tag) {
    case 'Bool':
    case 'Num':
    case 'Str':
      types.set(expr, expr.tag);
      break;

    case 'Unary':
      inferAndCheck(expr.child, types, errors);

      // Boolean 'not' is the only unary operator
      if (typesEqual(types.get(expr.child), 'Bool')) {
        types.set(expr, 'Bool');
      }
      break;

    case 'Binary':
      inferAndCheck(expr.left, types, errors);
      inferAndCheck(expr.right, types, errors);

      if (!typesEqual(types.get(expr.left), types.get(expr.right))) {
        errors.push({
          tag: 'Type',
          message: 'binary expression operands have different types',
          loc: expr.loc,
        });
        ok = false;
      }
      if (ok) {
        types.set(expr, resultType(expr));
      }
      break;

    case 'If':
      inferAndCheck(expr.cond, types, errors);
      inferAndCheck(expr.then, types, errors);
      inferAndCheck(expr.else, types, errors);

      if (!typesEqual(types.get(expr.cond), 'Bool')) {
        errors.push({
          tag: 'Type',
          message: 'if condition is not a boolean',
          loc: expr.loc,
        });
        ok = false;
      }
      if (!typesEqual(types.get(expr.then), types.get(expr.else))) {
        errors.push({
          tag: 'Type',
          message: 'if branches have different types',
          loc: expr.loc,
        });
        ok = false;
      }
      if (ok) {
        var t = types.get(expr.then);
        if (t) { // satisfy type system
          types.set(expr, t);
        }
      }
      break;

    case 'Transform': // ignore error
      break;

    default:
      throw ShouldNotGetHere;
  }
}
