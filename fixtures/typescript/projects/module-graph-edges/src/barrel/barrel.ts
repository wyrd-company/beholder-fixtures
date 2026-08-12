// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// Barrel exercising direct, renamed, namespace, type-only, and star re-exports
// (TS-CAN-020)

export { coveValue } from "./sources/alpha.js";
export { bayValue as renamedBay } from "./sources/beta.js";
export * as AlphaNs from "./sources/alpha.js";
export type { CoveType } from "./sources/alpha.js";
export type { BayType as RenamedBayType } from "./sources/beta.js";
export * from "./sources/alpha.js";
export * from "./sources/beta.js";

// Two star sources exposing same name — explicit local export resolves ambiguity
// Both alpha and beta export `sharedName`; barrel provides explicit resolution.
// This explicit `sharedName` also demonstrates local-export precedence over the same
// name provided by `export *` from alpha/beta — the local binding wins.
export const sharedName = "resolved-harbor";

// Identical origin reached twice through two star re-exports
export * from "./sources/common-a.js";
export * from "./sources/common-b.js";

// Default not forwarded by star (demonstrated: origins default is not forwarded)
// This barrel has no default export even though alpha/common-origin have named exports;
// importing default from barrel must be explicit.

// CommonJS re-export source — re-export without local binding
// `cjs-commonjs/cjs-source.js` is an actual CommonJS boundary via nearest package.json type:commonjs
export { cjsHarbor, cjsBeacon } from "./sources/cjs-commonjs/cjs-source.js";

// Re-export without local binding (no intermediate import)
export { HarborSkiff } from "../bindings/origins.js";

// Type-only re-export forwarded through barrel
export type { HarborChart } from "../type-only/models.js";
