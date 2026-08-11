import { describeShared, type SharedCard } from "./shared.js";

// Loose program — `lib: ["ES5"]`, `strict: false`, no `types` — DOM globals unavailable, strictNullChecks off.
const looseCard: SharedCard | undefined = {
  id: "l1",
  label: "loose",
  count: 1,
} as unknown as SharedCard;

export function runLoose(): string {
  // In loose program `null | undefined` handling is permissive; same source text checked under different strictness.
  const maybeNull: SharedCard | null = looseCard ?? null;
  // @ts-ignore loose program allows looser null handling
  return describeShared(maybeNull);
}

export const looseMarker = "loose-program";
