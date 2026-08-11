// isolatedModules repaired form: type re-export uses explicit type marker.
// This file is valid under isolatedModules because re-exported types are marked.

export type { ArchiveToken } from "./isolated-modules.js";
export { makeToken } from "./isolated-modules.js";

export type ReExportedLabel = string;

export function describeReExported(id: string): string {
  return `re-export:${id}`;
}
