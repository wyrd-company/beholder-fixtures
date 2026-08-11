// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export function aliasedConditionNarrowing(value: string | null): string {
  const isPresent = value !== null;
  if (isPresent) {
    return value.toUpperCase();
  }
  return "absent";
}

export function aliasedTruthinessCondition(
  payload: { label?: string } | null,
): string {
  const hasPayload = payload !== null && payload !== undefined;
  if (hasPayload) {
    const hasLabel = Boolean(payload.label);
    if (hasLabel) {
      return payload.label!.toLowerCase();
    }
  }
  return "missing";
}

export type AliasedUnion =
  | { kind: "alpha"; count: number }
  | { kind: "beta"; tag: string };

export function aliasedDiscriminant(payload: AliasedUnion): string {
  const isAlpha = payload.kind === "alpha";
  if (isAlpha) {
    return `alpha:${payload.count}`;
  }
  return `beta:${payload.tag}`;
}
