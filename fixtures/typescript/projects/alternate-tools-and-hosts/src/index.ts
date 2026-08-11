/**
 * Barrel for alternate-tools-and-hosts fixture library.
 * Re-exports the erasable vs non-erasable contrast and the
 * enum transform-differing construct.
 */

export * from "./erasable.ts";
export * from "./enum-differ.ts";
export * from "./non-erasable-enum.ts";
export * from "./non-erasable-namespace.ts";
export * from "./non-erasable-param-property.ts";
export { fileExists } from "./non-erasable-import-equals.ts";
export { withExtensionTs, extensionless } from "./with-extension.ts";
export { greet, greetingKind } from "./transform-source.ts";
export type { GreetFn } from "./transform-source.ts";
