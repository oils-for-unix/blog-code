interface Location {
  file: string;
  line: number;
  column: number;
}

//
// Expressions
//

export interface Expr<T> {
  location: Location;
  typ: T;
  kind: ExprKind<T>;
}

interface ExprBool<T> {
  tag: "bool",
  value: boolean;
}

interface ExprInt<T> {
  tag: "int",
  value: number;
}

export enum BinaryOp {
  Add, Sub, Mul, Div,
  Eq, Neq,
  Lt, Gt, Le, Ge,
}

interface ExprBinary<T> {
  tag: "binary";
  op: BinaryOp;
  lhs: Expr<T>;
  rhs: Expr<T>;
}

interface ExprIf<T> {
  tag: "if";
  cond: Expr<T>;
  then_branch: Expr<T>;
  else_branch: Expr<T>;
}

export type ExprKind<T> =
  | ExprBool<T>
  | ExprInt<T>
  | ExprBinary<T>
  | ExprIf<T>;

//
// Types
//

interface TypeBool {
  tag: "bool";
}
const MyBool: TypeBool = { tag: "bool" };

interface TypeInt {
  tag: "int";
}
const MyInt: TypeInt = { tag: "int" };

export interface TypeError {
  tag: "Error";
  location: Location;
  message: string;
}

export type Type = TypeBool | TypeInt | TypeError;

//
// Infer
//

function result_type(op: BinaryOp, location: Location): Type {
  switch(op) {
    case BinaryOp.Add:
    case BinaryOp.Sub:
    case BinaryOp.Mul:
    case BinaryOp.Div:
      return MyInt;

    case BinaryOp.Eq:
    case BinaryOp.Neq:
    case BinaryOp.Lt:
    case BinaryOp.Gt:
    case BinaryOp.Le:
    case BinaryOp.Ge:
      return MyBool;

    default:
      return {tag: "Error", location, message: "oops"};
  }
}

function type_equal(lhs: Type, rhs: Type): boolean {
  if (lhs.tag == "Error" || rhs.tag == "Error") {
    // If a subexpression has an error, we already assigned it
    // But the parent expression still gets a type, I guess so we don't spam errors
    return true;
  }
  return lhs.tag == rhs.tag;
}

export function infer_types(expr: Expr<void>, errors: TypeError[]): Expr<Type> {
  var ok = true;

  switch (expr.kind.tag) {
    case "bool":
      return {
        location: expr.location,
        typ: MyBool,
        kind: expr.kind,
      };

    case "int":
      return {
        location: expr.location,
        typ: MyInt,
        kind: expr.kind,
      };

    case "binary": {
      var lhs = infer_types(expr.kind.lhs, errors);
      var rhs = infer_types(expr.kind.rhs, errors);

      if (!type_equal(lhs.typ, rhs.typ)) {
        errors.push({
          tag: "Error",
          location: expr.location,
          message: "binary expression operands have different types",
        });
        ok = false;
      }

      return {
        location: expr.location,
        // The type of a valid binary expression is determined by the operator
        typ: ok ? result_type(expr.kind.op, expr.location) : errors[0],
        kind: {
          tag: "binary",
          op: expr.kind.op,
          lhs,
          rhs,
        }
      };
    }

    case "if": {
      var cond = infer_types(expr.kind.cond, errors);
      var then_branch = infer_types(expr.kind.then_branch, errors);
      var else_branch = infer_types(expr.kind.else_branch, errors);

      if (!type_equal(cond.typ, MyBool)) {
        errors.push({
          tag: "Error",
          location: expr.location,
          message: "if condition is not a boolean",
        });
        ok = false;
      }
      if (!type_equal(then_branch.typ, else_branch.typ)) {
        errors.push({
          tag: "Error",
          location: expr.location,
          message: "if branches have different types",
        });
        ok = false;
      }

      return {
        location: expr.location,
        // A valid if inherits the type of its branches
        typ: ok ? then_branch.typ : errors[0],
        kind: {
          tag: "if",
          cond,
          then_branch,
          else_branch,
        }
      }
    }
  }
}
