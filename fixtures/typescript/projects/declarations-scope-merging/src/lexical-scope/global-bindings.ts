// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export {};

declare global {
  var legacyCounter: number;
  var legacyGreeting: (name: string) => string;
  let modernCounter: number;
}

globalThis.legacyCounter = 0;
modernCounter = 0;

globalThis.legacyGreeting = function legacyGreeting(name: string): string {
  return `hello-${name}`;
};

export function readGlobalBindings(): {
  legacyOnGlobalThis: number;
  modernLexical: number;
  greeting: string;
} {
  return {
    legacyOnGlobalThis: globalThis.legacyCounter,
    modernLexical: modernCounter,
    greeting: globalThis.legacyGreeting("guest"),
  };
}
