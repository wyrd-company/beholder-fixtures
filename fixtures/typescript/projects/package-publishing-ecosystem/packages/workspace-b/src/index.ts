// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export function readWorkspaceB(value: string): string {
  return `workspace-b:${value}`;
}

export interface WorkspaceBMarker {
  source: "workspace-b";
}
