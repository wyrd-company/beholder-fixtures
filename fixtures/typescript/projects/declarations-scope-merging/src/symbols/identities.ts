// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

declare const brandSymbol: unique symbol;
export const brandToken = Symbol("brand") as typeof brandSymbol;

export interface BrandedHandle {
  readonly [brandSymbol]: void;
  readonly id: string;
}

export const brandedHandle: BrandedHandle = {
  id: "handle-1",
} as BrandedHandle;

export interface SymbolKeyedTable {
  [key: symbol]: number;
}

export type SymbolKeyedKeys = keyof SymbolKeyedTable;

export const greetKey = "greet" as const;
export const versionKey = "version" as const;

export const keyedService = {
  [greetKey](name: string) {
    return `hello-${name}`;
  },
  [versionKey]: 1,
};

export const iterator = Symbol.iterator;

export interface IterableBox<T> {
  values: T[];
  [iterator](): Iterator<T>;
}

export class IterableBoxImpl<T> implements IterableBox<T> {
  constructor(public values: T[]) {}

  [iterator](): Iterator<T> {
    return this.values[Symbol.iterator]();
  }
}

export function buildDynamicEntry(
  keyName: string,
  value: number,
): Record<string, number> {
  return {
    [keyName]: value,
  };
}

export function readSymbolKeyed(
  table: SymbolKeyedTable,
  key: symbol,
): number | undefined {
  return table[key];
}

export function describeKeys(keys: SymbolKeyedKeys): string {
  return String(keys);
}
