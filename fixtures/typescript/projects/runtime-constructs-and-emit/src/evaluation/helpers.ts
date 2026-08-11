// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export class SpreadDemo {
  values = [1, 2, 3];

  spreadArray(): number[] {
    return [...this.values];
  }

  spreadIterable(iterable: Iterable<number>): number[] {
    return [...iterable];
  }
}

export function spreadAssumptions(): string {
  const array = [1, 2, 3];
  const fromArray = [...array];
  const set = new Set([4, 5, 6]);
  const fromSet = [...set];
  const map = new Map([["a", 1]]);
  const fromMapKeys = [...map.keys()];
  void fromArray;
  void fromSet;
  void fromMapKeys;
  return `spread:${fromArray.length}:${fromSet.length}:${fromMapKeys.length}`;
}

import { BaseField } from "./fields.js";

export class HelperDedupA extends BaseField {
  prop = "a";
  method(): string {
    return this.prop;
  }
}

export class HelperDedupB extends BaseField {
  prop = "b";
  method(): string {
    return this.prop;
  }
}

export async function helperCreatedDependency(): Promise<string> {
  const value = await Promise.resolve("atlas");
  return `helper:${value}`;
}

export function inlineHelperExample(): string {
  const target = { a: 1 };
  const source = { b: 2 };
  const merged = { ...target, ...source };
  return `${merged.a}:${merged.b}`;
}
