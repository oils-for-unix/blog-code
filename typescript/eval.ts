import { Error, Expr, ShouldNotGetHere, Type, Value } from './header.ts';

const log = console.log;

type NNN_func = (x: number, y: number) => number;
type NNB_func = (x: number, y: number) => boolean;
type BBB_func = (x: boolean, y: boolean) => boolean;

// (Num, Num) => Num
const OPS_NNN: { [key: string]: NNN_func } = {
  '+': (x, y) => x + y,
  '-': (x, y) => x - y,
  '*': (x, y) => x * y,
  '/': (x, y) => x / y,
};

// (Num, Num) => Bool
const OPS_NNB: { [key: string]: NNB_func } = {
  // Exact equality
  '==': (x, y) => x === y,
  '!=': (x, y) => x !== y,
  '<': (x, y) => x < y,
  '>': (x, y) => x > y,
};

// (Bool, Bool) => Bool
const OPS_BBB: { [key: string]: BBB_func } = {
  'and': (x, y) => x && y,
  'or': (x, y) => x || y,
};

function typeError(expr: Expr, t: Type, desc: string): Error | null {
  return {
    tag: 'Error',
    message: `Expected ${desc} to be ${t}, got ${expr.tag}`,
    loc: expr.loc,
  };
}

export function evaluate(expr: Expr): Value {
  let result;

  switch (expr.tag) {
    case 'Name':
      throw ShouldNotGetHere;

    case 'Bool':
    case 'Num':
      return expr;

    case 'If': {
      if (evaluate(expr.cond)) {
        return evaluate(expr.then);
      } else {
        return evaluate(expr.else);
      }
    }

    case 'Binary': {
      let a = evaluate(expr.left);
      let b = evaluate(expr.right);
      let err;

      let func = OPS_NNN[expr.op];
      if (func !== undefined) {
        if (a.tag !== 'Num') throw typeError(a, 'Num', 'left operand');
        if (b.tag !== 'Num') throw typeError(b, 'Num', 'right operand');

        if (expr.op === '/' && b.value === 0) {
          throw { message: 'Divide by zero', loc: expr.loc };
        }
        let value = func(a.value, b.value);
        //log(value);
        return { tag: 'Num', value, loc: expr.loc };
      }

      let func2 = OPS_NNB[expr.op];
      if (func2 !== undefined) {
        if (a.tag !== 'Num') throw typeError(a, 'Num', 'left operand');
        if (b.tag !== 'Num') throw typeError(b, 'Num', 'right operand');

        let value = func2(a.value, b.value);
        return { tag: 'Bool', value, loc: expr.loc };
      }

      let func3 = OPS_BBB[expr.op];
      if (func3 !== undefined) {
        if (a.tag !== 'Bool') throw typeError(a, 'Bool', 'left operand');
        if (b.tag !== 'Bool') throw typeError(b, 'Bool', 'right operand');

        let value = func3(a.value, b.value);
        return { tag: 'Bool', value, loc: expr.loc };
      }
    }

    default: // 'Error' or some other node
      throw ShouldNotGetHere;
  }
}
