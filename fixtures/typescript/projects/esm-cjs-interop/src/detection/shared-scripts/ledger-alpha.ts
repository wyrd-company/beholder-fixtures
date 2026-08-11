// ---
// relationships:
//   implements: esm-cjs-interop
//   references: ground-rules
// ---

var sharedLedger = 0;

function bumpSharedLedger(amount: number): number {
  sharedLedger += amount;
  return sharedLedger;
}
