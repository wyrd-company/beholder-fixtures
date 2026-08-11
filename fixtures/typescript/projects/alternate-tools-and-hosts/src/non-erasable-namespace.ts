/**
 * Non-erasable syntax: namespace emits a runtime object.
 * Node strip-only mode rejects namespace; Bun transpiles it (TS-CAN-091).
 */

export namespace Catalog {
  export const version = "1.0.0";

  export type Entry = {
    id: string;
    label: string;
  };

  export function describe(entry: Entry): string {
    return `${entry.id}:${entry.label} v${version}`;
  }

  export const defaultEntry: Entry = { id: "root", label: "Catalog" };
}
