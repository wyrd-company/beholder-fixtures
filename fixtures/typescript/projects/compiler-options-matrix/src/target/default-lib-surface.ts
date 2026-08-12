// Default library surface: valid under modern target default libs (ES2022 + DOM).
// Under old target ES5 default libs, these modern built-ins are absent from the default set.
// This file is included only in the modern context to expose the target-dependent default lib difference.

export function useModernArrayAt(items: string[]): string | undefined {
  return items.at(0);
}

export function useObjectHasOwn(target: object, key: string): boolean {
  return Object.hasOwn(target, key);
}

export function useArrayFromAsync<T>(items: Iterable<T>): Promise<T[]> {
  return Promise.resolve(Array.from(items));
}
