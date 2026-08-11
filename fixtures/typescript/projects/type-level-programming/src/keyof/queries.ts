// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// TS-CAN-072: keyof, indexed access, and type queries

// keyof typeof value
export const catalogValue = {
  label: "atlas",
  count: 3,
  tag: "beacon",
} as const;

export type CatalogKeys = keyof typeof catalogValue; // "label" | "count" | "tag"
export type CatalogValueType = (typeof catalogValue)[CatalogKeys];

// Generic property lookup T[K]
export type PropertyOf<T, K extends keyof T> = T[K];

export function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

export type LabelType = PropertyOf<typeof catalogValue, "label">; // "atlas"

// Array element extraction
export type ElementOf<T extends readonly unknown[]> = T[number];

export type Pair = [string, number, boolean];
export type PairElement = ElementOf<Pair>; // string | number | boolean
export type ArrayElement = ElementOf<string[]>; // string

// Nested indexed access
export type Nested = {
  outer: {
    inner: { value: string };
    count: number;
  };
};

export type InnerValue = Nested["outer"]["inner"]["value"]; // string
export type OuterCount = Nested["outer"]["count"]; // number

// typeof of functions, classes, and namespaces
export function describeBeacon(label: string, count: number): string {
  return `${label}:${count}`;
}

export type DescribeType = typeof describeBeacon; // function type
export type DescribeReturn = ReturnType<DescribeType>; // string

export class Harbor {
  label = "atlas";
  count = 3;
}

export type HarborType = typeof Harbor; // typeof class (constructor)
export type HarborInstance = InstanceType<HarborType>;

export namespace Orchard {
  export const label = "atlas";
  export type Entry = { tag: string };
}

export type OrchardType = typeof Orchard;
export type OrchardEntry = Orchard.Entry;

// typeof import()
export type ImportType = typeof import("./queries.js");
export type ImportKeys = keyof ImportType;

// String-index widening of keyof
export type WithStringIndex = {
  [key: string]: number;
  known: number;
};

export type WidenedKeys = keyof WithStringIndex; // string | number (string index widens)

export type WithoutIndex = {
  label: string;
  count: number;
};

export type PreciseKeys = keyof WithoutIndex; // "label" | "count"

// Number and symbol keys
export const sym = Symbol("beacon");
export type WithNumberAndSymbol = {
  [sym]: string;
  [42]: boolean;
  label: string;
};

export type NumberSymbolKeys = keyof WithNumberAndSymbol; // typeof sym | 42 | "label"

// Optional result including undefined
export type OptionalRecord = {
  label?: string;
  count: number;
};

export type OptionalLabel = OptionalRecord["label"]; // string | undefined

export function readOptional(record: OptionalRecord): string | undefined {
  return record.label;
}

// Unions versus intersections
export type A = { label: string; count: number };
export type B = { label: string; tag: string };

export type UnionKeys = keyof (A | B); // "label" (common keys only)
export type IntersectionKeys = keyof (A & B); // "label" | "count" | "tag"
export type UnionAccess = (A | B)["label"]; // string
export type IntersectionAccess = (A & B)["label"]; // string

export const labelValue: LabelType = "atlas";
export const pairElementExample: PairElement = "atlas";
export const innerExample: InnerValue = "orchard";
export const widenedExample: WidenedKeys = "any-string";
export const optionalExample: OptionalLabel = undefined;
