// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// Type-only default interface — only a type, no runtime value
export default interface HarborBeacon {
  intensity: number;
  color: "amber" | "azure";
}
