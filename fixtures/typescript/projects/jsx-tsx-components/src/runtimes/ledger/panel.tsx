// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export const ledgerRuntimeView = (
  <>
    <ledger-panel heading="ledger-runtime" emphasis={true} />
    <custom-ledger-tag marker="intrinsic-augmentation" />
    <ns:widget ns:priority="ledger" catalog:kind="ledger" />
  </>
);
