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
  if (typeof record[key] === "string") {
    return record[key].toUpperCase();
  }
  if (typeof record[key] === "number") {
    return record[key].toFixed(2);
  }
  return "missing";
}

export function constantIndexNarrowingOnTuple(
  tuple: [string | number, string | number],
): string {
  const index = 0 as const;
  if (typeof tuple[index] === "string") {
    return tuple[index].toUpperCase();
  }
  return tuple[index].toFixed(2);
}
