// TS-CAN-064 — Index signatures and indexed access configuration

// String index signature with compatible named member and explicit override.
export interface StringCatalog {
  [key: string]: number;
  total: number;
  labeledCount: number;
  // Explicit member override keeps index type compatible.
  reserved: number;
}

// Number index constrained by string index: number value must be subtype of string index value.
export interface NumberConstrainedCatalog {
  [key: string]: string | number;
  [index: number]: string;
  // Compatible named member fits both indexes.
  tag: string;
}

// Symbol index signature.
export interface SymbolRegistry {
  [key: symbol]: boolean;
  [key: string]: boolean | number;
}

// Template-pattern index signature.
export interface TemplatePatternStore {
  [key: `prop_${string}`]: string;
  // Compatible named member.
  prop_default: string;
}

// Union index signature.
export interface UnionKeyStore {
  [key: string | number]: number;
}

// Readonly index signatures.
export interface ReadonlyStringIndex {
  readonly [key: string]: number;
}

export interface ReadonlyNumericIndex {
  readonly [index: number]: string;
  readonly [key: string]: string | number;
}

// Array and tuple indexing demonstration.
export const sampleArray: string[] = ["a", "b", "c"];
export const sampleTuple: [string, number, boolean] = ["x", 42, true];

// Keyof widening with string index.
export type StringCatalogKeys = keyof StringCatalog;
export type NumberConstrainedCatalogKeys = keyof NumberConstrainedCatalog;
export type SymbolRegistryKeys = keyof SymbolRegistry;

// Demonstrates reads under checked and unchecked access settings.
// Under default, indexed access yields the declared value type.
// Under noUncheckedIndexedAccess, the same access yields value | undefined.
export function readStringCatalog(
  catalog: StringCatalog,
  key: string,
): number | undefined {
  const declared: number | undefined = catalog[key];
  const explicit: number = catalog.total;
  return declared ?? explicit;
}

export function readNumberConstrained(
  store: NumberConstrainedCatalog,
  strKey: string,
  numKey: number,
): string | number | undefined {
  const fromString: string | number | undefined = store[strKey];
  const fromNumber: string | undefined = store[numKey];
  return fromString ?? fromNumber;
}

export function readSymbolRegistry(
  registry: SymbolRegistry,
  sym: symbol,
): boolean | undefined {
  const value: boolean | undefined = registry[sym];
  return value;
}

export function readTemplatePattern(
  store: TemplatePatternStore,
  key: `prop_${string}`,
): string | undefined {
  const value: string | undefined = store[key];
  return value;
}

export function readUnionKeyStore(
  store: UnionKeyStore,
  key: string | number,
): number | undefined {
  const value: number | undefined = store[key];
  return value;
}

export function readReadonlyIndex(
  store: ReadonlyStringIndex,
  key: string,
): number | undefined {
  const value: number | undefined = store[key];
  return value;
}

// Array and tuple indexing with safe handling for noUncheckedIndexedAccess.
export function readArrayElement(
  arr: string[],
  index: number,
): string | undefined {
  const value: string | undefined = arr[index];
  return value;
}

export function readTupleElements(
  tuple: [string, number, boolean],
): [string | undefined, number | undefined, boolean | undefined] {
  const first: string | undefined = tuple[0];
  const second: number | undefined = tuple[1];
  const third: boolean | undefined = tuple[2];
  return [first, second, third];
}

// Undeclared key gaining undefined under noUncheckedIndexedAccess.
// The catalog declares only string index -> number, so an arbitrary key is
// undefined when strict indexing is on and plain number otherwise; typing as
// number | undefined remains valid in both contexts.
export function readUndeclaredKey(
  catalog: StringCatalog,
  key: string,
): number | undefined {
  const value: number | undefined = catalog[key];
  if (value === undefined) return undefined;
  return value;
}

// Explicit member override demonstration: the explicit property already shown
// in StringCatalog, plus a separate type that overrides index with compatible type.
export interface ExplicitOverride {
  [key: string]: string | number;
  count: number;
  label: string;
}

export function readExplicitOverride(
  store: ExplicitOverride,
  key: string,
): string | number | undefined {
  const dynamic: string | number | undefined = store[key];
  const count: number = store.count;
  const label: string = store.label;
  return dynamic ?? count ?? label;
}

// Number and string index compatibility check via assignment.
export function checkIndexCompatibility(): void {
  const constrained: NumberConstrainedCatalog = {
    tag: "example",
    0: "zero",
    hello: "world",
  };
  void constrained;
}

// Number/string index compatibility for TS-CAN-076 also appears here but remains valid.
