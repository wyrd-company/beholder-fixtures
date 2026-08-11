// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export type StringOrNumber = string | number;
export type NullableRecord = { label: string } | null | undefined;

export type TaggedShape =
  | { kind: "circle"; radius: number }
  | { kind: "square"; side: number }
  | { kind: "triangle"; base: number; height: number };

export type InTarget =
  | { tag: string; note?: string }
  | { tag: string; note?: string; extra: number };

export function narrowByTypeof(value: StringOrNumber): string {
  if (typeof value === "string") {
    return value.toUpperCase();
  }
  return value.toFixed(2);
}

export function narrowByEquality(value: string | number | null): string {
  if (value === null) {
    return "empty";
  }
  if (value === 0) {
    return "zero";
  }
  if (value === "atlas") {
    return "matched";
  }
  return String(value);
}

export function narrowByTruthiness(
  value: StringOrNumber | null | undefined,
): string {
  if (value) {
    return String(value);
  }
  return "falsy";
}

export function narrowEmptyStringAndZero(label: string, count: number): string {
  const labelResult = label ? `label:${label}` : "empty-string-falsy";
  const countResult = count ? `count:${count}` : "zero-falsy";
  return `${labelResult}|${countResult}`;
}

export function narrowByInOperator(entry: InTarget): string {
  if ("extra" in entry) {
    return `extra:${entry.extra}:${entry.tag}`;
  }
  return `base:${entry.tag}`;
}

export function optionalPropertyOnBothInBranches(
  entry: { note?: string; tag: "a" } | { note?: string; tag: "b" },
): string {
  if ("note" in entry) {
    const note: string | undefined = entry.note;
    return note ? `with-note:${note}` : "note-undefined";
  }
  return "no-note-key";
}

export function narrowByInstanceof(value: Date | string): number {
  if (value instanceof Date) {
    return value.getTime();
  }
  return value.length;
}

export function narrowByDiscriminant(shape: TaggedShape): number {
  if (shape.kind === "circle") {
    return Math.PI * shape.radius * shape.radius;
  }
  if (shape.kind === "square") {
    return shape.side * shape.side;
  }
  return (shape.base * shape.height) / 2;
}

export function assignmentAndReachability(input: string | null): string {
  let current: string | null = input;
  if (current === null) {
    return "no-value";
  }
  current = current.trim();
  return current.toUpperCase();
}
