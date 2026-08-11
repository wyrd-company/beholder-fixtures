// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export function getPlatform(): "browser" {
  return "browser";
}

export interface PlatformMarker {
  platform: "browser";
}
