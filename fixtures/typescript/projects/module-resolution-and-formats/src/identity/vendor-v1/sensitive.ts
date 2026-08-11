// Vendor v1 of nominally sensitive type
export type Sensitive = {
  brand: "v1";
  value: number;
};

export const sensitiveV1: Sensitive = { brand: "v1", value: 1 };

export function describeSensitive(s: Sensitive): string {
  return `${s.brand}:${s.value}`;
}
