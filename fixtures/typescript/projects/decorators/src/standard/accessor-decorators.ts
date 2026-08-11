// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

/**
 * Standard accessor decorators covering getter, setter, and auto-accessor
 * targets with static/instance, private, factories, replacement, typed context,
 * addInitializer, and ordering.
 */

export const accessorInitLog: string[] = [];

function loggedGetter<This, Value>(
  value: (this: This) => Value,
  context: ClassGetterDecoratorContext<This, Value>,
): (this: This) => Value {
  context.addInitializer(function (this: This) {
    accessorInitLog.push(
      `getter-init:${String(context.name)}:${String(context.static)}`,
    );
  });
  return function (this: This): Value {
    accessorInitLog.push(`getter-call:${String(context.name)}`);
    return value.call(this);
  };
}

function loggedSetter<This, Value>(
  value: (this: This, value: Value) => void,
  context: ClassSetterDecoratorContext<This, Value>,
): (this: This, value: Value) => void {
  context.addInitializer(function (this: This) {
    accessorInitLog.push(
      `setter-init:${String(context.name)}:${String(context.static)}`,
    );
  });
  return function (this: This, v: Value): void {
    accessorInitLog.push(`setter-call:${String(context.name)}`);
    value.call(this, v);
  };
}

function withRange<This, Value extends number>(min: number, max: number) {
  return function (
    value: ClassAccessorDecoratorTarget<This, Value>,
    context: ClassAccessorDecoratorContext<This, Value>,
  ): ClassAccessorDecoratorResult<This, Value> {
    context.metadata[`range:${String(context.name)}`] = { min, max };
    return {
      get(this: This): Value {
        return value.get.call(this);
      },
      set(this: This, v: Value): void {
        const clamped = Math.min(max, Math.max(min, v as number)) as Value;
        value.set.call(this, clamped);
      },
      init(initialValue: Value): Value {
        return Math.min(max, Math.max(min, initialValue as number)) as Value;
      },
    };
  };
}

function loggedAccessor<This, Value>(
  value: ClassAccessorDecoratorTarget<This, Value>,
  context: ClassAccessorDecoratorContext<This, Value>,
): ClassAccessorDecoratorResult<This, Value> {
  context.addInitializer(function (this: This) {
    accessorInitLog.push(
      `accessor-init:${String(context.name)}:${String(context.static)}:${String(context.private)}`,
    );
  });
  return {
    get(this: This): Value {
      accessorInitLog.push(`accessor-get:${String(context.name)}`);
      return value.get.call(this);
    },
    set(this: This, v: Value): void {
      accessorInitLog.push(`accessor-set:${String(context.name)}`);
      value.set.call(this, v);
    },
    init(initialValue: Value): Value {
      accessorInitLog.push(`accessor-init-value:${String(context.name)}`);
      return initialValue;
    },
  };
}

function outerAccessor<This, Value>(
  value: ClassAccessorDecoratorTarget<This, Value>,
  _context: ClassAccessorDecoratorContext<This, Value>,
): ClassAccessorDecoratorResult<This, Value> {
  accessorInitLog.push(`apply:outerAccessor:${String(_context.name)}`);
  return value;
}

function innerAccessor<This, Value>(
  value: ClassAccessorDecoratorTarget<This, Value>,
  _context: ClassAccessorDecoratorContext<This, Value>,
): ClassAccessorDecoratorResult<This, Value> {
  accessorInitLog.push(`apply:innerAccessor:${String(_context.name)}`);
  return value;
}

export class AccessorGallery {
  private _label = "base";

  @loggedGetter
  get label(): string {
    return this._label;
  }

  @loggedSetter
  set label(value: string) {
    this._label = value;
  }

  @loggedAccessor
  accessor note = "note";

  @withRange(0, 100)
  accessor score = 42;

  @loggedGetter
  static get kind(): string {
    return "accessor-gallery";
  }

  @loggedSetter
  static set kind(value: string) {
    void value;
  }

  @loggedAccessor
  static accessor staticNote = "static-note";

  @outerAccessor
  @innerAccessor
  accessor orderedEntry = "entry";

  @loggedAccessor
  accessor #privateEntry = "private-entry";

  readPrivateEntry(): string {
    return this.#privateEntry;
  }

  writePrivateEntry(value: string): void {
    this.#privateEntry = value;
  }
}

export function readAccessorMetadata(): unknown {
  return (AccessorGallery as unknown as Record<symbol, unknown>)[
    Symbol.metadata
  ];
}
