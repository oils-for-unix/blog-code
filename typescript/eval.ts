// @ts-nocheck
// This file uses dynamic typing

import { Expr, ShouldNotGetHere, Value } from './header.ts';

const log = console.log;

type NNN = (x: number, y: number) => number;
type NNB = (x: number, y: number) => boolean;
type BBB = (x: boolean, y: boolean) => boolean;

// (Num, Num) => Num
// deno-fmt-ignore
const OPS_NNN: {[key:string]: NNN} = {
  '+': (x, y) => x + y,
  '-': (x, y) => x - y,
  '*': (x, y) => x * y,
  //'/': null,  // checked separately
};

// (Num, Num) => Bool
// deno-fmt-ignore
const OPS_NNB: {[key:string]: NNB} = {
  // Exact equality
  '==': (x, y) => x === y,
  '!=': (x, y) => x !== y,
  '<' : (x, y) => x < y,
  '>' : (x, y) => x > y,
};

// (Bool, Bool) => Bool
// deno-fmt-ignore
const OPS_BBB: {[key:string]: BBB} = {
  'and': (x, y) => x && y,
  'or' : (x, y) => x || y,
};

export function evaluate(expr: Expr): Value {
  let result;

  switch (expr.tag) {
    case 'Bool':
    case 'Num':
    case 'Str':
      return expr;

    case 'If': {
      if (evaluate(expr.cond)) {
        return evaluate(expr.then);
      } else {
        return evaluate(expr.else);
      }
    }

    case 'Binary': {
      let left = evaluate(expr.left);
      let right = evaluate(expr.right);

      if (expr.op === '/') {
        let x = left.value;
        let y = right.value;
        if (y === 0) {
          throw { tag: 'Runtime', message: 'Divide by zero', loc: expr.loc };
        }
        return x / y;
      }

      let func = OPS_NNN[expr.op];
      if (func !== undefined) {
        let value = func(left.value, right.value);
        //log(value);
        return { tag: 'Num', value, loc: expr.loc };
      }

      func = OPS_NNB[expr.op];
      if (func !== undefined) {
        let value = func(left.value, right.value);
        return { tag: 'Bool', value, loc: expr.loc };
      }

      func = OPS_BBB[expr.op];
      if (func !== undefined) {
        let value = func(left.value, right.value);
        return { tag: 'Bool', value, loc: expr.loc };
      }
    }

    default: // 'Error' or some other node
      throw ShouldNotGetHere;
  }
}
