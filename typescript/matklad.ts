interface Location {
  file: string;
  line: number;
  column: number;
}

export interface Expr<T> {
  location: Location;
  typ: T;
  kind: ExprKind<T>;
}

interface ExprLiteral<T, V, Tag> {
  tag: Tag;
  value: V;
}

type ExprBool<T> = ExprLiteral<T, boolean, "bool">;
type ExprInt<T> = ExprLiteral<T, number, "int">;

export type ExprKind<T> =
  | ExprBool<T>
  | ExprInt<T>
  | ExprBinary<T>
  | ExprControl<T>;

interface ExprBinary<T> {
  tag: "binary";
  op: BinaryOp;
  lhs: Expr<T>;
  rhs: Expr<T>;
}

export enum BinaryOp {
  Add, Sub, Mul, Div,
  Eq, Neq,
  Lt, Gt, Le, Ge,
}

type ExprControl<T> = ExprIf<T>;

interface ExprIf<T> {
  tag: "if";
  cond: Expr<T>;
  then_branch: Expr<T>;
  else_branch: Expr<T>;
}

/*
 * Types
 */

export type Type = TypeBool | TypeInt | TypeError;

interface TypeBool {
  tag: "bool";
}
const TypeBool: TypeBool = { tag: "bool" };

interface TypeInt {
  tag: "int";
}
const TypeInt: TypeInt = { tag: "int" };


type Visitor<T, R> = {
  bool(kind: ExprBool<T>): R;
  int(kind: ExprInt<T>): R;
  binary(kind: ExprBinary<T>, location: Location): R;
  if(kind: ExprIf<T>, location: Location): R;
};

function visit<T, R>(
  expr: Expr<T>,
  v: Visitor<T, R>,
): R {
  switch (expr.kind.tag) {
    case "bool": return v.bool(expr.kind);
    case "int": return v.int(expr.kind);
    case "binary": return v.binary(expr.kind, expr.location);
    case "if": return v.if(expr.kind, expr.location);
  }
}

function transform<U, V>(expr: Expr<U>, v: Visitor<V, V>): Expr<V> {
  switch (expr.kind.tag) {
    case "bool":
      return {
        location: expr.location,
        typ: v.bool(expr.kind),
        kind: expr.kind,
      };
    case "int":
      return {
        location: expr.location,
        typ: v.int(expr.kind),
        kind: expr.kind,
      };
    case "binary": {
      const kind: ExprBinary<V> = {
        tag: "binary",
        op: expr.kind.op,
        lhs: transform(expr.kind.lhs, v),
        rhs: transform(expr.kind.rhs, v),
      };
      return {
        location: expr.location,
        typ: v.binary(kind, expr.location),
        kind: kind,
      };
    }
    case "if": {
      const kind: ExprIf<V> = {
        tag: "if",
        cond: transform(expr.kind.cond, v),
        then_branch: transform(expr.kind.then_branch, v),
        else_branch: transform(expr.kind.else_branch, v),
      };
      return {
        location: expr.location,
        typ: v.if(kind, expr.location),
        kind: kind,
      };
    }
  }
}

interface TypeError {
  tag: "Error";
  location: Location;
  message: string;
}

function type_equal(lhs: Type, rhs: Type): boolean {
  if (lhs.tag == "Error" || rhs.tag == "Error") return true;
  return lhs.tag == rhs.tag;
}

export function infer_types(expr: Expr<void>): Expr<Type> {
  return transform(expr, {
    bool: (): Type => TypeBool,
    int: (): Type => TypeInt,

    binary: (kind: ExprBinary<Type>, location: Location): Type => {
      if (!type_equal(kind.lhs.typ, kind.rhs.typ)) {
        return {
          tag: "Error",
          location,
          message: "binary expression operands have different types",
        };
      }
      return result_type(kind.op, location);
    },

    if: (kind: ExprIf<Type>, location: Location): Type => {
      if (!type_equal(kind.cond.typ, TypeBool)) {
        return {
          tag: "Error",
          location,
          message: "if condition is not a boolean",
        };
      }
      if (!type_equal(kind.then_branch.typ, kind.else_branch.typ)) {
        return {
          tag: "Error",
          location,
          message: "if branches have different types",
        };
      }
      return kind.then_branch.typ;
    },
  });
}

function result_type(op: BinaryOp, location: Location): Type {
  switch(op) {
    case BinaryOp.Add:
    case BinaryOp.Sub:
    case BinaryOp.Mul:
    case BinaryOp.Div:
      return TypeInt;

    case BinaryOp.Eq:
    case BinaryOp.Neq:
    case BinaryOp.Lt:
    case BinaryOp.Gt:
    case BinaryOp.Le:
    case BinaryOp.Ge:
      return TypeBool;

    default:
      return {tag: "Error", location, message: "oops"};
  }
}
