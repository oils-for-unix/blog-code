// Imported module must be string literal
import { infer_types, ExprKind, BinaryOp, Expr, Type, TypeError } from './bool-int-andy.ts'

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

function runCase(s: string, ex: Expr<void>) {
  var errors: TypeError[] = [];

  console.log('\t%s =>', s);

  var t = infer_types(ex, errors);
  if (errors.length !== 0) {
    console.log("Errors:");
    for (var e of errors) {
      console.log(e);
    }
  } else {
    console.log("OK");
    console.log(t.typ);
  }
  console.log('---');
}

function run_tests() {
  var loc = {"file": "foo.lang", line: 1, column: 1};

  function make_expr(kind: ExprKind<void>) {
    return {location: loc, typ: undefined, kind: kind};
  }

  var b = make_expr({tag: "bool", value: true });
  runCase('true', b);

  var i = make_expr({tag: "int", value: 42 })
  runCase('42', i);

  var b_plus_i = make_expr({tag: "binary", op: BinaryOp.Add, lhs: b, rhs: i })
  runCase('true + 42', b_plus_i);

  var if_1 = make_expr({tag: "if", cond: i, then_branch: b, else_branch: b})
  runCase('if (42) { true } else { true }', if_1);

  var if_true = make_expr({tag: "if", cond: b, then_branch: b, else_branch: b})
  runCase('if (true) { true } else { true }', if_true);

  var if_bad = make_expr({tag: "if", cond: b, then_branch: b, else_branch: i})
  runCase('if (true) { true } else { 42 }', if_bad);

  var else_bad = make_expr({tag: "if", cond: b, then_branch: b, else_branch: b_plus_i})
  runCase('if (true) { true } else { true + 42 }', else_bad);

  var r_bad = make_expr({tag: "binary", op: BinaryOp.Add, lhs: i, rhs: b_plus_i});
  runCase('42 + (true + 42)', r_bad);

  var two_errors = make_expr({tag: "if", cond: i, then_branch: b, else_branch: b_plus_i})
  runCase('if (42) { true } else { true + 42 }', two_errors);

  var three_errors = make_expr({tag: "if", cond: i, then_branch: b_plus_i, else_branch: b_plus_i})
  runCase('if (42) { true + 42 } else { true + 42 }', three_errors);
}

run_tests();
