// One source placed in two configured programs with different `types`, `lib`, and strictness.
export type SharedCard = {
  id: string;
  label: string;
  count: number;
};

// This function behaves differently under strict vs loose compilation due to strictNullChecks and lib differences.
export function describeShared(card: SharedCard | null): string {
  if (card === null) {
    return "null-card";
  }
  return `${card.id}:${card.label}:${card.count}`;
}

// DOM lib is available in strict program (lib ES2022,DOM) but not in loose (lib ES5 only).
export function domProbe(): string {
  const doc = (
    globalThis as unknown as { document?: { createElement?: unknown } }
  ).document;
  if (
    typeof doc !== "undefined" &&
    typeof (doc as { createElement?: unknown }).createElement === "function"
  ) {
    return "dom:present";
  }
  return "dom:absent";
}
