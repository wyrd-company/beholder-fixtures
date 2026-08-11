// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// TS-CAN-071: homomorphic modifier preservation and +/- optional/readonly modifiers

export type BaseRecord = {
  readonly label: string;
  count?: number;
  note: string;
};

// Homomorphic: preserves readonly and optional from source
export type Homomorphic<T> = {
  [K in keyof T]: T[K];
};

export type HomomorphicBase = Homomorphic<BaseRecord>;
// label remains readonly, count remains optional

// + and - optional modifiers
export type MakeOptional<T> = {
  [K in keyof T]+?: T[K];
};

export type MakeRequired<T> = {
  [K in keyof T]-?: T[K];
};

// + and - readonly modifiers
export type MakeReadonly<T> = {
  +readonly [K in keyof T]: T[K];
};

export type MakeMutable<T> = {
  -readonly [K in keyof T]: T[K];
};

export type OptionalBase = MakeOptional<BaseRecord>;
export type RequiredBase = MakeRequired<BaseRecord>;
export type ReadonlyBase = MakeReadonly<BaseRecord>;
export type MutableBase = MakeMutable<BaseRecord>;

// Combined modifier change
export type MutableRequired<T> = {
  -readonly [K in keyof T]-?: T[K];
};

export type MutableRequiredBase = MutableRequired<BaseRecord>;

// Homomorphic preservation demo: mapped over exact source keeps modifiers
export type PreserveDemo = Homomorphic<{
  readonly tag: string;
  value?: number;
}>;

export const homomorphicExample: HomomorphicBase = {
  label: "atlas",
  note: "harbor",
};

export const modifierRequiredExample: RequiredBase = {
  label: "atlas",
  count: 3,
  note: "harbor",
};
