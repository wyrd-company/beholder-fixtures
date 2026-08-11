// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

/** @jsx Ledger.createElement */
/** @jsxFrag Ledger.Fragment */

function LedgerSidePanel(props: { heading: string }): JSX.Element | null {
  return null;
}

export const pragmaClassicView = (
  <>
    <ledger-panel heading="pragma-factory" />
    <LedgerSidePanel heading="pragma-child" />
  </>
);
