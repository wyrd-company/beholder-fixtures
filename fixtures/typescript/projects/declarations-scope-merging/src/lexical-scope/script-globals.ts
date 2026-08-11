// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

var legacyCounter = 0;

function legacyGreeting(name: string): string {
  return `hello-${name}`;
}

let modernCounter = 0;
const modernFrozen = 0;

function readGlobalBindingsForScript(): {
  legacyOnGlobalThis: number;
  modernLexical: number;
  greeting: string;
} {
  return {
    legacyOnGlobalThis: legacyCounter,
    modernLexical: modernCounter,
    greeting: legacyGreeting("guest"),
  };
}

void modernFrozen;
