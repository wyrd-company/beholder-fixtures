// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

/** Ordered function overloads with one broader implementation covering optional and rest candidates. */
export function describe(value: string): { kind: "text"; value: string };
export function describe(value: number): { kind: "count"; value: number };
export function describe(
  value: string,
  tag: string,
): { kind: "tagged"; value: string; tag: string };
export function describe(
  value: string | number,
  tag?: string,
  ...notes: string[]
): { kind: string; value: string | number; tag?: string; notes?: string[] };
export function describe(
  value: string | number,
  tag?: string,
  ...notes: string[]
): { kind: string; value: string | number; tag?: string; notes?: string[] } {
  if (typeof value === "string" && tag !== undefined) {
    return { kind: "tagged", value, tag, notes };
  }
  if (typeof value === "string") return { kind: "text", value };
  return { kind: "count", value };
}

/** Calls resolving to different return types via overload selection. */
export function exerciseFunctionOverloads(): void {
  const textResult: { kind: "text"; value: string } = describe("hello");
  const countResult: { kind: "count"; value: number } = describe(42);
  const taggedResult: { kind: "tagged"; value: string; tag: string } = describe(
    "hello",
    "label",
  );
  const withRest: { kind: string; value: string | number } = describe(
    "hello",
    "label",
    "a",
    "b",
  );

  void textResult;
  void countResult;
  void taggedResult;
  void withRest;

  // The hidden implementation signature (string|number, tag?, ...notes) is not directly callable
  // with a boolean; such a call would be rejected. No invalid call is included here.

  // Union argument matching no single overload would be rejected; valid calls use a single
  // overload's parameter.
}
