// isolatedModules repaired namespace form: module with exported namespace.
// A bare script namespace would be rejected under isolatedModules (file must be a module);
// adding export makes it per-file transpilable.

export namespace ArchiveNamespace {
  export const token = "archive-token";
  export interface Config {
    id: string;
    kind: string;
  }
  export function describe(config: Config): string {
    return `${config.id}:${config.kind}`;
  }
}

export const namespaceMarker: string = ArchiveNamespace.token;
