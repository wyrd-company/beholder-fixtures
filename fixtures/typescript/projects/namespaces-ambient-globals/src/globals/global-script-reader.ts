// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

function readHostGlobalsFromScript(): {
  counter: number;
  importedMarker: HostMarkerToken;
} {
  const counter = HostCounter;
  const importedMarker: HostMarkerToken = HostImportedMarker;

  return { counter, importedMarker };
}
