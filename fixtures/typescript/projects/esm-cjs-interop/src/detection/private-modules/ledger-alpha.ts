// ---
// relationships:
//   implements: esm-cjs-interop
//   references: ground-rules
// ---

export {};

var privateLedger = 0;

function bumpPrivateLedger(amount: number): number {
  privateLedger += amount;
  return privateLedger;
}
