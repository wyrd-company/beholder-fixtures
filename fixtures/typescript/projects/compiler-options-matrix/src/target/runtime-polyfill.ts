// Successful checking supplies no runtime polyfill.
// Checking passes under modern lib, but emit is a plain reference without polyfill injection.

export function hasFlatSupport(items: unknown[][]): boolean {
  return typeof (items as { flat?: unknown }).flat === "function";
}

export function useFromEntries(
  entries: Array<[string, string]>,
): Record<string, string> {
  return Object.fromEntries(entries);
}

export function useAllSettled<T>(
  promises: Promise<T>[],
): Promise<Array<PromiseSettledResult<T>>> {
  return Promise.allSettled(promises);
}

export function useReplaceAll(
  source: string,
  search: string,
  replacement: string,
): string {
  return source.replaceAll(search, replacement);
}
