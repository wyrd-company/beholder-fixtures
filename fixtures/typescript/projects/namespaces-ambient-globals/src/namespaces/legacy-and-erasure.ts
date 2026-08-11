// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

module LegacyShelf {
  export const legacyToken = "legacy-shelf";
}

export namespace TypeOnlyAtlas {
  export type Marker = "marker";
}

export namespace ValueAtlas {
  export const marker = "value-marker";
}

export function describeNamespaces(): {
  legacy: string;
  typeOnly: TypeOnlyAtlas.Marker;
  value: string;
  ambient: AmbientShelf.ShelfSlot;
} {
  const legacy = LegacyShelf.legacyToken;
  const typeOnly: TypeOnlyAtlas.Marker = "marker";
  const value = ValueAtlas.marker;
  const ambient: AmbientShelf.ShelfSlot = { id: AmbientShelf.shelfTag };

  return { legacy, typeOnly, value, ambient };
}
