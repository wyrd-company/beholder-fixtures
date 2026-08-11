// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export function getPlatform(): "server" {
  return "server";
}

export interface PlatformMarker {
  platform: "server";
}
