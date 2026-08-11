/// <reference path="./part-first.ts" />
/// <reference path="./part-second.ts" />
/// <reference path="./module-first.ts" />
/// <reference path="./module-second.ts" />
/// <reference path="../../namespaces/script-atlas-a.ts" />
/// <reference path="../../namespaces/script-atlas-b.ts" />
/// <amd-module name="namespaces-ambient-globals-amd" />
/// <amd-dependency path="module-second" />

// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

var concatMarker = concatSuffix;
var scriptAtlasEmitMarker = scriptAtlasMarker;
