// TS-CAN-076 — Call, construct, overloaded, and hybrid object types

// Stateful callable object with properties.
export interface StatefulCallable {
  count: number;
  label: string;
  (): string;
  increment(): void;
  reset(): void;
  [key: string]: unknown;
  [index: number]: unknown;
}

// Separate call and construct signatures returning different types.
export interface CallAndConstruct {
  (value: string): string;
  new (value: string): { instanceId: string; value: string };
}

// Generic call and construct signatures.
export interface GenericHybrid<T> {
  (value: T): T;
  new (value: T): { wrapped: T };
  transform<U>(input: T, mapper: (value: T) => U): U;
  [key: string]: unknown;
}

// Overloaded hybrid with index members.
export interface OverloadedHybrid {
  (value: string): string;
  (value: number): number;
  (value: string | number): string | number;
  kind: string;
  [key: string]: unknown;
  [index: number]: string | number;
}

// Runtime implementation assigned to hybrid interface.
export const statefulCounter: StatefulCallable = Object.assign(
  function callCounter(): string {
    statefulCounter.count += 1;
    return `${statefulCounter.label}:${statefulCounter.count}`;
  },
  {
    count: 0,
    label: "counter",
    increment() {
      statefulCounter.count += 1;
    },
    reset() {
      statefulCounter.count = 0;
    },
  },
) as StatefulCallable;

export const callConstructExample: CallAndConstruct = function (
  this: unknown,
  value: string,
): string | { instanceId: string; value: string } {
  if (new.target) {
    const self = this as { instanceId: string; value: string };
    self.instanceId = `id-${value}`;
    self.value = value;
    return self;
  }
  return `call:${value}`;
} as unknown as CallAndConstruct;

// Provide construct behavior via class for the generic hybrid.
export class GenericHybridImpl<T> {
  static transform<T, U>(input: T, mapper: (value: T) => U): U {
    return mapper(input);
  }

  private _value: T;

  constructor(value: T) {
    this._value = value;
  }

  call(value: T): T {
    return value;
  }

  get wrapped(): T {
    return this._value;
  }
}

// Abstract construct signature.
export type AbstractConstruct = abstract new (id: string) => { id: string };

export abstract class AbstractBase {
  constructor(public id: string) {}
}

export class ConcreteBase extends AbstractBase {}

// Demonstrating abstract construct signature via assignment — concrete class satisfies abstract construct.
export const AbstractFactory: AbstractConstruct = ConcreteBase;

export type ConcreteConstruct = new (id: string) => { id: string };

export function createAbstractInstance(
  factory: AbstractConstruct,
  id: string,
): { id: string } {
  const concrete = factory as unknown as ConcreteConstruct;
  return new concrete(id);
}

export function createConcreteInstance(id: string): { id: string } {
  return new ConcreteBase(id);
}

// Constructor this — constructor returns this.
export class SelfConstructed {
  public tag = "self";

  constructor(public name: string) {
    return this;
  }

  clone(): this {
    const copy = new (this.constructor as new (name: string) => this)(
      this.name,
    );
    return copy;
  }
}

// Number and string index compatibility — number index constrained by string index.
export interface CompatibleIndexes {
  [key: string]: string | number;
  [index: number]: string;
  name: string;
}

export function useCompatibleIndexes(
  store: CompatibleIndexes,
): string | undefined {
  const fromString: string | number | undefined = store["name"];
  const fromNumber: string | undefined = store[0];
  return (fromString as string) ?? fromNumber;
}

// Additional callable with generic signatures and overloads assigned.
export interface ComplexCallable {
  <T>(value: T): T;
  (value: string): string;
  (value: number): number;
  meta: string;
  [key: string]: unknown;
}

export const complexCallable: ComplexCallable = Object.assign(
  function callComplex(value: unknown): unknown {
    return value;
  },
  { meta: "complex" },
) as ComplexCallable;

// OverloadedHybrid runtime instance.
export const overloadedHybridInstance: OverloadedHybrid = Object.assign(
  function hybridFn(value: string | number): string | number {
    return value;
  },
  {
    kind: "overloaded",
  },
) as OverloadedHybrid;
