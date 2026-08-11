export interface Shared {
  tag: "shared";
  value: number;
}

export const sharedValue: Shared = { tag: "shared", value: 42 };

export function describeShared(s: Shared): string {
  return `${s.tag}:${s.value}`;
}
