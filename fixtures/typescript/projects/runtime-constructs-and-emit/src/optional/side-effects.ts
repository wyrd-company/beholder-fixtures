// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export const sideEffectLog: string[] = [];

export function resetLog(): void {
  sideEffectLog.length = 0;
}

export const tracked = {
  get value(): string | undefined {
    sideEffectLog.push("getter");
    return "atlas";
  },
};

export function sideEffectGetterSkipped(container?: {
  data?: { value?: string };
}): string | undefined {
  return container?.data?.value;
}

export function sideEffectGetterEvaluated(container: {
  data: { get value(): string };
}): string | undefined {
  return container?.data.value;
}

export function sideEffectIndexSkipped(
  record?: Record<string, string>,
): string | undefined {
  sideEffectLog.push("before-optional");
  const result =
    record?.[
      (() => {
        sideEffectLog.push("compute-key");
        return "atlas";
      })()
    ];
  sideEffectLog.push("after-optional");
  return result;
}

export function sideEffectIndexEvaluated(
  record: Record<string, string>,
): string | undefined {
  const key = (() => {
    sideEffectLog.push("compute-key-evaluated");
    return "atlas";
  })();
  return record?.[key];
}

export function optionalChainWithSideEffectCall(obj?: {
  run?(): string;
}): string | undefined {
  sideEffectLog.push("call-before");
  const result = obj?.run?.();
  sideEffectLog.push("call-after");
  return result;
}
