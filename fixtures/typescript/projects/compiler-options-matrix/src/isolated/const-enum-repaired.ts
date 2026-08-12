// isolatedModules repaired const-enum form: a non-ambient const enum.
// An ambient `declare const enum` cannot be accessed under isolatedModules (TS2748): a per-file
// transpiler erases the ambient declaration and has no member values to inline. Removing
// `declare` makes the enum non-ambient, and isolatedModules emits it as a preserved runtime
// enum object per file rather than inlining member accesses.

export const enum ArchiveStatus {
  Ready = "ready",
  Done = "done",
  Pending = 0,
}

export function describeStatus(status: ArchiveStatus): string {
  return `${status}`;
}

export const statusMarker: ArchiveStatus = ArchiveStatus.Ready;
