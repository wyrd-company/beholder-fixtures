// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export function* innerSequence(): Generator<string, void, unknown> {
  yield "inner-a";
  yield "inner-b";
}

export function* outerSequence(): Generator<string, string, unknown> {
  yield "outer-a";
  yield* innerSequence();
  yield "outer-b";
  return "outer-done";
}

export function* delegatedWithReturn(): Generator<number, string, unknown> {
  const result: string = yield* stringDelegated();
  return `delegated:${result}`;
}

function* stringDelegated(): Generator<number, string, unknown> {
  yield 1;
  yield 2;
  return "inner-result";
}

export function collectDelegation(): string[] {
  return [...outerSequence()];
}
