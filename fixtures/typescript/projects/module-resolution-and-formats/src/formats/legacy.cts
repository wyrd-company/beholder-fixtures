// Forced CJS via .cts extension (always CJS regardless of package type)
export const legacyKind = "cts-cjs" as const;

export function describeLegacy(value: string): string {
  return `${legacyKind}:${value}`;
}

// import.meta not valid in .cts; use regular value export
export const legacyMarker = "cts-marker";
