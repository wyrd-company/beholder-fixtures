// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// TS-CAN-070: constrained and nested infer, overload return extraction, multiple inference sites

// Constrained infer: infer U extends string
export type ExtractStringPayload<T> = T extends {
  payload: infer U extends string;
}
  ? U
  : never;

export type ConstrainedResult = ExtractStringPayload<{ payload: "atlas" }>; // "atlas"

// Nested infer: infer inside inferred tuple
export type UnwrapPair<T> = T extends [infer A, infer B]
  ? A extends string
    ? B
    : never
  : never;

export type NestedResult = UnwrapPair<["atlas", 42]>; // 42
export type NestedFiltered = UnwrapPair<[42, "atlas"]>; // never

// Multiple inference sites and variance
export type FirstArg<T> = T extends { fn: (a: infer A, b: infer A) => unknown }
  ? A
  : never;

export type MultiSiteResult = FirstArg<{ fn: (a: string, b: string) => void }>; // string

// Overload return extraction (last overload wins through conditional infer)
export function overloaded(value: string): number;
export function overloaded(value: number): string;
export function overloaded(value: string | number): string | number {
  return typeof value === "string" ? value.length : String(value);
}

export type OverloadReturn<T> = T extends {
  (value: string): infer R1;
  (value: number): infer R2;
}
  ? R1 | R2
  : never;

export type OverloadedReturnType = OverloadReturn<typeof overloaded>; // number | string

// Last-overload extraction via infer directly
export type LastOverloadReturn<T> = T extends { (...args: infer _A): infer R }
  ? R
  : never;

export type LastReturn = LastOverloadReturn<typeof overloaded>; // string (last overload)

// Nested infer with arrays
export type FlattenInferred<T> = T extends Array<infer U> ? U : T;

export type FlatString = FlattenInferred<string[]>; // string
export type FlatUnknown = FlattenInferred<number>; // number (non-array branch)

export const constrainedExample: ConstrainedResult = "atlas";
export const multiSiteExample: MultiSiteResult = "atlas";
