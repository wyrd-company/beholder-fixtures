// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// Intentionally unsound but trusted predicate body: valid, compilable source.
// The compiler trusts the signature; runtime behavior diverges.

export function isAlwaysString(value: unknown): value is string {
  void value;
  return true;
}

export function consumeUnsoundPredicate(value: unknown): string {
  if (isAlwaysString(value)) {
    return value.toUpperCase();
  }
  return "unreachable";
}

export function unsoundNumericPredicate(value: unknown): value is number {
  return typeof value === "string" ? true : typeof value === "number";
}

export function useUnsoundNumeric(value: unknown): string {
  if (unsoundNumericPredicate(value)) {
    return value.toFixed(1);
  }
  return "0";
}
