// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// This consumer is valid only under customConditions ["workspace"]; it demonstrates the expanded surface.
import { read, workspaceOnly, marker } from "@fixtures/custom-conditions-dep";
import type { CustomDepWorkspace } from "@fixtures/custom-conditions-dep";

export function describeWorkspaceConditions(value: string): string {
  const a = read(value);
  const b = workspaceOnly(value);
  return `${a}|${b}|${marker}`;
}

export type WorkspaceSurface = CustomDepWorkspace;
