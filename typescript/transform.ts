import { Error, Expr, List, Node, ShouldNotGetHere } from './header.ts';

const log = console.log;

function checkArity(node: List, expected: number, errors: Error[]) {
  let actual = node.children.length;
  if (actual !== expected) {
    let message = `${node.name} expected ${expected} children, got ${actual}`;
    errors.push({ tag: 'Transform', message, loc: node.loc });
    return false;
  }
  return true;
}

export function transform(node: Node, errors: Error[]): Expr {
  switch (node.tag) {
    // Atom PNodes are also valid expressions
    case 'Bool':
    case 'Num':
      return node;

    case 'List': {
      switch (node.name) {
        case 'if': {
          if (!checkArity(node, 3, errors)) {
            return errors[0];
          }
          let cond = transform(node.children[0], errors);
          let then = transform(node.children[1], errors);
          let else_ = transform(node.children[2], errors);
          return { tag: 'If', loc: node.loc, cond, then, else: else_ };
        }

        // Binary
        // Num -> Num
        case '+':
        case '-':
        case '*':
        case '/':
        // Num -> Bool
        case '==':
        case '!=':
        case '>':
        case '<':
        // Bool -> Bool
        case 'and':
        case 'or': {
          if (!checkArity(node, 2, errors)) {
            return errors[0];
          }
          let left = transform(node.children[0], errors);
          let right = transform(node.children[1], errors);
          return { tag: 'Binary', op: node.name, loc: node.loc, left, right };
        }

        default: {
          let message = `Invalid node '${node.name}'`;
          errors.push({ tag: 'Transform', message, loc: node.loc });
          return errors[0];
        }
      }
    }
  }

  throw ShouldNotGetHere;
}
