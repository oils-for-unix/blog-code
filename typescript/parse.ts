var log = console.log;

type Id = 'lparen' | 'rparen' | 'lbrack' | 'rbrack' | 'bool' | 'int' | 'str' | 'eof';

interface Token {
  id: Id;
  start: number;  // 3
  len: number;  // 1
  source: string;  // Use the whole program for now
                   // Avoid string allocations unless we need them
}

function tokenValue(tok: Token) {
  return tok.source.slice(tok.start, tok.start + tok.len);
}

// Shortcuts from https://norvig.com/lispy.html

const MATCH = new RegExp(
    '(\\s+)'               // whitespace ignored
  + '|(#[^\\n]+)'          // comment until end of line ignored
  + '|(\\()'               // lparen
  + '|(\\))'               // rparen
  + '|(\\[)'               // lbrack
  + '|(\\])'               // rbrack
  + '|(true|false)'        // boolean
  + '|([0-9]+)'            // integer
  + '|([-\\+a-z*/=<>]+)',  // string: define, + - * /  == != < >
  'y');             // sticky bit for exec()


export function lex(s: string) {
  var tokens: Token[] = [];

  var pos = 0;
  while (true) {
    var m = MATCH.exec(s);

    if (m === null) {
      tokens.push({id: "eof", start: pos, len: 0, source: s})
      break;
    }

    pos = m.index;

    var id: Id | null = null;
    var len = -1;

    if (m[1] !== undefined) {
      // ignore whitespace

    } else if (m[2] !== undefined) {
      // ignore comment

    } else if (m[3] !== undefined) {
      id = "lparen";

    } else if (m[4] !== undefined) {
      id = "rparen";

    } else if (m[5] !== undefined) {
      id = "lbrack";

    } else if (m[6] !== undefined) {
      id = "rbrack";

    } else if (m[7] !== undefined) {
      id = "bool";
      // no length needed, parser looks at first char 't' or 'f'

    } else if (m[8] !== undefined) {
      id = "int";
      len = m[8].length;

    } else if (m[9] !== undefined) {
      id = 'str';
      len = m[9].length;

    } else {
      throw Error('should not happen')
    }

    if (id !== null) {
      tokens.push({id, start: pos, len, source: s});
    }

    // Set pos to end position of last token, so a potential EOF token will
    // blame the right column position
    pos = MATCH.lastIndex;
  }
  return tokens;
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
type Atom = Bool | Int | Str;

// (== 5 (+ 2 3))
interface List {
  name: string,
  loc: number;
  children: Node[];
}

type Node = Atom | List;

interface SyntaxError {
  message: string;
  pos: number;
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

export function read(tokens: Token[]): Node {
  var p = {tokens, pos: 0, current: tokens[0]}
  var node = parseNode(p);

  // We only parse one expression
  if (p.current.id !== 'eof') {
    //throw new Error('Extra token ' + p.current.id);
    throw {message: `Extra token ${p.current.id} at ${p.pos}`, pos: p.pos};
  }

  return node;
}
