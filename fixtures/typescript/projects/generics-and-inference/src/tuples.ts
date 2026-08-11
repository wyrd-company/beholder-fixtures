// TS-CAN-066 — Arrays, tuples, labels, and variadic relations

// Fixed-length tuple.
export type FixedPair = [string, number];

// Optional tuple.
export type OptionalPair = [string, number?];
export type OptionalTriple = [string, number, boolean?];

// Readonly tuple forms.
export type ReadonlyPair = readonly [string, number];
export type ReadonlyLabeled = readonly [name: string, age: number];

// Labeled tuples — labels are preserved but identity-neutral.
export type LabeledPoint = [x: number, y: number];
export type EquivalentPoint = [number, number];

export function takesLabeled(point: LabeledPoint): number {
  return point[0] + point[1];
}

export function takesEquivalent(point: EquivalentPoint): number {
  return point[0] + point[1];
}

// Leading, middle, and rest patterns.
export type LeadingRest = [string, ...number[]];
export type MiddleRest = [string, ...number[], boolean];
export type TrailingRest = [...string[], number];
export type GenericVariadic<T extends unknown[]> = [string, ...T, boolean];

// Rest generic helper.
export type RestGeneric<T extends unknown[]> = [...T];

// Union rest.
export type UnionRest = [...(string | number)[]];

// Indexing and destructuring.
export function getTupleElement(
  tuple: FixedPair,
  index: 0 | 1,
): string | number {
  const value: string | number | undefined = tuple[index];
  return value ?? tuple[0];
}

export function destructureFixed([first, second]: FixedPair): [string, number] {
  return [first, second];
}

export function destructureOptional([first, second]: OptionalTriple): void {
  void first;
  if (second !== undefined) void second;
}

export function destructureWithRest(tuple: LeadingRest): [string, number[]] {
  const [first, ...rest] = tuple;
  return [first, rest];
}

export function destructureMiddle(
  tuple: MiddleRest,
): [string, number[], boolean] {
  const [first, ...middleAndLast] = tuple;
  const last = middleAndLast.pop() as boolean;
  const middle = middleAndLast as number[];
  return [first, middle, last];
}

// Concatenation via spread.
export function concatTuples<A extends unknown[], B extends unknown[]>(
  a: A,
  b: B,
): [...A, ...B] {
  return [...a, ...b];
}

// Parameter lists and spread into calls.
export function variadicParams(
  ...args: [string, number, ...boolean[]]
): string {
  const [first, second, ...rest] = args;
  return `${first}:${second}:${rest.length}`;
}

export function callWithSpread(): void {
  const pair: FixedPair = ["hello", 42];
  destructureFixed(...([pair] as const));
  const args: [string, number, ...boolean[]] = ["a", 1, true, false];
  variadicParams(...args);
}

// Generic variadic tuple usage.
export function wrapWithTags<T extends unknown[]>(
  first: string,
  ...middle: T
): [string, ...T, boolean] {
  return [first, ...middle, true];
}

export function useGenericVariadic(): void {
  const result: [string, number, string, boolean] = wrapWithTags(
    "start",
    42,
    "end",
  );
  void result;
  const empty: [string, boolean] = wrapWithTags("only");
  void empty;
}

// Labels preserved but identity-neutral — assignability check.
export function checkLabelIdentity(): void {
  const labeled: LabeledPoint = [1, 2];
  const equivalent: EquivalentPoint = labeled;
  void takesLabeled(equivalent);
  void takesEquivalent(labeled);
}

// Readonly forms.
export function readReadonlyTuple(tuple: ReadonlyPair): string {
  const first: string | undefined = tuple[0];
  return first ?? "default";
}

export function concatReadonly<
  A extends readonly unknown[],
  B extends readonly unknown[],
>(a: A, b: B): readonly [...A, ...B] {
  return [...a, ...b] as const;
}

// Union rest usage.
export function handleUnionRest(values: UnionRest): number {
  return values.length;
}

export function handleOptionalTuple(tuple: OptionalPair): string {
  const [first, second] = tuple;
  if (second === undefined) return first;
  return `${first}:${second}`;
}

// Variadic in function signature with generic.
export function collectItems<T extends unknown[]>(
  head: string,
  ...tail: T
): [string, ...T] {
  return [head, ...tail];
}

export function spreadIntoCollect(): void {
  const items: [string, ...number[]] = ["head", 1, 2, 3];
  const [first, ...rest] = items;
  collectItems(first, ...rest);
}
