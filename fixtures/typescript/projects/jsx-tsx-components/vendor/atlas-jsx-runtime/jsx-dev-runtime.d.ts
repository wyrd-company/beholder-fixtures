// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export * from "./jsx-runtime.js";

export function jsxDEV(
  type: JSX.ElementType,
  props: Record<string, unknown> | null,
  key?: string | number,
  isStaticChildren?: boolean,
  source?: object,
  self?: unknown,
): JSX.Element;
