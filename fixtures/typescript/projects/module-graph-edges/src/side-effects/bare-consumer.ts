// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// Resolvable bare import — the specifier resolves to bare-target via relative import
// In a published package this would be a bare specifier; here we model with relative
// path plus package sideEffects metadata demonstrates same graph edge.
import { bareToken } from "./bare-target.js";

export function describeBareImport(): string {
  return `bare:${bareToken}`;
}

// Also model as true bare specifier using tsconfig paths "harbor-seed"
import { readBareToken } from "./bare-target.js";

export function describeBareViaPath(): string {
  return readBareToken();
}
