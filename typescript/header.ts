
// Lexer <=> Token <=> Parser

export type Id = 'lparen' | 'rparen' | 'lbrack' | 'rbrack' | 'bool' | 'int' |
  'str' | 'eof';

export interface Token {
  id: Id;
  start: number;  // 3
  len: number;  // 1
  source: string;  // Use the whole program for now
                   // Avoid string allocations unless we need them
}

// Parser <=> Node <=> Transformer

interface SyntaxError {
  message: string;
  pos: number;
}

interface Bool {
  id: "bool";
  value: boolean;
  loc: number,
}

interface Int {
  id: 'int';
  value: number;
  loc: number,
}

interface Str {
  id: "str";
  value: string;
  loc: number,
}

// Note: in an efficient implementation, this would be a flat list of
//
// (int id, int start, int end)
//
// And then the parser would instantiate the values it needs.  But it's
// convenient to do all the non-recursive work in the lexer.

// 42 is parsed as a number
// "+" and "define" are parsed as strings
export type Atom = Bool | Int | Str;

// (== 5 (+ 2 3))
export interface List {
  name: string,
  loc: number;
  children: Node[];
}

export type Node = Atom | List;
