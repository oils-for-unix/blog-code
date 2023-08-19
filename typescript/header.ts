// Lexer -> [Token] -> Parser

export type Id = 'lparen' | 'rparen' | 'lbrack' | 'rbrack' | 'bool' | 'int' |
  'str' | 'eof';

export interface Token {
  id: Id;
  start: number;  // 3
  len: number;  // 1
  source: string;  // Use the whole program for now
                   // Avoid string allocations unless we need them
}

// Parser -> [Node] -> Transformer

interface SyntaxError {
  message: string;
  pos: number;
}

export interface Bool {
  id: "bool";
  value: boolean;
  loc: number,
}

export interface Int {
  id: 'int';
  value: number;
  loc: number,
}

export interface Str {
  id: "str";
  value: string;
  loc: number,
}

// (== 5 (+ 2 3))
export interface List {
  name: string,
  loc: number;
  children: Node[];
}

export type Node = Bool | Int | Str | List;

// Transformer -> [Expr] -> Type Checker

export interface Expr {
}
