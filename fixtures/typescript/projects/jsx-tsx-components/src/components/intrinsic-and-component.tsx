// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import type { JSX } from "@fixtures/atlas-jsx-runtime/jsx-runtime";

function CatalogPanel(props: { title: string }): JSX.Element | null {
  return null;
}

export const mixedIntrinsicAndComponent = (
  <>
    <atlas-panel label="intrinsic-lowercase" />
    <CatalogPanel title="component-uppercase" />
  </>
);
