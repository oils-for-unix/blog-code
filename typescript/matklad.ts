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
  | ExprInt<T>;
  //| ExprBinary<T>
  //| ExprControl<T>;

/*

export interface ExprBinary<T> {
  op: BinaryOp;
  lhs: Expr<T>;
  rhs: Expr<T>;
}

export enum BinaryOp {
  Add, Sub, Mul, Div,
  Eq, Neq,
  Lt, Gt, Le, Ge,
}

*/
