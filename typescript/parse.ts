interface Token {
  id: string,  // "rparen"
  start: number,  // 3
  len: number,  // 1
  source: string;  // Use the whole program for now
                   // Avoid string allocations unless we need them
}

// Shortcuts from https://norvig.com/lispy.html

const MATCH = new RegExp(
    '(\\s+)'         // whitespace ignored
  + '|(#[^\\n]+)'    // comment until end of line ignored
  + '|(\\()'         // lparen
  + '|(\\))'         // rparen
  + '|(true|false)'  // boolean
  + '|([0-9]+)'      // integer
  + '|(\\S+)',       // string: define, +, ==
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

    var id: string | null = null;
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
      id = "bool";
      // no length needed, parser looks at first char 't' or 'f'

    } else if (m[6] !== undefined) {
      id = "int";
      len = m[6].length;

    } else if (m[7] !== undefined) {
      id = 'str';
      len = m[7].length;

    } else {
      throw Error('should not happen')
    }

    if (id !== null) {
      tokens.push({id, start: pos, len, source: s});
    }
  }
  return tokens;
}

interface Bool {
  id: "bool";
  value: boolean;
  loc: Token,
}

interface Int {
  id: 'int';
  value: number;
  loc: Token,
}

interface Str {
  id: "str";
  value: string;
  loc: Token,
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
  name: Token;
  children: Node[];
}

type Node = Atom | List;

// S-Expression Grammar
//
// Atom ::= Bool | Int | Str
// Node ::= Atom | List
// List ::= '(' Str Node* ')

function parseList(tokens: Token[], pos: number): List {
  pos++;  // eat (

  if (tokens[pos].id !== 'str') {
    throw new Error('Expected string after (');
  }

  var node: Node = {name: tokens[pos], children: []};
  pos++;

  while (tokens[pos].id !== 'rparen') {
    node.children.push(parseNode(tokens, pos));
    pos++;
  }
  pos++;  // eat rparen

  return node;
}

export function parseNode(tokens: Token[], pos: number): Node {
  var tok = tokens[pos];

  switch (tok.id) {
    case 'eof':
      throw new Error('Unexpected EOF');

    case 'lparen':
      return parseList(tokens, pos);

    case 'rparen':
      throw new Error('Unexpected )');

    case 'bool':
      return {id: 'bool', value: tok.source[tok.start] === 't', loc: tok};

    case 'int':
      var i = parseInt(tok.source.slice(tok.start, tok.start + tok.len));
      return {id: 'int', value: i, loc: tok}

    case 'str':
      var s = tok.source.slice(tok.start, tok.start + tok.len);
      return {id: 'str', value: s, loc: tok}

    default:
      throw new Error('should not happen')
  }
}

export function parse(tokens: Token[]): Node {
  return parseNode(tokens, 0);  // from the first token
}

