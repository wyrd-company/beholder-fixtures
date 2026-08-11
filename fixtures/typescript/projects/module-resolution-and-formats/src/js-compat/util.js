// JavaScript counterpart where allowJs permits .js input
export const jsCompatMarker = "js-compat";

export function readCompat(value) {
  return `compat:${value}`;
}
