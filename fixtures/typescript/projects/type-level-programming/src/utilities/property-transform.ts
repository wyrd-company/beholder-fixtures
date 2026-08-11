// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// TS-CAN-080: property-transform utilities applied to unions, overloads, optional properties, any, never

export type UtilCatalog = {
  label: string;
  count?: number;
  tag: string;
  note?: string;
};

// Partial, Required, Readonly, Pick, Omit, Record
export type PartialCatalog = Partial<UtilCatalog>;
export type RequiredCatalog = Required<UtilCatalog>;
export type ReadonlyCatalog = Readonly<UtilCatalog>;
export type PickedCatalog = Pick<UtilCatalog, "label" | "count">;
export type OmittedCatalog = Omit<UtilCatalog, "note">;
export type RecordCatalog = Record<"label" | "count", string>;

// Applied to unions
export type CatalogUnion = UtilCatalog | { label: string; extra: boolean };

export type PartialUnion = Partial<CatalogUnion>;
export type PickedUnion = Pick<CatalogUnion & UtilCatalog, "label">;

// Applied to any and never
export type PartialAny = Partial<any>; // any
export type PartialNever = Partial<never>; // never (Partial<never> distributes to never)
export type RequiredUnknown = Required<unknown>;

// Applied to optional properties: exactOptionalPropertyTypes behavior visible via Required
export type OptionalSet = {
  label?: string;
  count: number;
};

export type RequiredOptional = Required<OptionalSet>; // label becomes required

export const partialExample: PartialCatalog = { label: "atlas" };
export const utilRequiredExample: RequiredCatalog = {
  label: "atlas",
  count: 3,
  tag: "beacon",
  note: "harbor",
};
export const pickedExample: PickedCatalog = { label: "atlas", count: 3 };
export const omittedExample: OmittedCatalog = {
  label: "atlas",
  count: 3,
  tag: "beacon",
};
