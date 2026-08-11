// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

/**
 * Legacy descriptor mutation.
 * Method and accessor decorators mutate the property descriptor
 * (writable, enumerable, value/get/set) which is reflected in the
 * defined property on the prototype.
 */

export const descriptorLog: string[] = [];

function sealDescriptor(
  target: Object,
  propertyKey: string | symbol,
  descriptor: PropertyDescriptor,
): PropertyDescriptor {
  descriptorLog.push(`seal:${String(propertyKey)}`);
  descriptor.writable = false;
  descriptor.configurable = false;
  return descriptor;
}

function wrapDescriptor(
  target: Object,
  propertyKey: string | symbol,
  descriptor: PropertyDescriptor,
): PropertyDescriptor {
  descriptorLog.push(`wrap:${String(propertyKey)}`);
  const original = descriptor.value as (...args: unknown[]) => unknown;
  descriptor.value = function (this: unknown, ...args: unknown[]): unknown {
    descriptorLog.push(`invoke:${String(propertyKey)}`);
    const result = original.apply(this, args);
    return `wrapped:${String(result)}`;
  };
  return descriptor;
}

function nonEnumerable(
  target: Object,
  propertyKey: string | symbol,
  descriptor: PropertyDescriptor,
): void {
  descriptorLog.push(`nonEnumerable:${String(propertyKey)}`);
  descriptor.enumerable = false;
}

export class DescriptorGallery {
  @sealDescriptor
  fixed(value: string): string {
    return value;
  }

  @wrapDescriptor
  greet(name: string): string {
    return `hello:${name}`;
  }

  @nonEnumerable
  hidden(): string {
    return "hidden";
  }

  @sealDescriptor
  @wrapDescriptor
  combined(value: string): string {
    return value;
  }

  get descriptor(): PropertyDescriptor | undefined {
    return Object.getOwnPropertyDescriptor(
      DescriptorGallery.prototype,
      "greet",
    );
  }

  get hiddenDescriptor(): PropertyDescriptor | undefined {
    return Object.getOwnPropertyDescriptor(
      DescriptorGallery.prototype,
      "hidden",
    );
  }
}

export function getDescriptorLog(): string[] {
  return [...descriptorLog];
}

export function isHiddenEnumerable(): boolean {
  const desc = Object.getOwnPropertyDescriptor(
    DescriptorGallery.prototype,
    "hidden",
  );
  return desc?.enumerable ?? true;
}

export function isFixedWritable(): boolean {
  const desc = Object.getOwnPropertyDescriptor(
    DescriptorGallery.prototype,
    "fixed",
  );
  return desc?.writable ?? true;
}
