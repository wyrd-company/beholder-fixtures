// ---
// relationships:
//   implements: esm-cjs-interop
//   references: ground-rules
// ---

declare class CtsGaugeDecl {
  read(): number;
}

declare namespace CtsGaugeDecl {
  const marker: string;
}

export = CtsGaugeDecl;
