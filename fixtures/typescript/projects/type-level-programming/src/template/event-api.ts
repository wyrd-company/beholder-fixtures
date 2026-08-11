// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// TS-CAN-073: event-name and key API generated from object keys, cross-product, intrinsic transforms

export type TemplateCatalog = {
  label: string;
  count: number;
  tag: string;
};

// Event-name and key API generated from object keys
export type CatalogEvent = `catalog:${keyof TemplateCatalog & string}:changed`;

export type CatalogHandlers = {
  [K in CatalogEvent]: (payload: { key: string; value: unknown }) => void;
};

// Cross-product of multiple union substitutions
export type Color = "red" | "green" | "blue";
export type Size = "small" | "large";
export type Variant = `${Color}-${Size}`; // 6 combinations

// Numeric, bigint, boolean interpolation
export type NumericKey = `item-${number}`;
export type BigIntKey = `big-${bigint}`;
export type BooleanFlag = `flag-${boolean}`;

export type MixedInterpolation = `count-${number}-active-${boolean}`;

// Uppercase, Lowercase, Capitalize, Uncapitalize
export type UpperAtlas = Uppercase<"atlas">; // "ATLAS"
export type LowerAtlas = Lowercase<"ATLAS">; // "atlas"
export type Capitalized = Capitalize<"atlas">; // "Atlas"
export type Uncapitalized = Uncapitalize<"Atlas">; // "atlas"

// Wide string interaction
export type WideString = string;
export type PrefixedWide = `prefix-${WideString}`; // `prefix-${string}` remains string

// Key-remapping interaction with template literal
export type PrefixedCatalog = {
  [K in keyof TemplateCatalog as `catalog_${string & K}`]: TemplateCatalog[K];
};

export type PrefixedCatalogExample = PrefixedCatalog;
// { catalog_label: string; catalog_count: number; catalog_tag: string }

export const catalogEventExample: CatalogEvent = "catalog:label:changed";
export const variantExample: Variant = "red-small";
export const numericKeyExample: NumericKey = "item-42";
export const booleanFlagExample: BooleanFlag = "flag-true";
export const templateUpperExample: UpperAtlas = "ATLAS";
