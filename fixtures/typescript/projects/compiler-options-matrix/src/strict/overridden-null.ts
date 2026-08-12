// Child override for strictNullChecks: this file is valid only when strictNullChecks is false.
// Under strict true, assigning string | null to string is an error; under overridden false it is allowed.

export function assignNullableToString(value: string | null): string {
  const result: string = value;
  return result;
}

export function getStringOrNull(flag: boolean): string | null {
  return flag ? "token" : null;
}
