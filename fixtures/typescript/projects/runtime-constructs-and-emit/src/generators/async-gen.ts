// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export async function* asyncCount(
  start: number,
  end: number,
): AsyncGenerator<number, string, unknown> {
  for (let i = start; i < end; i++) {
    await Promise.resolve();
    yield i;
  }
  return "async-done";
}

export async function* asyncDelegation(): AsyncGenerator<
  string,
  void,
  unknown
> {
  yield "async-outer";
  yield* asyncInner();
  yield "async-end";
}

async function* asyncInner(): AsyncGenerator<string, void, unknown> {
  await Promise.resolve();
  yield "async-inner";
}

export async function collectAsyncGen(): Promise<string[]> {
  const values: string[] = [];
  for await (const value of asyncDelegation()) {
    values.push(value);
  }
  return values;
}
