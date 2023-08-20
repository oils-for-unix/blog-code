import { Error, Expr, Node, ShouldNotGetHere } from './header.ts';

var log = console.log;

export function transform(node: Node, errors: Error[]): Expr {
  switch (node.tag) {
    case 'List': {
      switch (node.name) {
        case 'If': {
          let actual = node.children.length;
          if (actual !== 3) {
            let message = `If expected 3 children, got ${actual}`;
            errors.push({ tag: 'Transform', message, loc: node.loc });
          }
          break;
        }
        case 'Unary':
          break;
        case 'Binary':
          break;
      }
      return { tag: 'Bool', value: true, loc: -1 };
    }

    case 'Bool':
    case 'Int':
    case 'Str':
      return node;
  }

  throw ShouldNotGetHere;
}
