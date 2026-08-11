// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

declare function readGlobalBindingsForScript(): {
  legacyOnGlobalThis: number;
  modernLexical: number;
  greeting: string;
};

export function readGlobalBindings(): {
  legacyOnGlobalThis: number;
  modernLexical: number;
  greeting: string;
} {
  return readGlobalBindingsForScript();
}
