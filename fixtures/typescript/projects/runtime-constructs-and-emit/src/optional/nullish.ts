// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export function nullishVersusOr(
  zero: number | null | undefined,
  empty: string | null | undefined,
): {
  nullishZero: number | string;
  orZero: number | string;
  nullishEmpty: string;
  orEmpty: string;
} {
  const nullishZero = zero ?? 99;
  const orZero = zero || 99;
  const nullishEmpty = empty ?? "fallback";
  const orEmpty = empty || "fallback";
  return { nullishZero, orZero, nullishEmpty, orEmpty };
}

export function nullishDemo(value: string | null | undefined): string {
  return value ?? "default";
}

export function orDemo(value: string | null | undefined): string {
  return value || "fallback";
}

export function coalesceZeroVsEmpty(): string {
  const zero = 0;
  const empty = "";
  const nullishZero = zero ?? 10;
  const logicalZero = zero || 10;
  const nullishEmpty = empty ?? "atlas";
  const logicalEmpty = empty || "atlas";
  return `nZ:${nullishZero}|oZ:${logicalZero}|nE:${nullishEmpty}|oE:${logicalEmpty}`;
}
