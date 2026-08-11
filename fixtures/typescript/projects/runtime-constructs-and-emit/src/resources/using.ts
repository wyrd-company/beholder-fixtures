// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export const disposeLog: string[] = [];

export function resetDisposeLog(): void {
  disposeLog.length = 0;
}

export function createSyncResource(label: string): Disposable {
  return {
    [Symbol.dispose](): void {
      disposeLog.push(`dispose:${label}`);
    },
  };
}

export function createAsyncResource(label: string): AsyncDisposable {
  return {
    [Symbol.asyncDispose](): Promise<void> {
      return Promise.resolve().then(() => {
        disposeLog.push(`async-dispose:${label}`);
      });
    },
  };
}

export function usingSingle(): string {
  resetDisposeLog();
  {
    using res = createSyncResource("single");
    void res;
    disposeLog.push("inside");
  }
  disposeLog.push("after");
  return disposeLog.join("|");
}

export function usingMultiple(): string {
  resetDisposeLog();
  {
    using a = createSyncResource("a");
    using b = createSyncResource("b");
    void a;
    void b;
    disposeLog.push("inside");
  }
  return disposeLog.join("|");
}

export function nestedScopes(): string {
  resetDisposeLog();
  {
    using outer = createSyncResource("outer");
    void outer;
    disposeLog.push("outer-inside");
    {
      using inner = createSyncResource("inner");
      void inner;
      disposeLog.push("inner-inside");
    }
    disposeLog.push("outer-after-inner");
  }
  return disposeLog.join("|");
}

export function earlyReturn(flag: boolean): string {
  resetDisposeLog();
  {
    using res = createSyncResource("early");
    void res;
    disposeLog.push("before-return");
    if (flag) {
      return disposeLog.join("|") + "|returning";
    }
    disposeLog.push("no-return");
  }
  disposeLog.push("after");
  return disposeLog.join("|");
}

export function thrownCompletion(): string {
  resetDisposeLog();
  try {
    {
      using a = createSyncResource("first");
      using b = createSyncResource("second");
      void a;
      void b;
      disposeLog.push("before-throw");
      throw new Error("boom");
    }
  } catch (error) {
    disposeLog.push(`caught:${(error as Error).message}`);
  }
  return disposeLog.join("|");
}

export function suppressedErrorDemo(): string {
  resetDisposeLog();
  try {
    {
      using failing = {
        [Symbol.dispose](): void {
          disposeLog.push("dispose-throws");
          throw new Error("dispose-error");
        },
      };
      void failing;
      disposeLog.push("before-throw");
      throw new Error("body-error");
    }
  } catch (error) {
    const err = error as Error & { suppressed?: unknown };
    disposeLog.push(`caught:${err.message}`);
    if (
      typeof SuppressedError !== "undefined" &&
      err instanceof SuppressedError
    ) {
      disposeLog.push(
        `suppressed:${String((err as unknown as { suppressed: Error }).suppressed.message)}`,
      );
    } else if ((error as { suppressed?: unknown }).suppressed) {
      disposeLog.push("suppressed-present");
    }
  }
  return disposeLog.join("|");
}

export async function awaitUsingSingle(): Promise<string> {
  resetDisposeLog();
  {
    await using res = createAsyncResource("async-single");
    void res;
    disposeLog.push("inside-async");
  }
  disposeLog.push("after-async");
  return disposeLog.join("|");
}

export async function awaitUsingMultiple(): Promise<string> {
  resetDisposeLog();
  {
    await using a = createAsyncResource("am-a");
    await using b = createAsyncResource("am-b");
    void a;
    void b;
    disposeLog.push("inside-async-multi");
  }
  return disposeLog.join("|");
}

export function cleanupDispatchObservable(): string {
  resetDisposeLog();
  const order: string[] = [];
  function make(label: string): Disposable {
    return {
      [Symbol.dispose](): void {
        order.push(label);
        disposeLog.push(`cleanup:${label}`);
      },
    };
  }
  try {
    using x = make("x");
    using y = make("y");
    using z = make("z");
    void x;
    void y;
    void z;
    disposeLog.push("work");
    throw new Error("work-error");
  } catch {
    disposeLog.push("handled");
  }
  return `${disposeLog.join("|")}|order:${order.join(",")}`;
}
