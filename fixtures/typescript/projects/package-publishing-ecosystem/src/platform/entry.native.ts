// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export function getPlatform(): "native" {
  return "native";
}

export interface PlatformMarker {
  platform: "native";
}
