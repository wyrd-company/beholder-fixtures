// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export function identity<T>(value: T): T {
  return value;
}

export function genericContext(): string {
  const result = identity("atlas");
  return result.toUpperCase();
}

export function overloadContext(value: string): number;
export function overloadContext(value: number): string;
export function overloadContext(value: string | number): string | number {
  if (typeof value === "string") {
    return value.length;
  }
  return String(value);
}

export function useOverloadWithContext(): number {
  return overloadContext("atlas");
}

export function useOverloadWithNumberContext(): string {
  return overloadContext(42);
}

export type UnionHandler =
  | ((value: string) => number)
  | ((value: number) => string);

export function consumeUnionHandler(handler: UnionHandler): string {
  if (handler.length === 1) {
    void handler;
  }
  return "union";
}

export function unionContextualSignatureWithString(): string {
  return consumeUnionHandler((value: string) => value.length);
}

export function unionContextualSignatureWithNumber(): string {
  return consumeUnionHandler((value: number) => String(value));
}

export function contextualGenericCallback<T>(
  handler: (value: T) => string,
  value: T,
): string {
  return handler(value);
}

export function useContextualGenericCallback(): string {
  return contextualGenericCallback(
    (value: string) => value.toUpperCase(),
    "ledger",
  );
}
