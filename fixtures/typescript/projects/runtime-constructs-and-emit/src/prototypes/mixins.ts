// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export type Constructor<T = object> = new (...args: any[]) => T;

export class CatalogBase {
  constructor(public readonly id: string) {}

  describe(): string {
    return `catalog:${this.id}`;
  }
}

export function Timestamped<TBase extends Constructor>(Base: TBase) {
  return class extends Base {
    timestamp = 42;

    getTimestamp(): number {
      return this.timestamp;
    }
  };
}

export function Labeled<TBase extends Constructor>(Base: TBase) {
  return class extends Base {
    label = "atlas";

    getLabel(): string {
      return this.label;
    }
  };
}

export const MixedCatalog = Labeled(
  Timestamped(CatalogBase as unknown as Constructor<object>),
);

export type MixedCatalogInstance = InstanceType<typeof MixedCatalog>;

export function createMixed(id: string): MixedCatalogInstance {
  return new MixedCatalog(id) as MixedCatalogInstance;
}

export function demonstrateMixinDispatch(
  instance: MixedCatalogInstance,
): string {
  const anyInstance = instance as unknown as CatalogBase & {
    getLabel(): string;
    getTimestamp(): number;
  };
  return `${anyInstance.describe()}:${anyInstance.getLabel()}:${anyInstance.getTimestamp()}`;
}

export type LedgerEntry = { id: string };
export type AtlasEntry = LedgerEntry & { label: string };

export function intersectionInstanceTypes(entry: AtlasEntry): string {
  return `${entry.id}:${entry.label}`;
}

export interface Convertible {
  toString(): string;
}

export function interfaceOnlyConformance(): string {
  class Standalone implements Convertible {
    toString(): string {
      return "standalone";
    }
  }
  const value: Convertible = new Standalone();
  return value.toString();
}
