export interface Crate {
  id: string;
  label: string;
  weight: number;
}

export interface Shelf {
  id: string;
  crates: Crate[];
}

export function createCrate(id: string, label: string, weight: number): Crate {
  return { id, label, weight };
}

export function describeShelf(shelf: Shelf): string {
  return `${shelf.id}:${shelf.crates.length}`;
}

export const catalogVersion = "1.0.0";
