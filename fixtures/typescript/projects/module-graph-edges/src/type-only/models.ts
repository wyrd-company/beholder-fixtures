// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export class HarborBuoy {
  constructor(public readonly beacon: number) {}
  ping(): string {
    return `ping:${this.beacon}`;
  }
}

export enum TideLevel {
  Low = "low",
  High = "high",
}

export interface HarborChart {
  depth: number;
  label: string;
}

export type HarborSignal = HarborChart & { active: boolean };
