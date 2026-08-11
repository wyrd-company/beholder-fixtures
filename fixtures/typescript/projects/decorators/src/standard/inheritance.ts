// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

/**
 * Standard decorator inheritance and metadata inheritance.
 * Base and derived decorators each contribute metadata and initializers.
 */

export const inheritanceLog: string[] = [];

function baseTag(
  value: abstract new (...args: unknown[]) => unknown,
  context: ClassDecoratorContext,
): void {
  context.metadata["base"] = true;
  context.metadata["baseName"] = String(context.name);
  context.addInitializer(function () {
    inheritanceLog.push(`base-init:${String(context.name)}`);
  });
}

function derivedTag(
  value: abstract new (...args: unknown[]) => unknown,
  context: ClassDecoratorContext,
): void {
  context.metadata["derived"] = true;
  context.metadata["derivedName"] = String(context.name);
  context.addInitializer(function () {
    inheritanceLog.push(`derived-init:${String(context.name)}`);
  });
}

function baseMethod<
  This,
  Value extends (this: This, ...args: unknown[]) => unknown,
>(value: Value, context: ClassMethodDecoratorContext<This, Value>): Value {
  context.metadata[`baseMethod:${String(context.name)}`] = true;
  context.addInitializer(function () {
    inheritanceLog.push(`baseMethod-init:${String(context.name)}`);
  });
  return value;
}

function derivedMethod<
  This,
  Value extends (this: This, ...args: unknown[]) => unknown,
>(value: Value, context: ClassMethodDecoratorContext<This, Value>): Value {
  context.metadata[`derivedMethod:${String(context.name)}`] = true;
  context.addInitializer(function () {
    inheritanceLog.push(`derivedMethod-init:${String(context.name)}`);
  });
  return value;
}

function baseFieldDecorator(
  _value: undefined,
  context: ClassFieldDecoratorContext,
): (initialValue: any) => any {
  context.metadata["baseField"] = true;
  return function (initialValue: any): any {
    return initialValue;
  };
}

export class BaseCatalog {
  @baseMethod
  describe(): string {
    return "base";
  }

  @baseFieldDecorator
  static baseField = "base-field";
}

@derivedTag
export class DerivedCatalog extends BaseCatalog {
  @derivedMethod
  override describe(): string {
    return "derived";
  }

  @derivedMethod
  extra(): string {
    return "extra";
  }
}

export function readBaseMetadata(): unknown {
  return (BaseCatalog as unknown as Record<symbol, unknown>)[Symbol.metadata];
}

export function readDerivedMetadata(): unknown {
  return (DerivedCatalog as unknown as Record<symbol, unknown>)[
    Symbol.metadata
  ];
}

export function getInheritanceLog(): string[] {
  return [...inheritanceLog];
}

/**
 * Metadata inheritance check: derived metadata object prototype chain
 * includes base metadata where supported, otherwise each class has its own
 * metadata object. This demonstrates the separation and per-class metadata
 * while showing derived inherits from base via prototype or own properties.
 */
export function describeMetadataInheritance(): {
  base: unknown;
  derived: unknown;
  hasBaseFlagOnDerived: boolean;
} {
  const base = readBaseMetadata() as Record<string, unknown> | undefined;
  const derived = readDerivedMetadata() as Record<string, unknown> | undefined;
  const hasBaseFlagOnDerived =
    derived !== undefined &&
    ("base" in derived ||
      (Object.getPrototypeOf(derived) !== null &&
        "base" in (Object.getPrototypeOf(derived) as Record<string, unknown>)));
  return { base, derived, hasBaseFlagOnDerived };
}
