// noUnusedParameters: unused parameters are gated. Valid file uses or explicitly marks unused params.

export function describeWithUsedParams(id: string, label: string): string {
  return `${id}:${label}`;
}

export function handleWithIgnoredParam(
  _unusedToken: string,
  label: string,
): string {
  return label;
}

export function combineWithRest(first: string, ...rest: string[]): string {
  return [first, ...rest].join("-");
}
