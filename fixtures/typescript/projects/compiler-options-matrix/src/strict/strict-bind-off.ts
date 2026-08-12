// strictBindCallApply off: call/apply argument checking is relaxed.
// Under strict true, greet.call with a string for age would be an error; under false it is allowed.
// This file is isolated to the off context.

export function greet(name: string, age: number): string {
  return `${name}:${age}`;
}

export function invokeWithMismatchedCall(): string {
  return greet.call(undefined, "sam", "thirty");
}

export function invokeWithMismatchedApply(): string {
  return greet.apply(undefined, ["sam", "thirty"]);
}
