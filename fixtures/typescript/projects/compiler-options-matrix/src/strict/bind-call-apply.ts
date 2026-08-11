// strictBindCallApply: call/apply/bind checking is gated.
// Under strictBindCallApply, argument tuples are checked against the target signature.

export function greet(name: string, age: number): string {
  return `${name}:${age}`;
}

export function invokeWithCall(): string {
  return greet.call(undefined, "sam", 30);
}

export function invokeWithApply(): string {
  return greet.apply(undefined, ["sam", 30] as const);
}

export function invokeWithBind(): string {
  const bound = greet.bind(undefined, "sam");
  return bound(30);
}
