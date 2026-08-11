export interface MutableLedger {
  entries: string[];
  revision: number;
}

export type ReadonlyLedgerView = {
  readonly entries: readonly string[];
  readonly revision: number;
};

export function viewThroughAliases(ledger: MutableLedger): {
  mutable: MutableLedger;
  readonly: ReadonlyLedgerView;
} {
  const mutable: MutableLedger = ledger;
  const readonly: ReadonlyLedgerView = ledger;
  return { mutable, readonly };
}

export interface ReadonlyIndexed {
  readonly [key: string]: number;
}

export function readonlyIndexSignature(
  record: ReadonlyIndexed,
): number | undefined {
  return record["lane"];
}

export type ReadonlyTuple = readonly [string, number];

export function readonlyTuple(tuple: ReadonlyTuple): string {
  return tuple[0];
}

export function shallowConstAssertion(): Readonly<{ token: string }> {
  return { token: "fixed" } as const;
}

export interface NestedLedger {
  meta: { tags: string[] };
  revision: number;
}

export function nestedMutation(ledger: NestedLedger): void {
  ledger.meta.tags.push("draft");
  ledger.revision += 1;
}

export function runtimeMutationThroughAlias(
  ledger: MutableLedger,
  alias: MutableLedger,
): void {
  alias.entries.push("via-alias");
  ledger.revision = alias.revision + 1;
}

export interface GetterOnly {
  readonly headline: string;
}

export class GetterHost implements GetterOnly {
  private stored = "ledger";

  get headline(): string {
    return this.stored;
  }
}

export function readonlyArrayVariance(
  source: readonly string[],
): readonly string[] {
  return source;
}

export interface PrivateLedger {
  revision: number;
}

export class PrivateLedgerImpl implements PrivateLedger {
  private hidden = 0;

  constructor(public revision: number) {
    this.hidden = revision;
  }
}

export function privateStateView(ledger: PrivateLedgerImpl): PrivateLedger {
  return ledger;
}

export function freezeTyping<T extends object>(value: T): Readonly<T> {
  return Object.freeze(value);
}
