// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import type { JSX } from "@fixtures/atlas-jsx-runtime/jsx-runtime";

interface RowProps {
  title: string;
  optionalNote?: string;
  children?: JSX.Element | JSX.Element[];
}

function Row(props: RowProps): JSX.Element | null {
  return null;
}

export const propsAndChildrenView = (
  <Row title="required-title" optionalNote="optional-note">
    <atlas-slot slotName="lead" />
    <atlas-slot slotName="trail" />
  </Row>
);
