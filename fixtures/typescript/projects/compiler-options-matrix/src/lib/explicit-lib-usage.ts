// explicit lib: consumer typed against explicitly listed libs ["ES2022", "DOM", "ES2022.Array", "ES2022.Object"].
// Valid under explicit-lib context where lib set is enumerated rather than default.

export function filterWithArrayFrom(source: Set<string>): string[] {
  return Array.from(source).filter((item) => item.length > 0);
}

export function entriesFromObject(
  record: Record<string, number>,
): Array<[string, number]> {
  return Object.entries(record);
}

export function fetchJson(url: string): Promise<unknown> {
  return fetch(url).then((response) => response.json());
}
