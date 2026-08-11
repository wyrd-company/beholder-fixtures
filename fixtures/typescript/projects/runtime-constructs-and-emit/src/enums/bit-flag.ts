// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export enum Permission {
  None = 0,
  Read = 1 << 0,
  Write = 1 << 1,
  Execute = 1 << 2,
  All = Read | Write | Execute,
}

export function hasPermission(flags: Permission, check: Permission): boolean {
  return (flags & check) === check;
}

export function combinePermissions(...flags: Permission[]): Permission {
  return flags.reduce((acc, cur) => acc | cur, Permission.None);
}

export function permissionToString(flags: Permission): string {
  const parts: string[] = [];
  if (hasPermission(flags, Permission.Read)) parts.push("read");
  if (hasPermission(flags, Permission.Write)) parts.push("write");
  if (hasPermission(flags, Permission.Execute)) parts.push("execute");
  return parts.join("|") || "none";
}
