// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export function readWorkspaceA(value: string): string {
  return `workspace-a:${value}`;
}

export interface WorkspaceAMarker {
  source: "workspace-a";
}
