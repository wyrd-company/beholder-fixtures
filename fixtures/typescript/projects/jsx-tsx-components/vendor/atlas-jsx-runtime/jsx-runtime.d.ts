// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export namespace JSX {
  export interface Element {
    readonly atlasKind: "element";
    props: unknown;
  }

  export interface IntrinsicElements {
    "atlas-panel": AtlasPanelProps;
    "atlas-slot": AtlasSlotProps;
    "catalog:item": CatalogItemProps;
    "ns:widget": AtlasNsWidgetProps;
  }

  export type ElementType<P = any> =
    | keyof IntrinsicElements
    | ((props: P) => Element | null)
    | (new (props: P) => Element);
}

export interface AtlasPanelProps {
  label: string;
  priority?: number;
}

export interface AtlasSlotProps {
  slotName: string;
}

export interface CatalogItemProps {
  catalog: "ledger" | "atlas";
  code: string;
}

export interface AtlasNsWidgetProps {
  "ns:priority"?: string;
  "catalog:kind"?: string;
}

export function jsx(
  type: JSX.ElementType,
  props: Record<string, unknown> | null,
  key?: string | number,
): JSX.Element;

export function jsxs(
  type: JSX.ElementType,
  props: Record<string, unknown> & { children?: unknown },
  key?: string | number,
): JSX.Element;

export function Fragment(props: { children?: unknown }): JSX.Element;
