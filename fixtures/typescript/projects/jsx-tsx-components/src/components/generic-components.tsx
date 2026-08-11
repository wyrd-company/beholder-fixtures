// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import type { JSX } from "@fixtures/atlas-jsx-runtime/jsx-runtime";

interface GridProps<T> {
  items: T[];
  render: (item: T) => JSX.Element;
}

function Grid<T>(props: GridProps<T>): JSX.Element | null {
  return null;
}

export const inferredGenericGrid = (
  <Grid
    items={["alpha", "beta"]}
    render={(item) => <atlas-slot slotName={item} />}
  />
);

export const explicitGenericGrid = (
  <Grid<string>
    items={["gamma"]}
    render={(item) => <atlas-slot slotName={item} />}
  />
);
