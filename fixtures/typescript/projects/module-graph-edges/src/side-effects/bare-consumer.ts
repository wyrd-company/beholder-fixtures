// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// Resolvable bare import — bare specifier "harbor-seed" resolves via tsconfig paths
// to ./src/side-effects/bare-target.ts (offline, no network). Also modeled via
// relative path for contrast; both demonstrate the same graph edge.
import { bareToken } from "harbor-seed";

export function describeBareImport(): string {
  return `bare:${bareToken}`;
}

// Relative contrast for the same target
import { readBareToken } from "./bare-target.js";

export function describeBareViaPath(): string {
  return readBareToken();
}
