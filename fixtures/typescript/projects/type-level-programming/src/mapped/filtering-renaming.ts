// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// TS-CAN-071: key filtering via never, renaming via as, template-generated names, union sources

export type FilterCatalog = {
  label: string;
  count: number;
  revision: string;
  internalNote: string;
};

// Key filtering via never
export type PublicKeys<T> = {
  [K in keyof T as K extends `internal${string}` ? never : K]: T[K];
};

export type PublicCatalog = PublicKeys<FilterCatalog>;
// internalNote filtered out

// Renaming via as (non-template)
export type Renamed<T> = {
  [K in keyof T as K extends "label" ? "title" : K]: T[K];
};

export type RenamedCatalog = Renamed<FilterCatalog>;

// Template-generated names
export type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};

export type CatalogGetters = Getters<FilterCatalog>;
// getLabel, getCount, getRevision, getInternalNote

export type Setters<T> = {
  [K in keyof T as `set${Capitalize<string & K>}`]: (value: T[K]) => void;
};

export type CatalogSetters = Setters<FilterCatalog>;

// Union sources: mapped over union distributes keys
export type UnionSource = { label: string; count: number } | { tag: string };

export type MappedUnion<T> = {
  [K in keyof T]: T[K];
};

export type UnionMapped = MappedUnion<UnionSource>;

// Symbol and number keys
export const symbolKey = Symbol("atlas");
export type SymbolRecord = {
  [symbolKey]: string;
  [42]: number;
  label: string;
};

export type MappedSymbolRecord = {
  [K in keyof SymbolRecord]: SymbolRecord[K];
};

// Index signature preservation
export type FilterWithIndex = {
  [key: string]: number;
  known: number;
};

export type MappedWithIndex = {
  [K in keyof FilterWithIndex]: FilterWithIndex[K];
};

export const publicExample: PublicCatalog = {
  label: "atlas",
  count: 3,
  revision: "a1",
};

export const getterExample: CatalogGetters = {
  getLabel: () => "atlas",
  getCount: () => 3,
  getRevision: () => "a1",
  getInternalNote: () => "harbor",
};
