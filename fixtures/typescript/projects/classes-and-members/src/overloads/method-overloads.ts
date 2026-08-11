// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

/** Class with ordered method overloads; implementation is broader than any single signature. */
export class Ledger {
  add(entry: string): string;
  add(entry: string, amount: number): string;
  add(entry: string, amount?: number, ...tags: string[]): string;
  add(entry: string, amount?: number, ...tags: string[]): string {
    if (amount !== undefined) return `${entry}:${amount}:${tags.join(",")}`;
    return `${entry}:${tags.join(",")}`;
  }

  /** Overload with different return type based on input type. */
  render(value: string): string;
  render(value: number): number;
  render(value: string | number): string | number;
  render(value: string | number): string | number {
    return value;
  }
}

export function exerciseMethodOverloads(): void {
  const ledger = new Ledger();
  const a: string = ledger.add("slot");
  const b: string = ledger.add("slot", 10);
  const c: string = ledger.add("slot", 10, "x", "y");

  const s: string = ledger.render("hi");
  const n: number = ledger.render(42);

  void a;
  void b;
  void c;
  void s;
  void n;
}
