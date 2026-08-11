// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

/** Merged class constructor, namespace type facet, and namespace value facet. */
export class Registry {
  readonly token = "registry";
}

export namespace Registry {
  export interface Entry {
    id: string;
    label: string;
  }

  export type Reader = (id: string) => Entry | undefined;

  export const version = 1;
}

/** Class as both a type and a runtime constructor. */
export class CatalogItem {
  constructor(public readonly sku: string) {}
}

/** Enum as both a type and a runtime object. */
export enum Availability {
  InStock = "in_stock",
  Backorder = "backorder",
}

/** Interface contributes type space only. */
export interface ItemDescriptor {
  sku: string;
  title: string;
}

/** Qualified namespace access, typeof, annotation, and constructor call on one spelling. */
export function describeRegistry(): Registry.Entry {
  const reader: Registry.Reader = (id) =>
    id === "a1" ? { id, label: "sample" } : undefined;

  const factory: typeof Registry = Registry;
  const created = new factory();
  const version = Registry.version;
  const entry = reader("a1") ?? { id: "fallback", label: created.token };

  return entry;
}

export function describeCatalog(): {
  item: CatalogItem;
  availability: Availability;
  descriptor: ItemDescriptor;
} {
  const item: CatalogItem = new CatalogItem("sku-100");
  const availability: Availability = Availability.InStock;
  const descriptor: ItemDescriptor = { sku: item.sku, title: "Sample item" };

  return { item, availability, descriptor };
}
