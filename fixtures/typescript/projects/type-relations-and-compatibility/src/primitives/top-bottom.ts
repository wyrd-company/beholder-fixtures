export function assignPrimitiveLiterals(): {
  text: string;
  count: number;
  active: boolean;
  empty: null;
} {
  const text: string = "anchor";
  const count: number = 42;
  const active: boolean = true;
  const empty: null = null;
  return { text, count, active, empty };
}

export function contrastObjectTopTypes(): {
  record: object;
  openRecord: Record<string, unknown>;
  emptyObject: {};
} {
  const record: object = { lane: "north" };
  const openRecord: Record<string, unknown> = { lane: "north", depth: 3 };
  const emptyObject: {} = { marker: true };
  return { record, openRecord, emptyObject };
}

export function propagateAny(value: any): any {
  const copied = value;
  const nested = copied.nested;
  return nested?.token;
}

export function evolvingAny(): number {
  let total;
  total = 1;
  total = total + 1;
  total = total.toFixed(0);
  return Number(total);
}

export function refineUnknown(candidate: unknown): string {
  if (typeof candidate === "string") {
    return candidate.toUpperCase();
  }
  if (typeof candidate === "number") {
    return candidate.toFixed(2);
  }
  return "fallback";
}

export function impossibleBranch(tag: "alpha" | "beta"): never {
  switch (tag) {
    case "alpha":
      throw new Error("alpha");
    case "beta":
      throw new Error("beta");
    default: {
      const unreachable: never = tag;
      return unreachable;
    }
  }
}

export function inferNeverFromEmpty(value: string | number): string {
  if (typeof value === "string") {
    return value;
  }
  if (typeof value === "number") {
    return value.toFixed(0);
  }
  const unreachable: never = value;
  return String(unreachable);
}

export function acceptVoidCallback(run: () => void): void {
  run();
}

export function returnValueFromVoidTarget(run: () => void): void {
  run();
}

export function useVoidCallback(): void {
  acceptVoidCallback(() => {
    return 7;
  });
}

export function boxedPrimitives(): {
  textObject: String;
  countObject: Number;
  flagObject: Boolean;
} {
  const textObject = new String("ledger");
  const countObject = new Number(9);
  const flagObject = new Boolean(false);
  return { textObject, countObject, flagObject };
}

export function nullablePrimitive(
  maybeCount: number | null | undefined,
): number {
  if (maybeCount == null) {
    return 0;
  }
  return maybeCount;
}

export function callWithPrimitive(value: string): string {
  return value.trim();
}

export function readProperty(record: { token: string }): string {
  return record.token;
}

export function exhaustLiteralKind(kind: "draft" | "final"): string {
  switch (kind) {
    case "draft":
      return "pending";
    case "final":
      return "sealed";
    default: {
      const _exhaustive: never = kind;
      return _exhaustive;
    }
  }
}
