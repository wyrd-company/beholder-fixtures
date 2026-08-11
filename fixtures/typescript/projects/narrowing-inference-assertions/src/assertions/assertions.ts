// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export function wideningAssertion(value: "atlas"): string {
  const widened = value as string;
  return widened;
}

export function narrowingAssertion(value: unknown): string {
  const narrowed = value as string;
  return narrowed.toUpperCase();
}

export function doubleAssertion(value: unknown): string {
  const bridged = value as unknown as string;
  return bridged.toUpperCase();
}

export function postfixNonNull(value: string | null | undefined): string {
  return value!.toUpperCase();
}

export function nonNullInChain(
  payload: { label?: string | null } | null,
): string {
  if (payload?.label) {
    return payload.label!.toUpperCase();
  }
  return "empty";
}

export function assertionPreservesLiteral(): void {
  const token = "atlas" as const;
  const widened = token as string;
  void widened;
  const narrowed = "atlas" as unknown as "atlas";
  void narrowed;
}

export function doubleAssertionBetweenUnrelated(): string {
  const mixed: unknown = { tag: "atlas" };
  const asRecord = mixed as unknown as { tag: string };
  return asRecord.tag;
}
