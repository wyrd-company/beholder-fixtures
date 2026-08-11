// ---
// relationships:
//   implements: esm-cjs-interop
//   references: ground-rules
// ---

class CtsGauge {
  read(): number {
    return 1;
  }
}

namespace CtsGauge {
  export const marker = "cts";
}

export = CtsGauge;
