// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export const harborName = "north-harbor";
export const harborCount = 12;
export function launchVessel(name: string): string {
  return `launch:${name}`;
}

export class HarborSkiff {
  constructor(public readonly id: string) {}
  moor(): string {
    return `moor:${this.id}`;
  }
}

export type HarborKind = "fishing" | "cargo" | "research";
export interface HarborConfig {
  name: string;
  kind: HarborKind;
}

export const defaultHarborConfig: HarborConfig = {
  name: harborName,
  kind: "research",
};

export default HarborSkiff;

export const sharedAliasValue = 42;
export type SharedAliasType = HarborConfig;
