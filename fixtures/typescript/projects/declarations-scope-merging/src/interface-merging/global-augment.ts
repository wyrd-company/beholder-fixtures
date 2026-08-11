// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export {};

declare global {
  interface Array<T> {
    describeFixture(): string;
  }
}

Array.prototype.describeFixture = function describeFixture(
  this: unknown[],
): string {
  return `items:${this.length}`;
};

export function describeAugmented(values: string[]): string {
  return values.describeFixture();
}
