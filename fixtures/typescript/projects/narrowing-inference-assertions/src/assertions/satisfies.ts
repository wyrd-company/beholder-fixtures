// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export type AtlasEntry = { label: string; count: number };

export const annotatedRecord: AtlasEntry = { label: "atlas", count: 3 };

export const satisfiesRecord = {
  label: "atlas",
  count: 3,
} satisfies AtlasEntry;

export const asConstSatisfiesRecord = {
  label: "atlas",
  count: 3,
} as const satisfies AtlasEntry;

export function consumeAnnotationVsSatisfies(): [string, string] {
  const annotated: AtlasEntry = { label: "atlas", count: 3 };
  const satisfied = { label: "atlas", count: 3 } satisfies AtlasEntry;
  return [annotated.label, satisfied.label];
}

export function asConstSatisfiesPreservesLiteral(): "atlas" {
  const record = { label: "atlas" } as const satisfies { label: "atlas" };
  return record.label;
}

export type LedgerEntry = { tag: string; revision: number };

export const ledgerSatisfies: LedgerEntry = {
  tag: "ledger",
  revision: 1,
} satisfies LedgerEntry;

export const constLedger = {
  tag: "ledger",
  revision: 1,
} as const satisfies LedgerEntry;
