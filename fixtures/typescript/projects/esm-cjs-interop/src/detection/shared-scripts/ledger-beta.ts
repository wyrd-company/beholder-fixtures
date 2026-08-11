// ---
// relationships:
//   implements: esm-cjs-interop
//   references: ground-rules
// ---

declare var sharedLedger: number;

function readSharedLedger(): number {
  return sharedLedger;
}
