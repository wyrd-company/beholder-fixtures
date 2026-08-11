// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export type Parcel =
  | { kind: "book"; title: string; pages: number }
  | { kind: "crate"; weight: number }
  | { kind: "envelope"; priority: number };

export function narrowViaDestructuredDiscriminant(parcel: Parcel): string {
  const { kind } = parcel;
  if (kind === "book") {
    return `book:${parcel.title}:${parcel.pages}`;
  }
  if (kind === "crate") {
    return `crate:${parcel.weight}`;
  }
  return `envelope:${parcel.priority}`;
}

export function destructuredWithAliasedKind(parcel: Parcel): number {
  const { kind: parcelKind } = parcel;
  switch (parcelKind) {
    case "book":
      return parcel.pages;
    case "crate":
      return parcel.weight;
    case "envelope":
      return parcel.priority;
  }
}
