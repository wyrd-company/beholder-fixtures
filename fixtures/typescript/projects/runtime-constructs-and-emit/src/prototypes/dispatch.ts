// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export class Base {
  label(): string {
    return "base";
  }

  describe(): string {
    return `base:${this.label()}`;
  }
}

export class Derived extends Base {
  override label(): string {
    return "derived";
  }
}

export function dispatchThroughBase(base: Base): string {
  return base.label();
}

export function extractedReceiverLoss(instance: Base): string {
  const fn = instance.label;
  try {
    return (fn as () => string)();
  } catch {
    return "lost-receiver";
  }
}

export function prototypeMutation(): string {
  const instance = new Derived();
  const before = instance.label();
  (Base.prototype as unknown as { label: () => string }).label = () =>
    "mutated";
  const after = instance.label();
  (Base.prototype as unknown as { label: () => string }).label = () => "base";
  return `${before}:${after}`;
}

export function superDispatch(): string {
  class Child extends Base {
    override label(): string {
      return `child:${super.label()}`;
    }
  }
  return new Child().label();
}

export function arrowPropertyDispatch(): string {
  class Holder {
    label = "holder";
    getLabel = (): string => this.label;
  }
  const holder = new Holder();
  const fn = holder.getLabel;
  return fn();
}

export function instanceofCheck(value: unknown): string {
  if (value instanceof Derived) return "derived";
  if (value instanceof Base) return "base";
  return "other";
}

export function assignShallowCopy(): string {
  const source = { nested: { value: 1 }, plain: "atlas" };
  const copy = Object.assign({}, source);
  (copy.nested as { value: number }).value = 2;
  return `${source.nested.value}:${copy.nested.value}:${copy.plain}`;
}
