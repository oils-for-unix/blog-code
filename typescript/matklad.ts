export interface Location {
  file: string;
  line: number;
  column: number;
}

export interface Expr<T> {
  location: Location;
  data: T;
  kind: ExprKind<T>;
}

export interface ExprLiteral<T, V, Tag> {
  tag: Tag;
  value: V;
}

export type ExprBool<T> = ExprLiteral<T, boolean, "bool">;
export type ExprInt<T> = ExprLiteral<T, number, "int">;

export type ExprKind<T> =
  | ExprBool<T>
  | ExprInt<T>
  | ExprBinary<T>
  | ExprControl<T>;

export interface ExprBinary<T> {
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

export type ExprControl<T> = ExprIf<T>;

export interface ExprIf<T> {
  tag: "if";
  cond: Expr<T>;
  then_branch: Expr<T>;
  else_branch: Expr<T>;
}

/*
 * Types
 */

type Type = TypeBool | TypeInt | TypeError;

interface TypeBool {
  tag: "bool";
}
const TypeBool: TypeBool = { tag: "bool" };

interface TypeInt {
  tag: "int";
}
const TypeInt: TypeInt = { tag: "int" };


export type Visitor<T, R> = {
  bool(kind: ExprBool<T>): R;
  int(kind: ExprInt<T>): R;
  binary(kind: ExprBinary<T>, location: Location): R;
  if(kind: ExprIf<T>, location: Location): R;
};

export function visit<T, R>(
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

export function transform<U, V>(expr: Expr<U>, v: Visitor<V, V>): Expr<V> {
  switch (expr.kind.tag) {
    case "bool":
      return {
        location: expr.location,
        data: v.bool(expr.kind),
        kind: expr.kind,
      };
    case "int":
      return {
        location: expr.location,
        data: v.int(expr.kind),
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
        data: v.binary(kind, expr.location),
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
        data: v.if(kind, expr.location),
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

function infer_types(expr: Expr<void>): Expr<Type> {
  return transform(expr, {
    bool: (): Type => TypeBool,
    int: (): Type => TypeInt,

    binary: (kind: ExprBinary<Type>, location: Location): Type => {
      if (!type_equal(kind.lhs.data, kind.rhs.data)) {
        return {
          tag: "Error",
          location,
          message: "binary expression operands have different types",
        };
      }
      return result_type(kind.op, location);
    },

    if: (kind: ExprIf<Type>, location: Location): Type => {
      if (!type_equal(kind.cond.data, TypeBool)) {
        return {
          tag: "Error",
          location,
          message: "if condition is not a boolean",
        };
      }
      if (!type_equal(kind.then_branch.data, kind.else_branch.data)) {
        return {
          tag: "Error",
          location,
          message: "if branches have different types",
        };
      }
      return kind.then_branch.data;
    },
  });
}

function result_type(op: BinaryOp, location: Location): Type {
  switch(op) {
    case BinaryOp.Add:
      return TypeInt;
    case BinaryOp.Eq:
      return TypeBool;
    default:
      return {"tag": "Error", location, message: "oops"};
  }
}

//var t = infer_types( {"tag": "bool", value: true } );

var loc = {"file": "foo.lang", line: 1, column: 1};

var expr = {"location": loc, data: undefined, kind: {tag: "bool", value: true }};

var t = infer_types(expr);

//var t = infer_types( {"tag": "bool", value: true } );
console.log(t);
