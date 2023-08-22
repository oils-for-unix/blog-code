import { Error, Expr, List, Node, ShouldNotGetHere } from './header.ts';

const log = console.log;

function checkArity(node: List, expected: number, errors: Error[]) {
  let actual = node.args.length;
  if (actual !== expected) {
    let message = `${node.name} expected ${expected} args, got ${actual}`;
    errors.push({ tag: 'Error', message, loc: node.loc });
    return false;
  }

  for (let child of node.args) {
    switch (child.tag) {
      case 'Bool':
      case 'Num':
      case 'List':
        break;

      // Name is only for the head
      // This only happens when we have no variables in the language!
      default: {
        let message = `Unexpected arg of type ${child.tag}`;
        errors.push({ tag: 'Error', message, loc: child.loc });
        return false;
      }
    }
  }

  return true;
}

export function transform(node: Node, errors: Error[]): Expr {
  switch (node.tag) {
    // Atom PNodes are also valid expressions
    case 'Bool':
    case 'Num':
    case 'Name':  // TODO: take it out and remove Name from Expr?
      return node;

    case 'List': {
      switch (node.name) {
        case 'if': {
          if (!checkArity(node, 3, errors)) {
            return errors[0];
          }
          let cond = transform(node.args[0], errors);
          let then = transform(node.args[1], errors);
          let else_ = transform(node.args[2], errors);
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
          let left = transform(node.args[0], errors);
          let right = transform(node.args[1], errors);
          return { tag: 'Binary', op: node.name, loc: node.loc, left, right };
        }

        default: {
          let message = `Invalid node '${node.name}'`;
          errors.push({ tag: 'Error', message, loc: node.loc });
          return errors[0];
        }
      }
    }
  }

  throw ShouldNotGetHere;
}
