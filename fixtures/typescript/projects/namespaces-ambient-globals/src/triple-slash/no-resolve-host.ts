// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

/// <reference path="./no-resolve-lib.d.ts" />
/// <reference types="fixture-reference-types" />

export function readNoResolveFixture(): {
  explicit: string;
  typesRoot: string;
} {
  return {
    explicit: readNoResolveExplicit(),
    typesRoot: readFixtureReferenceToken().token,
  };
}
