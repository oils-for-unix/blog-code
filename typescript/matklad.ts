interface Location {
  file: string;
  line: number;
  column: number;
}

//
// Expressions
//

interface Expr<T> {
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

enum BinaryOp {
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

type ExprKind<T> =
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

type Type = TypeBool | TypeInt | TypeError;

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
  if (lhs.tag == "Error" || rhs.tag == "Error") return true;
  return lhs.tag == rhs.tag;
}

function infer_types(expr: Expr<void>): Expr<Type> {
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
      const kind: ExprBinary<Type> = {
        tag: "binary",
        op: expr.kind.op,
        lhs: infer_types(expr.kind.lhs),
        rhs: infer_types(expr.kind.rhs),
      };

      var err: Type | undefined = undefined;
      if (!type_equal(kind.lhs.typ, kind.rhs.typ)) {
        err = {
          tag: "Error",
          location: expr.location,
          message: "binary expression operands have different types",
        };
      }

      return {
        location: expr.location,
        typ: err || result_type(kind.op, expr.location),
        kind: kind,
      };
    }

    case "if": {
      const kind: ExprIf<Type> = {
        tag: "if",
        cond: infer_types(expr.kind.cond),
        then_branch: infer_types(expr.kind.then_branch),
        else_branch: infer_types(expr.kind.else_branch),
      };

      var err: Type | undefined = undefined;
      if (!type_equal(kind.cond.typ, MyBool)) {
        err = {
          tag: "Error",
          location: expr.location,
          message: "if condition is not a boolean",
        };
      }
      if (!type_equal(kind.then_branch.typ, kind.else_branch.typ)) {
        err = {
          tag: "Error",
          location: expr.location,
          message: "if branches have different types",
        };
      }

      return {
        location: expr.location,
        typ: err || kind.then_branch.typ,
        kind: kind,
      };
    }
  }
}

//
// Test
//

var loc = {"file": "foo.lang", line: 1, column: 1};

function make_expr(kind: ExprKind<void>) {
  return {location: loc, typ: undefined, kind: kind};
}

var b = make_expr({tag: "bool", value: true });

var t = infer_types(b);
console.log(t.typ);

var i = make_expr({tag: "int", value: 42 })

var t = infer_types(i);
console.log(t.typ);

// true + 42
var b_plus_i = make_expr({tag: "binary", op: BinaryOp.Add, lhs: b, rhs: i })

var t = infer_types(b_plus_i);
console.log(t.typ);

// if (42) { true } else { true }
var if_1 = make_expr({tag: "if", cond: i, then_branch: b, else_branch: b})
var t = infer_types(if_1);
console.log(t.typ);

// if (true) { true } else { true }
var if_true = make_expr({tag: "if", cond: b, then_branch: b, else_branch: b})
var t = infer_types(if_true);
console.log(t.typ);

// if (true) { true } else { 42 }
var if_bad = make_expr({tag: "if", cond: b, then_branch: b, else_branch: i})
var t = infer_types(if_bad);
console.log(t.typ);
