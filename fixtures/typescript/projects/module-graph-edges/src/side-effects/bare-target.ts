// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// Bare import target (resolvable via paths or direct specifier)
export const bareToken = "harbor-seed";
export function readBareToken(): string {
  return bareToken;
}
