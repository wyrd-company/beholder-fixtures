// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// Private unnameable type leaked through public API.
type HiddenLedgerRef = { readonly __brand: "hidden"; token: number };

function makeHidden(token: number): HiddenLedgerRef {
  return { __brand: "hidden", token };
}

// Public function leaks HiddenLedgerRef via inferred return type.
export function acquireHiddenLedger(token: number) {
  return makeHidden(token);
}

// Exported interface that references leaked private via property.
export interface LedgerHolder {
  ref: ReturnType<typeof acquireHiddenLedger>;
  label: string;
}
