// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// TS-CAN-080: small value/schema API whose exported type exists only through generic instantiation,
// recursive thenable, isolatedDeclarations repair with annotation

// Value-derived schema API: exported type exists only through generic instantiation
export function defineCatalog<const T extends Record<string, unknown>>(
  shape: T,
): { shape: T; describe: () => string } {
  return { shape, describe: () => "atlas" };
}

export const catalogDefinition = defineCatalog({
  label: "atlas",
  count: 3,
  tag: "beacon",
});

export type CatalogFromDefinition = typeof catalogDefinition.shape;
// { label: string; count: number; tag: string } inferred only through generic

export type InferredCatalog = CatalogFromDefinition;

// Generic schema factory with mapped inference
export function createRecord<T extends Record<string, string>>(fields: T): T {
  return fields;
}

export const recordInstance = createRecord({ label: "atlas", tag: "harbor" });
export type RecordInstanceType = typeof recordInstance; // inferred via generic instantiation

// Recursive thenable and Awaited
export type RecursiveThenable<T> = {
  then: (resolve: (value: T) => void) => void;
};

export type ThenableString = RecursiveThenable<string>;
export type AwaitedThenable = Awaited<ThenableString>; // string via Awaited unwrapping thenable

export type NestedThenable = RecursiveThenable<RecursiveThenable<string>>;
export type AwaitedNestedThenable = Awaited<NestedThenable>; // string

export function adoptThenable<T>(value: RecursiveThenable<T>): Promise<T> {
  return new Promise<T>((resolve) => value.then(resolve));
}

// isolatedDeclarations repair: explicit annotation satisfies isolatedDeclarations
// Without annotation, `export const inferred = { label: "atlas" }` would need annotation under isolatedDeclarations.
// Repair adds explicit type.
export type LabeledRecord = { label: string; count: number };

export const labeledRecord: LabeledRecord = { label: "atlas", count: 3 };

export function buildLabeled(label: string, count: number): LabeledRecord {
  return { label, count };
}

export const isolatedExample: LabeledRecord = buildLabeled("atlas", 3);
export const schemaAwaitedExample: AwaitedThenable = "atlas";
export const nestedAwaitedExample: AwaitedNestedThenable = "atlas";
