// alwaysStrict: emit always includes "use strict" regardless of file-level directives.
// This module is valid under both settings; the difference is in emitted JavaScript.

export function computeStrict(value: number): number {
  return value * 2;
}

export function strictAwareCombine(a: string, b: string): string {
  return `${a}-${b}`;
}

export class StrictCounter {
  count = 0;

  increment(): number {
    this.count += 1;
    return this.count;
  }
}
