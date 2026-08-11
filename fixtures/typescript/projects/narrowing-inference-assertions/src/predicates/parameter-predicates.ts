// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export function isString(value: unknown): value is string {
  return typeof value === "string";
}

export function isNumber(value: unknown): value is number {
  return typeof value === "number";
}

export function isNonEmptyString(
  value: string,
): value is string & { length: number } {
  return value.length > 0;
}

export function isRecordWithTag<Tag extends string>(
  value: unknown,
  tag: Tag,
): value is { tag: Tag } {
  return (
    typeof value === "object" &&
    value !== null &&
    "tag" in value &&
    (value as { tag: unknown }).tag === tag
  );
}

export function isTagged<T extends { kind: string }>(
  value: unknown,
  kind: T["kind"],
): value is T {
  return (
    typeof value === "object" &&
    value !== null &&
    "kind" in value &&
    (value as { kind: unknown }).kind === kind
  );
}

export class Ledger {
  constructor(public readonly revision: string) {}

  isAtlas(): this is AtlasLedger {
    return this.revision.startsWith("atlas-");
  }
}

export class AtlasLedger extends Ledger {
  readonly atlasMarker = "atlas";

  readRevision(): string {
    return this.revision.toUpperCase();
  }
}

export function consumeThisPredicate(ledger: Ledger): string {
  if (ledger.isAtlas()) {
    return ledger.readRevision();
  }
  return ledger.revision;
}
