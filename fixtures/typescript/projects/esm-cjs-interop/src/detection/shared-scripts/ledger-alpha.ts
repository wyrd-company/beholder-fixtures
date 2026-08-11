// ---
// relationships:
//   implements: esm-cjs-interop
//   references: ground-rules
// ---

(globalThis as { sharedLedger?: number }).sharedLedger = 0;

function bumpSharedLedger(amount: number): number {
  const ledgerHost = globalThis as { sharedLedger?: number };
  ledgerHost.sharedLedger = (ledgerHost.sharedLedger ?? 0) + amount;
  return ledgerHost.sharedLedger;
}
