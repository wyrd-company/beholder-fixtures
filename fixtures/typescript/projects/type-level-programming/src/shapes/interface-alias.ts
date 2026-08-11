// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// TS-CAN-075: equivalent object shapes as interface and alias; alias for various forms

// Equivalent object shapes as interface and alias
export interface AtlasInterface {
  label: string;
  count: number;
}

export type AtlasAlias = {
  label: string;
  count: number;
};

export const interfaceExample: AtlasInterface = { label: "atlas", count: 3 };
export const aliasExample: AtlasAlias = { label: "atlas", count: 3 };

// Reopening only the interface (second declaration merges)
export interface AtlasInterface {
  tag?: string;
}

export const reopenedExample: AtlasInterface = {
  label: "atlas",
  count: 3,
  tag: "beacon",
};

// Alias for primitive, union, tuple, and conditional forms
export type PrimitiveAlias = string;
export type UnionAlias = string | number;
export type TupleAlias = [string, number];
export type ConditionalAlias<T> = T extends string ? string : number;

export type ConditionalString = ConditionalAlias<string>; // string
export type ConditionalNumber = ConditionalAlias<number>; // number

export const primitiveExample: PrimitiveAlias = "atlas";
export const shapeTupleExample: TupleAlias = ["atlas", 42];

// Interface extension versus alias intersection versus class implementation
export interface BaseShape {
  label: string;
}

export interface ExtendedViaInterface extends BaseShape {
  count: number;
}

export type IntersectedViaAlias = BaseShape & { count: number };

export class HarborClass implements BaseShape {
  constructor(
    public label: string,
    public count: number,
  ) {}
}

export const extendedExample: ExtendedViaInterface = {
  label: "atlas",
  count: 3,
};
export const intersectedExample: IntersectedViaAlias = {
  label: "atlas",
  count: 3,
};
export const classExample = new HarborClass("atlas", 3);

// Generic recursion
export interface Box<T> {
  value: T;
  next: Box<T> | null;
}

export type BoxAlias<T> = {
  value: T;
  next: BoxAlias<T> | null;
};

export const boxExample: Box<string> = { value: "atlas", next: null };
export const boxAliasExample: BoxAlias<number> = { value: 42, next: null };

// Declaration-emit alias preservation: type alias used in exported signature
export type OrchardPayload = { label: string; count: number };

export function createPayload(label: string, count: number): OrchardPayload {
  return { label, count };
}
