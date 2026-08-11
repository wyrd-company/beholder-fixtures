// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export function readImportMeta(): string {
  return import.meta.harbor;
}

export function readFixtureTag(): string {
  return import.meta.fixtureTag;
}
