// Most stages can have errors

// Errors can be thrown (not checked by TypeScript), or put in an array
export interface Error {
  tag: 'Error';
  message: string;
  loc: number;
}

export const ShouldNotGetHere = { tag: 'Assert' };

// [String] -> Lexer -> [Token]

export type Id =
  | 'BAD'
  | 'lparen'
  | 'rparen'
  | 'lbrack'
  | 'rbrack'
  | 'bool'
  | 'int'
  | 'name'
  | 'eof';

export interface Token {
  id: Id;
  start: number; // 3
  len: number; // 1
  source: string; // Use the whole program for now
  // Avoid string allocations unless we need them
}

// [Token] -> Parser -> [Node]

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

export interface Name {
  tag: 'Name';
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

export type Node = Bool | Num | Name | List;

// [Node] -> Transformer -> [Expr]

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

// It would be nice if Error wasn't a valid Expr, but transform() can report
// multiple errors, and having the first one as the return value simplifies the
// code.  The main run() function should not type check or eval with errors.

export type Expr = Bool | Num | Name | If | Binary | Error;

// [Expr] -> Type Checker -> Map<Expr, Type>

export type Type = 'Bool' | 'Num';

// [Expr] -> Evaluator -> [Value]

export type Value = Bool | Num;
