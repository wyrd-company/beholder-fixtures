// Vendor v2 of nominally sensitive type — distinct declaration identity
export type Sensitive = {
  brand: "v2";
  value: number;
};

export const sensitiveV2: Sensitive = { brand: "v2", value: 2 };

export function describeSensitive(s: Sensitive): string {
  return `${s.brand}:${s.value}`;
}
