// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// Centerpiece boundary case for TS 5.5 inferred-type-predicate (5.4.5 -> 5.9.3).
// The same valid source emits different inferred declarations:
// - under typescript@5.4.5: (value: unknown) => boolean
// - under typescript@5.9.3: (value: unknown) => value is string
// Zero diagnostics in both contexts; valid under both releases.

export function isString(value: unknown) {
  return typeof value === "string";
}

export const isNumber = (value: unknown) => typeof value === "number";

export function isBoolean(value: unknown) {
  return typeof value === "boolean";
}

export function hasTag(value: unknown) {
  return (
    typeof value === "object" &&
    value !== null &&
    "tag" in value &&
    typeof (value as { tag: unknown }).tag === "string"
  );
}
