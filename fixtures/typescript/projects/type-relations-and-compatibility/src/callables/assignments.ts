export type BroadHandler = (value: string | number) => void;
export type NarrowHandler = (value: string) => void;

export function assignBroaderParameter(handler: BroadHandler): NarrowHandler {
  return handler;
}

export type FewerParams = (first: string) => void;
export type MoreParams = (first: string, second: number) => void;

export function assignDifferentCounts(handler: FewerParams): MoreParams {
  return handler;
}

export type OptionalRest = (first?: string, ...rest: number[]) => string;
export type RequiredHead = (first: string) => string;

export function assignOptionalRest(handler: OptionalRest): RequiredHead {
  return handler;
}

export type Returning = (input: string) => number;
export type VoidTarget = (input: string) => void;

export function discardReturnValue(handler: Returning): VoidTarget {
  return handler;
}

export function genericCallback<T>(
  value: T,
  project: (item: T) => string,
): string {
  return project(value);
}

export type NarrowProperty = { onEvent: (detail: string) => void };
export type BroadProperty = { onEvent: (detail: string | number) => void };

export function contravariantProperty(source: BroadProperty): NarrowProperty {
  return source;
}

export type Constructible = new (seed: number) => { seed: number };

export class SeedBox {
  constructor(public seed: number) {}
}

export function assignConstructor(ctor: Constructible): typeof SeedBox {
  return ctor as typeof SeedBox;
}

export interface Overloaded {
  (input: string): number;
  (input: number): string;
}

export function overloadedCall(fn: Overloaded, text: string): number;
export function overloadedCall(fn: Overloaded, value: number): string;
export function overloadedCall(
  fn: Overloaded,
  value: string | number,
): string | number {
  if (typeof value === "string") {
    return fn(value);
  }
  return fn(value);
}

export type VoidReturnTarget = () => void;

export function voidReturnSource(): number {
  return 1;
}

export function assignVoidReturn(): VoidReturnTarget {
  return voidReturnSource;
}

export interface MutableGenericContainer<T> {
  value: T;
  onChange: (next: T) => void;
}

export function mutableGenericContainer<T>(
  seed: T,
): MutableGenericContainer<T> {
  return {
    value: seed,
    onChange: (next) => {
      seed = next;
    },
  };
}

export type EventHandlerConvention = (event: { type: string }) => void;

export function eventHandlerConvention(
  handler: EventHandlerConvention,
): EventHandlerConvention {
  return handler;
}
