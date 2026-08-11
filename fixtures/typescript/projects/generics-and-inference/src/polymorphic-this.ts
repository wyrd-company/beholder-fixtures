// TS-CAN-077 — Polymorphic this and receiver-linked types

// Base fluent method returning this chained through derived subtype.
export class FluentBase {
  protected steps: string[] = [];

  addStep(step: string): this {
    this.steps.push(step);
    return this;
  }

  getSteps(): string[] {
    return [...this.steps];
  }

  // Method returning named base type — contrast with this.
  snapshot(): FluentBase {
    const copy = new FluentBase();
    copy.steps = [...this.steps];
    return copy;
  }

  // Explicit this parameter.
  describe(this: FluentBase): string {
    return this.steps.join(" -> ");
  }

  // This is T predicate.
  isActive(this: FluentBase): this is ActiveFluent {
    return this.steps.length > 0;
  }

  // Static-side contrast — static method not polymorphic over instance this.
  static create(): FluentBase {
    return new FluentBase();
  }
}

export class ActiveFluent extends FluentBase {
  markActive(): this {
    this.addStep("active");
    return this;
  }

  getActiveSteps(): string[] {
    return this.getSteps();
  }
}

export class DerivedFluent extends FluentBase {
  withLabel(label: string): this {
    this.addStep(`label:${label}`);
    return this;
  }

  static createDerived(): DerivedFluent {
    return new DerivedFluent();
  }
}

export function chainFluent(): DerivedFluent {
  const fluent = new DerivedFluent();
  return fluent.addStep("start").withLabel("core").addStep("end");
}

// This is T predicate usage.
export function checkIsActive(fluent: FluentBase): void {
  if (fluent.isActive()) {
    const active: ActiveFluent = fluent;
    void active.getActiveSteps();
  }
}

// F-bounded generic alternative to polymorphic this.
export class FBbounded<T extends FBbounded<T>> {
  protected items: string[] = [];

  add(item: string): T {
    this.items.push(item);
    return this as unknown as T;
  }

  getItems(): string[] {
    return [...this.items];
  }
}

export class ConcreteBounded extends FBbounded<ConcreteBounded> {
  withTag(tag: string): this {
    this.add(`tag:${tag}`);
    return this;
  }
}

export function useFBounded(): ConcreteBounded {
  const bounded = new ConcreteBounded();
  return bounded.add("first").withTag("second");
}

// Mixin or intersection builder — mixin pattern.

export type Constructor<T = object> = new (...args: any[]) => T;

export function Timestamped<TBase extends Constructor>(Base: TBase) {
  return class extends Base {
    timestamp = Date.now();

    getTimestamp(): number {
      return this.timestamp;
    }
  };
}

export function Labelled<TBase extends Constructor>(Base: TBase) {
  return class extends Base {
    label = "default";

    setLabel(value: string): this {
      this.label = value;
      return this;
    }
  };
}

// Intersection builder alternative.
export type Builder<T> = T & {
  with<V extends object>(extra: V): Builder<T & V>;
};

export function makeBuilder<T extends object>(initial: T): Builder<T> {
  return {
    ...initial,
    with<V extends object>(extra: V): Builder<T & V> {
      return makeBuilder({ ...initial, ...extra });
    },
  } as Builder<T>;
}

// Usage of mixins.
export class BaseItem {
  constructor(public name: string) {}
}

export const MixedItem = Labelled(Timestamped(BaseItem));

export function useMixedItem(): void {
  const item = new MixedItem("example") as InstanceType<typeof MixedItem> &
    BaseItem & {
      getTimestamp(): number;
      setLabel(value: string): InstanceType<typeof MixedItem>;
    };
  item.setLabel("updated");
  void item.getTimestamp();
  void item.name;
}

// Static-side contrast demonstration.
export class StaticContrast {
  instanceValue = 1;

  instanceMethod(): this {
    return this;
  }

  static staticValue = 100;

  static staticMethod(): StaticContrast {
    return new StaticContrast();
  }
}

export class DerivedStaticContrast extends StaticContrast {
  extra = 2;

  derivedMethod(): this {
    return this;
  }
}

export function checkStaticContrast(): void {
  const derived = new DerivedStaticContrast();
  const chained: DerivedStaticContrast = derived
    .instanceMethod()
    .derivedMethod();
  void chained;
  const fromStatic: StaticContrast = StaticContrast.staticMethod();
  void fromStatic;
}

// Private/protected state with polymorphic this.
export class ProtectedFluent {
  protected count = 0;

  increment(): this {
    this.count += 1;
    return this;
  }

  getCount(): number {
    return this.count;
  }
}

export class ExtendedProtected extends ProtectedFluent {
  decrement(): this {
    this.count -= 1;
    return this;
  }
}

export function chainProtected(): ExtendedProtected {
  return new ExtendedProtected().increment().increment().decrement();
}
