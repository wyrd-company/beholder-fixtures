// Additional isolatedModules-valid surface: module with type-only import.
// Importing a type uses `import type` so the import can be erased per-file.

import type { ArchiveToken } from "./isolated-modules.js";

export function describeArchiveToken(token: ArchiveToken): string {
  return `${token.id}:${token.label}`;
}

export type TokenView = Pick<ArchiveToken, "id">;

export function takeTokenId(token: ArchiveToken): string {
  return token.id;
}
