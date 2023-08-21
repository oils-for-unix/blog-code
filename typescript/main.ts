import { interpret } from './yaks.ts';
import { Value } from './header.ts';

function write(s: string) {
  let bytes = new TextEncoder().encode(s);
  Deno.writeAllSync(Deno.stdout, bytes);
}

export function run(prog: string, flags: number): Value | undefined {
  let ctx = { log: console.log, write: write };
  return interpret(ctx, prog, flags);
}
