// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

import type { JSX } from "@fixtures/atlas-jsx-runtime/jsx-runtime";

type AtlasPanelComponent = JSX.ElementType<{
  label: string;
  priority?: number;
}>;

function resolveElementType(
  component: AtlasPanelComponent,
): AtlasPanelComponent {
  return component;
}

export const intrinsicElementType: AtlasPanelComponent = "atlas-panel";

export const functionElementType: AtlasPanelComponent = (
  props,
): JSX.Element | null => (
  <atlas-panel label={props.label} priority={props.priority} />
);

export const resolvedElementType = resolveElementType("atlas-panel");
