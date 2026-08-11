// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export type AtlasRecord = { label: string; count: number };
export type AtlasRecordOptional = { label: string; count?: number };

export function consumeAtlasRecord(record: AtlasRecord): string {
  return `atlas:${record.label}:${record.count}`;
}

export function sameObjectWithContext(): string {
  return consumeAtlasRecord({ label: "atlas", count: 3 });
}

export function sameObjectWithoutContext(): AtlasRecord {
  const record = { label: "atlas", count: 3 };
  return record;
}

export function consumeNumbers(values: number[]): number {
  return values.reduce((sum, value) => sum + value, 0);
}

export function sameArrayWithContext(): number {
  return consumeNumbers([1, 2, 3]);
}

export function sameArrayWithoutContext(): number[] {
  const values = [1, 2, 3];
  return values;
}

export function heterogeneousBestCommonType(): Array<string | number> {
  const mixed: Array<string | number> = ["atlas", 2, "ledger", 4];
  return mixed;
}

export function heterogeneousWithoutContext(): Array<string | number> {
  const items = ["atlas", 2, "ledger", 4];
  return items;
}
