// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export class CatalogItem {
  constructor(
    public readonly sku: string,
    public readonly title: string,
  ) {}
}

export class LedgerEntry {
  constructor(
    public readonly id: string,
    public readonly amount: number,
  ) {}
}
