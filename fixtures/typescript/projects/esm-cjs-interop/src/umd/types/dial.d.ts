// ---
// relationships:
//   implements: esm-cjs-interop
//   references: ground-rules
// ---

export = Dial;

interface Dial {
  spin(): number;
}

declare function Dial(): Dial;

declare namespace Dial {
  function spin(): number;
}
