// noImplicitReturns: missing return in a code path is gated. Every branch returns explicitly.

export function classifyWeight(weight: number): string {
  if (weight > 100) {
    return "heavy";
  }
  if (weight > 10) {
    return "medium";
  }
  return "light";
}

export function getLabelOrDefault(label: string | undefined): string {
  if (label !== undefined) {
    return label;
  }
  return "default";
}
