// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export class TaggedRecord {
  constructor(
    public readonly tag: string,
    public readonly count: number,
  ) {}

  static [Symbol.hasInstance](instance: unknown): boolean {
    return (
      typeof instance === "object" &&
      instance !== null &&
      "tag" in instance &&
      typeof (instance as { tag: unknown }).tag === "string"
    );
  }
}

export class SpecialRecord extends TaggedRecord {
  constructor(
    tag: string,
    count: number,
    public readonly extra: string,
  ) {
    super(tag, count);
  }
}

export function narrowViaCustomHasInstance(value: unknown): string {
  if (value instanceof TaggedRecord) {
    return `tagged:${value.tag}:${value.count}`;
  }
  if (value instanceof SpecialRecord) {
    return `special:${value.extra}`;
  }
  return "unknown";
}

export function demonstrateHasInstanceWithUnknown(values: unknown[]): string[] {
  return values.map((item) => {
    if (item instanceof TaggedRecord) {
      return item.tag.toUpperCase();
    }
    return "other";
  });
}
