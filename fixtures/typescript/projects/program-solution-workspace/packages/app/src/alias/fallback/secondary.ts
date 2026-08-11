export const aliasSource = "fallback";
export function describeSecondary(id: string): string {
  return `fallback:${id}:${aliasSource}`;
}
