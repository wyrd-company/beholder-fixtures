// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export function filterNonNull<T>(values: Array<T | null | undefined>): T[] {
  return values.filter((value) => value !== null && value !== undefined);
}

export function filterByIsString(values: unknown[]): string[] {
  return values.filter((value): value is string => typeof value === "string");
}

export function inferredPredicateFilter(items: Array<string | null>): string[] {
  return items.filter((item) => item !== null);
}

export function inferredTruthinessFilter(
  entries: Array<{ label: string } | null>,
): Array<{ label: string }> {
  return entries.filter((entry): entry is { label: string } => entry !== null);
}

export function demonstrateFilterNarrowing(
  mixed: Array<string | number | null>,
): string[] {
  const strings = mixed.filter(isString);
  return strings.map((entry) => entry.toUpperCase());
}

function isString(value: unknown): value is string {
  return typeof value === "string";
}
