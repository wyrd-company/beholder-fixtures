// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// Side-effectful module whose evaluation point differs between eager and deferred imports (TS-CAN-033)
export const harborTideCounter = { count: 0 };

globalThis.harborDeferCounter = globalThis.harborDeferCounter ?? 0;
globalThis.harborDeferCounter += 1;
harborTideCounter.count = globalThis.harborDeferCounter;

export const sideEffectTag = `evaluated-${harborTideCounter.count}`;

export function readSideEffect(): string {
  return sideEffectTag;
}

declare global {
  var harborDeferCounter: number | undefined;
}
