/**
 * TypeScript module imported by JavaScript and vice versa.
 */

export function describeFromTs(): string {
  return "from-typescript";
}

export interface TsShape {
  id: string;
}

export function makeShape(id: string): TsShape {
  return { id };
}
