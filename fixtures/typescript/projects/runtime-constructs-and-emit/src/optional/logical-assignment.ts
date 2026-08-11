// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export function andAssign(
  target: { value?: string | null } | undefined,
  fallback: string,
): string | null | undefined {
  let current = target?.value;
  current &&= fallback;
  return current;
}

export function orAssign(
  target: { value?: string | null } | undefined,
  fallback: string,
): string | null | undefined {
  let current = target?.value;
  current ||= fallback;
  return current;
}

export function nullishAssign(
  target: { value?: string | null } | undefined,
  fallback: string,
): string | null | undefined {
  let current = target?.value;
  current ??= fallback;
  return current;
}

export function flowEffectsDemo(input: string | null | undefined): string {
  let value: string | null | undefined = input;
  value ??= "initialized";
  if (value) {
    value &&= value.toUpperCase();
  }
  return value ?? "absent";
}

export function logicalAssignWithCount(
  counts: Map<string, number>,
  key: string,
): number {
  let current = counts.get(key);
  current ??= 0;
  current &&= current + 1;
  current ||= 1;
  counts.set(key, current);
  return current;
}
