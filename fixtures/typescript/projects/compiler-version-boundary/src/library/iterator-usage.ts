// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

// Library declarations that changed across the 5.4.5 -> 5.9.3 boundary.
// The bundled lib.*.d.ts set differs between vendored compilers. This module
// consumes declarations whose shapes changed, notably iterator types that
// gained generic parameters and refined signatures.

export function collectIterator<T>(iterable: Iterable<T>): T[] {
  return [...iterable];
}

export function arrayIteratorSample(
  values: string[],
): IterableIterator<string> {
  return values.values();
}

export function iterableIteratorSample(
  iterable: Iterable<string>,
): IterableIterator<string> {
  const iterator = iterable[Symbol.iterator]();
  return iterator as IterableIterator<string>;
}

export function stringKeysSample(values: string[]): IterableIterator<number> {
  return values.keys();
}

export function entriesSample(
  values: string[],
): IterableIterator<[number, string]> {
  return values.entries();
}

export function mapIteratorSample(
  map: Map<string, number>,
): IterableIterator<string> {
  return map.keys();
}

export function setIteratorSample(set: Set<string>): IterableIterator<string> {
  return set.values();
}
