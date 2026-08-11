// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

declare type FixtureReferenceToken = {
  token: string;
};

declare function readFixtureReferenceToken(): FixtureReferenceToken;
