// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export function throwError(): never {
  throw new Error("ledger failure");
}

export function throwNonError(): never {
  throw "string failure";
}

export function throwNumber(): never {
  throw 42;
}

export function throwObject(): never {
  throw { code: "ATLAS", reason: "unknown" };
}

export function guardUnknownCatch(): string {
  try {
    throw new Error("caught");
  } catch (error: unknown) {
    if (error instanceof Error) {
      return `error:${error.message}`;
    }
    return `unknown:${String(error)}`;
  }
}

export function guardNonErrorCatch(): string {
  try {
    throw "non-error";
  } catch (error: unknown) {
    if (typeof error === "string") {
      return `string:${error}`;
    }
    return `other:${String(error)}`;
  }
}
