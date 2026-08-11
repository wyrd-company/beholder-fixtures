// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// Runtime-patch-installation import target (TS-CAN-021)
// Imported solely for its side effect of patching the global harbor registry.

declare global {
  var harborPatchApplied: boolean | undefined;
}

globalThis.harborPatchApplied = true;

export function isPatchApplied(): boolean {
  return globalThis.harborPatchApplied === true;
}
