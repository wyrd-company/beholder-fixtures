export class Shared {
  private __brand = "shared" as const;
  value: number = 42;
  get tag(): "shared" {
    return "shared";
  }
}

export const sharedValue = new Shared();

export function describeShared(s: Shared): string {
  return `${s.tag}:${s.value}`;
}
