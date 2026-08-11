// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// TS-CAN-074: conditional or mapped recursion

// Conditional recursion: deep unwrap via conditional
export type DeepArray<T> = T extends Array<infer U> ? DeepArray<U> : T;

export type DeepArrayResult = DeepArray<string[][][]>; // string

// Mapped recursion: deep partial via mapped
export type DeepPartial<T> = {
  [K in keyof T]?: T[K] extends object ? DeepPartial<T[K]> : T[K];
};

export type NestedRecord = {
  label: string;
  child: { tag: string; count: number };
};

export type DeepPartialNested = DeepPartial<NestedRecord>;

// Recursive conditional that terminates on primitive
export type Flatten<T> = T extends object
  ? T extends Array<infer U>
    ? Flatten<U>
    : { [K in keyof T]: Flatten<T[K]> }
  : T;

export type FlattenedNested = Flatten<NestedRecord>;

export const deepArrayExample: DeepArrayResult = "atlas";
export const deepPartialExample: DeepPartialNested = { label: "atlas" };
export const flattenedExample: FlattenedNested = {
  label: "atlas",
  child: { tag: "beacon", count: 3 },
};
