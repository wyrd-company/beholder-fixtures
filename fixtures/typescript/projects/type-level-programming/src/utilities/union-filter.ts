// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// TS-CAN-080: union-filter and string utilities

export type MixedUnion = string | number | boolean | null;

// Extract, Exclude
export type ExtractString = Extract<MixedUnion, string>; // string
export type ExcludeString = Exclude<MixedUnion, string>; // number | boolean | null
export type NonNullableUnion = NonNullable<MixedUnion>; // string | number | boolean
export type ExtractNever = Extract<MixedUnion, never>; // never
export type ExcludeNever = Exclude<MixedUnion, never>; // MixedUnion
export type ExtractAny = Extract<any, string>; // any
export type ExcludeAny = Exclude<any, string>; // any

// String utilities applied to unions
export type UpperUnion = Uppercase<"atlas" | "ledger">; // "ATLAS" | "LEDGER"
export type LowerUnion = Lowercase<"ATLAS" | "LEDGER">;
export type CapitalizeUnion = Capitalize<"atlas" | "ledger">;
export type UncapitalizeUnion = Uncapitalize<"Atlas" | "Ledger">;

// Awaited applied to unions
export type AwaitedUnion = Awaited<Promise<string> | Promise<number>>; // string | number
export type AwaitedNested = Awaited<Promise<Promise<string>>>; // string

export const extractExample: ExtractString = "atlas";
export const excludeExample: ExcludeString = 42;
export const unionUpperExample: UpperUnion = "ATLAS";
export const unionAwaitedExample: AwaitedUnion = "atlas";
