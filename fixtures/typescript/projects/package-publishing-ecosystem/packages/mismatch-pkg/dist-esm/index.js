// Runtime intentionally exports a different name than the declared surface.
// Declared: readMismatch; Runtime: readOther. Type-checks but would fail at load.
export function readOther(value) {
  return `other:${value}`;
}
export const mismatchMarker = "runtime-other";
