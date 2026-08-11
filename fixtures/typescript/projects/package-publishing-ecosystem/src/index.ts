// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export * from "./declaration-emit/barrel.js";
export * from "./declaration-emit/dts-consumer.js";
export * from "./package-exports/import-consumer.js";
export * from "./internal-alias/alias-consumer.js";
export * from "./declaration-discovery/consumer-via-exports.js";
export * from "./workspace-links/consumer.js";
export * from "./dual-package/import-consumer.js";
export * from "./platform/conditional-consumer.js";
export * from "./dependency-quality/quality-consumer.js";
