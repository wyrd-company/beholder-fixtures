// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export function withContextCallback(
  handler: (value: string) => number,
  input: string,
): number {
  return handler(input);
}

export function sameCallbackWithContext(): number {
  return withContextCallback((value) => value.length, "atlas");
}

export function sameCallbackWithoutContext(): number {
  const handler = (value: string) => value.length;
  return handler("atlas");
}

export function contextualReturn(): string {
  const produce = withContextCallback((value) => value.length, "atlas");
  const asString = String(produce);
  return asString;
}

export type Handler = (value: string) => number;

export function applyHandler(handler: Handler, value: string): number {
  return handler(value);
}

export function callbackContextContrast(): [number, number] {
  const contextual = withContextCallback((input) => input.length, "ledger");
  const standalone: Handler = (input) => input.length;
  return [contextual, standalone("ledger")];
}
