interface Bool {
  id: "bool",
  value: boolean;
}

interface Int {
  id: "int",
  value: number;
}

interface Str {
  id: "str",
  value: string;
}

type Token = "eof" | "lparen" | "rparen" | Bool | Int | Str;

// 42 is parsed as a number
// "+" and "define" are parsed as strings
type Atom = Bool | Int | Str;

// (+ 1 2)
interface List {
  head: string;
  children: Node[];
}

type Node = Atom | List;

// Shortcuts from https://norvig.com/lispy.html

export function tokenize(s: string): Token[] {
  var spaces = s.replace('(', ' ( ').replace(')', ' ) ');

  var parts = spaces.match(/\S+/g);

  if (parts === null) {
    return ["eof"];  // empty token string
  }

  var tokens: Token[] = [];
  for (var part of parts) { 
    var tok: Token | null = null;
    if (part === "(") {
      tok = "lparen"

    } else if (part === ")") {
      tok = "rparen"

    } else if (part === "true") {
      tok = {id: "bool", value: true}

    } else if (part === "false") {
      tok = {id: "bool", value: false}

    } else {
      // 42 becomes a number, everything else becomes a string
      var i = parseInt(part);

      if (isNaN(i)) {
        tok = {id: "str", value: part}
      } else {
        tok = {id: "int", value: i}
      }
    }
    tokens.push(tok);
  }
  tokens.push("eof");
  return tokens;
}

function parseList(tokens: Token[]): List {
  return {head: 'a', children: []}
}

export function parse(tokens: Token[]): Node {
  var tok = tokens[0];

  switch (tok) {
    case 'eof':
      throw new Error('Unexpected EOF');

    case 'lparen':
      return parseList(tokens);

    case 'rparen':
      throw new Error('Unexpected )');

    default: 
      switch (tok.id) {
        case 'bool':
        case 'int':
        case 'str':
          return tok;
      }
  }
}
