// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export type Thenable<T> = {
  then(
    onFulfilled: (value: T) => T | Thenable<T> | Promise<T>,
    onRejected?: (reason: unknown) => unknown,
  ): Thenable<T> | Promise<T>;
};

export function createThenable<T>(value: T): Thenable<T> {
  return {
    then(onFulfilled) {
      return Promise.resolve(onFulfilled(value));
    },
  };
}

export async function unwrapThenable(): Promise<string> {
  const inner = createThenable("inner");
  const outer = createThenable(inner);
  const result = await outer;
  return `unwrap:${String(result)}`;
}

export async function nestedPromiseUnwrap(): Promise<string> {
  const nested: Promise<Promise<string>> = Promise.resolve(
    Promise.resolve("nested") as unknown as Promise<string>,
  ) as unknown as Promise<Promise<string>>;
  const value = await nested;
  return `nested:${String(value)}`;
}

export async function thenableAdoption(value: string): Promise<string> {
  const thenable = createThenable(value);
  return await thenable;
}
