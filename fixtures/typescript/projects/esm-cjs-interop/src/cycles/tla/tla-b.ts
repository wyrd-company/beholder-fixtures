// ---
// relationships:
//   implements: esm-cjs-interop
//   references: ground-rules
// ---

const deferred = await import("./tla-a.js");

export function readTokenB(): string {
  return deferred.tlaSeed;
}
