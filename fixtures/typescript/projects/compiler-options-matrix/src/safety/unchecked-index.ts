// noUncheckedIndexedAccess: indexed reads gain `| undefined`.
// Dictionary and array accesses include undefined under the flag, requiring a check that remains valid when flag is off.

export type CatalogMap = Record<string, string>;

export function lookupToken(
  catalog: CatalogMap,
  key: string,
): string | undefined {
  return catalog[key];
}

export function lookupWithFallback(catalog: CatalogMap, key: string): string {
  return catalog[key] ?? "fallback";
}

export function readArrayItem(
  items: string[],
  index: number,
): string | undefined {
  return items[index];
}

export function readArrayOrDefault(items: string[], index: number): string {
  return items[index] ?? "default";
}
