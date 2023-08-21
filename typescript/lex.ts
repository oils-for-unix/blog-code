import { Id, Token } from './header.ts';

// lex with regular languages

// deno-fmt-ignore
const MATCH = new RegExp(
    '(\\s+)'               // whitespace ignored
  + '|(#[^\\n]+)'          // comment until end of line ignored
  + '|(\\()'               // lparen
  + '|(\\))'               // rparen
  + '|(\\[)'               // lbrack
  + '|(\\])'               // rbrack
  + '|(true|false)'        // boolean
  + '|([0-9]+)'            // integer
  + '|([-\\+a-z*/=<>]+)'   // name: define, + - * /  == != < >  TODO: add more
  + '|(.)',                // BAD
  'y'); // sticky bit for exec()

export function lex(s: string) {
  let tokens: Token[] = [];

  let pos = 0;
  while (true) {
    let m = MATCH.exec(s);

    if (m === null) {
      tokens.push({ id: 'eof', start: pos, len: 0, source: s });
      break;
    }

    pos = m.index;

    let id: Id | null = null;
    let len = -1;

    if (m[1] !== undefined) {
      // ignore whitespace
    } else if (m[2] !== undefined) {
      // ignore comment
    } else if (m[3] !== undefined) {
      id = 'lparen';
    } else if (m[4] !== undefined) {
      id = 'rparen';
    } else if (m[5] !== undefined) {
      id = 'lbrack';
    } else if (m[6] !== undefined) {
      id = 'rbrack';
    } else if (m[7] !== undefined) {
      id = 'bool';
      // no length needed, parser looks at first char 't' or 'f'
    } else if (m[8] !== undefined) {
      id = 'int';
      len = m[8].length;
    } else if (m[9] !== undefined) {
      id = 'name';
      len = m[9].length;
    } else if (m[10] !== undefined) {
      id = 'BAD';
    } else {
      throw Error('should not happen');
    }

    if (id !== null) {
      tokens.push({ id, start: pos, len, source: s });
    }

    // Set pos to end position of last token, so a potential EOF token will
    // blame the right column position
    pos = MATCH.lastIndex;
  }
  return tokens;
}
