// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export enum Augmented {
  Atlas = 0,
  Ledger = 1,
}

export namespace Augmented {
  export const label = "augmented";
  export const extraValue = 42;
  export function fromLabel(input: string): Augmented | undefined {
    if (input === "atlas") return Augmented.Atlas;
    if (input === "ledger") return Augmented.Ledger;
    return undefined;
  }
}

export function consumeAugmented(value: Augmented): string {
  return `${Augmented.label}:${value}:${Augmented[value]}`;
}
