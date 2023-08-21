import { Type } from './header.ts';

// Signatures for static type checking

export type Sig = [Type, Type, Type];

const NNN: Sig = ['Num', 'Num', 'Num'];
const NNB: Sig = ['Num', 'Num', 'Bool'];
const BBB: Sig = ['Bool', 'Bool', 'Bool'];

// Weird syntax for dictionary type!
export const OP_SIGNATURES: { [key: string]: Sig } = {
  '+': NNN,
  '-': NNN,
  '*': NNN,
  '/': NNN,

  '==': NNB, // NOT polymorphic!  only for integers.
  '!=': NNB,
  '<': NNB,
  '>': NNB,

  'and': BBB,
  'or': BBB,
};

// Types and functions for dynamic checking and evaluation

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
