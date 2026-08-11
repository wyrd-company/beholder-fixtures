// TS-CAN-069 — Const parameters, instantiation expressions, NoInfer, and variance annotations

// Paired ordinary and const type-parameter APIs.
export function collect<T>(items: T[]): T[] {
  return items;
}

export function collectConst<const T>(items: T[]): T {
  return items as unknown as T;
}

// Const parameter preserves literal types (paired API).
export function asConstArray<const T extends readonly unknown[]>(items: T): T {
  return items;
}

export function asWidenedArray<T extends readonly unknown[]>(items: T): T {
  return items;
}

// Inline versus pre-widened argument.
export function compareInlineVsWidened(): void {
  const inline = asConstArray(["a", "b"] as const);
  void inline;

  const widenedSource: string[] = ["a", "b"];
  const preWidened = asWidenedArray(widenedSource);
  void preWidened;
}

// Readonly candidate against mutable constraint — valid inference chooses fallback.
export function mutableTarget<T extends string[]>(value: T): T {
  return value;
}

export function demonstrateReadonlyCandidate(): void {
  const readonlyCandidate = ["x", "y"] as const;
  const result = mutableTarget(readonlyCandidate as unknown as string[]);
  void result;
}

// Instantiation expression specializing a generic function value.
export function genericIdentity<T>(value: T): T {
  return value;
}

export const stringIdentity = genericIdentity<string>;
export const numberIdentity = genericIdentity<number>;

export function useInstantiationExpression(): void {
  const a: string = stringIdentity("hello");
  const b: number = numberIdentity(42);
  void a;
  void b;

  const specialized = genericIdentity<string>;
  const c: string = specialized("specialized");
  void c;
}

// NoInfer blocking one inference site.
export function withNoInfer<T>(a: T, b: NoInfer<T>): T {
  return b ?? a;
}

export function useNoInfer(): void {
  const first: string = "hello";
  const second: string = "world";
  const result1 = withNoInfer(first, second);
  void result1;

  const result2 = withNoInfer<string>("hello", "world");
  void result2;
}

// Correct variance annotations — covariant, contravariant, invariant.

export interface Producer<out T> {
  produce(): T;
}

export interface Consumer<in T> {
  consume(value: T): void;
}

export interface Invariant<in out T> {
  process(value: T): T;
}

// Usage demonstrating correct variance via assignment compatibility.
export function demonstrateVariance(): void {
  const stringProducer: Producer<string> = { produce: () => "hello" };
  const unknownProducer: Producer<unknown> = stringProducer;
  void unknownProducer;

  const unknownConsumer: Consumer<unknown> = { consume: (_: unknown) => {} };
  const stringConsumer: Consumer<string> = unknownConsumer;
  void stringConsumer;

  const invariantString: Invariant<string> = { process: (v) => v };
  void invariantString;
}

// Measured versus annotated variance — recursive generic with explicit annotation.
export interface LinkedNode<out T> {
  value: T;
  next: LinkedNode<T> | null;
}

// Inline versus pre-widened argument with const param contrast.
export function createBox<T>(value: T): { value: T } {
  return { value };
}

export function createBoxConst<const T>(value: T): { value: T } {
  return { value };
}

export function demonstrateConstVsOrdinary(): void {
  const inlineConst = createBoxConst("hello");
  const checkLiteral: "hello" = inlineConst.value;
  void checkLiteral;

  const stored: string = "hello";
  const widened = createBox(stored);
  const checkWidened: string = widened.value;
  void checkWidened;
}

// Discarded overload after instantiation expression — valid coverage via generic function with overloads.
export function overloaded<T>(value: T): T;
export function overloaded(value: string): string;
export function overloaded(value: unknown): unknown {
  return value;
}

export const overloadedString = overloaded<string>;

export function useOverloadedInstantiation(): void {
  const result: string = overloadedString("test");
  void result;
}
