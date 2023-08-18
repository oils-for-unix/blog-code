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
  if (lhs.tag == "Error" || rhs.tag == "Error") {
    // If a subexpression has an error, we already assigned it
    // But the parent expression still gets a type, I guess so we don't spam errors
    return true;
  }
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

// Find the first error by DFS, or return the top level type
function find_error(expr: Expr<Type>): Type {
  switch (expr.kind.tag) {
    case "bool":
    case "int":
      return expr.typ;

    case "binary":
      var lhs = find_error(expr.kind.lhs);
      var rhs = find_error(expr.kind.rhs);
      if (lhs.tag === "Error") {
        return lhs;
      }
      if (rhs.tag === "Error") {
        return rhs;
      }
      return expr.typ;  // top level type

    case "if":
      var cond = find_error(expr.kind.cond);
      var then_branch = find_error(expr.kind.then_branch);
      var else_branch = find_error(expr.kind.else_branch);

      if (cond.tag === "Error") {
        return cond;
      }
      if (then_branch.tag === "Error") {
        return then_branch;
      }
      if (else_branch.tag === "Error") {
        return else_branch;
      }
      return expr.typ;  // top level type
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
console.log(find_error(t));

var i = make_expr({tag: "int", value: 42 })

var t = infer_types(i);
console.log(find_error(t));

// true + 42
var b_plus_i = make_expr({tag: "binary", op: BinaryOp.Add, lhs: b, rhs: i })

var t = infer_types(b_plus_i);
console.log(find_error(t));

// if (42) { true } else { true }
var if_1 = make_expr({tag: "if", cond: i, then_branch: b, else_branch: b})
var t = infer_types(if_1);
console.log(find_error(t));

// if (true) { true } else { true }
var if_true = make_expr({tag: "if", cond: b, then_branch: b, else_branch: b})
var t = infer_types(if_true);
console.log(find_error(t));

// if (true) { true } else { 42 }
var if_bad = make_expr({tag: "if", cond: b, then_branch: b, else_branch: i})
var t = infer_types(if_bad);
console.log(find_error(t));

// if (true) { true } else { true + 42 }
var else_bad = make_expr({tag: "if", cond: b, then_branch: b, else_branch: b_plus_i})
var t = infer_types(else_bad);
console.log(find_error(t));

// 42 + (true + 42)
var r_bad = make_expr({tag: "binary", op: BinaryOp.Add, lhs: i, rhs: b_plus_i});
var t = infer_types(r_bad);
console.log(find_error(t));
