// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

/**
 * Standard field decorators covering instance/static, private, factories,
 * replacement via initializer, typed context, addInitializer, and ordering.
 */

if (!(Symbol as unknown as Record<string, symbol>).metadata) {
  (Symbol as unknown as Record<string, symbol>).metadata =
    Symbol("Symbol.metadata");
}

export const fieldInitLog: string[] = [];

function trackedField<This, Value>(
  value: undefined,
  context: ClassFieldDecoratorContext<This, Value>,
): (initialValue: Value) => Value {
  context.addInitializer(function (this: This) {
    fieldInitLog.push(
      `field-init:${String(context.name)}:${String(context.static)}:${String(context.private)}`,
    );
  });
  return function (initialValue: Value): Value {
    fieldInitLog.push(`field-init-value:${String(context.name)}`);
    return initialValue;
  };
}

function withDefault(fallback: any) {
  return function (
    _value: undefined,
    context: ClassFieldDecoratorContext,
  ): (initialValue: any) => any {
    if (context.metadata)
      context.metadata[`default:${String(context.name)}`] = fallback;
    return function (initialValue: any): any {
      return (initialValue as unknown) ?? fallback;
    };
  };
}

function outerField<This, Value>(
  _value: undefined,
  context: ClassFieldDecoratorContext<This, Value>,
): (initialValue: Value) => Value {
  fieldInitLog.push(`apply:outerField:${String(context.name)}`);
  return function (initialValue: Value): Value {
    return initialValue;
  };
}

function innerField<This, Value>(
  _value: undefined,
  context: ClassFieldDecoratorContext<This, Value>,
): (initialValue: Value) => Value {
  fieldInitLog.push(`apply:innerField:${String(context.name)}`);
  return function (initialValue: Value): Value {
    return initialValue;
  };
}

export class FieldGallery {
  @trackedField
  title = "untitled";

  @withDefault("fallback")
  subtitle: string | undefined = undefined;

  @trackedField
  static kind = "field-gallery";

  @outerField
  @innerField
  orderedField = 1;

  @trackedField
  #privateNote = "secret";

  readPrivateNote(): string {
    return this.#privateNote;
  }
}

export function readFieldMetadata(): unknown {
  return (FieldGallery as unknown as Record<symbol, unknown>)[Symbol.metadata];
}
