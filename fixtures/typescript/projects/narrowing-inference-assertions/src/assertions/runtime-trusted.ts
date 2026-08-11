// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// At least one trusted claim that type-checks but fails at runtime.
// Valid source whose failure is runtime behavior rather than a compiler error.

export function trustedNonNullThatFails(): string {
  const maybeNull: string | null = null;
  return maybeNull!.toUpperCase();
}

export function trustedDoubleAssertionThatFails(): number {
  const unknownValue: unknown = "atlas";
  const asNumber = unknownValue as unknown as number;
  return asNumber.toFixed(2) as unknown as number;
}

export function trustedPredicateThatFails(): string {
  const sample: unknown = 42;
  if (isString(sample)) {
    return sample.toUpperCase();
  }
  return String(sample);
}

function isString(value: unknown): value is string {
  void value;
  return true;
}

export function trustedSatisfiesThenAssertion(): string {
  const record = { label: "atlas", count: 3 } satisfies {
    label: string;
    count: number;
  };
  const widened = record as unknown as { label: number };
  return String(widened.label);
}

export function demonstrateRuntimeFailure(): string[] {
  const results: string[] = [];
  try {
    results.push(trustedNonNullThatFails());
  } catch {
    results.push("caught-non-null");
  }
  try {
    results.push(trustedDoubleAssertionThatFails().toString());
  } catch {
    results.push("caught-double-assertion");
  }
  return results;
}
