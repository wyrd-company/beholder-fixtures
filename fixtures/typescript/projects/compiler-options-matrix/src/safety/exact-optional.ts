// exactOptionalPropertyTypes: distinguishes absent versus present-undefined.
// With flag true, `tag?: string` cannot be assigned `undefined` explicitly unless `| undefined` is added.

export interface CrateDescriptor {
  id: string;
  tag?: string;
}

export interface CrateDescriptorExact {
  id: string;
  tag?: string | undefined;
}

export function createDescriptor(id: string): CrateDescriptor {
  return { id };
}

export function createDescriptorWithTag(
  id: string,
  tag: string,
): CrateDescriptorExact {
  return { id, tag };
}

export function readTag(descriptor: CrateDescriptor): string | undefined {
  return descriptor.tag;
}

export function hasTag(descriptor: CrateDescriptor): boolean {
  return descriptor.tag !== undefined;
}
