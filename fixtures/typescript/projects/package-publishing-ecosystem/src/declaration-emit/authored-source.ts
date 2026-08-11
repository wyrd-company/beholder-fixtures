// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

/**
 * Authored source for declaration emit coverage.
 * Inferred public types, leaked private type, and internal stripping.
 */

export interface BeaconCatalogItem {
  id: string;
  label: string;
}

/** @internal */
export interface InternalLedgerNote {
  secret: string;
  catalog: BeaconCatalogItem;
}

type PrivateToken = { brand: "private"; value: number };

function createPrivateToken(value: number): PrivateToken {
  return { brand: "private", value };
}

// Inferred public type: return type is inferred from PrivateToken leakage.
export function createBeaconEntry(id: string) {
  const token = createPrivateToken(id.length);
  return {
    item: { id, label: `beacon-${id}` } as BeaconCatalogItem,
    token,
  };
}

// @internal helper should be stripped when stripInternal is true.
export function describeInternal(note: InternalLedgerNote): string {
  return `${note.catalog.label}:${note.secret}`;
}

export function describeCatalog(item: BeaconCatalogItem): string {
  return `${item.id}:${item.label}`;
}
