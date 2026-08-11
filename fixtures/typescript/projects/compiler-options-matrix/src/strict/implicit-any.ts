// noImplicitAny: explicit annotations satisfy the check in both modes.
// Without the flag, an unannotated parameter would be inferred as any implicitly;
// with the flag, that implicit any is gated and requires annotation.

export function formatLabel(value: string): string {
  return value.trim().toUpperCase();
}

export function applyTransform(
  input: string,
  transform: (value: string) => string,
): string {
  return transform(input);
}

export function collectTokens(items: string[]): string[] {
  return items.map((item: string) => item.toLowerCase());
}
