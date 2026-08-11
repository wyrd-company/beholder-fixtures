// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// Bridge that resolves "@fixtures/sensitive-lib" from within workspace-a, hitting nested v2.
export { SensitiveToken, tokenV2 } from "@fixtures/sensitive-lib";
export type { SensitiveToken as SensitiveTokenV2 } from "@fixtures/sensitive-lib";
