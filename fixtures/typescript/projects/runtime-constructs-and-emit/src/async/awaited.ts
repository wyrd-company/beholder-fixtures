// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export type WrappedString = Promise<string>;
export type Unwrapped = Awaited<WrappedString>;

export type NestedWrapped = Promise<Promise<number>>;
export type DeepUnwrapped = Awaited<NestedWrapped>;

export type ThenableString = {
  then: (onFulfilled: (v: string) => string) => string;
};
export type AwaitedThenable = Awaited<ThenableString>;

export async function demonstrateAwaited(
  input: Promise<string>,
): Promise<Awaited<Promise<string>>> {
  const value: Awaited<typeof input> = await input;
  return value;
}

export function createAwaitedValue(value: string): Unwrapped {
  return value;
}
