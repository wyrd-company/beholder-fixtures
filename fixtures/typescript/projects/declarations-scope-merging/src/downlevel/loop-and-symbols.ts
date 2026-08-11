// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export function captureLoopWithLet(): number[] {
  const results: number[] = [];

  for (let index = 0; index < 3; index += 1) {
    results.push(
      (function () {
        return index;
      })(),
    );
  }

  return results;
}

export function useSymbolWithDownlevelLib(): {
  keyed: Record<symbol, number>;
  description: string;
} {
  const marker = Symbol("marker");
  const keyed: Record<symbol, number> = {
    [marker]: 7,
  };

  return {
    keyed,
    description: String(marker),
  };
}
