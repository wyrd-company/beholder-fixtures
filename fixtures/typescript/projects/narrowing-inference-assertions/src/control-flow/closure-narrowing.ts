// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export function closureNarrowing(value: string | null): () => string {
  if (value === null) {
    return () => "no-value";
  }
  return () => value.toUpperCase();
}

export function preservedClosureNarrowing(
  payload: { label: string } | null,
): string {
  if (payload === null) {
    return "empty";
  }
  const readLabel = (): string => payload.label;
  return readLabel().toLowerCase();
}

export function constIndexedAccessNarrowing(
  record: Record<string, string | number>,
): string {
  const key = "label" as const;
  const value = record[key];
  if (typeof value === "string") {
    return value.toUpperCase();
  }
  if (typeof value === "number") {
    return value.toFixed(2);
  }
  return "missing";
}

export function constantIndexNarrowingOnTuple(
  tuple: [string, number, boolean],
): string {
  const index = 0 as const;
  const first = tuple[index];
  return first.toUpperCase();
}
