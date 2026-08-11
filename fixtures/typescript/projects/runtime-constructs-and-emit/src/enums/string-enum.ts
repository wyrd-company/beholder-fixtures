// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export enum Direction {
  North = "NORTH",
  South = "SOUTH",
  East = "EAST",
  West = "WEST",
}

export enum TaskState {
  Idle = "idle",
  Running = "running",
  Done = "done",
}

export function stringEnumMissingReverseMap(
  value: Direction,
): string | undefined {
  const table = Direction as unknown as Record<string, string>;
  return table[value];
}

export function consumeDirection(value: Direction): string {
  return `direction:${value}`;
}

export function directionValues(): string[] {
  return [Direction.North, Direction.South, Direction.East, Direction.West];
}
