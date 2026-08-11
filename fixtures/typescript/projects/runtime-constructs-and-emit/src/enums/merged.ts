// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export enum Merged {
  Alpha = 0,
  Beta = 1,
}

export enum Merged {
  Gamma = 2,
  Delta = 3,
}

export namespace Merged {
  export function values(): Merged[] {
    return [Merged.Alpha, Merged.Beta, Merged.Gamma, Merged.Delta];
  }

  export function describe(value: Merged): string {
    return `merged:${value}:${Merged[value]}`;
  }
}

export function consumeMerged(value: Merged): string {
  return Merged.describe(value);
}
