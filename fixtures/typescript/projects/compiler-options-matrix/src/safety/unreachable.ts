// allowUnreachableCode false: unreachable code is gated. Valid file has no unreachable statements.

export function processValue(value: string | null): string {
  if (value === null) {
    return "missing";
  }
  return value.toUpperCase();
}

export function earlyReturn(flag: boolean): string {
  if (flag) {
    return "yes";
  }
  return "no";
}
