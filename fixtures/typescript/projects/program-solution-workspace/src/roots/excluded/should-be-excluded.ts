// This file is listed in `exclude` but re-enters via import from include/consumer.ts.
export const excludedValue = "still-present";
export function describeExcluded(): string {
  return `excluded:${excludedValue}`;
}
