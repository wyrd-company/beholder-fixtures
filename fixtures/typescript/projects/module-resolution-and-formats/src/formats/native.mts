// Forced ESM via .mts extension (always ESM regardless of package type)
export const nativeKind = "mts-esm" as const;

export function describeNative(value: string): string {
  return `${nativeKind}:${value}`;
}

export const metaForMts: string = import.meta.url;
