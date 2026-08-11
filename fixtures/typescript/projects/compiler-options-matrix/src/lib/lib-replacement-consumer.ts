// libReplacement: tsconfig has libReplacement true.
// Consumer uses built-ins whose declaration can be replaced via replacement lib file.
// Valid program that remains valid whether replacement is applied.

export function usePromiseWithReplacement(value: string): Promise<string> {
  return Promise.resolve(value).then((resolved) => resolved.toUpperCase());
}

export function useArrayFromWithReplacement(
  source: Iterable<string>,
): string[] {
  return Array.from(source);
}

// Local replacement shape (not a replacement of the bundled lib, but a project-side
// consumer that mirrors the replacement concept for code-graph visibility).
export interface ReplacementMarker {
  marker: string;
}

export function describeReplacement(marker: ReplacementMarker): string {
  return `replacement:${marker.marker}`;
}
