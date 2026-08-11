// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// Re-export surface exercising TS-CAN-018 re-export forms
export { harborName, harborCount } from "./origins.js";
export { default as HarborSkiffDefault } from "./origins.js";
export { default as AnonymousClassDefault } from "./anonymous-defaults.js";
export * from "./origins.js";
export * as HarborOrigins from "./origins.js";

// Alias chain re-export
export { harborLabel as harborLabelRe } from "./alias-chain.js";

// export { default as X } form
import HarborSkiff from "./origins.js";

export { default as HarborAlias } from "./origins.js";
export const reexportedHarborAlias = HarborSkiff;

// Default not forwarded by star is demonstrated in barrel/sources
