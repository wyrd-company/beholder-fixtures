// Vendor v2 of nominally sensitive type — private brand makes it nominally distinct from v1
// eslint-disable-next-line @typescript-eslint/no-unused-vars
export class Sensitive {
  private __brand: "v2" = "v2";
  value: number = 2;
  get brand(): "v2" {
    return "v2";
  }
}

export const sensitiveV2 = new Sensitive();

export function describeSensitive(s: Sensitive): string {
  return `${s.brand}:${s.value}`;
}
