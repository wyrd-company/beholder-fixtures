// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// TS-CAN-070: distributive and bracket-suppressed conditional types

export type DistributiveToArray<T> = T extends unknown ? T[] : never;

export type BracketSuppressed<T> = [T] extends [string] ? true : false;

// Demonstration values
export type DistributiveStringNumber = DistributiveToArray<string | number>; // string[] | number[]
export type DistributiveNever = DistributiveToArray<never>; // never (never input)
export type SuppressedUnion = BracketSuppressed<string | number>; // false (bracket suppresses distribution)
export type SuppressedSingle = BracketSuppressed<string>; // true
export type NeverInput = DistributiveToArray<never>; // never

// Deferred generic condition: condition not resolved until instantiation
export type DeferredCheck<T> = T extends { label: string } ? T["label"] : never;

export function getLabel<T extends { label: string } | { count: number }>(
  value: T,
): DeferredCheck<T> {
  return (value as { label: string }).label as DeferredCheck<T>;
}

// any and unknown in conditional positions
export type WithAny = DistributiveToArray<any>; // any[] (any distributes specially)
export type WithUnknown = DistributiveToArray<unknown>; // unknown[]
export type AnyExtendsString = any extends string ? true : false;
export type UnknownExtendsString = unknown extends string ? true : false;
