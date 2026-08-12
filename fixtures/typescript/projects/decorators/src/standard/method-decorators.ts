// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

/**
 * Standard method decorators covering static/instance, private, typed context,
 * factories, replacement, addInitializer, and ordering.
 */

if (!(Symbol as unknown as Record<string, symbol>).metadata) {
  (Symbol as unknown as Record<string, symbol>).metadata =
    Symbol("Symbol.metadata");
}

export const methodInitLog: string[] = [];

function loggedMethod(value: any, context: ClassMethodDecoratorContext): any {
  context.addInitializer(function (this: unknown) {
    methodInitLog.push(
      `method-init:${String(context.name)}:${String(context.static)}`,
    );
  });
  const wrapped = function (this: unknown, ...args: unknown[]): unknown {
    methodInitLog.push(`call:${String(context.name)}`);
    return (value as (...args: unknown[]) => unknown).apply(this, args);
  };
  return wrapped;
}

function withRetry(retries: number) {
  return function (value: any, context: ClassMethodDecoratorContext): any {
    if (context.metadata)
      context.metadata[`retry:${String(context.name)}`] = retries;
    return value;
  };
}

function outerMethod(value: any, context: ClassMethodDecoratorContext): any {
  methodInitLog.push(`apply:outerMethod:${String(context.name)}`);
  return value;
}

function innerMethod(value: any, context: ClassMethodDecoratorContext): any {
  methodInitLog.push(`apply:innerMethod:${String(context.name)}`);
  return value;
}

function replaceMethod(value: any, context: ClassMethodDecoratorContext): any {
  const replacement = function (this: unknown, ...args: unknown[]): unknown {
    return `replaced:${String(context.name)}`;
  };
  return replacement;
}

export class MethodGallery {
  @loggedMethod
  @withRetry(2)
  describe(label: string): string {
    return `describe:${label}`;
  }

  @loggedMethod
  static create(id: string): MethodGallery {
    return new MethodGallery();
  }

  @outerMethod
  @innerMethod
  ordered(value: string): string {
    return value;
  }

  @replaceMethod
  toReplace(): string {
    return "original";
  }

  @loggedMethod
  #privateCompute(value: number): number {
    return value * 2;
  }

  exposePrivate(value: number): number {
    return (
      (this as unknown as { _callPrivate(v: number): number })._callPrivate?.(
        value,
      ) ?? this.#privateCompute(value)
    );
  }
}

export function readMethodMetadata(): unknown {
  return (MethodGallery as unknown as Record<symbol, unknown>)[Symbol.metadata];
}
