// noLib: this file is compiled with noLib true and uses only fixture-owned
// minimal globals from no-lib-globals.d.ts. No bundled lib is loaded.

export function describeNoLibToken(token: string): string {
  return `no-lib:${token}`;
}

export function sumNoLibValues(values: Array<number>): number {
  return values.length;
}

export function formatNoLibLabel(label: String): String {
  return label;
}
