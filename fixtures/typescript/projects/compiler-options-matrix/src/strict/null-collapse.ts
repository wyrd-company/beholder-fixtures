// strictNullChecks: type-changing null collapse when strict-null checking is off.
// Under strictNullChecks false, null/undefined are assignable to string and collapse the union;
// under true they remain distinct. This valid program handles both with explicit checks.

export function getMaybeLabel(): string | null {
  return Math.random() > 0.5 ? "harbor" : null;
}

export function describeMaybeLabel(value: string | null): string {
  if (value === null) {
    return "missing";
  }
  return value.toUpperCase();
}

export function readMaybeWithFallback(value: string | null): string {
  return value ?? "fallback";
}

export function lengthOrZero(value: string | null): number {
  return value !== null ? value.length : 0;
}
