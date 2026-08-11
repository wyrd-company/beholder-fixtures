// Hidden implementation symbols not re-exported from public entry.
export const internalMultiplier = 3;

const hiddenSequence = [1, 2, 3];

export function hiddenTransform(value: number): number {
  return value * internalMultiplier + hiddenSequence.length;
}

type HiddenConfig = {
  seed: number;
  tag: string;
};
