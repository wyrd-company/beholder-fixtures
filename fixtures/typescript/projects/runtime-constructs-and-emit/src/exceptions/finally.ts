// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export function finallyOverrides(): string {
  try {
    throw new Error("original");
  } catch {
    return "from-catch";
  } finally {
    return "from-finally";
  }
}

export function finallyOverridesCompletion(): number {
  try {
    return 1;
  } finally {
    return 2;
  }
}

export function disposalErrorDemo(): string {
  const log: string[] = [];
  try {
    {
      using resource = {
        [Symbol.dispose](): void {
          log.push("dispose");
          throw new Error("dispose failed");
        },
      };
      void resource;
      log.push("inside");
      throw new Error("body failed");
    }
  } catch (error) {
    const suppressed = error as unknown as {
      message?: string;
      suppressed?: unknown;
    };
    log.push(`caught:${String(suppressed.message ?? suppressed)}`);
    if (typeof (error as { suppressed?: unknown }).suppressed !== "undefined") {
      log.push("suppressed-present");
    }
  }
  return log.join("|");
}

export async function asyncRejection(): Promise<string> {
  try {
    await Promise.reject(new Error("async failure"));
    return "unreachable";
  } catch (error: unknown) {
    return `async-caught:${(error as Error).message}`;
  }
}
