// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export const orderLog: string[] = [];

function log(label: string): string {
  orderLog.push(label);
  return label;
}

function makeKey(label: string): string {
  orderLog.push(`key:${label}`);
  return label;
}

export function resetOrderLog(): void {
  orderLog.length = 0;
}

export function computedKeysOrder(): string[] {
  resetOrderLog();
  const obj = {
    [makeKey("a")]: 1,
    [makeKey("b")]: 2,
  };
  void obj;
  return [...orderLog];
}

export function spreadOrder(): string[] {
  resetOrderLog();
  const a = { [log("a")]: 1, [log("b")]: 2 };
  const b = { [log("c")]: 3 };
  const merged = { ...a, ...b };
  void merged;
  return [...orderLog];
}

export function argumentOrder(): string[] {
  resetOrderLog();
  function target(x: string, y: string, z: string): string {
    orderLog.push(`call:${x},${y},${z}`);
    return `${x}${y}${z}`;
  }
  target(log("first"), log("second"), log("third"));
  return [...orderLog];
}

export function getterOrder(): string[] {
  resetOrderLog();
  const source = {
    get value(): string {
      orderLog.push("getter");
      return "atlas";
    },
  };
  const copy = { ...source };
  void copy;
  const spread = { a: source.value, b: source.value };
  void spread;
  return [...orderLog];
}

export function classElementsOrder(): string[] {
  resetOrderLog();
  class Demo {
    fieldA = log("fieldA");
    fieldB = log("fieldB");
    method() {
      log("method-body");
      return 1;
    }
  }
  void new Demo();
  return [...orderLog];
}

export function cleanupOrderWithUsing(): string[] {
  resetOrderLog();
  try {
    using r1 = {
      [Symbol.dispose](): void {
        orderLog.push("cleanup:r1");
      },
    };
    using r2 = {
      [Symbol.dispose](): void {
        orderLog.push("cleanup:r2");
      },
    };
    void r1;
    void r2;
    orderLog.push("body");
    throw new Error("boom");
  } catch {
    orderLog.push("catch");
  }
  return [...orderLog];
}
