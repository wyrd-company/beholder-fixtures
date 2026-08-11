// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

declare namespace JSX {
  interface Element {
    readonly ledgerKind: "element";
    props: unknown;
  }

  interface IntrinsicElements {
    "ledger-panel": LedgerPanelProps;
    "ledger-slot": LedgerSlotProps;
    "ns:widget": NsWidgetProps;
  }

  type ElementType<P = any> =
    | keyof IntrinsicElements
    | ((props: P) => Element | null)
    | (new (props: P) => Element);
}

interface LedgerPanelProps {
  heading: string;
  emphasis?: boolean;
}

interface LedgerSlotProps {
  name: string;
}

interface NsWidgetProps {
  "ns:priority"?: string;
  "catalog:kind"?: string;
}

declare const Ledger: {
  createElement(
    type: JSX.ElementType,
    props: Record<string, unknown> | null,
    ...children: unknown[]
  ): JSX.Element;
  Fragment: { children?: unknown };
};
