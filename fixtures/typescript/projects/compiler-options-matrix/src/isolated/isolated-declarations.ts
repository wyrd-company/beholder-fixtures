// isolatedDeclarations: every exported declaration must have a type that can be emitted
// from a single file without cross-file inference. Explicit annotations repair the surface.

export interface ShelfDescriptor {
  id: string;
  kind: string;
}

export function createDescriptor(id: string, kind: string): ShelfDescriptor {
  return { id, kind };
}

export function describeDescriptor(descriptor: ShelfDescriptor): string {
  return `${descriptor.id}:${descriptor.kind}`;
}

export const defaultDescriptor: ShelfDescriptor = {
  id: "default",
  kind: "standard",
};

// Explicit return type and param types satisfy isolatedDeclarations for a function
// whose inferred type would otherwise require cross-file resolution.
export function formatDescriptors(descriptors: ShelfDescriptor[]): string[] {
  return descriptors.map((descriptor) => describeDescriptor(descriptor));
}
