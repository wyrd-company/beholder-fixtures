// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export const enum LocalConst {
  Alpha = 1,
  Beta = 2,
  Gamma = 3,
}

export const enum ExportedConst {
  Red = 0,
  Green = 1,
  Blue = 2,
}

export enum Ordinary {
  Alpha = 1,
  Beta = 2,
  Gamma = 3,
}

export function useLocalConst(value: LocalConst): number {
  return value * 2;
}

export function useExportedConst(value: ExportedConst): string {
  return `exported:${value}`;
}

export function useOrdinary(value: Ordinary): number {
  return Ordinary[value] ? value : -1;
}

export function compareConstVsOrdinary(
  local: LocalConst,
  ordinary: Ordinary,
): string {
  return `const:${local}:ordinary:${ordinary}:${Ordinary[ordinary]}`;
}
