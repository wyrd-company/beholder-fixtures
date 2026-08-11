// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export declare const enum AmbientConst {
  Alpha = 0,
  Beta = 1,
  Gamma = 2,
}

export function useAmbient(value: AmbientConst): number {
  return value + 10;
}

export function ambientValues(): AmbientConst[] {
  return [AmbientConst.Alpha, AmbientConst.Beta, AmbientConst.Gamma];
}
