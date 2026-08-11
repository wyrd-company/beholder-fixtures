// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

declare namespace JSX {
  interface Element {
    _jsxBrand: string;
  }
  interface IntrinsicElements {
    [elemName: string]: Record<string, unknown>;
  }
  interface ElementChildrenAttribute {
    children: unknown;
  }
}
