// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export function evolvingArray(): number[] {
  const values = [];
  values.push(1);
  values.push(2);
  values.push(3);
  return values;
}

export function evolvingArrayMixed(): Array<string | number> {
  const items: string[] = [];
  items.push("atlas");
  return items;
}

export function evolvingArrayWithPushAndNarrow(): string {
  const ledger: Array<string | null> = [];
  ledger.push("atlas");
  ledger.push(null);
  const filtered = ledger.filter((value): value is string => value !== null);
  return filtered.join(",");
}

export function constContextArray(): readonly [string, number] {
  const pair = ["atlas", 42] as const;
  return pair;
}

export function constContextObject(): {
  readonly label: "atlas";
  readonly count: 3;
} {
  const record = { label: "atlas", count: 3 } as const;
  return record;
}

export function constContextInCallback(): string {
  const apply = (handler: (value: "atlas") => string): string =>
    handler("atlas");
  return apply((value) => value.toUpperCase());
}
