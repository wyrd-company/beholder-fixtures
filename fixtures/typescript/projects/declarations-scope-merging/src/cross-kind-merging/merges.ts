// ---
// relationships:
//   references:
//     - ground-rules
//     - reports/typescript/synthesis/checklist
// ---

export function connect(endpoint: string): string {
  return `connected:${endpoint}`;
}

export namespace connect {
  export function retry(endpoint: string, attempts: number): string {
    return `retry:${endpoint}:${attempts}`;
  }

  export type Options = {
    timeoutMs: number;
  };
}

export class Vector {
  x = 0;
}

export interface Vector {
  y: number;
}

export enum Palette {
  Warm,
}

export enum Palette {
  Cool = 2,
}

function helper(value: number): number {
  return value + 1;
}

namespace helper {
  export type Transform = (value: number) => number;
  export const identity: Transform = (value) => value;
}

namespace exportedFacet {
  export const visible = "exported";
  namespace privateFacet {
    export const hidden = "block-private";
  }
  export function readPrivate(): string {
    return privateFacet.hidden;
  }
}

export function demonstrateCrossKind(): {
  connection: string;
  retried: string;
  point: Vector;
  paletteValue: number;
  transformed: number;
  exportedMember: string;
  privateMember: string;
} {
  const connection = connect("api");
  const retried = connect.retry("api", 2);
  const point = new Vector();
  point.y = 5;

  const paletteValue = Palette.Cool;
  const transformed = helper(4);

  return {
    connection,
    retried,
    point,
    paletteValue,
    transformed,
    exportedMember: exportedFacet.visible,
    privateMember: exportedFacet.readPrivate(),
  };
}

export { helper };
