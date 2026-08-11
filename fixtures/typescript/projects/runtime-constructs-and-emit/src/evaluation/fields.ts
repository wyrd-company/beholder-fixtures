// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export const fieldInitLog: string[] = [];

export class NativeFields {
  a = "atlas";
  b = 42;
  c = (() => {
    fieldInitLog.push("init:c");
    return "ledger";
  })();
}

export class BaseField {
  base = "base";
}

export class DerivedField extends BaseField {
  derived = "derived";
  override base = "overridden";
}

export function nativeVsTransformed(): string[] {
  fieldInitLog.length = 0;
  const instance = new NativeFields();
  fieldInitLog.push(`instance:${instance.a}:${instance.b}`);
  return [...fieldInitLog];
}

export function fieldInitializationOrder(): string[] {
  fieldInitLog.length = 0;
  fieldInitLog.push("before-new");
  void new DerivedField();
  fieldInitLog.push("after-new");
  return [...fieldInitLog];
}
