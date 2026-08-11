// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// TS-CAN-070: recursive unwrapping transformation

export type DeepUnwrap<T> =
  T extends Promise<infer U>
    ? DeepUnwrap<U>
    : T extends Array<infer V>
      ? DeepUnwrap<V>
      : T;

export type UnwrappedPromise = DeepUnwrap<Promise<string>>; // string
export type UnwrappedNested = DeepUnwrap<Promise<Promise<number>>>; // number
export type UnwrappedArray = DeepUnwrap<string[][]>; // string
export type UnwrappedMixed = DeepUnwrap<Promise<string[]>>; // string

// Recursive conditional with any / unknown
export type UnwrapAny = DeepUnwrap<any>; // any (any passes through)
export type UnwrapUnknown = DeepUnwrap<unknown>; // unknown
export type UnwrapNever = DeepUnwrap<never>; // never

export function unwrapValue<T>(value: T): DeepUnwrap<T> {
  return value as DeepUnwrap<T>;
}

// Deferred generic condition layered with recursion
export type DeepLabel<T> = T extends { nested: infer N }
  ? DeepUnwrap<N>
  : never;

export type DeepLabelResult = DeepLabel<{ nested: Promise<string[]> }>; // string

export const unwrappedExample: UnwrappedNested = 42;
export const labelExample: DeepLabelResult = "atlas";
