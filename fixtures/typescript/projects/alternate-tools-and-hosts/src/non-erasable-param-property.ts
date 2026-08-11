/**
 * Non-erasable syntax: parameter properties synthesize a class field assignment.
 * Node strip-only mode rejects parameter properties; Bun supports them (TS-CAN-091).
 */

export class CatalogEntry {
  constructor(
    public id: string,
    private label: string,
    protected kind: string,
  ) {}

  get display(): string {
    return `${this.id}:${this.label} [${this.kind}]`;
  }

  withLabel(next: string): CatalogEntry {
    return new CatalogEntry(this.id, next, this.kind);
  }
}

export const entry = new CatalogEntry("a-1", "Example", "sample");
