// Vendor v1 of nominally sensitive type — private brand makes it nominally distinct
// eslint-disable-next-line @typescript-eslint/no-unused-vars
export class Sensitive {
  private __brand: "v1" = "v1";
  value: number = 1;
  get brand(): "v1" {
    return "v1";
  }
}

export const sensitiveV1 = new Sensitive();

export function describeSensitive(s: Sensitive): string {
  return `${s.brand}:${s.value}`;
}
