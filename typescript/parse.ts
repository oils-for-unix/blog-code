import {
  Bool,
  List,
  Name,
  Node,
  Num,
  ShouldNotGetHere,
  Token,
} from './header.ts';

let log = console.log;

function tokenValue(tok: Token) {
  return tok.source.slice(tok.start, tok.start + tok.len);
}

interface Parser {
  tokens: Token[];
  pos: number;
  current: Token;
}

function next(p: Parser) {
  p.pos++;
  p.current = p.tokens[p.pos];
}

// S-Expression Grammar
//
// Node    ::= Bool | Num | Name  # Atoms
//           | List               # Compound data
//
// List    ::= '(' Str Node* ')'
//           | '[' Str Node* ']'  # Clojure-like sugar
//
// Program ::= Node               # Top level

export function parseNode(p: Parser): Node {
  switch (p.current.id) {
    case 'eof':
      throw { message: 'Unexpected end of file', loc: p.pos };

    case 'lparen':
      return parseList(p, 'rparen');
    case 'lbrack':
      return parseList(p, 'rbrack');

    case 'rparen':
      throw { message: 'Unexpected )', loc: p.pos };
    case 'rbrack':
      throw { message: 'Unexpected ]', loc: p.pos };

    case 'bool': {
      let value = p.current.source[p.current.start] === 't';
      let b: Bool = { tag: 'Bool', value, loc: p.pos };
      next(p);
      return b;
    }
    case 'int': {
      let value = parseInt(tokenValue(p.current));
      let i: Num = { tag: 'Num', value, loc: p.pos };
      next(p);
      return i;
    }
    case 'name': {
      let s: Name = { tag: 'Name', value: tokenValue(p.current), loc: p.pos };
      next(p);
      return s;
    }
    case 'BAD':
      throw { message: 'Bad characters', loc: p.pos };

    default:
      //log('tok ' + JSON.stringify(p.current))
      throw ShouldNotGetHere;
  }
}

function parseList(p: Parser, end_id: string): List {
  next(p); // eat (

  if (p.current.id !== 'name') {
    throw { message: 'Expected name after (', loc: p.pos };
  }
  let list: List = {
    tag: 'List',
    name: tokenValue(p.current),
    loc: p.pos,
    children: [],
  };
  next(p); // move past head

  while (p.current.id !== end_id) {
    //log('p.current.id ' + p.current.id);
    list.children.push(parseNode(p));
  }
  next(p); // eat rparen / rbrack

  return list;
}

export function parse(tokens: Token[]): Node {
  let p = { tokens, pos: 0, current: tokens[0] };
  let node = parseNode(p);

  // We only parse one expression
  if (p.current.id !== 'eof') {
    //throw new Error('Extra token ' + p.current.id);
    throw {
      message: `Extra token ${p.current.id} at position ${p.pos}`,
      loc: p.pos,
    };
  }
  return node;
}
