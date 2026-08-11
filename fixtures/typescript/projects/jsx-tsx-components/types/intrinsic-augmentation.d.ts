// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

declare namespace JSX {
  interface IntrinsicElements {
    "custom-ledger-tag": CustomLedgerTagProps;
  }
}

interface CustomLedgerTagProps {
  marker: string;
}
