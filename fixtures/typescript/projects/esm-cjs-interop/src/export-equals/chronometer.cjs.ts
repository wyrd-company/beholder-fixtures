// ---
// relationships:
//   implements: esm-cjs-interop
//   references: ground-rules
// ---

class Chronometer {
  elapsed(): number {
    return 0;
  }
}

namespace Chronometer {
  export const unit = "ms";
  export function zero(): Chronometer {
    return new Chronometer();
  }
}

export = Chronometer;
