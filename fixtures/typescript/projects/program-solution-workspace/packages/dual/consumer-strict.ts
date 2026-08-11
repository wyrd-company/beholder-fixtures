import { describeShared, domProbe, type SharedCard } from "./shared.js";

// Strict program — `types: ["node"]`, `lib: ["ES2022","DOM"]`, `strict: true`
const card: SharedCard = { id: "s1", label: "strict", count: 3 };

export function runStrict(): string {
  return `${describeShared(card)}|${domProbe()}`;
}

// Referenced-source redirection: when this file is compiled as part of the strict program,
// `shared.ts` resolves via the strict program identity, not the loose one.
export const strictMarker = "strict-program";
