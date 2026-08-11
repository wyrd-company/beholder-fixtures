// Hidden implementation symbols not re-exported from public entry.
// Annotated `: number` so its value is an implementation detail: changing it
// leaves the emitted `internal.d.ts` identical, which is what makes the
// implementation-only rebuild scope in TS-CAN-005 observable.
export const internalMultiplier: number = 3;

const hiddenSequence = [1, 2, 3];

export function hiddenTransform(value: number): number {
  return value * internalMultiplier + hiddenSequence.length;
}

type HiddenConfig = {
  seed: number;
  tag: string;
};
