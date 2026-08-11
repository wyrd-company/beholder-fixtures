/**
 * Transform-differing construct: enum.
 * tsc and Bun transpiler emit different JavaScript for the same enum (TS-CAN-090).
 *
 * tsc (5.9.3) emits:
 *   var Color; (function (Color) { Color[Color["Red"] = 0] = "Red"; })(Color || (Color = {}));
 * Bun transpiler emits:
 *   var Color; ((Color) => { Color[Color["Red"] = 0] = "Red"; })(Color ||= {});
 *
 * Both are valid, but the runtime shape and helper differ. The retained
 * `tsc` check validates types separately from the non-tsc transform.
 */

export enum Color {
  Red = 0,
  Green = 1,
  Blue = 2,
}

export function colorName(c: Color): string {
  return Color[c];
}

export const primary: Color = Color.Green;
