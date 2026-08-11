// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// Anonymous default class declaration (TS-CAN-018 distinct form 1)
export default class {
  readonly tag = "anonymous-skiff";
  anchor(): string {
    return this.tag;
  }
}

// The companion anonymous default function is in anonymous-default-function.ts
// to keep each default export distinct per module.
