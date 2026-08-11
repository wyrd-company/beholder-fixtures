// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

/**
 * Standard class decorators covering factories, replacement, addInitializer,
 * typed context, ordering, and Symbol.metadata.
 */

export const classInitLog: string[] = [];

function withTag(tag: string) {
  return function (
    value: abstract new (...args: unknown[]) => unknown,
    context: ClassDecoratorContext,
  ): void {
    context.metadata[tag] = true;
    context.addInitializer(function (
      this: abstract new (...args: unknown[]) => unknown,
    ) {
      classInitLog.push(`init:${String(context.name)}:${tag}`);
    });
  };
}

function replaceWithTagged<
  T extends abstract new (...args: unknown[]) => unknown,
>(value: T, context: ClassDecoratorContext<T>): T {
  class Replacement extends (value as abstract new (
    ...args: unknown[]
  ) => object) {
    readonly replaced = true;
  }
  Object.defineProperty(Replacement, "name", {
    value: `${String(context.name)}_Replaced`,
  });
  context.addInitializer(function (this: T) {
    classInitLog.push(`replace-init:${String(context.name)}`);
  });
  return Replacement as unknown as T;
}

function outer(
  value: abstract new (...args: unknown[]) => unknown,
  context: ClassDecoratorContext,
): void {
  classInitLog.push(`apply:outer:${String(context.name)}`);
  context.addInitializer(function () {
    classInitLog.push(`init:outer:${String(context.name)}`);
  });
}

function inner(
  value: abstract new (...args: unknown[]) => unknown,
  context: ClassDecoratorContext,
): void {
  classInitLog.push(`apply:inner:${String(context.name)}`);
  context.addInitializer(function () {
    classInitLog.push(`init:inner:${String(context.name)}`);
  });
}

@withTag("alpha")
export class Catalog {
  static kind = "generic";
}

@withTag("beta")
@withTag("gamma")
export class Ledger {
  static kind = "ledger";
}

@outer
@inner
export class OrderedCatalog {
  static kind = "ordered";
}

@replaceWithTagged
export class ReplacedCatalog {
  static kind = "replaced";
}

export function readCatalogMetadata(): unknown {
  return (Catalog as unknown as Record<symbol, unknown>)[Symbol.metadata];
}

export function readLedgerMetadata(): unknown {
  return (Ledger as unknown as Record<symbol, unknown>)[Symbol.metadata];
}

export function readOrderedInitLog(): string[] {
  return [...classInitLog];
}
