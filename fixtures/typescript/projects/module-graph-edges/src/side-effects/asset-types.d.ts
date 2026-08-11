// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// Wildcard declaration admitting non-code side-effect import (TS-CAN-021)
declare module "*.css" {
  const content: string;
  export default content;
}
