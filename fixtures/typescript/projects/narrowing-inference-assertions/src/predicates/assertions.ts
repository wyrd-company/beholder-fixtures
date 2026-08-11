// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export function assert(condition: unknown): asserts condition {
  if (!condition) {
    throw new Error("assertion failed");
  }
}

export function assertIsString(value: unknown): asserts value is string {
  if (typeof value !== "string") {
    throw new Error("expected string");
  }
}

export function assertIsNonNull<T>(
  value: T | null | undefined,
): asserts value is T {
  if (value === null || value === undefined) {
    throw new Error("expected non-null");
  }
}

export function useAssertCondition(payload: unknown): string {
  assert(typeof payload === "string");
  return payload.toUpperCase();
}

export function useAssertIsString(value: unknown): number {
  assertIsString(value);
  return value.length;
}

export function useAssertNonNull(value: string | null): string {
  assertIsNonNull(value);
  return value.trim();
}
