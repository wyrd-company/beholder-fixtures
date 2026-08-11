// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// Root program entry. This module is the stable root for the program identity
// (root program) and re-exports the boundary, library, host, and dependency
// surfaces so they are part of one coherent library.

export * from "../boundary/predicate.js";
export * from "../boundary/filter-usage.js";
export * from "../library/iterator-usage.js";
export * from "../host/identity.js";
export * from "../dependency-consumer.js";

export const programIdentity = "compiler-version-boundary@v1";
