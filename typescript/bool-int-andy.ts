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

interface TypeError {
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

export function infer_types(expr: Expr<void>): Expr<Type> {
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
      var lhs = infer_types(expr.kind.lhs);
      var rhs = infer_types(expr.kind.rhs);

      var err: Type | undefined = undefined;
      if (!type_equal(lhs.typ, rhs.typ)) {
        err = {
          tag: "Error",
          location: expr.location,
          message: "binary expression operands have different types",
        };
      }

      return {
        location: expr.location,
        typ: err || result_type(expr.kind.op, expr.location),
        kind: {
          tag: "binary",
          op: expr.kind.op,
          lhs: lhs,
          rhs: rhs,
        }
      };
    }

    case "if": {
      var cond = infer_types(expr.kind.cond);
      var then_branch = infer_types(expr.kind.then_branch);
      var else_branch = infer_types(expr.kind.else_branch);

      var err: Type | undefined = undefined;
      if (!type_equal(cond.typ, MyBool)) {
        err = {
          tag: "Error",
          location: expr.location,
          message: "if condition is not a boolean",
        };
      }
      if (!type_equal(then_branch.typ, else_branch.typ)) {
        err = {
          tag: "Error",
          location: expr.location,
          message: "if branches have different types",
        };
      }

      return {
        location: expr.location,
        typ: err || then_branch.typ,
        kind: {
          tag: "if",
          cond: cond,
          then_branch: then_branch,
          else_branch: else_branch,
        }
      }
    }
  }
}
