// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

declare module "@fixture/lib-stub" {
  export type StubToken = {
    label: string;
  };

  export function readStubToken(): StubToken;
}
