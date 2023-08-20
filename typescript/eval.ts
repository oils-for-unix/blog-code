import { Binary, Error, Expr, ShouldNotGetHere, Value } from './header.ts';

const log = console.log;

export function evaluate(expr: Expr): Value {
  switch (expr.tag) {
    case 'Bool':
    case 'Num':
    case 'Str':
      return expr;

    var left_num = -1, right_num = -1, num = -1;
    var left_bool, right_bool, bool;

    case 'Binary':
      {
        let left = evaluate(expr.left);
        let right = evaluate(expr.right);

        switch (expr.op) {
          // Int -> Int
          case '+':
          case '-':
          case '*':
          case '==':

          // Int -> Bool
          case '!=':
          case '<':
          case '>':
          case '/':
            left_num = left.value as number;
            right_num = right.value as number;
            break;

          case 'and':
          case 'or':
            left_bool = left.value as boolean;
            right_bool = right.value as boolean;
            break;

          default:
            throw ShouldNotGetHere;
        }

        switch (expr.op) {
          // Int -> Int
          case '+':
            // @ts-ignore
            num = left_num + right_num;
            break;
          case '-':
            // @ts-ignore
            num = left_num - right_num;
            break;
          case '*':
            // @ts-ignore
            num = left_num * right_num;
            break;
          case '/':
            // @ts-ignore
            if (right_num == 0) {
              throw {message: 'Divide by zero', loc: expr.loc};
            }

            // @ts-ignore
            num = left_num / right_num;

            // @ts-ignore
            // log(` divide ${left_num} / ${right_num} -> ${num}`);
            break;

          // Int -> Bool
          case '==':
            // @ts-ignore
            bool = left_num == right_num;
            break;
          case '!=':
            // @ts-ignore
            bool = left_num != right_num;
            break;
          case '<':
            // @ts-ignore
            bool = left_num < right_num;
            break;
          case '>':
            // @ts-ignore
            bool = left_num > right_num;
            break;

          // Bool -> Bool
          case 'and':
            // @ts-ignore
            bool = left_bool && right_bool;
            break;
            // @ts-ignore
            //log(` ${left_bool} && ${right_bool} -> ${bool}`);
          case 'or':
            // @ts-ignore
            bool = left_bool || right_bool;
            break;

          default:
            throw ShouldNotGetHere;
        }

        switch (expr.op) {
          // Int -> Int
          case '+':
          case '-':
          case '*':
          case '==':
            // @ts-ignore
            return { tag: 'Num', value: num, loc: expr.loc };

          // Int -> Bool
          case '!=':
          case '<':
          case '>':
          case '/':

          // Bool -> Bool
          case 'and':
          case 'or':
            // @ts-ignore
            return { tag: 'Bool', value: bool, loc: expr.loc };

          default:
            throw ShouldNotGetHere;
        }
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
