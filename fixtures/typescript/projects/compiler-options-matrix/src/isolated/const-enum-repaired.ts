// isolatedModules repaired ambient const enum form: exported const enum.
// An ambient const enum without export would be inlined across files and is not per-file
// transpilable; the repaired form exports the enum so each file can be transpiled alone.

export const enum ArchiveStatus {
  Ready = "ready",
  Done = "done",
  Pending = 0,
}

export function describeStatus(status: ArchiveStatus): string {
  return `${status}`;
}

export const statusMarker: ArchiveStatus = ArchiveStatus.Ready;
