// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// TS-CAN-073: substring parsing with conditional inference and recursive parser

// Substring parsing with conditional inference
export type SplitOnUnderscore<S extends string> =
  S extends `${infer Head}_${infer Tail}` ? [Head, Tail] : [S];

export type SplitAtlasLedger = SplitOnUnderscore<"atlas_ledger">; // ["atlas", "ledger"]
export type SplitNoUnderscore = SplitOnUnderscore<"atlas">; // ["atlas"]

// Recursive parser: split dot-path into tuple
export type SplitPath<S extends string> =
  S extends `${infer Head}.${infer Tail}` ? [Head, ...SplitPath<Tail>] : [S];

export type PathAtlas = SplitPath<"atlas.ledger.beacon">; // ["atlas", "ledger", "beacon"]
export type PathSingle = SplitPath<"atlas">; // ["atlas"]

// Parsing key-value pairs
export type ParsePair<S extends string> =
  S extends `${infer Key}=${infer Value}` ? { key: Key; value: Value } : never;

export type ParsedPair = ParsePair<"label=atlas">; // { key: "label"; value: "atlas" }

// Recursive key remapping interaction via parser
export type DotToUnderscore<S extends string> =
  S extends `${infer Head}.${infer Tail}`
    ? `${Head}_${DotToUnderscore<Tail>}`
    : S;

export type UnderscorePath = DotToUnderscore<"atlas.ledger.beacon">; // "atlas_ledger_beacon"

// Capitalize interaction with template parsing
export type CapitalizeWords<S extends string> =
  S extends `${infer First}_${infer Rest}`
    ? `${Capitalize<First>}_${CapitalizeWords<Rest>}`
    : Capitalize<S>;

export type CapitalizedWords = CapitalizeWords<"atlas_ledger_beacon">; // "Atlas_Ledger_Beacon"

export const splitExample: SplitAtlasLedger = ["atlas", "ledger"];
export const pathExample: PathAtlas = ["atlas", "ledger", "beacon"];
export const parsedExample: ParsedPair = { key: "label", value: "atlas" };
export const underscoreExample: UnderscorePath = "atlas_ledger_beacon";
