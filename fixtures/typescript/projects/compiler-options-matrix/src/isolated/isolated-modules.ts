// isolatedModules: per-file transpilable form.
// - Files must be modules (have import/export)
// - Re-exported types use `export type`
// - No ambient const enum cross-file inlining without declaration

export interface ArchiveToken {
  id: string;
  label: string;
}

export type ArchiveLabel = string;

export function makeToken(id: string, label: string): ArchiveToken {
  return { id, label };
}

export const isolatedMarker = "isolated-modules-valid";
