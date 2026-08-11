// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// Wildcard declaration for custom extension (TS-CAN-023)
declare module "*.bloom" {
  const content: string;
  export default content;
}
