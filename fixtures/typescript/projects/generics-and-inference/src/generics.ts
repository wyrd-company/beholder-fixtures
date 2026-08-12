// TS-CAN-068 — Generic declarations, constraints, defaults, and inference

// Generic functions.
export function identity<T>(value: T): T {
  return value;
}

export function pair<F, S>(first: F, second: S): [F, S] {
  return [first, second];
}

// Constrained generic with default.
export function withConstraint<T extends string>(value: T): T {
  return value;
}

export function withDefault<T = string>(
  value: T = "default" as unknown as T,
): T {
  return value;
}

// Generic class.
export class Container<T> {
  constructor(public value: T) {}

  map<U>(fn: (value: T) => U): Container<U> {
    return new Container(fn(this.value));
  }

  get(): T {
    return this.value;
  }
}

// Generic interface.
export interface Holder<T> {
  value: T;
  getValue(): T;
}

// Generic alias.
export type Box<T> = { content: T };

// Call and construct signatures — generic.
export interface CallableSignature {
  <T>(value: T): T;
  <T, U>(first: T, second: U): [T, U];
}

export interface ConstructSignature {
  new <T>(value: T): Container<T>;
}

// Nested shadowed parameters — inner T shadows outer T.
export function outer<T>(outerValue: T): <T>(innerValue: T) => T {
  return <T>(innerValue: T) => innerValue ?? (outerValue as unknown as T);
}

// Context-driven inference.
export function processWithCallback<T>(
  items: T[],
  callback: (item: T) => string,
): string[] {
  return items.map(callback);
}

export function useContextInference(): void {
  const result = processWithCallback([1, 2, 3], (item) => item.toFixed(1));
  void result;
}

// Return-driven inference.
export function makeHolder<T>(value: T): Holder<T> {
  return {
    value,
    getValue() {
      return value;
    },
  };
}

export function makeEmptyHolder<T>(): Holder<T> {
  return {
    value: undefined as unknown as T,
    getValue() {
      return undefined as unknown as T;
    },
  };
}

export function useReturnInference(): void {
  // Return-driven: T supplied by contextual return type, no value argument to infer from.
  const holderFromContext: Holder<number> = makeEmptyHolder();
  void holderFromContext;
  const holderExplicit: Holder<string> = makeEmptyHolder<string>();
  void holderExplicit;
  // Value-driven for contrast still present
  const inferred = makeHolder("hello");
  const checked: string = inferred.getValue();
  void checked;
}

// Default referencing earlier parameter.
export function withDependentDefault<K extends string, V = K>(
  key: K,
  value: V = key as unknown as V,
): [K, V] {
  return [key, value];
}

// Explicit and inferred arguments.
export function useExplicitAndInferred(): void {
  const inferredPair = pair("a", 1);
  void inferredPair;
  const explicitPair = pair<string, number>("a", 1);
  void explicitPair;
  const explicitIdentity = identity<string>("hello");
  void explicitIdentity;
  const inferredIdentity = identity(123);
  void inferredIdentity;
}

// Higher-order inference.
export function higherOrder<T, U>(fn: (arg: T) => U, value: T): U {
  return fn(value);
}

export function useHigherOrderInference(): void {
  const result = higherOrder((x: string) => x.length, "hello");
  const checked: number = result;
  void checked;
  const mapped = higherOrder((n: number) => n * 2, 21);
  void mapped;
}

// Recursive generic — tree structure.
export interface TreeNode<T> {
  value: T;
  children: TreeNode<T>[];
}

export function flattenTree<T>(node: TreeNode<T>): T[] {
  return [node.value, ...node.children.flatMap(flattenTree)];
}

// Generic alias with constraint and default, using recursive.
export type Result<T, E extends string = string> =
  | { ok: true; value: T }
  | { ok: false; error: E };

// Additional generic class with constraint and default.
export class Registry<T extends { id: string }, U = T[]> {
  private items: Map<string, T> = new Map();

  add(item: T): void {
    this.items.set(item.id, item);
  }

  get(id: string): T | undefined {
    return this.items.get(id);
  }

  list(): U {
    return Array.from(this.items.values()) as unknown as U;
  }
}

// Demonstrate partial inference limitation is not required to fail — show valid inference still works.
export function combine<A, B>(a: A, b: B): [A, B] {
  return [a, b];
}

export function useCombine(): void {
  const inferred: [string, number] = combine("x", 42);
  void inferred;
  const withExplicitFirst = combine<string, number>("x", 42);
  void withExplicitFirst;
}
