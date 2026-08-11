// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// TS-CAN-071: tuple and array mapping, recursive maps

export type ToArray<T> = {
  [K in keyof T]: T[K][];
};

// Tuple mapping: preserves tuple structure homomorphically
export type TupleToUnion<T extends readonly unknown[]> = {
  [K in keyof T]: T[K];
};

export type MappedPairSource = [string, number];
export type MappedPair = TupleToUnion<MappedPairSource>; // [string, number] mapped retains tuple

export type ArrayMapped = ToArray<{ label: string; count: number }>;
// { label: string[]; count: number[] }

// Recursive maps
export type DeepReadonly<T> = {
  readonly [K in keyof T]: T[K] extends object ? DeepReadonly<T[K]> : T[K];
};

export type MappedNested = {
  label: string;
  child: { tag: string; value: number };
};

export type DeepReadonlyNested = DeepReadonly<MappedNested>;

export type MappedDeepPartial<T> = {
  [K in keyof T]?: T[K] extends object ? MappedDeepPartial<T[K]> : T[K];
};

export type MappedDeepPartialNested = MappedDeepPartial<MappedNested>;

export const deepReadonlyExample: DeepReadonlyNested = {
  label: "atlas",
  child: { tag: "beacon", value: 42 },
};

export const mappedDeepPartialExample: MappedDeepPartialNested = {
  label: "atlas",
};
