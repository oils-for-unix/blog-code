// Most stages can have errors

// Errors can be thrown (not checked by TypeScript), or put in an array
export interface Error {
  tag: 'Parse' | 'Transform' | 'Type' | 'Runtime';
  message: string;
  loc: number;
}

export const ShouldNotGetHere = { tag: 'Assert' };

// Lexer -> [Token] -> Parser

export type Id =
  | 'BAD'
  | 'lparen'
  | 'rparen'
  | 'lbrack'
  | 'rbrack'
  | 'bool'
  | 'int'
  | 'str'
  | 'eof';

export interface Token {
  id: Id;
  start: number; // 3
  len: number; // 1
  source: string; // Use the whole program for now
  // Avoid string allocations unless we need them
}

// Parser -> [Node] -> Transformer

export interface Bool {
  tag: 'Bool';
  value: boolean;
  loc: number;
}

export interface Num {
  tag: 'Num';
  value: number;
  loc: number;
}

export interface Str {
  tag: 'Str';
  value: string;
  loc: number;
}

// (== 5 (+ 2 3))
export interface List {
  tag: 'List';
  name: string;
  loc: number;
  children: Node[];
}

export type Node = Bool | Num | Str | List;

// Transformer -> [Expr] -> Type Checker

export interface If {
  tag: 'If';
  loc: number; // index of Token for if
  cond: Expr;
  then: Expr;
  else: Expr;
}

export interface Binary {
  tag: 'Binary';
  op: '+' | '-' | '/' | '*' | '==' | '!=' | '<' | '>' | 'and' | 'or';
  loc: number; // index of Token for op
  left: Expr;
  right: Expr;
}

export type Expr = Bool | Num | Str | If | Binary | Error;

// Type Checker -> [Expr with Types] -> Evaluator

export type Type = 'Bool' | 'Num' | 'Str' | 'TypeError';

// Evaluator -> [Value]

export type Value = Bool | Num | Str;
