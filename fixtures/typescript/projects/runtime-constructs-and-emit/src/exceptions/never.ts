// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export function fail(message: string): never {
  throw new Error(message);
}

export function callNever(input: string | null): string {
  if (input === null) {
    fail("value was null");
  }
  return input.toUpperCase();
}

export function assertIsString(value: unknown): asserts value is string {
  if (typeof value !== "string") {
    throw new Error("not a string");
  }
}

export function useAssertion(value: unknown): string {
  assertIsString(value);
  return value.toUpperCase();
}
