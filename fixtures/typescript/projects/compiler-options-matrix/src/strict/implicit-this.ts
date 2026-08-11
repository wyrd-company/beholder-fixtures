// noImplicitThis: implicit any this is gated.
// Methods with explicit this parameters remain valid in both modes.

export interface Archive {
  title: string;
  getTitle(this: Archive): string;
}

export function createArchive(title: string): Archive {
  return {
    title,
    getTitle(this: Archive) {
      return this.title;
    },
  };
}

export function callWithExplicitThis(
  archive: Archive,
  fn: (this: Archive) => string,
): string {
  return fn.call(archive);
}
