// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

/**
 * Standard decorators on private elements including private fields,
 * methods, getters, setters, and auto-accessors with typed context.
 */

export const privateLog: string[] = [];

function privateFieldDecorator<This, Value>(
  _value: undefined,
  context: ClassFieldDecoratorContext<This, Value>,
): (initialValue: Value) => Value {
  privateLog.push(
    `field:${String(context.name)}:private=${String(context.private)}:static=${String(context.static)}`,
  );
  context.addInitializer(function (this: This) {
    privateLog.push(`field-init:${String(context.name)}`);
  });
  return function (initialValue: Value): Value {
    return initialValue;
  };
}

function privateMethodDecorator(
  value: any,
  context: ClassMethodDecoratorContext,
): any {
  privateLog.push(
    `method:${String(context.name)}:private=${String(context.private)}:static=${String(context.static)}`,
  );
  context.addInitializer(function () {
    privateLog.push(`method-init:${String(context.name)}`);
  });
  return value;
}

function privateGetterDecorator<This, Value>(
  value: (this: This) => Value,
  context: ClassGetterDecoratorContext<This, Value>,
): (this: This) => Value {
  privateLog.push(
    `getter:${String(context.name)}:private=${String(context.private)}`,
  );
  return value;
}

function privateSetterDecorator<This, Value>(
  value: (this: This, value: Value) => void,
  context: ClassSetterDecoratorContext<This, Value>,
): (this: This, value: Value) => void {
  privateLog.push(
    `setter:${String(context.name)}:private=${String(context.private)}`,
  );
  return value;
}

function privateAccessorDecorator<This, Value>(
  value: ClassAccessorDecoratorTarget<This, Value>,
  context: ClassAccessorDecoratorContext<This, Value>,
): ClassAccessorDecoratorResult<This, Value> {
  privateLog.push(
    `accessor:${String(context.name)}:private=${String(context.private)}:static=${String(context.static)}`,
  );
  context.addInitializer(function () {
    privateLog.push(`accessor-init:${String(context.name)}`);
  });
  return value;
}

export class PrivateGallery {
  @privateFieldDecorator
  #note = "private-note";

  @privateFieldDecorator
  static #staticNote = "private-static-note";

  @privateMethodDecorator
  #compute(value: number): number {
    return value * 3;
  }

  @privateMethodDecorator
  static #staticCompute(value: number): number {
    return value + 1;
  }

  @privateGetterDecorator
  get #label(): string {
    return this.#note;
  }

  @privateSetterDecorator
  set #label(value: string) {
    this.#note = value;
  }

  @privateAccessorDecorator
  accessor #entry = "private-entry";

  @privateAccessorDecorator
  static accessor #staticEntry = "private-static-entry";

  exposeNote(): string {
    return this.#note;
  }

  exposeComputed(value: number): number {
    return this.#compute(value);
  }

  exposeLabel(): string {
    return this.#label;
  }

  updateLabel(value: string): void {
    this.#label = value;
  }

  exposeEntry(): string {
    return this.#entry;
  }

  updateEntry(value: string): void {
    this.#entry = value;
  }

  static exposeStaticCompute(value: number): number {
    return PrivateGallery.#staticCompute(value);
  }

  static exposeStaticNote(): string {
    return PrivateGallery.#staticNote;
  }

  static exposeStaticEntry(): string {
    return PrivateGallery.#staticEntry;
  }
}

export function getPrivateLog(): string[] {
  return [...privateLog];
}

export function readPrivateMetadata(): unknown {
  return (PrivateGallery as unknown as Record<symbol, unknown>)[
    Symbol.metadata
  ];
}
