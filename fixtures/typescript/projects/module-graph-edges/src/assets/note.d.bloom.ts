// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// Per-file declaration typed through {name}.d.{ext}.ts pattern (TS-CAN-023)
// Types the specific arbitrary-extension asset `note.bloom`.
declare module "./note.bloom" {
  const content: "harbor-bloom-content";
  export default content;
}

export {};
