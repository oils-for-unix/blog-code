var log = console.log;

import { Token, Atom, List, Node } from './header.ts';

function tokenValue(tok: Token) {
  return tok.source.slice(tok.start, tok.start + tok.len);
}


// S-Expression Grammar
//
// Atom ::= Bool | Int | Str
// Node ::= Atom | List
// List ::= '(' Str Node* ')

interface Parser {
  tokens: Token[],
  pos: number,
  current: Token;
}

function next(p: Parser) {
  p.pos++;
  p.current = p.tokens[p.pos];
}

function parseList(p: Parser, end_id: string): List {
  next(p);  // eat (

  if (p.current.id !== 'str') {
    throw {message: 'Expected string after (', pos: p.pos};
  }
  var node: Node = {name: tokenValue(p.current), loc: p.pos, children: []};
  next(p);  // move past head

  while (p.current.id !== end_id) {
    //log('p.current.id ' + p.current.id);
    node.children.push(parseNode(p));
  }
  next(p);  // eat rparen / rbrack

  return node;
}

export function parseNode(p: Parser): Node {
  switch (p.current.id) {
    case 'eof':
      throw {message: 'Unexpected end of file', pos: p.pos};

    case 'lparen':
      return parseList(p, 'rparen');

    case 'lbrack':
      return parseList(p, 'rbrack');

    case 'rparen':
      throw {message: 'Unexpected )', pos: p.pos};

    case 'rbrack':
      throw {message: 'Unexpected ]', pos: p.pos};

    case 'bool':
      var b = p.current.source[p.current.start] === 't';
      var atom: Atom = {id: 'bool', value: b, loc: p.pos};
      next(p);
      return atom;

    case 'int':
      var i = parseInt(tokenValue(p.current));
      var atom: Atom = {id: 'int', value: i, loc: p.pos}
      next(p);
      return atom;

    case 'str':
      var atom: Atom = {id: 'str', value: tokenValue(p.current), loc: p.pos}
      next(p);
      return atom;

    default:
      //log('tok ' + JSON.stringify(p.current))
      throw new Error('ASSERT: Unexpected ID ' + p.current.id)
  }
}

export function parse(tokens: Token[]): Node {
  var p = {tokens, pos: 0, current: tokens[0]}
  var node = parseNode(p);

  // We only parse one expression
  if (p.current.id !== 'eof') {
    //throw new Error('Extra token ' + p.current.id);
    throw {message: `Extra token ${p.current.id} at ${p.pos}`, pos: p.pos};
  }

  return node;
}
