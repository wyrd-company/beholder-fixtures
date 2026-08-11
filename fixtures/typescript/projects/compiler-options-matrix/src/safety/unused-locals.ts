// noUnusedLocals: unused locals are gated. This valid file uses every declared local.

export function sumUsedLocals(a: number, b: number): number {
  const sum = a + b;
  const doubled = sum * 2;
  return doubled;
}

export function formatUsedLocals(label: string): string {
  const trimmed = label.trim();
  const upper = trimmed.toUpperCase();
  return upper;
}
