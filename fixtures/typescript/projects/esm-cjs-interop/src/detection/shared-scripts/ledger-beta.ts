// ---
// relationships:
//   implements: esm-cjs-interop
//   references: ground-rules
// ---

function readSharedLedger(): number {
  return (globalThis as { sharedLedger?: number }).sharedLedger ?? 0;
}
