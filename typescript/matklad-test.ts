// Imported module must be string literal
import { infer_types, ExprKind, BinaryOp, Expr, Type } from './matklad.ts'

// Find the first error by DFS, or return the top level type
export function find_error(expr: Expr<Type>): Type {
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
