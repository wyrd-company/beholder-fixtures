/**
 * Source consumed by the compiler-API transformer (TS-CAN-090).
 * The transformer injects a synthetic node and a generated runtime edge
 * absent from this source.
 */

export function greet(name: string): string {
  return `hello ${name}`;
}

export type GreetFn = typeof greet;

export const greetingKind = "formal" as const;
