/**
 * Shared helper module used to exercise real relative extensions and
 * Bun's distinct resolution (TS-CAN-091). Importers use explicit
 * relative specifiers; no `paths` alias is present in tsconfig.
 */

export const helperValue = 42;

export type HelperType = {
  value: number;
};

export function helperAdd(a: number, b: number): number {
  return a + b;
}
