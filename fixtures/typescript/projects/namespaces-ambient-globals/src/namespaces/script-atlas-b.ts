// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

/// <reference path="./script-atlas-a.ts" />

namespace ScriptAtlas {
  export function readToken(): string {
    return atlasToken + "-extended";
  }
}

var scriptAtlasMarker = ScriptAtlas.readToken();
